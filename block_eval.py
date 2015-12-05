import ast
import inspect


def block_eval(code_str, globals_=None, locals_=None, block_name='<string>'):
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
    # AST manipulation and evaluation
    code_ast = ast.parse(code_str)
    assert isinstance(code_ast, ast.Module)
    last_stmt = code_ast.body[-1]
    if isinstance(last_stmt, ast.Expr):
        del code_ast.body[-1]
        if len(code_ast.body) > 0:
            eval(compile(code_ast, block_name, 'exec'), p_globals, p_locals)
        expr = ast.Expression(last_stmt.value)
        final_code = compile(expr, block_name, 'eval')
    else:
        final_code = compile(code_ast, block_name, 'exec')
    return eval(final_code, p_globals, p_locals)