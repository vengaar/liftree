
# liftree import
import sys, os
LIFTREE_PATH_TEST = os.path.dirname(os.path.realpath(__file__))
LIFTREE_PATH_ROOT = os.path.dirname(LIFTREE_PATH_TEST)
LIFTREE_PATH_LIB = os.path.join(LIFTREE_PATH_ROOT, 'bin')

sys.path.append(LIFTREE_PATH_LIB)
