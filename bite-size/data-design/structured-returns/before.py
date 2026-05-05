##
## === DEPENDENCIES
##

import numpy
from numpy.typing import NDArray

##
## === FIELD STATS
##


def compute_field_stats_as_tuple(
    field: NDArray,
) -> tuple:
    min_value = field.min()
    p16_value = numpy.percentile(field, 16)
    p50_value = numpy.percentile(field, 50)
    p84_value = numpy.percentile(field, 84)
    max_value = field.max()
    return (
        min_value,
        p16_value,
        p50_value,
        p84_value,
        max_value,
    )


def compute_field_stats_as_dict(
    field: NDArray,
) -> dict:
    min_value = field.min()
    p16_value = numpy.percentile(field, 16)
    p50_value = numpy.percentile(field, 50)
    p84_value = numpy.percentile(field, 84)
    max_value = field.max()
    return {
        "min_value": min_value,
        "p16_value": p16_value,
        "p50_value": p50_value,
        "p84_value": p84_value,
        "max_value": max_value,
    }


##
## === MAIN
##


def main() -> None:
    rng = numpy.random.default_rng(seed=0)
    rho = rng.uniform(
        low=0.1,
        high=10.0,
        size=(64, 64, 64),
    )

    ## --- tuple: what is the order?
    min_value, p16_value, p50_value, p84_value, max_value = compute_field_stats_as_tuple(rho)

    ## --- tuple: what does index 2 mean?
    stats = compute_field_stats_as_tuple(rho)
    print(stats[0], stats[2])

    ## --- dict: typo on assignment silently adds a wrong key; no error
    stats = compute_field_stats_as_dict(rho)
    stats["p50_val"] = 0.0
    print(stats)

    ## --- dict: typo on access raises KeyError; but only at access time, not when the bug was introduced
    stats = compute_field_stats_as_dict(rho)
    # print(stats["p50_val"])  # uncomment to see KeyError


if __name__ == "__main__":
    main()
