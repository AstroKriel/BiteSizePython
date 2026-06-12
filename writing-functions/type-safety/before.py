##
## === DEPENDENCIES
##

## third-party
import numpy

##
## === STATISTICS
##


def compute_stats(values):
    mean = float(numpy.mean(values))
    std = float(numpy.std(values))
    return mean, std


##
## === NORMALISATION
##


def normalise(values, mean, std):
    return (values - mean) / std


##
## === PROGRAM MAIN
##


def main():
    ## std is 0.0; the result is nan but no error is raised
    flat_data = numpy.array([3.0, 3.0, 3.0, 3.0])
    mean, std = compute_stats(flat_data)
    normalised_flat = normalise(flat_data, mean, std)
    print(normalised_flat)

    ## stats is a (mean, std) pair; the error says shapes don't match
    data = numpy.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    stats = compute_stats(data)
    normalised = normalise(data, stats, 1.0)
    print(normalised)


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()
