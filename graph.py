# nlp
import json
import spacy

## to json
# json.dumps(Graph().__dict__)
class CmdGraph:
    class Node:
        "node" = {
            "id": 0,
            "type": "node type",
            "label": "node label(0)",
            "metadata": {}
        }

    def __init__(self, metadata, label):
        self.graph =  {
            "directed": True,
            "type": "Directed Tree",
            "label": label,
            "metadata": metadata,
            "nodes": [{
                "id": 0,
                "type": 'Base',
                "label": 'Unix',
                "metadata": {}
            }],
            "edges": []
        }

    def add_cmd(cmd):
        "add  entry to graph, building multiple nodes and edges in the process"

    unix_node = {
        "id": node_id,
        "type": "Object",
        "label": 'None',
        "metadata": {}
    }


    doc = nlp(entry.get('man_apropos'))

    # infer the object of this entry
    for token in doc:
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #     token.shape_, token.is_alpha, token.is_stop)

        # dobj is the object acted on by the verb, so it is our object
        if token.dep_ == 'dobj'

        # this is the action
        if token.tag_ == 'VERB' and token.dep_ == 'ROOT':
            print(token.text)

    for nc in doc.noun_chunks:
        nouns.append(nc)

        # TODO command + flag UNIX nodes obtained from parsing man page as well
        # as subcommands, such as for ip or for docker
        # if X is command:
        #     add_additional_nodes()

    # TODO attach node to base

    # TODO move node down tree if its OBJECT is a hyponym of any of it's OBJECT
    # non-unix child nodes.

    # TODO move node down tree if its COMMAND is a hyponym of
    # any of it's non-unix child nodes

    # TODO 'specify node', meaning if a COMMAND or OBJECT node has >5 unix
    # nodes attached, look through their descriptions and try to infer
    # the hyponym that is shared the most among them - then create that node
    # and move its hypernym's unix commands underneath it.

def create_graph():
    "returns a graph represented by a list of nodes and list of edges"



    apropos_list =  extract_raw_apropos()

    ### generate nodes and edges with POS-Tagger ###

    #TODO model better suited to man/apropos?
    #TODO custom tagger rules for the unix universe (eg. load always verb, return always verb)
    nlp = spacy.load('en_core_web_sm')
    # use spacy POS tagger on the words in each apropos description
    # the NOUN dobj is an Object, the VERB (commands) from entry.man_apropos
    for entry in apropos_list:


        add_node(graph, entry)



create_graph()
