import torch

class LinearModel:

    def __init__(self):
        self.w = None 

    def score(self, X):
        """
        Compute the scores for each data point in the feature matrix X. 
        The formula for the ith entry of s is s[i] = <self.w, x[i]>. 

        If self.w currently has value None, then it is necessary to first initialize self.w to a random value. 

        ARGUMENTS: 
            X, torch.Tensor: the feature matrix. X.size() == (n, p), 
            where n is the number of data points and p is the 
            number of features. This implementation always assumes 
            that the final column of X is a constant column of 1s. 

        RETURNS: 
            s torch.Tensor: vector of scores. s.size() = (n,)
        """
        if self.w is None: 
            self.w = torch.rand((X.size()[1]))

        # your computation here: compute the vector of scores s
        return X@self.w

    def predict(self, X):
        """
        Compute the predictions for each data point in the feature matrix X. The prediction for the ith data point is either 0 or 1. 

        ARGUMENTS: 
            X, torch.Tensor: the feature matrix. X.size() == (n, p), 
            where n is the number of data points and p is the 
            number of features. This implementation always assumes 
            that the final column of X is a constant column of 1s. 

        RETURNS: 
            y_hat, torch.Tensor: vector predictions in {0.0, 1.0}. y_hat.size() = (n,)
        """
        s = self.score(X)
        return 1.0*(s >= 0 )
    
class Perceptron(LinearModel):

    def loss(self, X, y):
        """
        Compute the misclassification rate. In the perceptron algorith, the target vector y is assumed to have labels in {-1, 1}. A point i is classified correctly if its score s_i has the same sign as y_i. 

        ARGUMENTS: 
            X, torch.Tensor: the feature matrix. X.size() == (n, p), 
            where n is the number of data points and p is the 
            number of features. This implementation always assumes 
            that the final column of X is a constant column of 1s. 

            y, torch.Tensor: the target vector.  y.size() = (n,). In the perceptron algorithm, the possible labels for y are assumed to be {-1, 1}
        """

        # replace with your implementation
        s = self.score(X)
        return (1.0 - 1.0*(s*(2*y-1) > 0)).mean()

    def grad(self, X, y):
        s = self.score(X)
        z = 2*y-1
        return -((X.t()*z*(s*z<0))).t().mean(dim = 0)

class PerceptronOptimizer:

    def __init__(self, model):
        self.model = model 
    
    def step(self, X, y):
        """
        Compute one step of the perceptron update using the feature matrix X 
        and target vector y. 
        """
        

        # compute the loss 
        loss          = self.model.loss(X, y)

        # adjust w by the "gradient"
        self.model.w -= self.model.grad(X, y)
        
