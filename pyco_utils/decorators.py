
def retry(func, count=3):
    def decorator(*args, **kwargs):
        for i in range(count - 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log(e.args, e.message, func, *args, level='error', **kwargs)
        return func(*args, **kwargs)

    return decorator