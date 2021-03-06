# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:10:33 2018

@author: dungnq9
"""

# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals
import math, random
import numpy as np
import matplotlib.pyplot as plt
random.seed(0)

N = 100 # number of points per class
d0  = 2 # dimensionality
C = 3 # number of classes
X = np.zeros((d0, N*C)) # data matrix (each row = single example)
y = np.zeros(N*C, dtype = 'uint8') # class labels

""" https://www.geeksforgeeks.org/range-vs-xrange-python/ """
for j in range(C):
    ix = range(N*j, N*(j+1))            
    r = np.linspace(0.0, 1, N) # radius
    t = np.linspace(j*4, (j+1)*4, N) + np.random.randn(N)*0.2 # theta
    l = np.c_[r*np.sin(t), r*np.cos(t)]
    X[:, ix]  = l.T
    y[ix] = j
    
print(np.max(X))    
# lets visualize the data:
# plt.scatter(X[:N, 0], X{:N, 1}, c=y[:N], s=40, cmap=plt.cm.Spectral)

plt.plot(X[0, :N], X[1, :N], 'bs', markersize = 7);
plt.plot(X[0, N:2*N], X[1, N:2*N], 'ro', markersize = 7);
plt.plot(X[0, 2*N:], X[1, 2*N:], 'g^', markersize = 7);
# plt.axis('off')
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5, 1.5])
cur_axes = plt.gca()
cur_axes.axes.get_xaxis().set_ticks([])
cur_axes.axes.get_yaxis().set_ticks([])

plt.savefig('EX.png', bbox_inches='tight', dpi = 600)
plt.show()

def softmax(V):
    e_V = np.exp(V - np.max(V, axis = 0, keepdims = True))
    Z = e_V / e_V.sum(axis = 0)
    return Z

## One-hot coding
""" See https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html#scipy.sparse.coo_matrix """
from scipy import sparse
def convert_labels(y, C = 3):
    Y = sparse.coo_matrix((np.ones_like(y),
                           (y, np.arange(len(y)))), shape = (C, len(y))).toarray()
    return Y

#cost or loss function
def cost(Y, Yhat):
    return -np.sum(Y*np.log(Yhat))/Y.shape[1]

d0 = 2
d1 = h = 100 # size of hidden layer
d2 = C = 3
# initialize parameters randomly
W1_init = 0.01*np.random.randn(d0, d1)
b1_init = np.zeros((d1, 1))
W2_init = 0.01*np.random.randn(d1, d2)
b2_init = np.zeros((d2, 1))

eta = 1 # learning rate

def mlpClassifier(X, y, W1, b1, W2, b2, eta, max_count = 10000):
    Y = convert_labels(y, C)
    N = X.shape[1]
    
    for i in range(max_count):
        ## Feedforward
        Z1 = np.dot(W1.T, X) + b1
        A1 = np.maximum(Z1, 0)
        Z2 = np.dot(W2.T, A1) + b2
        Yhat = softmax(Z2)  # output using softmax activation function
        
        # print loss after each 1000 iterations
        if i % 1000 == 0:
            # compute the loss: average cross-entropy loss
            loss = cost(Y, Yhat)
            print("iter %d, lost: %f" %(i, loss))
        
        # backpropagation
        E2 = (Yhat - Y)/N
        dW2 = np.dot(A1, E2.T)    
        db2 = np.sum(E2, axis = 1, keepdims = True)
        E1 = np.dot(W2, E2)
        E1[Z1 <= 0] = 0 # gradient of ReLU
        dW1 = np.dot(X, E1.T)
        db1 = np.sum(E1, axis = 1, keepdims = True)
        
        # Gradient Descent update
        W1 += -eta*dW1
        b1 += -eta*db1
        W2 += -eta*dW2
        b2 += -eta*db2
    
    return (W1, b1, W2, b2)

W1, b1, W2, b2 = mlpClassifier(X, y, W1_init, b1_init, W2_init, b2_init, eta)

print(W1, W2)
print()
print(b1, b2)
print()

Z1 = np.dot(W1.T, X) + b1
A1 = np.maximum(Z1, 0)
Z2 = np.dot(W2.T, A1) + b2
"""
DUNGNQ9: Returns the indices of the maximum values along an axis.
This is equivalent to the maximum values using softmax
"""
predicted_class = np.argmax(Z2, axis=0)
print('training accuracy: %.2f %%' % (100*np.mean(predicted_class == y)))

#use sklearn library
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='lbfgs', alpha = 1e-5,
                    hidden_layer_sizes = (d1,), random_state = 0)
clf.fit(X.T, y)
print()
print(clf.coefs_)
print()
print(clf.intercepts_)
print(clf.n_iter_, clf.n_layers_, clf.n_outputs_)


