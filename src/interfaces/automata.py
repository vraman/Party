from itertools import chain
from helpers.hashable import HashableDict


class Automaton:
    def __init__(self, init_sets_list, rejecting_nodes, nodes):
        self._init_sets_list = list(init_sets_list)
        self._rejecting_nodes = set(rejecting_nodes)
        self._nodes = set(nodes)

    @property
    def nodes(self):
        return self._nodes

    @property
    def initial_sets_list(self):
        """ Return list of sets of initial nodes (non-deterministic) """
        return self._init_sets_list

    @property
    def rejecting_nodes(self):
        return self._rejecting_nodes


    def __str__(self):
        return "nodes:\n" + \
               "\n".join([str(x) for x in self._nodes]) +\
               "\n initial nodes:\n" +\
               "\n".join([str(x) for x in self._init_sets_list]) +\
               "\n rejecting nodes:\n" + \
               "\n".join([str(x) for x in self._rejecting_nodes])


class Label(HashableDict):
    """
    hashable dict: variable_name -> True/False
    """
    pass


class Node:
    def __init__(self, name):
        self._transitions = {} # label->[nodes, nodes, nodes]
        self._name = name
        assert name != "0"
        assert ',' not in name, name

    @property
    def name(self):
        return self._name

    @property
    def transitions(self):
        """ Return map { label->[nodes_set, .., nodes_set] ... label->[nodes_set, .., nodes_set] } """
        return self._transitions

    def add_transition(self, label, dst_set):
        """ Add transition:
            dst_set - set of destination nodes, singleton set if non-universal transition.
            Several calls with the same label are allowed - this means that transition is non-deterministic.
        """
        label = Label(label)
        label_transitions = self._transitions[label] = self._transitions.get(label, [])
        if dst_set not in label_transitions:
            label_transitions.append(dst_set)


    def __str__(self):
        labels_strings = []
        for l, dst_list in self.transitions.items():
            dst_strings = []
            for dst_set in dst_list:
                dst_strings.append('({0})'.format(str(', '.join([d.name for d in dst_set]))))

            labels_strings.append('[{0}: {1}]'.format(str(l), ', '.join(dst_strings)))

        return "'{0}', transitions: {1}".format(self.name, ' '.join(labels_strings))


    def __repr__(self):
        return "'{0}'".format(self.name)


#------------------------------helper functions--------------------------
def satisfied(label, signal_values):
    """ Do signal values satisfy the label? """

    for var, val in signal_values.items():
        if var not in label:
            continue
        if label[var] != val:
            return False
    return True


def get_next_states(state, signal_values):
    """ Return list of state_sets """

    total_list_of_state_sets = []
    for label, list_of_state_sets in state.transitions.items():
        if satisfied(label, signal_values):
            total_list_of_state_sets.extend(list_of_state_sets)

    return total_list_of_state_sets


def label_to_short_string(label):
    if len(label) == 0:
        return '1'

    short_string = ''
    for var, val in label.items():
        if val is False:
            short_string += '!'
        short_string += var

    return short_string


def to_dot(automaton):
    rej_header = []
    for rej in automaton.rejecting_nodes:
        rej_header.append('"{0}" [shape=doublecircle]'.format(rej.name))

    assert len(list(filter(lambda states: len(states) > 1, automaton.initial_sets_list))) == 0,\
    'no support of universal init states!'

    init_header = []
    init_nodes = chain(*automaton.initial_sets_list)
    for init in init_nodes:
        init_header.append('"{0}" [shape=box]'.format(init.name))

    trans_dot = []
    for n in automaton.nodes:
        colors = 'black purple green yellow blue orange red brown pink'.split() + ['gray']*10

        for label, list_of_sets in n.transitions.items():
            for states in list_of_sets:
                color = colors.pop(0)

                edge_is_labelled = False

                for dst in states:
                    edge_label_add = ''
                    if not edge_is_labelled:
                        edge_label_add = ', label="{0}"'.format(label_to_short_string(label))
                        edge_is_labelled = True

                    trans_dot.append('"{0}" -> "{1}" [color={2} {3}];'.format(
                        n.name, dst.name, color, edge_label_add))

                trans_dot.append('\n')

    dot_lines = ['digraph "automaton" {'] + \
                init_header + ['\n'] + \
                rej_header + ['\n'] + \
                trans_dot + ['}']

    return '\n'.join(dot_lines)