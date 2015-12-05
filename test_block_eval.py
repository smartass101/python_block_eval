import unittest
from textwrap import dedent

from block_eval import split_block, block_eval

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
        for i in range(1, 3+1):
            f *= i
        f
        """))
        self.assertEqual(ret, 6)

    def test_locals_update_fails(self):
        block_eval('b = 42')
        with self.assertRaises(NameError):
            self.assertEqual(b, 42)

    def test_eval_in_current_scope_workaround(self):
        a = 1
        exec_part, eval_part = split_block(dedent("""
        f = a
        for i in range(1, 3+1):
            f *= i
        f / a
        """))
        exec(exec_part)
        ret = eval(eval_part)

        self.assertEqual(ret, 6)
        self.assertEqual(f, ret)
