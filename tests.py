import unittest

from utils import *


class TestFunctions(unittest.TestCase):
    def test_generate_filename(self):
        self.assertEqual(
            generate_filename("Frasier", 1, 1, None, "The Good Son"),
            "Frasier - S01E01 - The Good Son",
        )
        self.assertEqual(
            generate_filename("Frasier", "01", "02", None, "Space Quest"),
            "Frasier - S01E02 - Space Quest",
        )
        self.assertEqual(
            generate_filename("Frasier", 6, "23", 24, "Shutout in Seattle"),
            "Frasier - S06E23-E24 - Shutout in Seattle",
        )
        self.assertEqual(
            generate_filename(
                "Frasier", "08", 1, "2", "And the Dish Ran Away With the Spoon"
            ),
            "Frasier - S08E01-E02 - And the Dish Ran Away With the Spoon",
        )

    def test_guess_the_show(self):
        self.assertEqual(
            guess_the_show("Frasier.S07E01.BDRip.x265-ION265.mp4"), "Frasier"
        )
        self.assertEqual(guess_the_show("RARBG.txt"), None)

    def test_is_dual_episode(self):
        self.assertFalse(is_dual_episode("Frasier.S07E01.BDRip.x265-ION265.mp4"))
        self.assertTrue(is_dual_episode("Frasier.S07E23E24.BDRip.x265-ION265.srt"))
        self.assertTrue(is_dual_episode("Frasier.S07E23.E24.BDRip.x265-ION265.srt"))
        self.assertTrue(is_dual_episode("Frasier.S07E23-E24.BDRip.x265-ION265.srt"))
        self.assertFalse(is_dual_episode("RARBG.txt"))

    def test_is_valid_file(self):
        self.assertTrue(is_valid_file("Frasier.S07E01.BDRip.x265-ION265.mp4"))
        self.assertTrue(is_valid_file("Frasier.S07E23E24.BDRip.x265-ION265.srt"))
        self.assertFalse(is_valid_file("RARBG.txt"))

    def test_parse_filename(self):
        self.assertEqual(
            parse_filename("Frasier.S08E01E02.BDRip.x265-ION265"), (8, 1, 2)
        )
        self.assertEqual(
            parse_filename("Frasier.S08E03.BDRip.x265-ION265"), (8, 3, None)
        )
        self.assertEqual(
            parse_filename("Frasier.S08E21E22.BDRip.x265-ION265"), (8, 21, 22)
        )
        self.assertEqual(parse_filename("RARBG.txt"), (None, None, None))

    def test_slugify(self):
        self.assertEqual(slugify("Episode 5: What's Up?"), "Episode 5 What's Up")


if __name__ == "__main__":
    unittest.main()
