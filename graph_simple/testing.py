import spacy
from spacy import displacy

test = ['zsh built-in commands',
        'send and receive internet mail'
        'BPF programmable classifier and actions for ingress/egress queueing disciplines'
        'XKB extension user utility',
        'edit the sudoers file',
        'view zstandard-compressed files',
        'GNU project Emacs editor',
        'michael eats food',
        'michael eats or makes food',
        'michael eats and makes delicious food',
        'michael eats and makes delicious food that grows in australia',
        'eat food',
        'eat or make food',
        'eat and make delicious food',
        'convert Adobe font metrics to TeX font metrics',
        'eat and make delicious food that grows in australia',
        'command-line utility to gather old information about the ALSA subsystem',

        # TODO think about how to connect prep as to create more specific hyponym
        'print the file name of the terminal connected to standard input']

nlp = spacy.load('en_core_web_sm')
# generate best guess nouns (objects) and verbs (commands) from entry.man_apropos
span = nlp(test[1])[0:]
for token in span:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

displacy.serve(span, style='dep')

    # # extract spacy's tagged NOUN chunks and VERBS
    # verbs = []
    # nouns = []
    # for token in doc:
    #     # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #     #         token.shape_, token.is_alpha, token.is_stop)
    #     if token.pos_ == 'VERB':
    #         verbs.append(token.text)


    # print(verbs)
    # print(nouns)
