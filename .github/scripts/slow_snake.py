"""Slows down the Platane/snk animation and holds the full graph on screen before the snake starts.

usage: python slow_snake.py <svg> [<svg> ...]
"""
import re
import sys

SLOW = 2.5      # snake speed divisor
HOLD_MS = 6000  # full graph shown before the snake moves


def process(path):
    svg = open(path, encoding="utf-8").read()
    durations = set(re.findall(r"(\d+)ms", svg))
    if len(durations) != 1:
        sys.exit(f"{path}: expected a single animation duration, found {durations}")
    old = int(durations.pop())
    run = old * SLOW
    total = HOLD_MS + run

    def remap(m):
        p = float(m.group(2))
        new = f"{(HOLD_MS + p / 100 * run) / total * 100:.4f}%"
        # a 0% frame keeps its state for the whole hold
        return f"{m.group(1)}0%,{new}" if p == 0 else f"{m.group(1)}{new}"

    # keyframe selectors only: a percentage that starts a keyframe block or selector list
    svg = re.sub(r"([{},])(\d+(?:\.\d+)?)%(?=[{,])", remap, svg)
    svg = svg.replace(f"{old}ms", f"{round(total)}ms")
    open(path, "w", encoding="utf-8").write(svg)
    print(f"{path}: {old}ms -> {round(total)}ms (hold {HOLD_MS}ms)")


for p in sys.argv[1:]:
    process(p)
