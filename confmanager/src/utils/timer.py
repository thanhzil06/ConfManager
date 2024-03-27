import functools
import time


def Timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"Elapsed time: " + "{:0>2}h:{:0>2}m:{:05.2f}s".format(int(hours), int(minutes), seconds))
        return value
    return wrapper_timer