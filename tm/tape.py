class Tape:
    def __init__(self, content, blank="_"):
        self.blank = blank
        self.tape = list(content)
        self.head = 0

    def read(self):
        if self.head < 0:
            self.tape.insert(0, self.blank)
            self.head = 0
        if self.head >= len(self.tape):
            self.tape.append(self.blank)
        return self.tape[self.head]

    def write(self, symbol):
        if self.head < 0:
            self.tape.insert(0, symbol)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(symbol)
        else:
            self.tape[self.head] = symbol

    def move_left(self):
        self.head -= 1

    def move_right(self):
        self.head += 1

    def get_content(self):
        return "".join(self.tape).strip(self.blank)

    def as_str(self):
        """Return tape content as a string representation."""
        return "".join(self.tape)

    def at(self):
        """Return the symbol at the current head position (same as read but more convenient name)."""
        return self.read()

    def move(self, direction):
        """Move the head in the specified direction: 'L' for left, 'R' for right, 'S' for stay."""
        if direction == 'L':
            self.move_left()
        elif direction == 'R':
            self.move_right()
        # 'S' means stay, do nothing

    def trim_blanks(self):
        """Remove leading and trailing blank symbols from the tape, keeping the head position relative."""
        if not self.tape:
            return
        # Find first non-blank
        first_nonblank = None
        for i, ch in enumerate(self.tape):
            if ch != self.blank:
                first_nonblank = i
                break
        if first_nonblank is None:
            # All blanks
            self.tape = [self.blank]
            self.head = 0
            return
        # Find last non-blank
        last_nonblank = None
        for i in range(len(self.tape) - 1, -1, -1):
            if self.tape[i] != self.blank:
                last_nonblank = i
                break
        if last_nonblank is None:
            self.tape = [self.blank]
            self.head = 0
            return
        # Trim and adjust head
        old_head = self.head
        self.tape = self.tape[first_nonblank:last_nonblank + 1]
        self.head = max(0, min(old_head - first_nonblank, len(self.tape) - 1))

    def leftmost_nonblank_index(self):
        """Return the index of the leftmost non-blank symbol, or 0 if all are blank."""
        for i, ch in enumerate(self.tape):
            if ch != self.blank:
                return i
        return 0

    def rightmost_nonblank_index(self):
        """Return the index of the rightmost non-blank symbol, or len(tape)-1 if all are blank."""
        for i in range(len(self.tape) - 1, -1, -1):
            if self.tape[i] != self.blank:
                return i
        return len(self.tape) - 1 if self.tape else 0