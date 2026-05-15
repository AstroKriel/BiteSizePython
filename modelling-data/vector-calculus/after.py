##
## === DEPENDENCIES
##

## stdlib
from pathlib import Path

## third-party
import matplotlib.pyplot as plt
import numpy
from numpy.typing import NDArray

##
## === CONSTANTS
##

NUM_POINTS = 64
X_MIN, X_MAX = -numpy.pi, numpy.pi
Y_MIN, Y_MAX = -numpy.pi, numpy.pi
FIGURES_DIR = Path("figures")

##
## === SETUP
##


def make_vector_field(xx: NDArray, yy: NDArray) -> NDArray:
    return numpy.stack(
        [
            numpy.sin(yy) + 1.5,
            numpy.cos(xx) + 1.5,
        ],
        axis=0,
    )


def normalise(b: NDArray) -> NDArray:
    magnitude = numpy.sqrt(numpy.sum(b**2, axis=0, keepdims=True))
    return b / magnitude


def compute_gradient_tensor(b: NDArray, dx: float, dy: float) -> NDArray:
    n_comp = b.shape[0]
    nx, ny = b.shape[1], b.shape[2]
    grad_b = numpy.zeros(
        shape=(n_comp, n_comp, nx, ny),
    )
    for j in range(n_comp):
        grads = numpy.gradient(b[j], dx, dy)
        for i, g in enumerate(grads):
            grad_b[j, i] = g
    return grad_b


##
## === MAIN
##


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    x = numpy.linspace(
        start=X_MIN,
        stop=X_MAX,
        num=NUM_POINTS,
        endpoint=False,
    )
    y = numpy.linspace(
        start=Y_MIN,
        stop=Y_MAX,
        num=NUM_POINTS,
        endpoint=False,
    )
    dx = float(x[1] - x[0])
    dy = float(y[1] - y[0])
    xx, yy = numpy.meshgrid(x, y, indexing="ij")
    b = make_vector_field(xx, yy)
    b_hat = normalise(b)
    grad_b = compute_gradient_tensor(b_hat, dx, dy)
    ## kappa_j = b_i * d(b_j)/d(x_i): "ixy,jixy->jxy" sums over i, keeps j, x, y
    kappa = numpy.einsum("ixy,jixy->jxy", b_hat, grad_b)
    kappa_magn = numpy.sqrt(numpy.sum(kappa**2, axis=0))
    print(f"\t> curvature magnitude: min={kappa_magn.min():.4f}, max={kappa_magn.max():.4f}")
    fig, ax = plt.subplots()
    im = ax.pcolormesh(xx, yy, kappa_magn, cmap="inferno")
    fig.colorbar(im, ax=ax, label=r"$|\kappa|$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig_path = FIGURES_DIR / "curvature_after.png"
    fig.savefig(fig_path, dpi=150)
    print(f"\t> saved: {fig_path}")


if __name__ == "__main__":
    main()
