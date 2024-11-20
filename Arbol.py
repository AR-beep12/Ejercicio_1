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
        # Permitir insertar según posición específica
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
            raise ValueError("Posición inválida: use 'left', 'middle' o 'right'.")

    def print_tree(self, node, level=0):
        if node is not None:
            print(" " * (level * 4) + f"|- {node.value}")
            if node.left:
                print(" " * (level * 4) + "  Left:")
                self.print_tree(node.left, level + 1)
            if node.middle:
                print(" " * (level * 4) + "  Middle:")
                self.print_tree(node.middle, level + 1)
            if node.right:
                print(" " * (level * 4) + "  Right:")
                self.print_tree(node.right, level + 1)
