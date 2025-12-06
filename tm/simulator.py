# tm/simulator.py
import time
from tm.tape import Tape
from typing import Generator, Optional, Tuple
from config import MAX_STEPS

# transition type: (state, read, write, move, next_state, note)
Transition = Tuple[str, Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]

class TMSimulator:
    """
    Simulator running a generator that yields transitions.
    The generator is responsible for manipulating the Tape directly (writes/moves).
    Each yielded transition is informative for logging / UI.
    """
    def __init__(self, tape: Tape, gen_steps: Generator[Transition, None, None], max_steps: int = MAX_STEPS):
        self.tape = tape
        self.gen = gen_steps
        self.max_steps = max_steps
        self.step_count = 0
        self.halted = False
        self.last_transition: Optional[Transition] = None
        self._pause = False

    def step(self) -> Optional[Transition]:
        if self.halted:
            return None
        if self.step_count >= self.max_steps:
            self.halted = True
            return ('HALT', None, None, None, None, 'max steps reached')
        try:
            trans = next(self.gen)
        except StopIteration:
            self.halted = True
            return ('HALT', None, None, None, None, 'halt')
        self.step_count += 1
        self.last_transition = trans
        return trans

    def run(self, callback=None, delay: float = 0.02):
        while not self.halted:
            if self._pause:
                return
            trans = self.step()
            if callback:
                callback(trans)
            if self.halted:
                return
            if delay > 0:
                time.sleep(delay)

    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False

    def is_halted(self) -> bool:
        return self.halted
