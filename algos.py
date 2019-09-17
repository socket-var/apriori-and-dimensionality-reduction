import numpy as np
from sklearn.manifold import TSNE


def pca(X):
    # subtract mean
    X1 = X - X.mean(axis=0)

    # covariance
    cov_matrix = np.cov(X1.T)

    # obtain eigen values and eigen vectors of covariance matrix
    eig_values, eig_vectors = np.linalg.eig(cov_matrix)

    # select top n eigen values as the principal components

    top_eig_indices = eig_values.argsort()[::-1][:2]
    top_eig_vectors = eig_vectors[:, top_eig_indices]

    row_feature_vector = top_eig_vectors.T
    row_data_adjust = X1.T

    new_X = np.dot(row_feature_vector, row_data_adjust).T

    return new_X


def svd(X):
    U, _, _ = np.linalg.svd(X)
    new_X = U[:, :2]

    return new_X


def tsne(X):
    tsne = TSNE(n_components=2, n_iter=1000, init="pca")
    new_X = tsne.fit_transform(X)

    return new_X
