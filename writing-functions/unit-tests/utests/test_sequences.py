##
## === DEPENDENCIES
##

## stdlib
import unittest

## local
from local_helpers import sequences

##
## === TEST SUITE
##


class TestChunk(unittest.TestCase):

    def test_even_split(
        self,
    ) -> None:
        result = sequences.chunk(
            [1, 2, 3, 4],
            size=2,
        )
        self.assertEqual(
            result,
            [[1, 2], [3, 4]],
        )

    def test_last_chunk_is_shorter(
        self,
    ) -> None:
        result = sequences.chunk(
            [1, 2, 3, 4, 5],
            size=2,
        )
        self.assertEqual(
            result,
            [[1, 2], [3, 4], [5]],
        )

    def test_empty_input(
        self,
    ) -> None:
        result = sequences.chunk(
            [],
            size=3,
        )
        self.assertEqual(
            result,
            [],
        )


class TestRunningTotals(unittest.TestCase):

    def test_accumulates_left_to_right(
        self,
    ) -> None:
        result = sequences.running_totals(
            [1.0, 2.0, 3.0],
        )
        self.assertEqual(
            result,
            [1.0, 3.0, 6.0],
        )

    def test_empty_input(
        self,
    ) -> None:
        result = sequences.running_totals(
            [],
        )
        self.assertEqual(
            result,
            [],
        )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    unittest.main()
