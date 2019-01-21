import traceback
from cgi import parse_qs
import json
from logging.config import fileConfig

import liftree
from liftree.utils import format_search_results_for_sui

def application(environ, start_response):

    try:
        fileConfig('/etc/liftree/logging.conf')
        all_values = [
            'Allemagne',
            'Albanie',
            'Andorre',
            'Arménie',
            'Autriche',
            'Azerbaïdjan',
            'Belgique',
            'Biélorussie',
            'Bosnie-Herzégovine',
            'Bulgarie',
            'Chypre',
            'Croatie',
            'Danemark',
            'Espagne',
            'Estonie',
            'Finlande',
            'France',
            'Géorgie',
            'Grèce',
            'Hongrie',
            'Irlande',
            'Islande',
            'Italie',
            'Lettonie',
            'Liechtenstein',
            'Lituanie',
            'Luxembourg',
            'République de Macédoine',
            'Malte',
            'Moldavie',
            'Monaco',
            'Monténégro',
            'Norvège',
            'Pays-Bas',
            'Pologne',
            'Portugal',
            'République tchèque',
            'Roumanie',
            'Royaume-Uni',
            'Russie',
            'Saint-Marin',
            'Serbie',
            'Slovaquie',
            'Slovénie',
            'Suède',
            'Suisse',
            'Ukraine',
            'Vatican',
        ]
        parameters = parse_qs(environ['QUERY_STRING'])
        query = parameters.get('query', [''])[0]
        results = [
            dict(name=value, value=value)
            for value in all_values
            if query in value
        ]
        output = dict(
            success=True,
            results=results
        )
        status = liftree.HTTP_200
        content_type = liftree.CONTENT_TYPE_JSON
        output = json.dumps(output)
        output = output.encode('utf-8')
    except:
        status = liftree.HTTP_500
        content_type = liftree.CONTENT_TYPE_TEXT
        trace = traceback.format_exc()
        output = trace.encode('utf-8')

    response_headers = [
        ('Content-type', content_type),
        ('Content-Length', str(len(output)))
    ]
    start_response(status, response_headers)
    return [output]
