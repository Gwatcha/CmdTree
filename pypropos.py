### Man page types.
# 0     Header files
# 0p    Header files (POSIX)
# 1     Executable programs or shell commands
# 1p    Executable programs or shell commands (POSIX)
# 2     System calls (functions provided by the kernel)
# 3     Library calls (functions within program libraries)
# 3n    Network Functions
# 3p    Perl Modules
# 4     Special files (usually found in /dev)
# 5     File formats and conventions eg /etc/passwd
# 6     Games
# 7     Miscellaneous  (including  macro  packages and conventions), e.g. man(7), groff(7)
# 8     System administration commands (usually only for root)
# 9     Kernel routines
# l     Local documentation
# n     New manpages


# regex
import re

# new python os libs
import subprocess as sp
from pathlib import Path

cache_dir = '/tmp/pypropros/'
cache_name = 'pypropros_cache'
cache_path = cache_dir + cache_name
# create cache for the command list & descriptions if it's the first time
# running this command in this boot
if not Path(cache_path).exists():
    if not Path(cache_dir).exists():
        sp.call(['mkdir', cache_dir])
    print("Creating cache...")
    # run apropos to get list of mans + short descriptions
    # populate cache - filtering out only shell commands and root commands
    apropos = sp.run(['apropos', '.'], stdout=sp.PIPE)
    all_mans = apropos.stdout.decode() #.splitlines()
    with open(cache_path, 'w') as out:
                            #a cmd name #match type (1) or (8)
        for m in re.finditer('^[\w\d\-\.]+ \([18]\).*$', all_mans, re.MULTILINE):
            # get rid of number tags and write to cache file
            out.write(m.group(0).replace("(8)", "#root").replace("(1)", "") + '\n')
    print("All done!")

with open(cache_path, 'r') as f:
    # as a start, just run the fzf utility
    sp.run(['fzf'], stdin=f.fileno())
