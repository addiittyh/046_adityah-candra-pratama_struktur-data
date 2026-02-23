import argparse
import random
import numpy as np

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plan_inserts(keys, size=20):
    table = [None] * size
    frame_data = []
    load_factors = []

    for step, key in enumerate(keys, 1):
        start = hash(key) % size
        idx = start
        probes = 0

        def snap(phase, placed=False):
            frame_data.append({
                "phase": phase,
                "step": step,
                "key": key,
                "start": start,
                "idx": idx,
                "probes": probes,
                "table": list(table),
                "placed": placed
            })

        snap("start", placed=False)

        while table[idx] is not None:
            snap("collision", placed=False)
            probes += 1
            idx = (idx + 1) % size
            snap("probe", placed=False)

        table[idx] = key
        snap("place", placed=True)

        lf = sum(v is not None for v in table) / size
        load_factors.append(lf)

        snap("pause", placed=True)

    return frame_data, load_factors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=20)
    parser.add_argument("--nkeys", type=int, default=18)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--save", choices=["none", "gif"], default="none")
    args = parser.parse_args()

    random.seed(args.seed)
    keys = [f"k{i}" for i in range(args.nkeys)]
    random.shuffle(keys)

    frames, load_factors = plan_inserts(keys, size=args.size)

    fig = plt.figure(figsize=(12, 6), constrained_layout=True)
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])

    ax_table = fig.add_subplot(gs[0])
    ax_lf = fig.add_subplot(gs[1])

    fig.suptitle("Hash Table (Linear Probing) — Keyboard Control", fontsize=14)

    n = args.size
    ax_table.set_xlim(-0.5, n - 0.5)
    ax_table.set_ylim(-0.5, 0.5)
    ax_table.set_yticks([])
    ax_table.set_xticks(range(n))
    ax_table.set_xlabel("Index Bucket")

    rects, texts = [], []
    for i in range(n):
        r = plt.Rectangle((i - 0.5, -0.35), 1.0, 0.7, fill=True, alpha=0.25)
        ax_table.add_patch(r)
        rects.append(r)
        t = ax_table.text(i, 0, "", ha="center", va="center", fontsize=9)
        texts.append(t)

    info = ax_table.text(0.01, 1.08, "", transform=ax_table.transAxes, fontsize=11)

    ax_lf.set_xlim(1, max(2, args.nkeys))
    ax_lf.set_ylim(0, 1.05)
    ax_lf.set_xlabel("Insert ke-")
    ax_lf.set_ylabel("Load Factor")
    ax_lf.grid(True, alpha=0.25)

    lf_line, = ax_lf.plot([], [])
    lf_dot, = ax_lf.plot([], [], marker="o", linestyle="")

    state = {"i": 0, "paused": False}

    def render(frame):
        table = frame["table"]
        start = frame["start"]
        idx = frame["idx"]
        phase = frame["phase"]

        for j in range(n):
            rects[j].set_alpha(0.25)
            texts[j].set_text("" if table[j] is None else str(table[j]))

        rects[start].set_alpha(0.55)
        rects[idx].set_alpha(0.75)

        filled = sum(v is not None for v in table)
        lf = filled / n

        info.set_text(
            f"Step {frame['step']} | key='{frame['key']}' | "
            f"hash%size={start} | idx={idx} | probes={frame['probes']} | "
            f"load_factor={lf:.2f} | phase={phase}"
        )

        completed = frame["step"] - 1 + (1 if frame["placed"] else 0)
        if completed > 0:
            x = list(range(1, completed + 1))
            y = load_factors[:completed]
            lf_line.set_data(x, y)
            lf_dot.set_data([x[-1]], [y[-1]])

        return rects + texts + [info, lf_line, lf_dot]

    def update(_):
        if not state["paused"]:
            state["i"] = min(state["i"] + 1, len(frames) - 1)
        return render(frames[state["i"]])

    ani = FuncAnimation(
        fig, update,
        frames=np.arange(len(frames)),
        interval=500,
        repeat=False
    )

    plt.show()


if __name__ == "__main__":
    main()
