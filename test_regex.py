import unittest
import regex


class TestRegex(unittest.TestCase):

    def test_single_char(self):
        self.assertEqual(regex.my_regex("a", "a"), True)
        self.assertEqual(regex.my_regex(".", "a"), True)
        self.assertEqual(regex.my_regex("", "a"), True)
        self.assertEqual(regex.my_regex("", ""), True)
        self.assertEqual(regex.my_regex("a", ""), False)

    def test_word_and_regex_same_length(self):
        self.assertEqual(regex.my_regex("apple", "apple"), True)
        self.assertEqual(regex.my_regex(".pple", "apple"), True)
        self.assertEqual(regex.my_regex("appl.", "apple"), True)
        self.assertEqual(regex.my_regex(".....", "apple"), True)
        self.assertEqual(regex.my_regex("peach", "apple"), False)

    def test_word_and_regex_different_length(self):
        self.assertEqual(regex.my_regex("apple", "apple"), True)
        self.assertEqual(regex.my_regex("ap", "apple"), True)
        self.assertEqual(regex.my_regex("le", "apple"), True)
        self.assertEqual(regex.my_regex("a", "apple"), True)
        self.assertEqual(regex.my_regex(".", "apple"), True)
        self.assertEqual(regex.my_regex("apwle", "apple"), False)
        self.assertEqual(regex.my_regex("peach", "apple"), False)

    def test_starts_with(self):
        self.assertEqual(regex.my_regex("^app", "apple"), True)
        self.assertEqual(regex.my_regex("^a", "apple"), True)
        self.assertEqual(regex.my_regex("^apple", "apple pie"), True)
        self.assertEqual(regex.my_regex("^le", "apple"), False)

    def test_ends_with(self):
        self.assertEqual(regex.my_regex("le$", "apple"), True)
        self.assertEqual(regex.my_regex("apple$", "tasty apple"), True)
        self.assertEqual(regex.my_regex(".$", "apple"), True)
        self.assertEqual(regex.my_regex("app$", "apple"), False)

    def test_starts_and_ends_with(self):
        self.assertEqual(regex.my_regex("^apple$", "apple pie"), False)
        self.assertEqual(regex.my_regex("^apple$", "apple"), True)
        self.assertEqual(regex.my_regex("^apple$", "tasty apple"), False)
        self.assertEqual(regex.my_regex("^apple$", "apple pie"), False)

    def test_repetition_with_question_mark(self):
        self.assertEqual(regex.my_regex("colou?r", "color"), True)
        self.assertEqual(regex.my_regex("colou?r", "colour"), True)
        self.assertEqual(regex.my_regex("colou?r", "colouur"), False)

    def test_repetition_with_asterisk(self):
        self.assertEqual(regex.my_regex("colou*r", "color"), True)
        self.assertEqual(regex.my_regex("colou*r", "colour"), True)
        self.assertEqual(regex.my_regex("colou*r", "colouur"), True)
        self.assertEqual(regex.my_regex("a*b", "aaaaaaaaaab"), True)

    def test_repetition_with_plus_operator(self):
        self.assertEqual(regex.my_regex("colou+r", "colour"), True)
        self.assertEqual(regex.my_regex("colou+r", "color"), False)
        self.assertEqual(regex.my_regex("a+b", "aaaaaaaaaab"), True)

    def test_repetitions_and_dots(self):
        self.assertEqual(regex.my_regex("col.*p", "coloooooooooooooeeeruto"), False)
        self.assertEqual(regex.my_regex(".*", "aaa"), True)
        self.assertEqual(regex.my_regex(".*b", "aaaaaaaaaab"), True)
        self.assertEqual(regex.my_regex("col.*r", "coloooooooooooooeeer"), True)
        self.assertEqual(regex.my_regex("col.*r", "color"), True)
        self.assertEqual(regex.my_regex("col.*r", "colour"), True)
        self.assertEqual(regex.my_regex("col.*r", "colr"), True)
        self.assertEqual(regex.my_regex("col.*r", "collar"), True)
        self.assertEqual(regex.my_regex("col.*r", "coloooooooooooooeeeruto"), True)
        self.assertEqual(regex.my_regex("col.+r", "coloooooooooooooeeeruto"), True)
        self.assertEqual(regex.my_regex("col.+r", "colour"), True)
        self.assertEqual(regex.my_regex("col.+r", "colr"), False)
        self.assertEqual(regex.my_regex(".+", "aaa"), True)
        self.assertEqual(regex.my_regex(".+b", "aaaaaaaaaab"), True)

    def test_combination_of_different_rules(self):
        self.assertEqual(regex.my_regex("^no+pe", "noooooooope"), True)
        self.assertEqual(regex.my_regex("^no+pe$", "noooooooope"), True)
        self.assertEqual(regex.my_regex("no+$", "noooooooope"), False)
        self.assertEqual(regex.my_regex("^no+pe$", "noooooooope"), True)
        self.assertEqual(regex.my_regex("col.*r$", "colors"), False)
        self.assertEqual(regex.my_regex("e.d$", "end"), True)

    def test_escaping(self):
        self.assertEqual(regex.my_regex("3\+3", "3+3=6"), True)
        self.assertEqual(regex.my_regex("\?", "Is this working?"), True)
        self.assertEqual(regex.my_regex("\\", "\\"), True)
        self.assertEqual(regex.my_regex("colou\?r", "color"), False)
        self.assertEqual(regex.my_regex("colou\?r", "colour"), False)
        self.assertEqual(regex.my_regex("\.", "end."), True)
        self.assertEqual(regex.my_regex("^no+\+pe$", "noooooooo+pe"), True)
        self.assertEqual(regex.my_regex("^no+\+pe$", "noooooooope"), False)
        self.assertEqual(regex.my_regex("\.$", "end."), True)
        self.assertEqual(regex.my_regex("\.$", "end."), True)
        self.assertEqual(regex.my_regex("\^no+\+pe$", "^noooooooo+pe"), True)
        self.assertEqual(regex.my_regex("\^no+\+pe$", "noooooooo+pe"), False)
