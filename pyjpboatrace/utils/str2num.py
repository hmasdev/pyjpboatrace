
def str2num(s: str, typ: type, default_val=None):
    ''' string to number whose type is the type given as typ.

    typ must be int, float or complex

    Note: Failure of casting returns default_val
    '''
    if typ not in [int, float, complex]:
        raise NotImplementedError(
            f'typ must be int, float or complex, but {typ.__name__} given.'
        )

    try:
        return typ(s)
    except ValueError:
        return default_val
