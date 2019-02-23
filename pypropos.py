## tui
# from blessings import Terminal
# t = Terminal()
# print ( t.bold('Hi there!') )
# print ( t.bold_red_on_bright_green('It hurts my eyes!'))
# with t.location(0, t.height - 1):
#     print ( 'This is at the bottom.' )

# regex
import re

import subprocess as sp
from pathlib import Path

from fetch_data import fetch_data

# store pypp_table as file for quick re-runs
import pickle
re_fetch = 0

cache_dir = '/tmp/pypropros/'
cache_name = 'pypropros_cache'
cache_path = cache_dir + cache_name

# fetch and cache pypp_table if it dosen't exist
if not Path(cache_path).exists():
    print("caching pypp_table...")
    if not Path(cache_dir).exists():
        sp.call(['mkdir', cache_dir])
    with open(cache_path, 'wb') as f:
        pickle.dump(fetch_data(), f)
    print("finished caching pypp_table!")

# load pypp_table
pypp_table = None
with open(cache_path, 'r') as f:
    pypp_table = pickle.load(f)
assert(pypp_table != None)
