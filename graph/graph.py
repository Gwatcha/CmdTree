# nlp
import spacy

from extract import extract_cmds_from_apropos
from extract import Cmd

# for hypernyms
import wordnet

import sp

import json

class Cmd:
    """
    'command' class. A command has a name, the action (act) it performs on
    an object (obj), and a dictionary type metadata.
    """
    def __init__(self, name, obj, act, metadata):
        "create command object"
        self.name = name
        self.obj = obj
        self.act = act
        self.metadata = metadata


## to json
# json.dumps(Graph().__dict__)
class CmdGraph:
    class Node:
        "ntype is either VERB, NOUN, UNIX, or BASE"
        def __init__(self, ntype, label, metadata):
            self.label = label
            self.ntype = ntype
            self.metadata = metadata


    def __init__(self, metadata=None):
        # adjacency list representation using Node class as keys and values
        base_node = Node('BASE', 'Unix Commands', None)
        self.graph = {
            base_node : []
        }

    def exportJSON_sigmajs(path):
        'serializes graph to JSON object that can be imported into sigmajs or visjs'

        ## TODO add id for each node and edge
        ## TODO add random x,y for each node

    # TODO remove cmd?
    def add(cmd):
        "adds the Cmd to graph, possibly building multiple nodes and edges in the process"

        # TODO attach node to base
        self.graph()

        # TODO move node down tree if its OBJECT is a hyponym of any of it's OBJECT
        # non-unix child nodes.

        # TODO move node down tree if its COMMAND is a hyponym of
        # any of it's non-unix child nodes

        # TODO 'specify node', meaning if a COMMAND or OBJECT node has >5 unix
        # nodes attached, look through their descriptions and try to infer
        # the hyponym that is shared the most among them - then create that node
        # and move its hypernym's unix commands underneath it.


def generate_graph():
    "returns a CmdGraph for the current system"

    metadata = {
        'uname': sp.run([ 'uname', '-a' ], stdout=sp.PIPE).stdout.decode(),
        'label': 'Unix Graph'
    }

    graph = CmdGraph( metadata = metadata )

    # extract commands and add them to graph
    for cmd in extract_cmds_from_apropos():
        graph.add(cmd)

    # export to JSON for sigmajs
    graph.exportJSON_sigmajs('graph.json')
