import logging
import unittest
from interfaces.automata import Label
from translation2uct.ltl2acw import parse_ltl3ba_aa


class Test(unittest.TestCase):
    def setUp(self):
        self._logger = logging.getLogger(__name__)

    def test__two_init(self):
        text = """Alternating automaton after simplification
            init :
            {1}
            {2}
            rejecting:
            {}
            state 2 : (b)
            (b) -> {}               {}
            state 1 : (a)
            (a) -> {}               {}\n\n"""
        init_nodes, rejecting_nodes, nodes = parse_ltl3ba_aa(text, self._logger)
        assert len(init_nodes) == 2, [str(n) for n in init_nodes]
        assert len(rejecting_nodes) == 0
        assert len(nodes) == 3, str(nodes) #+1 fot safe end


    def test__universal_and_non_deterministic_transitions(self):
        text = """Alternating automaton after simplification
                init :
                {7}
                rejecting:
                {4}
                state 7 : (false V (! ((r)) || (true U (g))))
                (!r) || (r && g) -> {7}         {}
                (1) -> {4,7}            {}
                (1) -> {7}
                state 4 : (true U (g))
                (g) -> {}               {}
                (1) -> {4}              {4}
                \n\n"""

        init_nodes_list, rejecting_nodes, nodes = parse_ltl3ba_aa(text, self._logger)
        assert len(init_nodes_list) == 1
        assert init_nodes_list[0].pop().name == '7'
        assert [n.name for n in rejecting_nodes] == ['4']
        assert set([n.name for n in nodes]) == {'4', '7',''}, str(nodes) #+safe end

        n7 = [n for n in nodes if n.name == '7'][0]
        n4 = [n for n in nodes if n.name == '4'][0]
        trans7 = n7.transitions

        empty_label = Label({})
        assert set(trans7.keys()) == {empty_label, Label({'r':False}), Label({'r':True, 'g':True})}, str(trans7.keys())
        assert {n4, n7} in trans7[empty_label], str(trans7[empty_label])
        assert {n7} in trans7[empty_label], str(trans7[empty_label])





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()