import markdown
import codecs

def get_data(path, params):
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.smarty'
    ]
    with codecs.open(path, mode="r", encoding="utf-8") as stream:
#     with open(path, 'r') as stream:
        md = stream.read()
    data = markdown.markdown(md, extensions=extensions, output_format='html5')
    return data
