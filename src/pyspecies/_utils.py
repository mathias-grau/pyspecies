import numpy as np


def XtoUV(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Recovers the concentration vector of species U and V from the concatenated vector.

    Args:
        X (np.ndarray): Concatenated vector.

    Returns:
        tuple[np.ndarray, np.ndarray]: Species concentration vectors.
    """
    K = len(X) // 2
    return X[:K], X[K:]


def UVtoX(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    """Concatenates the concentration vector of species U and V.

    Args:
        U (np.ndarray): First species concentration vector.
        V (np.ndarray): Second species concentration vector.

    Returns:
        np.ndarray: Concatenated vectors.
    """
    K = len(U)
    X = np.zeros(2 * K)
    X[:K] = U
    X[K:] = V
    return X


def merge_diags(P: list[list], Q: list[list], R: list[list], S: list[list]):
    """Assemble the list of diagonals of the Jacobian from block data.

    Args:
        P (list[list]): List of diagonals for upper-left Jacobian block.
        Q (list[list]): List of diagonals for upper-right Jacobian block.
        R (list[list]): List of diagonals for lower-left Jacobian block.
        S (list[list]): List of diagonals for lower-right Jacobian block.

    Returns:
        list[list]: List of diagonals for full Jacobian.
    """
    return [
        Q[0],
        Q[1],
        Q[2],
        np.concatenate((P[0], Q[3], S[0])),
        np.concatenate((P[1], Q[4], S[1])),
        np.concatenate((P[2], S[2])),
        np.concatenate((P[3], R[0], S[3])),
        np.concatenate((P[4], R[1], S[4])),
        R[2],
        R[3],
        R[4],
    ]


def f(i: int, A: np.ndarray, B: np.ndarray, D: np.ndarray, R: np.ndarray) -> np.ndarray:
    """Used to compute the function whose roots are looked for.

    See the theory for more details.

    Args:
        i (int): Species index.
        A (np.ndarray): First concentration vector.
        B (np.ndarray): Second concentration vector.
        D (np.ndarray): Normalized diffusion matrix.
        R (np.ndarray): Normalized reaction matrix.

    Returns:
        np.ndarray: Output vector.
    """
    assert i == 0 or i == 1
    A2, AB = A * A, A * B
    center = (
        ((1 - R[i, 0] + 2 * D[i, 0]) * A)
        + ((R[i, i + 1] + 2 * D[i, i + 1]) * A2)
        + ((R[i, 2 - i] + 2 * D[i, 2 - i]) * AB)
    )
    border = D[i, 0] * A + D[i, i + 1] * A2 + D[i, 2 - i] * AB
    return center - np.roll(border, 1) - np.roll(border, -1)


def mu(i: int, A: np.ndarray, B: np.ndarray, D: np.ndarray) -> np.ndarray:
    """Used to compute the Jacobian.

    See the theory for more details.

    Args:
        i (int): Species index.
        A (np.ndarray): First concentration vector.
        B (np.ndarray): Second concentration vector.
        D (np.ndarray): Normalized diffusion matrix.

    Returns:
        np.ndarray: Output vector.
    """
    assert i == 0 or i == 1
    return D[i, 0] * np.ones(len(A)) + 2 * D[i, i + 1] * A + D[i, 2 - i] * B


def nu(
    i: int, A: np.ndarray, B: np.ndarray, D: np.ndarray, R: np.ndarray
) -> np.ndarray:
    """Used to compute the Jacobian.

    See the theory for more details.

    Args:
        i (int): Species index.
        A (np.ndarray): First concentration vector.
        B (np.ndarray): Second concentration vector.
        D (np.ndarray): Normalized diffusion matrix.
        R (np.ndarray): Normalized reaction matrix.

    Returns:
        np.ndarray: Output vector.
    """
    assert i == 0 or i == 1
    return (
        (1 - R[i, 0] + 2 * D[i, 0]) * np.ones(len(A))
        + 2 * (R[i, i + 1] + 2 * D[i, i + 1]) * A
        + (R[i, 2 - i] + 2 * D[i, 2 - i]) * B
    )


def block_diags(i: int, A: np.ndarray, D: np.ndarray, R: np.ndarray):
    """Used to compute two of the Jacobian's blocks.

    See the theory for more details.

    Args:
        i (int): Species index.
        A (np.ndarray): First concentration vector.
        B (np.ndarray): Second concentration vector.
        D (np.ndarray): Normalized diffusion matrix.
        R (np.ndarray): Normalized reaction matrix.

    Returns:
        np.ndarray: Output vector.
    """
    DA = D[i, 2 - i] * A
    return [
        [-DA[-1]],
        -DA[1:],
        R[i, 2 - i] * A + 2 * DA,
        -DA[:-1],
        [-DA[0]],
    ]
