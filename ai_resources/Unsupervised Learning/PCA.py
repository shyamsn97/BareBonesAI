
import numpy as np
import sys
sys.path.append('../tools')
import tools

class PCA():
    """
    Dimensionality reduction using the diagonalization of a covariance matrix
    Can specify whether to use calculate the covariance matrix of the rows or columns of a given data matrix
    Parameters:
    numpy array X: data matrix
    boolean column: determines whether to generate covariance matrix from columns or rows
    numpy array eigenvalues and eigenvectors: eigenvalues and eigenvectors of the covariance matrix
    numpy array proportion_variance: variance explained by PCs
    numpy array cumulative_var: cumulative variance explained by PCs
    """
    def __init__(self, X,column=True):
        self.column = column #PCA using the rows of X or the columns to construct the cov matrix
        self.X = X
        if(column == True):
            self.mumat = X.mean(axis=0)
            self.cov = compute_covariance(X)
        else:
            self.mumat = X.mean(axis=1)
            self.cov = compute_covariance(X,False)
        self.X_shifted = self.X - self.mumat
        self.eigenvalues, self.eigenvectors = np.linalg.eig(self.cov)
        self.eigenvectors = self.eigenvectors.astype(float).real
        self.eigenvalues = np.sort(self.eigenvalues)[::-1]
        self.proportion_variance = ((self.eigenvalues/float(sum(self.eigenvalues))).astype(float)).real
        self.cumulative_var = np.cumsum(self.proportion_variance)
        
    def rank(self,n):
        #this approximates the original matrix by using n eigenvectors corresponding to the biggest eigenvalues    
        eigenvalues = self.eigenvalues
        eigenvectors = self.eigenvectors
        indices = eigenvalues.argsort()[::-1][:n]  
        Q = eigenvectors[:,indices]
        if self.column == False:
            return Q.dot(Q.T.dot(self.X_shifted)).astype(float) + self.mumat
        else:
            return self.X_shifted.dot(Q).dot(Q.T).astype(float) + self.mumat
            
    def project(self,n):
        #this projects the data onto a lower dimension
        eigenvalues = self.eigenvalues
        eigenvectors = self.eigenvectors
        indices = eigenvalues.argsort()[::-1][:n]
        Q = eigenvectors[:,indices]
        
        return self.X.dot(Q).astype(float) 