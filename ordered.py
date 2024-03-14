import numpy as np
import random
from tqdm import tqdm
import seaborn as sns
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 1})



d = 100 # length of time series

n = 4  # number of scenarios

split = np.linspace(0, d, n+1)  # split time series

# change splits into pairs of scenarios
scenarios = []
for i in range(len(split)-1):
    scenarios.append([split[i], split[i+1]])

# convert scenarios to numpy array
scenarios = np.array(scenarios)

class Node:
    def __init__(self, node_id, data=None, level=None, parent_id=None, child_id=None):
        self.node_id = node_id      # Node ID
        self.data = data            # Data
        self.level = level          # Level
        self.parent_id = parent_id  # Parent ID
        self.child_id = child_id    # Child ID

class OrderedTree: # Tree where common parent nodes cannot have gaps between them 
    def __init__(self, x, levels, branch_factor):
        self.x = x                                                                           # Data
        self.levels = levels                                                                     # Number of Levels
        self.branch_factor = branch_factor                                               # Log Branch Factor
        self.design = np.array([1] + [2 ** self.branch_factor for _ in range(self.levels)])
        self.scenarios = 1 * 2 ** (self.levels * self.branch_factor)                         # Number of Scenarios

    def build_tree(self):
        # root node
        self.tree = [Node(0, data=self.x, level=0, parent_id=None)]
        # iterate through levels
        for i in range(1, self.levels+1):
            # we must iterate through the parent nodes and split their data
            for j in range(len(self.level_set(i-1))):
                # parent node
                parent = self.tree[self.level_set(i-1)[j].node_id]
                # data (split data in log branch factor for each node)
                data = np.array_split(parent.data, 2**self.branch_factor)
                # iterate through branch factor
                for k in range(2**self.branch_factor):
                    # add node
                    self.tree.append(Node(len(self.tree), data=data[k], level=i, parent_id=parent.node_id))
        # add child_id to parent nodes
            for i in range(0, self.levels):
                for j in range(len(self.level_set(i))):
                    parent = self.tree[self.level_set(i)[j].node_id]
                    parent.child_id = [i.node_id for i in self.level_set(i+1) if i.parent_id == parent.node_id]


    def level_set(self, level): # return the set of nodes at a given level
        return [i for i in self.tree if i.level == level]
    
    def common_parent_set(self, parent_id): # return the set of nodes with the same parent
        return [i for i in self.tree if i.parent_id == parent_id]
    
    def child_set(self, node_id): # return the set of nodes with the same parent
        return [i for i in self.tree if i.parent_id == node_id]

    
    def shuffle_tree(self):
    # to shuffle the tree, we want to shuffle top down, swapping nodes of the same level, but making sure they stay
    # with their sibling and keep the same parent.
        for i in range(1, self.levels+1):
            # get the level set for the current level
            level_set = self.level_set(i)
            # create a reordered node_id list
            node_id_list = [i.node_id for i in level_set]
            node_id_list = np.random.permutation(node_id_list)
            # for each node in the level, replace the node_id with the shuffled node_id
            new_level_set = level_set
            for j in range(len(level_set)):
                new_level_set[j].node_id = node_id_list[j]
                # obtain common parent set for each node in the level
                common_parent_set = self.common_parent_set(level_set[j].parent_id)
                # for each node in the common parent set, change the parent_id to the parent's new node_id
                new_common_parent_set = common_parent_set
                for k in range(len(common_parent_set)):
                    new_common_parent_set[k].parent_id = node_id_list[j]
            # replace the tree level with the new level
            
    def shuffle_tree_2(self):
        # to shuffle the tree, we want to shuffle top down, swapping nodes of the same level, but making sure they stay
        # with their sibling and keep the same parent.
        # we must go through each common parent set and shuffle the nodes
        for i in range(1, self.levels+1):
            # get the level set for the level above
            level_set = self.level_set(i-1)
            # for each node in the level above, obtain the child set
            for j in range(len(level_set)):
                child_set = self.child_set(level_set[j].node_id)
                # create a reordered node_id list
                node_id_list = [i.node_id for i in child_set]
                node_id_list = np.random.permutation(node_id_list)
                # for each node in the common parent set, replace the node_id with the shuffled node_id
                new_child_set = child_set
                for k in range(len(child_set)):
                    new_child_set[k].node_id = node_id_list[k]
                    # obtain the children of the new nodes
                    c
                    # for each child, change the parent_id to the parent's new node_id
                    new_children = children
                    for l in range(len(children)):
                        new_children[l].parent_id = node_id_list[k]
                # replace the tree level with the new level
                self.tree = [i for i in self.tree if i.level != i]



a = 2
b = 1
tree = OrderedTree(scenarios , a, b)

tree.build_tree()

# for i in tree.tree:
#     print("Node ID: ", i.node_id, ", Level: ", i.level, ", Parent ID: ", i.parent_id, "\n Data: ", i.data, "\n")

tree.shuffle_tree()

for i in tree.tree:
    print("Node ID: ", i.node_id, ", Level: ", i.level, ", Parent ID: ", i.parent_id, ", Children IDs:", i.child_id, "\n Data: ", i.data, "\n")