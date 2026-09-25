import os
import sys

try:
    import pageindex
    print("pageindex version:", getattr(pageindex, '__version__', 'unknown'))
    print("pageindex location:", pageindex.__file__)
    print(dir(pageindex))
    from pageindex import PageIndexClient
    print("PageIndexClient methods:")
    print([m for m in dir(PageIndexClient) if not m.startswith('_')])
except Exception as e:
    print("Error:", e)
