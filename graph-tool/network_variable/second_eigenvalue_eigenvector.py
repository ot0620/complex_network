# 第二固有値と固有ベクトルを算出する関数
def no_normalized_laplacian(g):
    L = gt.laplacian(g)
    L_sparse = sp.sparse.csr_matrix(L)
    eigenvalues, eigenvectors = sp.sparse.linalg.eigsh(L_sparse, k=2, which='SM', maxiter=100000)
    return eigenvalues[1], eigenvectors[:, 1]