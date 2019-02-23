
#regex
import re
import subprocess as sp
from shutil import which
# for pos tagging
import spacy

use_subset = 1
limit_to_commands = True

class Cmd:
    """
    'command' class. A command has a name, the action (act) it performs on
    an object (obj), and any caller defined metadata.
    """

    def __init__(self, name, obj, act, metadata):
        "create command object"
        self.name = name
        self.obj = obj
        self.act = act
        self.metadata = metadata



def extract_obj_act_from_desc(cmd, desc):
    "given the apropos description (desc) of a command (cmd), returns a tuple (object, action) which is the best guess of the object acted on by the action of cmd."


    '''
    dobj: direct object from (x to y)
    The direct object of a VP is the noun phrase which is the (accusative) object of the verb; the
    direct object of a clause is the direct object of the VP which is the predicate of that clause.

    “She gave me a raise” dobj(gave, raise)
    “They win the lottery” dobj(win, lottery)
    '''


def extract_cmd_from_apropos():
    """
    "extracts the output of command:'apropos .' into a list of Cmd objects and returns it.
    each Cmd object's metadata has form as this example:
    {
        man_label: "1",
        man_type: "Executable programs or shell commands",
        man_desc: "change the working directory"
        whereis: ['/usrshare/man/mann/cd.n.gz', '/usr/share/man/man1/cd.1p.gz']
        which: "cd: shell built-in command"
    }

    """
    man_type_dict = {
        '0' : 'Header files',
        '1' : 'Executable programs or shell commands',
        '0p' : 'Header files (POSIX)',
        '1p' : 'Executable programs or shell commands (POSIX)',
        '2' : 'System calls (functions provided by the kernel)',
        '3' : 'Library calls (functions within program libraries)',
        '3n' : 'Network Functions',
        '3p' : 'Perl Modules (3p)',
        '3perl' : 'Perl Modules (3perl)',
        '4' : 'Special files (usually found in /dev)',
        '5' : 'File formats and conventions eg /etc/passwd',
        '6' : 'Games',
        '7' : 'Miscellaneous  (including  macro  packages and conventions)',
        '8' : 'System administration commands (usually only for root)',
        '9' : 'Kernel routines',
        'l' : 'Local documentation',
        'n' : 'New manpages',
    }

    # regex objects for capturing components in apropos output
    # eg output: 'zmq_z85_decode (3)   - decode a binary key from Z85 printable text'
    name_re = re.compile('^[\w\d\-\.\:]+')
    man_label_re = re.compile('(\(\d\))')
    man_type_re = re.compile('(\([^\)]+\))')
    man_desc_re = re.compile('(?=- ).+')
    man_re = re.compile('(?=- ).+')

    whereis_re = re.compile('(\/[^ \n]+)')

    cmd_list = []

    # extract information from 'apropos .' to cmd_list
    apropos_raw = None
    if limit_to_commands:
        apropos_raw = sp.run(['apropos', '-s', '1,8', '.'], stdout=sp.PIPE)
    else:
        apropos_raw = sp.run(['apropos', '.'], stdout=sp.PIPE)

    # used to limit number of entries read in the case of use_subset = True
    count = 0

    for line in apropos_raw.stdout.decode().splitlines():
        # pick apart apropos line
        name  = name_re.search(line).group(0)
        man_label = man_type_re.search(line).group(0).strip('()')
        man_desc = man_desc_re.search(line).group(0)[2:] #trim '- '

        # consult dictionary for readable man type for label
        man_type = man_type_dict.get(man_label)

        whereis_out = []
        if man_label != '(3)':
            whereis_raw_out = sp.run(['whereis', name], stdout=sp.PIPE).stdout.decode()
            whereis_out = whereis_re.findall(whereis_raw_out)

        which_out = which(name)

        metadata = {
            'man_label': man_label,
            'man_type': man_type,
            'man_desc': man_desc,
            'whereis': whereis_out,
            'which': which_out
        }


        ## extract object and action from apropos description
        (obj, act) = extract_obj_act_from_desc()

        # create and append new command
        cmd = Cmd(name, obj, act, metadata)
        cmd_list.append(cmd)

        if use_subset > 0:
            count = count + 1
            if count >= use_subset:
                break

    return cmd_list


# TODO: Extract commands such as ip config, or ls -a, as well
