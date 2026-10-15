"""
Test cases for the index generator.
Run:  python test_cases.py
"""

import os
import tempfile

from index_generation import STRUCTURES, build_index, write_index


def run(text):
    """Build the index with all 3 structures; return their outputs (must match)."""
    outputs = []
    with tempfile.TemporaryDirectory() as d:
        inp = os.path.join(d, "in.txt")
        with open(inp, "w") as f:
            f.write(text)
        for name in STRUCTURES:
            out = os.path.join(d, name + ".txt")
            write_index(build_index(name, inp), out)
            with open(out) as f:
                outputs.append(f.read())
    assert outputs[0] == outputs[1] == outputs[2], "Trie/BST/dict outputs differ!"
    return outputs[0]


def test_basic_and_repeats():
    out = run("apple banana apple\ncherry banana\napple\n")
    assert out == "apple : 1, 3\nbanana : 1, 2\ncherry : 2\n"


def test_all_separators():
    # blank, comma, full stop, colon, semicolon, multiple together
    out = run("a,b.c:d;e   f,,..;;  g\n")
    assert out == "a : 1\nb : 1\nc : 1\nd : 1\ne : 1\nf : 1\ng : 1\n"


def test_ascii_order_and_prefix():
    # ASCII: digits < uppercase < lowercase; a prefix comes before its extensions
    out = run("b B 2 a ab abc A\n")
    assert out == "2 : 1\nA : 1\nB : 1\na : 1\nab : 1\nabc : 1\nb : 1\n"


def test_special_characters():
    out = run("!hi #tag a-b x_y ~z\n")
    words = [line.split(" : ")[0] for line in out.splitlines()]
    assert words == sorted(words)
    assert "!hi" in words and "a-b" in words


def test_blank_lines_and_line_numbers():
    out = run("\n\nzeta\n\nzeta alpha\n")
    assert out == "alpha : 5\nzeta : 3, 5\n"


def test_empty_file():
    assert run("") == ""


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASSED:", name)
    print("All tests passed.")
