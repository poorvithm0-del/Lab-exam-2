"""
manual_tests.py - runs the 10 manual test cases on the real program.

It creates its own input files (so you do NOT need to make in.txt),
runs  index_generation.py  with trie, bst and dict, and compares the
output with the expected output.

How to run (keep this file in the SAME folder as index_generation.py):
    python manual_tests.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAM = os.path.join(HERE, "index_generation.py")

# (name, input text, expected output)
TESTS = [
    ("1. repeated words",
     "apple banana apple\ncherry banana\napple\n",
     "apple : 1, 3\nbanana : 1, 2\ncherry : 2\n"),

    ("2. all separators",
     "one,two.three:four;five   six,,..;;  seven\n",
     "five : 1\nfour : 1\none : 1\nseven : 1\nsix : 1\nthree : 1\ntwo : 1\n"),

    ("3. same word twice on one line",
     "go go go\nstop go\n",
     "go : 1, 2\nstop : 2\n"),

    ("4. ASCII order",
     "zebra Zebra 9 apple _x ~ ! a-b #1 Apple\n",
     "! : 1\n#1 : 1\n9 : 1\nApple : 1\nZebra : 1\n_x : 1\na-b : 1\napple : 1\nzebra : 1\n~ : 1\n"),

    ("5. prefix words",
     "car cart carpet ca c cat\n",
     "c : 1\nca : 1\ncar : 1\ncarpet : 1\ncart : 1\ncat : 1\n"),

    ("6. only symbols",
     "!!! ??? ### !!! ???\n",
     "!!! : 1\n### : 1\n??? : 1\n"),

    ("7. blank lines",
     "\n\nzeta\n\nzeta alpha\n\n",
     "alpha : 5\nzeta : 3, 5\n"),

    ("8. leading and trailing separators",
     ",,,hello;;;world...\n:: hello ;;\n",
     "hello : 1, 2\nworld : 1\n"),

    ("9. no newline at the end",
     "last one last",
     "last : 1\none : 1\n"),

    ("10. empty file",
     "",
     ""),
]


def run_program(args, folder):
    """Run index_generation.py with the given arguments inside folder."""
    return subprocess.run([sys.executable, PROGRAM] + args,
                          cwd=folder, capture_output=True, text=True)


def main():
    if not os.path.exists(PROGRAM):
        print("index_generation.py not found next to this file:", PROGRAM)
        return

    passed = 0
    failed = 0
    with tempfile.TemporaryDirectory() as folder:
        # ---- part 1: the 10 input/output tests, for all three versions ----
        for name, text, expected in TESTS:
            input_path = os.path.join(folder, "in.txt")
            with open(input_path, "w") as f:
                f.write(text)

            ok = True
            for method in ["trie", "bst", "dict"]:
                out_path = os.path.join(folder, "out_" + method + ".txt")
                run_program([input_path, out_path, method], folder)
                with open(out_path) as f:
                    actual = f.read()
                if actual != expected:
                    ok = False
                    print("  WRONG OUTPUT with", method)
                    print("  expected:", repr(expected))
                    print("  actual  :", repr(actual))

            if ok:
                print("PASS  Test", name)
                passed += 1
            else:
                print("FAIL  Test", name)
                failed += 1

        # ---- part 2: command-line checks ----
        result = run_program([], folder)
        if "Usage:" in result.stdout:
            print("PASS  Test 11. no arguments prints usage message")
            passed += 1
        else:
            print("FAIL  Test 11. no arguments prints usage message")
            failed += 1

        result = run_program(["in.txt", "out.txt", "abc"], folder)
        if "Method must be trie, bst or dict" in result.stdout:
            print("PASS  Test 12. wrong method name is rejected")
            passed += 1
        else:
            print("FAIL  Test 12. wrong method name is rejected")
            failed += 1

        result = run_program(["in.txt"], folder)
        if "Usage:" in result.stdout:
            print("PASS  Test 13. missing output file name prints usage message")
            passed += 1
        else:
            print("FAIL  Test 13. missing output file name prints usage message")
            failed += 1

    print()
    print("Passed:", passed, " Failed:", failed)
    if failed == 0:
        print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
