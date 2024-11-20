class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.middle = None
        self.right = None


class TernaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value, position=None):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value, position)

    def _insert(self, node, value, position):
        if position == "left":
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert(node.left, value, position)
        elif position == "middle":
            if node.middle is None:
                node.middle = Node(value)
            else:
                self._insert(node.middle, value, position)
        elif position == "right":
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert(node.right, value, position)
        else:
            raise ValueError("Invalid position: use 'left', 'middle', or 'right'.")

    def print_tree(self, node=None, prefix="", is_last=True):
        if node is None:
            node = self.root 

        connector = "└── " if is_last else "├── "
        print(prefix + connector + str(node.value))

        new_prefix = prefix + ("    " if is_last else "│   ")

        children = [node.left, node.middle, node.right]
        children = [child for child in children if child is not None]

        for i, child in enumerate(children):
            self.print_tree(child, new_prefix, i == len(children) - 1)
