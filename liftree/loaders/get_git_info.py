import os
import pprint
import difflib
import logging
try:
    import git
    MODULE_GIT_AVAILABLE = True
except ModuleNotFoundError:
    MODULE_GIT_AVAILABLE = False

def get_data(path, params):
    """
    """
    logger = logging.getLogger('LOADER_get_git_info')
    if MODULE_GIT_AVAILABLE:
        param_repo = params['repo']
        git_base = os.path.expanduser(param_repo)
        path_rel = os.path.relpath(path, start=git_base)
        repo = git.Repo(git_base)
        untracked = path_rel in repo.untracked_files
        status = "Unknown"
        diff = ''
        for item in repo.index.diff(None):
            file = os.path.abspath(item.a_path)
            if item.a_path == path_rel:
                filea = item.a_blob.data_stream.read().decode('utf-8').replace('\r\n', os.linesep)
                linesa = filea.split(os.linesep)
                # pprint.pprint(linesa)
                with open(path) as f:
                    fileb = f.read()
                linesb = fileb.split(os.linesep)
                # pprint.pprint(linesb)
                diff_lines = difflib.unified_diff(linesa, linesb, fromfile='filea', tofile='fileb', lineterm='')
                diff = os.linesep.join(diff_lines)
                status = item.change_type

        git_info = dict(
            untracked=untracked,
            status=status,
            diff=diff
        )
        return git_info
    else:
        return '''
Python git module missing
Try dnf install python3-GitPython
'''

