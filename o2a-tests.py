import unittest
from o2a import replace_all, strings_to_replace

test_cases = [
    ("This is a test $x^2$", "This is a test \(x^2\)"),
    ("This is a $$multiline$$ test", "This is a \[multiline\] test"),
    ("this tests [[obsidian links]]", "this tests obsidian links"),
    ("this tests [[obsidian links|with alias]]", "this tests with alias"),
    ("> this is a blockquote", " this is a blockquote"),	
    ("equals in $< latex >$ should remain", "equals in \(< latex >\) should remain"),
    ("double {{ curlies }} should be separated by a space", "double { { curlies } } should be separated by a space"),
    ("Latex should be split at equal signs $$x = 2$$", "Latex should be split at equal signs \[x \]\[=\]\[ 2\]"),
]
class TestReplaceAll(unittest.TestCase):
    def test_latex_inline(self):
        for inp, out in test_cases:
            self.assertEqual(replace_all(inp, strings_to_replace), out)


if __name__ == '__main__':
    unittest.main()