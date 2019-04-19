import unittest
import test_url
import test_api
import test_request
import test_input

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_url))
suite.addTests(loader.loadTestsFromModule(test_api))
suite.addTests(loader.loadTestsFromModule(test_input))
suite.addTests(loader.loadTestsFromModule(test_request))

runner = unittest.TextTestRunner()
result = runner.run(suite)