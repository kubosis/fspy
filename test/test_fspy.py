import sys
import os

from typing_extensions import assert_type

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from fspy.scrapper import *


class TestFSPY(unittest.TestCase):
    def test_scrapper(self):
        scrapper_NFL = FlashScrapper("test.csv", 2000, 2001,
                                     "american-football", "usa", "nfl",
                                     verbosity_level=VERBOSITY_LEVEL_DEBUG)
        assert scrapper_NFL is not None

        scrapper_NFL.run(save_csv=False)
        data = scrapper_NFL.get_data()


        assert data is not None
        assert data.shape == (259, 8)
        assert "DT" in data
        assert "Home" in data
        assert "Away" in data
        assert "Home_points" in data
        assert "Away_points" in data
        assert "season" in data
        assert "country" in data
        assert "league" in data

        print("[SUCCESS] All tests were successful!")


if __name__ == '__main__':
    unittest.main()
