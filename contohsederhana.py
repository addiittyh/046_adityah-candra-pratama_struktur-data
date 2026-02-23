import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ==============================
# HASH TABLE LOGIC
# ==============================
def simulate_hash(keys, size):
    table = [None] * size
    frames = []
    load_factors = []

    for step, key in enumerate(keys, 1):
        start = hash(key) % size
        idx = start
        probes = 0

        def snapshot(phase, placed=False):
            frames.append({
                "step": step,
                "key": key,
                "start": start,
                "idx": idx,
                "probes": probes,
                "table": list(table),
                "phase": phase,
                "placed": placed
            })

        snapshot("start")

        while table[idx] is not None:
            snapshot("collision")
            probes += 1
            idx = (idx + 1) % size
            snapshot("probe")

        table[idx] = key
        snapshot("placed", True)

        lf = sum(v is not None for v in table) / size
        load_factors.append(lf)

    return frames, load_factors


# ==============================
# GAME MAIN
# ==============================
def main():
    size = 15
    nkeys = 12

    keys = [f"K{i}" for i in range(nkeys)]
    random.shuffle(keys)

    frames, load_factors = simulate_hash(keys, size)

    fig, (ax_table, ax_lf) = plt.subplots(2, 1, figsize=(12, 6))

    # Table setup
    ax_table.set_xlim(-0.5, size - 0.5)
    ax_table.set_ylim(-0.5, 0.5)
    ax_table.set_yticks([])
    ax_table.set_xticks(range(size))
    ax_table.set_title("Hash Table Game (Linear Probing)")

    rects = []
    texts = []

    for i in range(size):
        r = plt.Rectangle((i - 0.5, -0.3), 1, 0.6, alpha=0.3)
        ax_table.add_patch(r)
        rects.append(r)
        t = ax_table.text(i, 0, "", ha="center", va="center")
        texts.append(t)

    # Load factor chart
    ax_lf.set_xlim(1, nkeys)
    ax_lf.set_ylim(0, 1.1)
    ax_lf.set_xlabel("Insert ke-")
    ax_lf.set_ylabel("Load Factor")
    line, = ax_lf.plot([], [])
    dot, = ax_lf.plot([], [], marker="o", linestyle="")

    state = {"i": 0, "paused": False}

    def render(frame):
        table = frame["table"]
        start = frame["start"]
        idx = frame["idx"]

        for j in range(size):
            rects[j].set_alpha(0.3)
            texts[j].set_text("" if table[j] is None else table[j])

        rects[start].set_alpha(0.6)
        rects[idx].set_alpha(0.9)

        completed = frame["step"] - 1 + (1 if frame["placed"] else 0)

        if completed > 0:
            x = list(range(1, completed + 1))
            y = load_factors[:completed]
            line.set_data(x, y)
            dot.set_data([x[-1]], [y[-1]])

        return rects + texts + [line, dot]

    def update(_):
        if not state["paused"]:
            state["i"] = min(state["i"] + 1, len(frames) - 1)
        return render(frames[state["i"]])

    def on_key(event):
        if event.key == " ":
            state["paused"] = not state["paused"]

        elif event.key == "right":
            state["i"] = min(state["i"] + 1, len(frames) - 1)

        elif event.key == "left":
            state["i"] = max(state["i"] - 1, 0)

        elif event.key == "r":
            state["i"] = 0
            state["paused"] = True

        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("key_press_event", on_key)

    ani = FuncAnimation(
        fig, update,
        frames=np.arange(len(frames)),
        interval=600,
        repeat=False
    )

    plt.show()


if __name__ == "__main__":
    main()
