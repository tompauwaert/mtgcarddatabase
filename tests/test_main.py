import unittest

# Test files
test_modules = [
    'tests.test_content',
    'tests.test_cli',
]
suite = unittest.TestSuite()
for module in test_modules:
    try:
        mod = __import__(module, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())

    except (ImportError, AttributeError):
        # else just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))

unittest.TextTestRunner(verbosity=2).run(suite)
