


def which_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    # from whichcraft import which

import re
import subprocess as sp
from pathlib import Path
from shutil import which

print("Creating db...")

tldr_exists = 0
if which('tldr'):
    tldr_exists = 1

db_dir = '/tmp/pypropros/'
db_name = 'pypropros_db'
db_path = db_dir + db_name

if not Path(db_dir).exists():
    sp.call(['mkdir', db_dir])

### Data structure for storing commands + details + nlp data + anything else
# pypp = pypropros
pypp_table = []

# pypp_row  = (string) [ apropos_entry, type, apropos_desc, path, --help, tldr]
# regex objects for components in apropos output
# eg output: 'zmq_z85_decode (3)   - decode a binary key from Z85 printable text'
name_re = re.compile('^[\w\d\-\.\:]+')
man_type_re = re.compile('(\([^\)]+\))')
desc_re = re.compile('(?=- ).+')

# extract information from 'apropos .' to pypp_table
apropos = sp.run(['apropos', '.'], stdout=sp.PIPE)
for line in apropos.stdout.decode().splitlines():
    # create a new row for the ppy_table
    pypp_row = []

    # pick apart apropos line
    name  = name_re.search(line).group(0)
    man_type = man_type_re.search(line).group(0)
    desc  = desc_re.search(line).group(0)[2:] #trim '- ' too

    # append apropos information
    pypp_row.append(name)
    pypp_row.append(man_type)
    pypp_row.append(desc)

    # append path of executable
    path = which(name)
    pypp_row.append(path)

    # if runnable, append --help, and tldr
    if path:
        # pypp_row.append(sp.run([name, '--help'], stdout=sp.PIPE).stdout.decode())

        # FIXME This takes SO long to run, and all the information is in man already.
        if tldr_exists == 1:
            tldr = sp.run(['tldr', '-s', name], stdout=sp.PIPE).stdout.decode()
            pypp_row.append(sp.run(['tldr', '-s', name], stdout=sp.PIPE).stdout.decode())
        else:
            pypp_row.append('tldr not installed')
    else:
        pypp_row.append('None')
        pypp_row.append('None')

    # finish information extract for this apropos entry
    # TODO NLP Additional information - Noun & Verb
    # nlp_append(pypp_row)
    pypp_table.append(pypp_row)

# write our db to the /tmp file
with open(db_path, 'w') as out:
    out.write(pypp_table)

print("All done!")
