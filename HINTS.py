import numpy as np
import random
from Tree import Tree
from tqdm import tqdm
import seaborn as sns
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 1})


'''HINTS Sampler Class

    Parameters
    ----------
    x : array
    Data

    levels : int
    Number of Levels

    branch_factor : int
    Branch Factor

    target : any
    Target Distribution

    log_likelihood : function
    Log Likelihood Function

    proposal : function
    Proposal Method Function

    theta0 : any
    Initial Parameter Values (can be specified at sampler)

    N : int
    Number of Iterations (can be specified at sampler)

    Methods
    -------
    prop(theta)
    Proposal Method

    ratio(data, theta, theta_n)
    Acceptance Ratio

    sampler(theta0, iter)
    HINTS Sampler
    '''


class HINTS():

    def __init__(self, x, levels, branch_factor, log_likelihood, proposal, theta0=None, N=None):
        self.levels = levels                                    # Number of Levels
        self.branch_factor = branch_factor                      # Log Branch Factor
        self.x = x                                              # Data
        # self.tree = Tree(x, self.levels, self.branch_factor)    # Tree Object
        # self.tree.build_tree()                                  # Build Tree Structure
        # self.design = self.tree.design                          # Design Matrix of Tree
        # self.leaves = self.tree.leaves                          # Leaf Nodes of Tree

        self.log_likelihood = log_likelihood                    # log likelihood function
        self.proposal = proposal                                # Proposal Method function

        self.theta0 = theta0                                    # Initial  values (can be specified at sampler)
        self.N = N                                              # Number of Iterations (can be specified at sampler)

    def prop(self, theta):                          # Proposal Method
        theta_n = self.proposal(theta)              # Propose new values
        return theta_n

    def ratio(self, data, theta, theta_n):          # Acceptance Ratio
        a = self.log_likelihood(data, theta_n) - self.log_likelihood(data, theta)  # Acceptance Ratio
        a = np.exp(a)                               # Exponent
        u = np.random.uniform(0, 1, 1)
        # print('acceptance threshold:', u, 'acceptance ratio:', a)
        if u <= a:
            # print('Accepted:', theta_n, 'Rejected:', theta)
            return theta_n                          # Accept Proposal
        else:
            # print('Rejected:', theta_n, 'Kept:', theta)
            return theta                            # Reject Proposal

    def sampler(self, theta0=None, iter=None):                               # HINTS Sampler
        if theta0 is not None:
            self.theta0 = theta0
        if iter is not None:
            self.N = iter

        thetas = []                                                         # Initialise theta parameter list
        theta_level = [[] for i in range(self.levels+1)]                    # Initialise theta level list
        theta_level[self.levels].append(self.theta0)                        # Append initial theta to lowest level
        thetas.append(self.theta0)                                          # Append initial theta

        for iter in tqdm(range(self.N)):                                  # HINTS Iterations
            self.x = np.random.permutation(self.x)                      # Randomly permute data
            self.tree = Tree(self.x, self.levels, self.branch_factor)    # Tree Object
            self.tree.build_tree()                                  # Build Tree Structure
            self.design = self.tree.design                          # Design Matrix of Tree
            self.leaves = self.tree.leaves                          # Leaf Nodes of Tree
            init_leaf = self.tree.rand_leaf_selection()                     # First select a random leaf to start
            parent = self.tree.parent(init_leaf)                            # Find parent node of chosen leaf
            for level in reversed(range(0, self.levels+1)):                 # For each level of the tree
                if level == self.levels:                                    # If level is lowest (leaf) level
                    common_parent_set = self.tree.common_parent(init_leaf)  # Common Parent Set of initial leaf
                else:
                    common_parent_set = self.tree.common_parent(parent)     # Common Parent Set of next level

                for index, node in enumerate(common_parent_set):            # Iterate through common parent set
                    theta_old = thetas[-1]                                  # Previous theta
                    theta_prop = self.prop(theta_old)                       # Propose new theta
                    theta_new = self.ratio(node.data, theta_old, theta_prop)    # Acceptance Ratio
                    thetas.append(theta_new)                                # Append new theta
                    theta_level[level].append(theta_new)                    # Append new theta to level list
                parent = self.tree.parent(common_parent_set[0])             # Parent Node
                if parent is not None:                          # Acceptance Ratio between first and last theta in common parent set against parent
                    theta_new = self.ratio(parent.data, thetas[-1], thetas[-(1+len(common_parent_set))])    
                else:
                    pass
        self.thetas = thetas                                            # Set theta parameter list
        self.theta_level = theta_level                                  # Set theta parameter list by level
        return self.thetas                                              # Return theta parameter list


# Test Example: Gaussian target and proposal
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from scipy.stats import norm

    target_mean = 20
    target_var = 1
    x = np.random.normal(target_mean, target_var, 128)
    target = {'mean': target_mean, 'var': target_var}

    proposal_var = 0.05

    def proposal(theta):
        theta_new = {}
        theta_new['mean'] = np.random.normal(theta['mean'], proposal_var)
        theta_new['var'] = np.abs(np.random.normal(theta['var'], proposal_var))
        return theta_new

    initial_mean = 10
    initial_var = 4
    initial = {'mean': initial_mean, 'var': initial_var}

    def log_likelihood(data, theta):
        mean, var = theta['mean'], theta['var']
        log_likelihoods = norm.logpdf(data, mean, var)
        return np.sum(log_likelihoods)

    levels = 3
    branch_factor = 1

    hints = HINTS(x, levels, branch_factor, log_likelihood, proposal, theta0=initial, N=1000)
    hints.sampler()
    thetas = []
    for i in hints.thetas:
        thetas.append(i['mean'])
    theta_level = hints.theta_level


    plt.figure()
    plt.plot(thetas)
    plt.xlabel('Iteration')
    plt.ylabel('Parameter Value')
    plt.title('HINTS Sampler')
    plt.show()
