import subprocess as sp
from shutil import which
import json
#regex
import re
# nlp
import spacy

use_subset = 1
limit_to_commands = True

def extract_raw_apropos():
    """
    "extracts the output of command:'apropos .' into a list of dictionaries objects  and returns it.
    each dictionary object has form as this example:
    {
        name: "cd",
        man_label: "1",
        man_type: "Executable programs or shell commands",
        man_apropos: "change the working directory"
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
    man_apropos_re = re.compile('(?=- ).+')
    man_re = re.compile('(?=- ).+')

    whereis_re = re.compile('(\/[^ \n]+)')

    apropos_list = []

    # extract information from 'apropos .' to apropos_list
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
        man_type = man_type_dict.get(man_label)
        man_apropos = man_apropos_re.search(line).group(0)[2:] #trim '- '

        whereis_out = []
        if man_label != '(3)':
            whereis_raw_out = sp.run(['whereis', name], stdout=sp.PIPE).stdout.decode()
            whereis_out = whereis_re.findall(whereis_raw_out)

        which_out = which(name)

        entry = {
            'name': name,
            'man_label': man_label,
            'man_type': man_type,
            'man_apropos': man_apropos,
            'whereis': whereis_out,
            'which': which_out
        }

        # finish information extract for this entry
        apropos_list.append(entry)

        if use_subset > 0:
            count = count + 1
            if count >= use_subset:
                break

    return apropos_list

def pypp_graph_infer_hypernyms():
    "given a pypp_graph, iterates over all NOUN and VERB nodes and infers hypernymy's, the node is created and it's hyponyms become its children"

def generate_graph(graph):
    # get a nicely packaged 'apropos .' output from the system
    apropos_list =  extract_raw_apropos()

    #TODO model better suited to man/apropos?
    nlp = spacy.load('en_core_web_sm')

    # generate best guess nouns (objects) and verbs (commands) from entry.man_apropos
    for entry in apropos_list:
        doc = nlp(entry.get('man_apropos'))

        # extract spacy's tagged NOUN chunks and VERBS
        for token in doc:
            # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                # token.shape_, token.is_alpha, token.is_stop)
            if token.pos_ == 'VERB':
                verbs.append(token.text)

        for nc in doc.noun_chunks:
            nouns.append(nc)

        # TODO command + flag UNIX nodes obtained from parsing man page as well
        # as subcommands, such as for ip or for docker
        # if X is command:
        #     add_additional_nodes()



def create_graph():
    "creates the graph. \
 returns a graph represented by an adjacency list with entries: [ apropos_entry, type, apropos_desc, path, NOUN, VERB ] \
    where NOUN is the subject of the command and VERB is the action on that subject"

    # see README.org for further specification
    nodes = []
    edges = []
    graph =  {
         "directed": True,
         "type": "Directed Tree",
         "label": "Unix manual visualization",
         "metadata": None,
         "nodes": nodes,
         "edges": edges
     }

    generate_graph(graph)





create_graph()
