import os
import glob

def get_data(path, params):
    dir_loader = os.path.dirname(os.path.realpath(__file__))
    dir_example = os.path.dirname(dir_loader)
    dir_app = os.path.dirname(dir_example)
    dir_liftree = os.path.dirname(dir_app)
    dir_data = os.path.join(dir_liftree, 'tests', 'data')
    tests_files = glob.glob(os.path.join(dir_data, 'test*'))
    return tests_files

