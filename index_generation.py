"""
Index Generation Utility (Lab Exam 2, Data Structures)

Usage:  python index_generation.py <input_file> <output_file> [trie|bst|dict]

Reads a text file and writes an index: every distinct word (in ASCII order)
followed by the line numbers where it appears.

Design in short:
  * Separators between words: blank, line break, '.', ',', ':', ';'
    Every other printable ASCII character is part of a word.
  * Every distinct word keeps its line numbers in a linked-list queue.
  * Three ways to store the words: Trie, BST, Python dict.
"""

import sys

sys.setrecursionlimit(100000)   # the Trie printing is recursive (depth = word length)


# ---------------------------------------------------------------
# Linked-list queue of line numbers
# ---------------------------------------------------------------
class LineNode:
    def __init__(self, line_no):
        self.line_no = line_no
        self.next = None


class LineQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, line_no):
        """Add a line number at the tail."""
        if self.tail is not None and self.tail.line_no == line_no:
            return                      # same word twice on one line: store once
        node = LineNode(line_no)
        if self.head is None:           # queue was empty
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def to_list(self):
        """Read all line numbers from head to tail."""
        numbers = []
        cur = self.head
        while cur is not None:
            numbers.append(cur.line_no)
            cur = cur.next
        return numbers


# ---------------------------------------------------------------
# 1) Trie
# ---------------------------------------------------------------
class TrieNode:
    def __init__(self):
        self.children = {}      # character -> TrieNode
        self.lines = None       # LineQueue if a word ends at this node


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, line_no):
        node = self.root
        for ch in word:                         # walk down, creating nodes
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        if node.lines is None:                  # first time we see this word
            node.lines = LineQueue()
        node.lines.enqueue(line_no)

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node.lines                       # None if no word ends here

    def items(self):
        """All (word, LineQueue) pairs in ASCII order."""
        result = []
        self._collect(self.root, "", result)
        return result

    def _collect(self, node, prefix, result):
        if node.lines is not None:              # a word ends here (comes first)
            result.append((prefix, node.lines))
        for ch in sorted(node.children):        # smallest character first
            self._collect(node.children[ch], prefix + ch, result)


# ---------------------------------------------------------------
# 2) Binary Search Tree
# ---------------------------------------------------------------
class BSTNode:
    def __init__(self, word):
        self.word = word
        self.lines = LineQueue()
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, word, line_no):
        # go down the tree until we find the word or reach an empty place
        parent = None
        cur = self.root
        while cur is not None and cur.word != word:
            parent = cur
            cur = cur.left if word < cur.word else cur.right
        if cur is None:                         # word is new: attach a new node
            cur = BSTNode(word)
            if parent is None:
                self.root = cur
            elif word < parent.word:
                parent.left = cur
            else:
                parent.right = cur
        cur.lines.enqueue(line_no)

    def search(self, word):
        cur = self.root
        while cur is not None and cur.word != word:
            cur = cur.left if word < cur.word else cur.right
        if cur is None:
            return None
        return cur.lines

    def items(self):
        """All (word, LineQueue) pairs in ASCII order (in-order traversal)."""
        result = []
        stack = []
        cur = self.root
        while cur is not None or stack:
            while cur is not None:              # go as far left as possible
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            result.append((cur.word, cur.lines))
            cur = cur.right
        return result


# ---------------------------------------------------------------
# 3) Python dictionary
# ---------------------------------------------------------------
class DictIndex:
    def __init__(self):
        self.table = {}                         # word -> LineQueue

    def insert(self, word, line_no):
        if word not in self.table:
            self.table[word] = LineQueue()
        self.table[word].enqueue(line_no)

    def search(self, word):
        return self.table.get(word)

    def items(self):
        # sorted() on strings uses ASCII order
        return [(word, self.table[word]) for word in sorted(self.table)]


# ---------------------------------------------------------------
# Reading the file and writing the index
# ---------------------------------------------------------------
STRUCTURES = {"trie": Trie, "bst": BST, "dict": DictIndex}


def build_index(structure_name, input_file):
    index = STRUCTURES[structure_name]()
    with open(input_file, "r", encoding="ascii", errors="replace") as f:
        for line_no, line in enumerate(f, start=1):
            for separator in ".,:;":            # turn separators into blanks
                line = line.replace(separator, " ")
            for word in line.split():           # split() ignores extra blanks
                index.insert(word, line_no)
    return index


def write_index(index, output_file):
    with open(output_file, "w", encoding="ascii", errors="replace") as out:
        for word, queue in index.items():
            numbers = ", ".join(str(n) for n in queue.to_list())
            out.write(word + " : " + numbers + "\n")


def main():
    if len(sys.argv) < 3:
        print("Usage: python index_generation.py <input_file> <output_file> [trie|bst|dict]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    method = sys.argv[3].lower() if len(sys.argv) > 3 else "dict"
    if method not in STRUCTURES:
        print("Method must be trie, bst or dict")
        sys.exit(1)

    index = build_index(method, input_file)
    write_index(index, output_file)
    print("Index built using", method, "- written to", output_file)


if __name__ == "__main__":
    main()
