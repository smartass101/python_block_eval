import unittest
from textwrap import dedent

from block_eval import block_eval

class TestBlockEval(unittest.TestCase):

    def test_simple_expr(self):
        ret = block_eval("6 * 7")
        self.assertEqual(ret, 42)

    def test_simple_expr_with_var(self):
        a = 6
        ret = block_eval("a * 7")
        self.assertEqual(ret, 42)

    def test_complicated_expr(self):
        alpha = 1.0 / 137
        ret = block_eval("alpha.is_integer() is False")
        self.assertIs(ret, True)

    def test_non_returning_block(self):
        ret = block_eval(dedent("""
        for i in range(3):
            i * 3
        """))
        self.assertIs(ret, None)

    def test_returning_block(self):
        ret = block_eval(dedent("""
        f = 1
        for i in range(3):
            f *= i
        f
        """))
        self.assertEqual(f, 6)
        self.assertEqual(ret, f * 2)
