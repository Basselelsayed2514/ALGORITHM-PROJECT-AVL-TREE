import tkinter as tk
from tkinter import messagebox
from functools import reduce

class Node:
    def __init__(self, key):
        self.key = key
        self.delta = 0
        self.left = None
        self.right = None
        self.parent = None
        self.x = None  # Added x attribute
        self.y = None  # Added y attribute

    def set_left(self, x):
        self.left = x
        if x is not None:
            x.parent = self

    def set_right(self, x):
        self.right = x
        if x is not None:
            x.parent = self

    def set_children(self, x, y):
        self.set_left(x)
        self.set_right(y)

    def replace_by(self, y):
        if self.parent is None:
            if y is not None:
                y.parent = None
        elif self.parent.left == self:
            self.parent.set_left(y)
        else:
            self.parent.set_right(y)
        self.parent = None

    def sibling(self):
        if self.parent.left == self:
            return self.parent.right
        else:
            return self.parent.left

    def uncle(self):
        return self.parent.sibling()

    def grandparent(self):
        return self.parent.parent

class AVLTreeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("AVL Tree GUI")

        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()

        self.avl_tree = None

        self.insert_entry = tk.Entry(master)
        self.insert_entry.pack()

        insert_button = tk.Button(master, text="Insert", command=self.insert_key)
        insert_button.pack()

        self.draw_tree()

    def insert_key(self):
        try:
            key = int(self.insert_entry.get())
            if self.avl_tree is None:
                self.avl_tree = Node(key)
            else:
                self.avl_tree = avl_insert(self.avl_tree, key)
            self.draw_tree()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def draw_tree(self):
        self.canvas.delete("all")
        if self.avl_tree:
            self.pre_order_traversal(self.avl_tree, self.canvas, 400, 50)

    def pre_order_traversal(self, root, canvas, x, y):
        if root:
            root.x = x  # Assign x coordinate
            root.y = y  # Assign y coordinate
            canvas.create_text(root.x, root.y, text=str(root.key), font=("Helvetica", 12, "bold"))

            if root.left:
                self.pre_order_traversal(root.left, canvas, x - 50, y + 30)  # Adjust spacing as needed
            if root.right:
                self.pre_order_traversal(root.right, canvas, x + 50, y + 30)  # Adjust spacing as needed

def left_rotate(t, x):
    (parent, y) = (x.parent, x.right)
    (a, b, c) = (x.left, y.left, y.right)
    x.replace_by(y)
    x.set_children(a, b)
    y.set_children(x, c)
    if parent is None:
        t = y
    return t

def right_rotate(t, y):
    (parent, x) = (y.parent, y.left)
    (a, b, c) = (x.left, x.right, y.right)
    y.replace_by(x)
    y.set_children(b, c)
    x.set_children(a, y)
    if parent is None:
        t = x
    return t

def avl_insert(t, key):
    root = t
    x = Node(key)
    parent = None
    while t:
        parent = t
        if key < t.key:
            t = t.left
        else:
            t = t.right
    if parent is None:
        root = x
    elif key < parent.key:
        parent.set_left(x)
    else:
        parent.set_right(x)
    return avl_insert_fix(root, x)

def avl_insert_fix(t, x):
    while x.parent is not None:
        d2 = d1 = x.parent.delta
        if x == x.parent.left:
            d2 = d2 - 1
        else:
            d2 = d2 + 1
        x.parent.delta = d2
        (p, l, r) = (x.parent, x.parent.left, x.parent.right)
        if abs(d1) == 1 and abs(d2) == 0:
            return t
        elif abs(d1) == 0 and abs(d2) == 1:
            x = x.parent
        elif abs(d1) == 1 and abs(d2) == 2:
            if d2 == 2:
                if r.delta == 1:  # Right-right case
                    p.delta = 0
                    r.delta = 0
                    t = left_rotate(t, p)
                if r.delta == -1:  # Right-Left case
                    dy = r.left.delta
                    if dy == 1:
                        p.delta = -1
                    else:
                        p.delta = 0
                    r.left.delta = 0
                    if dy == -1:
                        r.delta = 1
                    else:
                        r.delta = 0
                    t = right_rotate(t, r)
                    t = left_rotate(t, p)
            if d2 == -2:
                if l.delta == -1:  # Left-left case
                    p.delta = 0
                    l.delta = 0
                    t = right_rotate(t, p)
                if l.delta == 1:  # Left-right case
                    dy = l.right.delta
                    if dy == 1:
                        l.delta = -1
                    else:
                        l.delta = 0
                    l.right.delta = 0
                    if dy == -1:
                        p.delta = 1
                    else:
                        p.delta = 0
                    t = left_rotate(t, l)
                    t = right_rotate(t, p)
            break
        else:
            print("shouldn't be there! d1=', d1, 'd2=", d2)
            assert False
    return t

def to_list(t):
    if t is None:
        return []
    else:
        return to_list(t.left) + [t.key] + to_list(t.right)

def to_tree(l):
    return reduce(avl_insert, l, None)

def to_str(t):
    if t is None:
        return "."
    else:
        return "(" + to_str(t.left) + " " + str(t.key) + ":" + str(t.delta) + " " + to_str(t.right) + ")"

def height(t):
    if t is None:
        return 0
    else:
        return 1 + max(height(t.left), height(t.right))

def is_avl(t):
    if t is None:
        return True
    else:
        delta = height(t.right) - height(t.left)
        return is_avl(t.left) and is_avl(t.right) and abs(delta) <= 1

def is_bst(t, xs):
    return to_list(t) == sorted(xs)

def main():
    root = tk.Tk()
    app = AVLTreeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
