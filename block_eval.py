import ast
import inspect

_NONE_EXPRESSION = ast.Expression(ast.parse('None').body[0].value)

def split_block(code_str, block_name='<string>'):
    """Split a code (block) string into an exec and eval mode code objects

    They are returned as a tuple (exec_part, eval_part). If the last statement
    in the block is an expression, it is compiled in eval mode into a code
    object eval_part. Remaining preceding statements are compiled in exec code
    into a code object, If none remain, exec_part will be a void code object
    (can be evaluated, but won't do anything). If the last statement is not an
    expression, eval_part will a code object represetning an expression which
    returns None (so effectively it is ignored as the exec_part would retunr
    None anyways) and exec_part will be compiled in exec mode.
    """
    code_ast = ast.parse(code_str)
    if len(code_ast.body) > 0 and isinstance(code_ast.body[-1], ast.Expr):
        expr = ast.Expression(code_ast.body[-1].value)
        del code_ast.body[-1]   # may become empty (void) code
    else:
        expr = _NONE_EXPRESSION # just evaluates to None
    eval_part = compile(expr, block_name, 'eval')
    exec_part = compile(code_ast, block_name, 'exec')
    return exec_part, eval_part



def block_eval(code_str, globals_=None, locals_=None, block_name='<string>'):
    """Evaluate a code (block) string and possibly return its result

    The result is the result of the last statement if it is an expression. This
    function is a compromise between exec and eval: It evaluates all the
    statements like exec, but uses eval for the last statement if it is an
    expression and returns its value. If it is not, None is returned (exec mode)

    To emaulate eval behavior, the variable scope of the parent frame is
    captured and modified, which is know to work reliably only in top-level
    scope (e.g. interactive intepreter mode). It may not update local variable
    scope when used in a lower level scope (functions calling other functions).
    """

    # get scope in calling frame to truly emulate eval
    current_frame = inspect.currentframe()
    try:
        parent_frame = current_frame.f_back
        p_globals, p_locals = parent_frame.f_globals, parent_frame.f_locals
    except AttributeError:      # cannot get that frame or its vars
        p_globals, p_locals = locals(), globals() # these should always work
    finally:
        del current_frame       # otherwise might create reference cycle
    if globals_ is not None:
        p_globals = globals_
        # this is documented eval behavior
        p_locals = p_globals if locals_ is None else locals_

    exec_part, eval_part = split_block(code_str, block_name)
    exec(exec_part, p_globals, p_locals)
    return eval(eval_part, p_globals, p_locals)
