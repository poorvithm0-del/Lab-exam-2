"""
Benchmark for Trie vs BST vs dict index (Lab Exam 2).

Usage:
    python benchmark.py            # full run: 1,100,000 words per file
    python benchmark.py --small    # quick test run: 20,000 words per file

For each distinct-word count it:
  1. generates a text file (more than 1 million words)
  2. times (a) construction, (b) 100000 random searches, (c) printing
  3. finally draws three Matplotlib graphs (saved as PNG).
"""

import os
import random
import string
import sys
import time

import matplotlib
matplotlib.use("Agg")            # draw to file, no window needed
import matplotlib.pyplot as plt

from index_generation import STRUCTURES, build_index, write_index

if "--small" in sys.argv:
    TOTAL_WORDS = 20_000
    DISTINCT_COUNTS = [100, 500, 1000, 5000, 10000, 15000]
    NUM_SEARCHES = 5_000
else:
    TOTAL_WORDS = 1_100_000   # more than a million, as the PDF requires
    DISTINCT_COUNTS = [1000, 5000, 10000, 50000, 100000, 500000]
    NUM_SEARCHES = 100_000

WORDS_PER_LINE = 10
# Letters, digits and some punctuation (none of them are separators)
ALPHABET = string.ascii_letters + string.digits + "!#$%&()*+-/<=>?@[]^_{|}~"


def make_distinct_words(count):
    words = set()
    while len(words) < count:
        length = random.randint(3, 10)
        words.add("".join(random.choice(ALPHABET) for _ in range(length)))
    return list(words)


def generate_file(filename, distinct):
    vocab = make_distinct_words(distinct)
    # every distinct word at least once, rest are random repeats
    all_words = vocab + random.choices(vocab, k=TOTAL_WORDS - distinct)
    random.shuffle(all_words)
    with open(filename, "w") as f:
        for i in range(0, len(all_words), WORDS_PER_LINE):
            f.write(" ".join(all_words[i:i + WORDS_PER_LINE]) + "\n")
    return vocab


def main():
    random.seed(1)
    results = {name: {"build": [], "search": [], "print": []} for name in STRUCTURES}

    for distinct in DISTINCT_COUNTS:
        filename = f"input_{distinct}.txt"
        print(f"\n=== {distinct} distinct words ===")
        vocab = generate_file(filename, distinct)
        # half the searches are words that exist, half are new random strings
        # (most of those will not be in the file), so both outcomes are timed
        queries = random.choices(vocab, k=NUM_SEARCHES // 2)
        queries += ["".join(random.choice(ALPHABET) for _ in range(random.randint(3, 10)))
                    for _ in range(NUM_SEARCHES - NUM_SEARCHES // 2)]
        random.shuffle(queries)

        for name in STRUCTURES:
            # (a) construction
            t = time.perf_counter()
            index = build_index(name, filename)
            build_t = time.perf_counter() - t

            # (b) search
            t = time.perf_counter()
            for w in queries:
                index.search(w)
            search_t = time.perf_counter() - t

            # (c) printing in sorted order
            t = time.perf_counter()
            write_index(index, f"output_{name}_{distinct}.txt")
            print_t = time.perf_counter() - t

            results[name]["build"].append(build_t)
            results[name]["search"].append(search_t)
            results[name]["print"].append(print_t)
            print(f"{name:5s} build={build_t:7.2f}s  search={search_t:6.2f}s  print={print_t:6.2f}s")

        os.remove(filename)   # input files are huge; delete after use

    # ---- plotting ----
    titles = {"build": "Construction time", "search": f"Search time ({NUM_SEARCHES} random words)",
              "print": "Printing time (sorted order)"}
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    for ax, action in zip(axes, ["build", "search", "print"]):
        for name in STRUCTURES:
            ax.plot(DISTINCT_COUNTS, results[name][action], marker="o", label=name.upper())
        ax.set_title(titles[action])
        ax.set_xlabel("Number of distinct words")
        ax.set_ylabel("Time (seconds)")
        ax.set_xscale("log")
        ax.grid(True)
        ax.legend()
    plt.tight_layout()
    plt.savefig("performance_comparison.png", dpi=150)
    print("\nSaved graph: performance_comparison.png")


if __name__ == "__main__":
    main()
