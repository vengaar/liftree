def get_data(path):
    git = "Ha que coucou"
    with open(path) as f:
        playbook = f.read
    return dict(git=git, playbook=playbook)
