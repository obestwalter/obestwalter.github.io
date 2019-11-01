from sys import *

# def stars_everywhere(starsky, *, hutch="cool"):

# **WARNING** in the interest of your mental health: try not to make sense of this!
def star_wrapper(function, *, param=None):
    def star_reporter(*args, **kwargs):
        print(*args, **kwargs)
        return function(*args, **kwargs)
    return star_reporter

    first, *rest = args
    more = [*path[:3], *rest]
    print(more)


stars_everywhere("hutch", kw=1)
