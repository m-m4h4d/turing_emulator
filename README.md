# Turing-Emulator

This proposal is for a **Turing Machine (TM) Emulator for Arithmetic Operations**, developed for the **Theory of Automata and Formal Languages (TAFL)** course by Muhammad Mahad and Abdul Moiz, under the instruction of Dr. Sohail Iqbal.

---

## Project Goal and Motivation

The project is motivated by the fact that the Turing Machine is the **foundation of modern computation**, and arithmetic operations illustrate how complex logic stems from simple transitions.

* **Goal**: To **visualize TM behavior**—including tape reading, head movement, and state transitions—specifically during arithmetic operations.
* **Problem Identified (Gap)**: Current TM simulators are often theoretical and lack an interactive demonstration of arithmetic computation; they usually only show string acceptance.
* **Solution**: To create a **modern emulator** that visually demonstrates TM-based arithmetic (addition, subtraction, multiplication) step-by-step.

---

## Running the Emulator

Requires Python 3.10+ and no third-party packages. The GUI uses tkinter, which ships with most Python installs (on Debian/Ubuntu: `sudo apt install python3-tk`).

```bash
# GUI: pick unary/binary and an operation, enter a and b, then Step or Run
python main.py

# Command line: prints every transition, the final tape and the result
python main.py --cli --op multiply --numeral binary --a 6 --b 7

# Print a machine's full transition table
python main.py --table --op subtract --numeral unary
```

`--op` is `add`, `subtract` or `multiply`; `--numeral` is `unary` or `binary`. Operands are non-negative integers up to 200 (`INPUT_LIMIT` in `config.py`). Runs stop after 100,000 steps (`MAX_STEPS`); unary multiplication reaches that limit once the product passes roughly 250 (16 × 16 takes about 80,000 steps).

A web version of the unary machines runs at <https://tm-emulator-semester-project.vercel.app/>.

### Tape Format

| Numeral | Input tape | Halted tape |
|---|---|---|
| Unary | `1^a 0 1^b` (e.g. `111011` is 3, 2) | `1^result`; an empty tape is 0 |
| Binary | `a#b`, most significant bit first, 0 written as nothing (e.g. `11#10`) | the result in binary, no leading zeros; 0 is `0` |

Subtraction is monus: when b > a the result is 0. Every machine halts in state `q_accept` with the head on the first cell of the result.

### Project Structure

```
main.py             entry point: GUI, --cli and --table
config.py           step and input limits
tm/machines.py      the six machines as transition tables, and the interpreter that runs them
tm/simulator.py     steps a running machine and counts transitions
tm/tape.py          tape and head
operations/         builds the input tape for a, b and picks the machine
ui/gui.py           tkinter interface
tests/              test suite (see tests/README.md)
```

`tm/machines.py` is also copied verbatim into the web project as `api/tm_machines.py`; keep the two files identical.

### Running the Tests

```bash
python tests/run_all_tests.py
```

The suite also runs on every push through GitHub Actions (`.github/workflows/tests.yml`).
