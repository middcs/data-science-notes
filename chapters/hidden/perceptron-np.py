import numpy as np

class Perceptron:

    def __init__(self):
        self.w = None

    def score(self, X):
        if self.w is None:
            self.w = np.random.rand(1, X.shape[1])
        return X@self.w.T

    def loss(self, X, y):
        s = self.score(X)
        return (1 - (s.flatten()*y > 0)).mean()

    def grad(self, X, y):
        """
        not technically the gradient of the loss -- 
        actually a subgradient of the hinge loss
        """
        s = self.score(X)
        return -(X*y*(1.0*((s*y)<0))).mean(axis = 0)

class PerceptronOptimizer:

    def __init__(self, model):
        self.model = model 

    def step(self, X, y):
        # pick a random data point
        n = X.shape[0]
        i = np.random.randint(n)
        x = X[[i],:]

        # compute the loss 
        loss          = self.model.loss(x, y[i])

        # adjust w by the "gradient"
        self.model.w -= self.model.grad(x, y[i])

        return i, loss