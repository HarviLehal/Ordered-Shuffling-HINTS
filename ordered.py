import numpy as np
import random
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_id, data=None, level=None, parent_id=None):
        self.node_id = node_id      # Node ID
        self.data = data            # Data
        self.level = level          # Level
        self.parent_id = parent_id  # Parent ID
        self.children = []

    def add_child(self, child):
        child.parent_id = self.node_id
        self.children.append(child)

def swap_subnodes(node):
    if not node.children:
        return
    
    random.shuffle(node.children)
    
    for child in node.children:
        swap_subnodes(child)

def print_tree(node, level=0):
    if not node:
        return
    print("  " * level + f"Node ID: {node.node_id}, Data: {node.data}, Level: {node.level}, Parent ID: {node.parent_id}, Children: {[child.node_id for child in node.children]}")
    for child in node.children:
        print_tree(child, level + 1)

def plot_tree(node, level=0):
    if not node:
        return
    plt.scatter(level, node.node_id, color='blue')  # Plot the node
    for child in node.children:
        plt.plot([level, level+1], [node.node_id, child.node_id], color='black')  # Plot edge between parent and child
        plot_tree(child, level + 1)

class OrderedTree:
    def __init__(self, x, levels, branch_factor):
        self.x = x
        self.levels = levels
        self.branch_factor = branch_factor
        self.design = np.array([1] + [2 ** self.branch_factor for _ in range(self.levels)])
        self.scenarios = 1 * 2 ** (self.levels * self.branch_factor)

    def build_tree(self):
        self.tree = [Node(0, data=self.x, level=0, parent_id=None)]
        for i in range(1, self.levels+1):
            for j in range(len(self.level_set(i-1))):
                parent = self.tree[self.level_set(i-1)[j].node_id]
                data = np.array_split(parent.data, 2**self.branch_factor)
                for k in range(2**self.branch_factor):
                    child = Node(len(self.tree), data=data[k], level=i, parent_id=parent.node_id)
                    parent.add_child(child)
                    self.tree.append(child)

    def level_set(self, level):
        return [i for i in self.tree if i.level == level]

    def common_parent_set(self, parent_id):
        return [i for i in self.tree if i.parent_id == parent_id]

    def child_set(self, node_id):
        return [i for i in self.tree if i.parent_id == node_id]

# Example usage:
d = 16  # length of time series
a = 2  # number of levels
b = 2  # log branch factor
n = 2**(a*b)  # number of scenarios

split = np.linspace(0, d, n+1)  # split time series

# change splits into pairs of scenarios
scenarios = []
for i in range(len(split)-1):
    scenarios.append([split[i], split[i+1]])

# convert scenarios to numpy array
scenarios = np.array(scenarios)

# Create and build the tree
tree = OrderedTree(scenarios, levels=a, branch_factor=b)
tree.build_tree()

# Print the original tree
print("Original Tree:")
print_tree(tree.tree[0])  # Assuming the root node is at index 0


# Perform swapping
swap_subnodes(tree.tree[0])

# Print the tree after swapping
print("\nTree After Swapping")
print_tree(tree.tree[0])  # Assuming the root node is at index 0