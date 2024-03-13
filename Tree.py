import numpy as np
import random
from scipy.stats import multivariate_normal
import itertools

'''
I am trying to create a tree data structure in Python. I have a class called Node that has the following attributes:
    node_id: The ID of the node
    data: The data stored in the node
    level: The level of the node
    parent_id: The ID of the parent node

I have a class called Tree that has the following attributes:
    x: The data that is being stored in the tree
    levels: The number of levels in the tree
    branch_factor: The log of the branch factor
    data_tree: The tree data structure
    leaves: The leaf nodes

I have the following methods in the Tree class:
    build_tree that builds the tree data structure.
    get_node that returns a node given the node ID.
    rand_leaf_selection that returns a random leaf node.
    evel_set that returns a list of nodes in a given level.
    common_parent that returns a list of nodes that have the same parent.
    parent that returns the parent node.
    data_merge that merges the data from a list of nodes.
    path_to_root that returns a list of nodes that are on the path to the root.
    child that returns a list of child nodes.

I am having trouble with the following methods:
    leaf_nodes that returns a list of leaf nodes.
    path_to_node that returns a list of nodes that are on the path to a given node.
    path_to_common_parent that returns a list of nodes that are on the path to the common parent of two nodes.
'''


class Node:
    def __init__(self, node_id, data=None, level=None, parent_id=None):
        self.node_id = node_id      # Node ID
        self.data = data            # Data
        self.level = level          # Level
        self.parent_id = parent_id  # Parent ID


class Tree:
    def __init__(self, x, levels, branch_factor):
        self.levels = levels                                                                     # Number of Levels
        self.branch_factor = branch_factor                                               # Log Branch Factor
        self.design = np.array([1] + [2 ** self.branch_factor for _ in range(self.levels)])  # Design Matrix
        self.scenarios = 1 * 2 ** (self.levels * self.branch_factor)                         # Number of Scenarios
        self.x = np.split(x, self.scenarios)                                                     # Split Data into Scenarios

    def build_tree(self):
        D = []
        node = 0
        level_start = self.scenarios
        for i in range(self.levels+1):                                            # Iterate through levels
            if i == 0:                                                                  # If level is 0
                D.append([])                                                            # Append empty list
                z = int(2**(self.branch_factor*(self.levels-i-1)))                  # Number of nodes in level
                for j in range(self.scenarios):                                         # Iterate through nodes
                    node_id = node                                                      # Node ID
                    data = self.x[j]                                                    # Data
                    parent_id = self.scenarios + j % z                                  # Parent ID
                    level = self.levels                                                 # Level
                    D[i].append(Node(node_id, data, level, parent_id))                  # Append Node
                    node += 1                                                           # Increment node

            elif i == self.levels:                                                      # If level is last level
                D.append([])                                                            # Append empty list
                node_id = node                                                          # Node ID
                data = self.x                                                           # Data
                parent_id = None                                                        # Parent ID
                level = 0                                                               # Level
                D[i].append(Node(node_id=node_id, level=level, parent_id=parent_id))    # Append Node
                node += 1                                                               # Increment node

            else:
                D.append([])
                z = int(2**(self.branch_factor*(self.levels-i-1)))                  # Number of nodes in level
                for j in range(2**(self.branch_factor*(self.levels-i))):            # Iterate through nodes
                    node_id = node                                                      # Node ID
                    data = self.x[j]                                                    # Data
                    parent_id = level_start + j % z                                     # Parent ID
                    level = self.levels - i                                             # Level
                    D[i].append(Node(node_id=node_id, level=level, parent_id=parent_id))  # Append Node
                    node += 1                                                           # Increment node
            level_start = node + 2**(self.branch_factor*(self.levels-i-1))          # Number of nodes in level

        D = [elem for sublist in D for elem in sublist]     # Flatten list
        self.data_tree = D                                  # Data Tree
        leaves = []                                         # List of leaf nodes
        for x in self.data_tree:                            # Iterate through nodes
            if x.level == self.levels:                      # If node is a leaf node
                leaves.append(x)                            # Add leaf node to list
        for i in self.data_tree:                            # Iterate through nodes
            if i.data is None:                              # If node has no data
                i.data = self.data_merge(self.child(i))     # Merge data from children
        self.leaves = leaves                                # Leaf nodes

    def get_node(self, node_id):        # Get Node
        for x in self.data_tree:        # Iterate through nodes
            if x.node_id == node_id:    # If node ID matches
                return x                # Return node

    def rand_leaf_selection(self):              # Random Leaf Selection
        rand_leaf = random.choice(self.leaves)  # Random Leaf
        return rand_leaf                        # Return Random Leaf

    def level_set(self, level):                 # Level Set
        level_set = []                          # Level Set
        for x in self.data_tree:                # Iterate through nodes
            if x.level == level:                # If node is in level
                level_set.append(x)             # Add node to level set
        return level_set                        # Return level set

    def common_parent(self, node):              # Common Parent Node Set
        common_parent_set = []                  # Common Parent Node Set
        level_set = self.level_set(node.level)  # Level Set
        for x in level_set:                     # Iterate through nodes
            if x.parent_id == node.parent_id:   # If node has same parent
                common_parent_set.append(x)     # Add node to common parent set
        return common_parent_set                # Return common parent set

    def parent(self, node):                         # Parent Node
        level_set = self.level_set(node.level - 1)  # Level Set
        for x in level_set:                         # Iterate through nodes
            if x.node_id == node.parent_id:         # If node is parent
                return x                            # Return parent node

    def data_merge(self, node_set):             # Merge Data
        merge_set = []                          # Merge Set
        for i in node_set:                      # Iterate through nodes
            merge_set.append(i.data)            # Add data to merge set
        merge_set = list(itertools.chain.from_iterable(merge_set)) # Flatten list
        merge_set = np.array(merge_set)         # Convert to array
        return merge_set                        # Return merged data

    def child(self, node):                          # Child Node Set
        child_set = []                              # Child Node Set
        level_set = self.level_set(node.level + 1)  # Level Set
        for x in level_set:                         # Iterate through nodes
            if x.parent_id == node.node_id:         # If node is child
                child_set.append(x)                 # Add node to child set
        return child_set                            # Return child set

    def path_to_root(self, node):                   # Path to Root
        path = []                                   # Path to Root
        level = node.level                          # Node Level
        while level != 0:                           # While Node Level is not 0
            node = self.parent(node)                # Parent Node
            path.append(node)                       # Add Node to Path
            level = node.level                      # Node Level
        return path                                 # Return Path
