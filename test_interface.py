import unittest
from clientTranslation import geez_to_latin_syllable
from interface import vocab_dict

class TestInterface(unittest.TestCase):

    def test_geez_to_latin_syllable(self):
        self.assertEqual(geez_to_latin_syllable("ሰላም"), "selam")
        self.assertEqual(geez_to_latin_syllable("ኣንበሳ"), "anbesa")

    def test_vocab_translation(self):
        for word, translation in vocab_dict.items():
            phonetic = geez_to_latin_syllable(translation)
            self.assertIsNotNone(phonetic)
            self.assertIsInstance(phonetic, str)

if __name__ == '__main__':
    unittest.main()