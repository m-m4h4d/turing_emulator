class Transition:
    def __init__(self, current_state, read, write, move, next_state):
        """
        A single Turing Machine transition rule.
        Example:
            δ(q0, '1') → (q1, 'X', 'R')
        """
        self.current_state = current_state
        self.read = read
        self.write = write
        self.move = move   # 'L', 'R', or 'S' (stay)
        self.next_state = next_state

    def apply(self, tape):
        """
        Executes this transition on the given tape.
        Returns the next state name.
        """
        symbol = tape.read()

        if symbol != self.read:
            # Transition does not match → TM should NOT use this rule
            return self.current_state

        # Write new symbol
        tape.write(self.write)

        # Move head
        if self.move == "L":
            tape.move_left()
        elif self.move == "R":
            tape.move_right()
        # 'S' means stay

        return self.next_state
