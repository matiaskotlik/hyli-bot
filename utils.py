import functools
import asyncio


def run_in_executor(_func):  # https://stackoverflow.com/a/64506715
    @functools.wraps(_func)
    def _run_in_executor(*args, **kwargs):
        loop = asyncio.get_event_loop()
        func = functools.partial(_func, *args, **kwargs)
        return loop.run_in_executor(executor=None, func=func)
    return _run_in_executor
