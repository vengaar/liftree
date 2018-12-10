import markdown

def load(path):
    extensions = ['extra', 'smarty']
    with open(path, 'r') as stream:
        md = stream.read()
    data = markdown.markdown(md, extensions=extensions, output_format='html5')
    return data
