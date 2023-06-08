import unittest
from parameterized import parameterized
from o2a import replace_all, strings_to_replace

test_cases = [
    ("This is a test $x^2$", "This is a test \(x^2\)"),
    ("This is a $$multiline$$ test", "This is a \[multiline\] test"),
    ("this tests [[obsidian links]]", "this tests obsidian links"),
    ("this tests [[obsidian links|with alias]]", "this tests with alias"),
    ("> this is a blockquote", " this is a blockquote"),	
    ("this > isn't a block quote", "this > isn't a block quote"),
    ("equals in $< latex >$ should remain", "equals in \(< latex >\) should remain"),
    ("double {{ curlies }} should be separated by a space", "double { { curlies } } should be separated by a space"),
    ("Latex should be split at equal signs $x=2$", "Latex should be split at equal signs \(x\) \(=\) \(2\)"),
    ("$$a=b$$", "\n\(a\) \(=\) \(b\)\n"),
]
class TestReplaceAll(unittest.TestCase):
    @parameterized.expand(test_cases)
    def test_all(self, inp, out):
        self.assertEqual(replace_all(inp, strings_to_replace), out)


single_replacement_cases = [
    ("simple test", "(test)", "'.'", "simple 'test'"),
    ("this is a test with some testing", "(test)", "'.'", "this is a 'test' with some 'test'ing"),
    ("lets do something fancy, no really", "(do) (.+?) (fancy)", "'.'", "lets 'do', no really"),
    ("something with' a twist", "(with)", "'.", "something 'with' a twist"),
    ("something 'with a twist", "(with)", ".'", "something 'with' a twist"),
    ("lets test dot escape", "(dot)", "\.", "lets test . escape"),
    ("lets test dot escape dot multiple timesdot", "(dot)", "\.\...\.\..", "lets test ..dotdot..dot escape ..dotdot..dot multiple times..dotdot..dot")
]

from o2a import execute_single_group_replacement

class ExecuteSingleReplacementTests(unittest.TestCase):
    @parameterized.expand(single_replacement_cases)
    def test_all(self, inp, regex, replace, out):
        self.assertEqual(execute_single_group_replacement(inp, regex, replace), out)


from o2a import execute_multi_group_replacement
multi_replacement_cases = [
    ("simple test", "(test)", "'$1'", "simple 'test'"),
    ("this is a test with some testing", "(test)", "'$1'", "this is a 'test' with some 'test'ing"),
    ("some advanced testing", "(test) (.+?) (testing)", "'$1 $2 $3'", "some advanced testing"),
    ("test test test", "(test)", "\$$1\$", "$test$ $test$ $test$"),
]
class ExecuteMultiGroupReplacement(unittest.TestCase):
    @parameterized.expand(multi_replacement_cases)
    def test_all(self, inp, regex, replace, out):
        self.assertEqual(execute_multi_group_replacement(inp, regex, replace), out)

if __name__ == '__main__':
    unittest.main()