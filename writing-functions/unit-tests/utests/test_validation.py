## { U-TEST

##
## === DEPENDENCIES
##

## stdlib
import unittest

## local
from local_helpers import validation

##
## === TEST SUITE
##


class TestRequirePositive(unittest.TestCase):

    def test_returns_value_when_positive(
        self,
    ) -> None:
        result = validation.require_positive(
            3.0,
        )
        self.assertEqual(
            result,
            3.0,
        )

    def test_zero_raises(
        self,
    ) -> None:
        with self.assertRaises(
            ValueError,
        ):
            validation.require_positive(
                0.0,
            )

    def test_negative_raises(
        self,
    ) -> None:
        with self.assertRaises(
            ValueError,
        ):
            validation.require_positive(
                -1.0,
            )


class TestRequireNonEmpty(unittest.TestCase):

    def test_returns_items_when_non_empty(
        self,
    ) -> None:
        result = validation.require_non_empty(
            [1, 2, 3],
        )
        self.assertEqual(
            result,
            [1, 2, 3],
        )

    def test_empty_raises(
        self,
    ) -> None:
        with self.assertRaises(
            ValueError,
        ):
            validation.require_non_empty(
                [],
            )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    unittest.main()

## } U-TEST
