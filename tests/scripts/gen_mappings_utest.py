import unittest
from scripts import gen_mappings as gm


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestProduceEcommerceMappings(unittest.TestCase):

    def test_can_add_one_standard(self):
        input = {'suits': [{'cards': [{'cre': ['308-515'], 'value': '2'}], 'name': 'Data validation & encoding'}, {'cards': [{'cre': ['138-448'], 'value': '2'}], 'name': 'Session management'}]}
        standards = ['ASVS']
        expected = {'meta': {'component': 'mappings','edition': 'ecommerce','language': 'ALL','version': '1.20'},'suits': [{'cards': [{'cre': ['308-515'], 'value': '2'}],'name': 'Data validation & encoding'},{'cards': [{'ASVS': 'V2.3.3', 'cre': ['138-448'], 'value': '2'}],            'name': 'Session management'}]}

        self.assertEqual(gm.produce_ecommerce_mappings(input,standards),expected)

if __name__ == "__main__":
    unittest.main()
