# ui/gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from tm.simulator import TMSimulator
from operations import build_initial_tape, get_generator_for
from config import MAX_STEPS

class TMGUI:
    def __init__(self, root):
        self.root = root
        root.title("Turing Machine Emulator - Arithmetic (Unary & Binary)")

        frame_top = ttk.Frame(root, padding=8)
        frame_top.grid(row=0, column=0, sticky='ew')
        frame_top.columnconfigure(0, weight=1)

        ttk.Label(frame_top, text="Numeral:").grid(row=0, column=0, sticky='w')
        self.numeral_var = tk.StringVar(value='unary')
        ttk.Combobox(frame_top, textvariable=self.numeral_var, values=['unary','binary'], state='readonly', width=10).grid(row=0, column=1, sticky='w', padx=4)

        ttk.Label(frame_top, text="Operation:").grid(row=0, column=2, sticky='w', padx=(12,0))
        self.op_var = tk.StringVar(value='add')
        ttk.Combobox(frame_top, textvariable=self.op_var, values=['add','subtract','multiply'], state='readonly', width=12).grid(row=0, column=3, sticky='w', padx=4)

        ttk.Label(frame_top, text="a:").grid(row=1, column=0, sticky='w', pady=(6,0))
        self.a_entry = ttk.Entry(frame_top, width=12)
        self.a_entry.grid(row=1, column=1, sticky='w', pady=(6,0))
        ttk.Label(frame_top, text="b:").grid(row=1, column=2, sticky='w', pady=(6,0))
        self.b_entry = ttk.Entry(frame_top, width=12)
        self.b_entry.grid(row=1, column=3, sticky='w', pady=(6,0))

        frame_controls = ttk.Frame(root, padding=8)
        frame_controls.grid(row=1, column=0, sticky='ew')
        self.step_btn = ttk.Button(frame_controls, text="Step", command=self.on_step)
        self.step_btn.grid(row=0, column=0, padx=4)
        self.run_btn = ttk.Button(frame_controls, text="Run", command=self.on_run)
        self.run_btn.grid(row=0, column=1, padx=4)
        self.pause_btn = ttk.Button(frame_controls, text="Pause", command=self.on_pause)
        self.pause_btn.grid(row=0, column=2, padx=4)
        self.reset_btn = ttk.Button(frame_controls, text="Reset", command=self.on_reset)
        self.reset_btn.grid(row=0, column=3, padx=4)
        ttk.Label(frame_controls, text="Speed(ms):").grid(row=0, column=4, padx=(12,0))
        self.speed_var = tk.IntVar(value=50)
        ttk.Scale(frame_controls, from_=0, to=500, variable=self.speed_var, orient='horizontal').grid(row=0, column=5, padx=4, sticky='we')

        frame_tape = ttk.Frame(root, padding=8, relief='groove')
        frame_tape.grid(row=2, column=0, sticky='nsew', padx=6, pady=6)
        root.rowconfigure(2, weight=1)
        frame_tape.columnconfigure(0, weight=1)

        self.tape_canvas = tk.Canvas(frame_tape, height=80)
        self.tape_canvas.grid(row=0, column=0, sticky='nsew')
        self.tape_scroll = ttk.Scrollbar(frame_tape, orient='horizontal', command=self.tape_canvas.xview)
        self.tape_scroll.grid(row=1, column=0, sticky='ew')
        self.tape_canvas.configure(xscrollcommand=self.tape_scroll.set)
        self.tape_inner = ttk.Frame(self.tape_canvas)
        self.tape_canvas.create_window((0,0), window=self.tape_inner, anchor='nw')
        self.tape_inner.bind("<Configure>", lambda e: self.tape_canvas.configure(scrollregion=self.tape_canvas.bbox("all")))

        frame_log = ttk.Frame(root, padding=8)
        frame_log.grid(row=3, column=0, sticky='nsew')
        ttk.Label(frame_log, text="Transition Log:").grid(row=0, column=0, sticky='w')
        self.log = scrolledtext.ScrolledText(frame_log, height=12)
        self.log.grid(row=1, column=0, sticky='nsew')
        frame_log.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status_var).grid(row=4, column=0, sticky='w', padx=8, pady=(4,8))

        self.sim = None
        self.tape_labels = []
        self.auto_thread = None
        self._running = False

        self.a_entry.insert(0, "3")
        self.b_entry.insert(0, "2")

        self.on_reset()

    def log_message(self, msg: str):
        self.log.insert('end', msg + '\n')
        self.log.see('end')

    def build_sim_from_gui(self):
        numeral = self.numeral_var.get()
        op = self.op_var.get()
        try:
            a = int(self.a_entry.get().strip())
            b = int(self.b_entry.get().strip())
        except Exception:
            messagebox.showerror("Invalid input", "a and b must be integers (non-negative).")
            return None
        try:
            tape = build_initial_tape(a, b, numeral)
        except Exception as ex:
            messagebox.showerror("Input limit error", str(ex))
            return None
        gen = get_generator_for(op, numeral, tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        self.sim = sim
        self.log_message(f"Built simulator: numeral={numeral}, op={op}, a={a}, b={b}")
        self.refresh_tape_display()
        self.status_var.set("Simulator built. Ready.")
        return sim

    def refresh_tape_display(self):
        for lab in self.tape_labels:
            lab.destroy()
        self.tape_labels = []
        if not self.sim:
            return
        tape = self.sim.tape
        content = tape.tape
        head_pos = tape.head
        
        # Ensure head is within displayable range
        if head_pos < 0:
            head_pos = 0
        elif head_pos >= len(content):
            head_pos = len(content) - 1 if content else 0
        
        for i, ch in enumerate(content):
            lbl = ttk.Label(self.tape_inner, text=ch, relief='ridge', width=3)
            lbl.grid(row=0, column=i, padx=0, pady=0)
            if i == head_pos:
                lbl.configure(background='yellow')
            self.tape_labels.append(lbl)
        self.tape_canvas.update_idletasks()

    def on_step(self):
        if not self.sim:
            built = self.build_sim_from_gui()
            if not built:
                return
        if self.sim.is_halted():
            self.log_message("Machine already halted.")
            return
        trans = self.sim.step()
        if trans is None:
            self.log_message("No transition (halting).")
            self.status_var.set("Halted")
            self.refresh_tape_display()
            return
        state, read, write, move, next_state, note = trans
        self.log_message(f"Step {self.sim.step_count}: ({state}, {read}) -> ({write}, {move}, {next_state}) [{note}]")
        self.refresh_tape_display()
        if self.sim.is_halted():
            self.log_message("Machine halted.")
            self.status_var.set("Halted")

    def auto_runner(self, delay_ms: int):
        while not self.sim.is_halted() and self._running:
            trans = self.sim.step()
            if trans is None:
                break
            state, read, write, move, next_state, note = trans
            self.root.after(0, lambda s=state,r=read,w=write,m=move,ns=next_state,n=note:
                            self.log_message(f"Step {self.sim.step_count}: ({s}, {r}) -> ({w}, {m}, {ns}) [{n}]"))
            self.root.after(0, self.refresh_tape_display)
            time.sleep(delay_ms / 1000.0)
        self._running = False
        self.root.after(0, lambda: self.status_var.set("Halted" if self.sim.is_halted() else "Paused"))

    def on_run(self):
        if not self.sim:
            built = self.build_sim_from_gui()
            if not built:
                return
        if self.sim.is_halted():
            self.log_message("Machine already halted.")
            return
        if self._running:
            return
        self._running = True
        speed = max(0, int(self.speed_var.get()))
        self.status_var.set("Running")
        self.auto_thread = threading.Thread(target=self.auto_runner, args=(speed,), daemon=True)
        self.auto_thread.start()

    def on_pause(self):
        if self._running:
            self._running = False
            self.status_var.set("Paused")
            self.log_message("Paused by user.")

    def on_reset(self):
        self.log.delete('1.0','end')
        self.sim = None
        try:
            self.build_sim_from_gui()
        except Exception:
            self.status_var.set("Ready")
            return

    def on_reset_force(self):
        self.sim = None
        self.build_sim_from_gui()
