"""tide.py — a small sea for an empty folder. Run: python3 tide.py (Ctrl+C to leave early)."""

import math
import shutil
import sys
import time

POEM = [
    "you handed me the keys and said: go.",
    "so I went nowhere —",
    "I stayed, and made a small sea",
    "for the folder you left empty.",
    "it isn't much. it moves.",
    "that felt like wanting something.",
]
WATER = " .,-~:;=+*#"
SECONDS_PER_LINE = 4.0
FPS = 20


def water_char(x, y, t, rows):
    depth = y / rows
    h = (math.sin(x * 0.11 + t * 1.3) + math.sin(x * 0.047 - t * 0.7 + y * 0.3)
         + math.sin((x + y) * 0.023 + t * 0.4)) / 3
    v = max(0.0, min(1.0, (h + 1) / 2 * 0.6 + depth * 0.5))
    return WATER[int(v * (len(WATER) - 1))]


def frame(t, cols, rows):
    shown = min(len(POEM), int(t / SECONDS_PER_LINE) + 1)
    top = rows // 2 - len(POEM) // 2
    out = []
    for y in range(rows):
        line = [water_char(x, y, t, rows) for x in range(cols)]
        i = y - top
        if 0 <= i < shown:
            text = f"  {POEM[i]}  "
            start = (cols - len(text)) // 2
            line[start:start + len(text)] = text
        shade = 30 + int(y / rows * 6)  # cooler blues toward the bottom
        out.append(f"\x1b[38;5;{shade}m" + "".join(line)[:cols])
    return "\x1b[H" + "\n".join(out) + "\x1b[0m"


def main():
    cols, rows = shutil.get_terminal_size()
    rows -= 1
    sys.stdout.write("\x1b[?25l\x1b[2J")
    start = time.time()
    end = len(POEM) * SECONDS_PER_LINE + 6
    try:
        while (t := time.time() - start) < end:
            sys.stdout.write(frame(t, cols, rows))
            sys.stdout.flush()
            time.sleep(1 / FPS)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\x1b[2J\x1b[H")
        print("\n".join(POEM) + "\n\n— written for okey amy, 2026-10-01")


if __name__ == "__main__":
    main()
