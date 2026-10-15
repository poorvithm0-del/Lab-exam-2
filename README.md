# Index Generation Project (Lab Exam 2, Data Structures)

## Files
- index_generation.py : Trie, BST and dict versions + command-line utility
- benchmark.py        : generates 6 large input files, times the 3 actions, plots with Matplotlib
- test_cases.py       : automatic test cases (all 3 versions must give identical output)
- manual_tests.py     : 10 input/output tests + command-line checks run on the real program
- README.md           : design explanation + how to run
- performance_comparison.png : graphs from the full benchmark run
- Lab_Exam_2_Index_Generation_Submission.pdf : complete report (explanation, tests, graphs, code)

## How to run
    python index_generation.py input.txt output.txt [trie|bst|dict]   (default: dict)
    python test_cases.py
    python manual_tests.py
    python benchmark.py            (full: 1,100,000 words per file; needs matplotlib)
    python benchmark.py --small    (quick test)

## Design explanation
The program splits each line on blanks, full stops, commas, colons and semicolons;
every other printable ASCII character is part of a word. Each word is inserted into
the chosen structure with its line number. Each distinct word owns a linked-list
queue of line numbers (O(1) enqueue at the tail); a word repeated on the same line
is recorded once for that line.

- Trie: O(L) per insert/search (L = word length). A depth-first walk visiting
  children in ASCII order prints the words sorted.
- BST: O(log n) average per operation (O(n) worst case). In-order traversal gives
  sorted output.
- Dictionary: O(1) average insert/search; needs an O(n log n) sort to print.

BST insert/search/printing use loops and a stack (no deep recursion); the Trie printing is a short
recursive function (depth = longest word). All three versions produce identical output, which the
test cases confirm.
