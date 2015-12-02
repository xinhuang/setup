import unittest
from setup import *



class TestSetup(unittest.TestCase):

    def test_sort_package_dependency(self):
        packages = [{'name': 'ipython', 'dependencies': ['pip'], }, {'name': 'pip', }, ]
        packages = sort_packages(packages)

        self.assertEqual('pip', packages[0]['name'])
        self.assertEqual('ipython', packages[1]['name'])

if __name__ == '__main__':
    unittest.main()
