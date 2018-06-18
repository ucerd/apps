from decision_tree import DecisionTree

import numpy as np


class RandomForestClassifier:
    def __init__(self,
                 path_in,
                 n_instances,
                 n_features,
                 path_out,
                 n_estimators=10,
                 max_depth=None):
        self.path_in = path_in
        self.n_instances = n_instances
        self.n_features = n_features
        self.path_out = path_out
        self.n_estimators = n_estimators
        self.max_depth = max_depth

        self.trees = []

    def fit(self):

        for i in range(self.n_estimators):
            tree = DecisionTree(self.path_in, self.n_instances, self.n_features,
                                self.path_out, 'tree_' + str(i), self.max_depth)
            self.trees.append(tree)

        for tree in self.trees:
            tree.fit()

    def predict_probabilities(self, test_data_path):
        return sum(tree.predict_probabilities(test_data_path) for tree in self.trees) / len(self.trees)

    def predict(self, test_data_path):
        probabilities = self.predict_probabilities(test_data_path)
        # TODO
        # return self.classes_.take(np.argmax(probabilities, axis=1), axis=0)
