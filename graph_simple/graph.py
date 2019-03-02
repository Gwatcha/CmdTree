# nlp
import spacy
import subprocess as sp
import json

from extract import extract_cmds
from extract import Cmd

from anytree import AnyNode, RenderTree, AsciiStyle, find

class CmdTree:
    def __init__(self, metadata=None):
        self.root = AnyNode(ntype='BASE', name='Unix Commands', metadata=metadata)

        # metadata {
        # obj: ''
        # spec_obj: ''
        # verb: '',
        # }

    def render(self):
        print(RenderTree(self.root, style=AsciiStyle()).by_attr('name'))

    def exportJSON_sigmajs(self, path):
        'serializes tree to JSON object that can be imported into sigmajs or visjs'
        ## TODO add id for each node and edge
        ## TODO add random x,y for each node


    def add(self, cmd):
        "adds the Cmd to tree, possibly building multiple nodes and edges in the process"

        ## Implementation with 3 layers using only parts of speech

        # TODO attach node it's action node if it exists
        action = find(self.root, lambda node: node.name == cmd.act and node.ntype == 'ACTION')
        if (action == None):
            action = AnyNode(ntype='ACTION', name=cmd.act, parent=self.root)

        obj = find(action, lambda node: node.name == cmd.obj)
        if (obj == None):
            obj = AnyNode(ntype='HYPERYNM-OBJECT', name=cmd.obj, parent=action)

        spec_obj = find(obj, lambda node: node.name == cmd.spec_obj and node.ntype == 'ATOMIC-OBJECT')
        if ( spec_obj == None ):
            if ( cmd.spec_obj != cmd.obj ):
                spec_obj = AnyNode(ntype='ATOMIC-OBJECT', name=cmd.spec_obj, parent=obj)
            else:
                spec_obj = obj

        command = find(spec_obj, lambda node: node.name == cmd.name and node.ntype == 'COMMAND')
        if (command == None):
            command = AnyNode(ntype='COMMAND', name=cmd.name, parent=spec_obj, metadata=cmd.metadata)

        # TODO flags and expanded versions for command eg. ip config -a
        # subcommand AnyNode(ntype='ATOMIC-OBJECT', name=cmd.spec_obj, parent=obj)

        # TODO 'specify node', meaning if a COMMAND or OBJECT node has >5 unix
        # nodes attached, look through their descriptions and try to infer
        # the hyponym that is shared the most among them - then create that node
        # and move its hypernym's unix commands underneath it.


def generate_tree():
    "returns a CmdTree for the current system"

    metadata = {
        'uname': sp.run([ 'uname', '-a' ], stdout=sp.PIPE).stdout.decode(),
    }

    tree = CmdTree(metadata=metadata)
    # extract commands and add them to tree
    for cmd in extract_cmds():
        tree.add(cmd)

    return tree

    # export to JSON for sigmajs
    # tree.exportJSON_sigmajs('tree.json')

tree = generate_tree()
tree.render()
