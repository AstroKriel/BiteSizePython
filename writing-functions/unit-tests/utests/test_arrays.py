##
## === DEPENDENCIES
##

## stdlib
import unittest

## third-party
import numpy

## local
from local_helpers import arrays

##
## === TEST SUITE
##


class TestNormalise(unittest.TestCase):

    def test_maps_to_unit_range(
        self,
    ) -> None:
        result = arrays.normalise(
            numpy.array([2.0, 4.0, 6.0]),
        )
        numpy.testing.assert_array_almost_equal(
            result,
            [0.0, 0.5, 1.0],
        )

    def test_output_is_float(
        self,
    ) -> None:
        result = arrays.normalise(
            numpy.array([1, 2, 3]),
        )
        self.assertEqual(
            result.dtype,
            numpy.float64,
        )

    def test_shape_is_preserved(
        self,
    ) -> None:
        values = numpy.arange(6).reshape(2, 3)
        result = arrays.normalise(values)
        self.assertEqual(
            result.shape,
            values.shape,
        )


class TestSafeLog10(unittest.TestCase):

    def test_positive_values(
        self,
    ) -> None:
        result = arrays.safe_log10(
            numpy.array([1.0, 10.0, 100.0]),
        )
        numpy.testing.assert_array_almost_equal(
            result,
            [0.0, 1.0, 2.0],
        )

    def test_zero_gives_nan(
        self,
    ) -> None:
        result = arrays.safe_log10(
            numpy.array([0.0]),
        )
        self.assertTrue(
            numpy.isnan(
                result[0],
            ),
        )

    def test_negative_gives_nan(
        self,
    ) -> None:
        result = arrays.safe_log10(
            numpy.array([-1.0, -100.0]),
        )
        self.assertTrue(
            numpy.all(
                numpy.isnan(
                    result,
                ),
            ),
        )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    unittest.main()
