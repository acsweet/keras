import mlx.core as mx
import numpy as np

from keras.src.backend.common import dtypes
from keras.src.backend.common import standardize_dtype
from keras.src.backend.mlx.core import convert_to_tensor


def _det_2x2(a):
    return a[..., 0, 0] * a[..., 1, 1] - a[..., 0, 1] * a[..., 1, 0]


def _det_3x3(a):
    return (
        a[..., 0, 0] * a[..., 1, 1] * a[..., 2, 2]
        + a[..., 0, 1] * a[..., 1, 2] * a[..., 2, 0]
        + a[..., 0, 2] * a[..., 1, 0] * a[..., 2, 1]
        - a[..., 0, 2] * a[..., 1, 1] * a[..., 2, 0]
        - a[..., 0, 0] * a[..., 1, 2] * a[..., 2, 1]
        - a[..., 0, 1] * a[..., 1, 0] * a[..., 2, 2]
    )


def det(a):
    a_shape = a.shape
    if len(a_shape) >= 2 and a_shape[-1] == 2 and a_shape[-2] == 2:
        return _det_2x2(a)
    elif len(a_shape) >= 2 and a_shape[-1] == 3 and a_shape[-2] == 3:
        return _det_3x3(a)
    # elif len(a_shape) >= 2 and a_shape[-1] == a_shape[-2]:
    # TODO: Swap to mlx.linalg.det when supported
    a = np.array(a)
    output = np.linalg.det(a)
    return mx.array(output)


def eig(a):
    raise NotImplementedError("eig not yet implemented in mlx.")


def eigh(a):
    with mx.stream(mx.cpu):
        return mx.linalg.eigh(a)


def lu_factor(a):
    raise NotImplementedError("lu_factor not yet implemented in mlx.")


def solve(a, b):
    raise NotImplementedError("solve_triangular not yet implemented in mlx.")


def solve_triangular(a, b, lower=False):
    raise NotImplementedError("solve_triangular not yet implemented in mlx.")


def qr(x, mode="reduced"):
    if mode != "reduced":
        raise ValueError(
            "`mode` argument value not supported. "
            "Only 'reduced' is supported by the mlx backend. "
            f"Received: mode={mode}"
        )
    with mx.stream(mx.cpu):
        return mx.linalg.qr(x)


def svd(x, full_matrices=True, compute_uv=True):
    with mx.stream(mx.cpu):
        u, s, vt = mx.linalg.svd(x)
        if not compute_uv:
            return s
        if not full_matrices:
            n = min(x.shape[-2:])
            return u[..., :n], s, vt[:n, ...]
        # mlx returns full matrices by default
        return u, s, vt


def cholesky(a):
    with mx.stream(mx.cpu):
        return mx.linalg.cholesky(a)


def norm(x, ord=None, axis=None, keepdims=False):
    dtype = standardize_dtype(x.dtype)
    if "int" in dtype or dtype == "bool":
        dtype = dtypes.result_type(x.dtype, "float32")
    x = convert_to_tensor(x, dtype=dtype)
    # TODO: swap to mlx.linalg.norm when it support singular value norms
    x = np.array(x)
    output = np.linalg.norm(x, ord=ord, axis=axis, keepdims=keepdims)
    return mx.array(output)


def inv(a):
    with mx.stream(mx.cpu):
        return mx.linalg.inv(a)


def lstsq(a, b, rcond=None):
    raise NotImplementedError("lstsq not yet implemented in mlx.")
