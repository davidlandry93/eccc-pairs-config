import argparse
import datetime
import json

from ibmpairs import paw

CONFIG_DEFAULTS = {
    'download_dir': '.',
    'server': 'https://pairs.res.ibm.com'
}

ID_OF_FIELD = {
    'TT': '49717'
}


def cli():
    args = parse_args()

    with open(args.query_file) as f:
        query_and_config = json.load(f)

    query = query_and_config['query']

    if 'config' in query_and_config:
        config_from_file = query_and_config['config']
    else:
        config_from_file = {}

    config = generate_config(vars(args), config_from_file)

    process_query(query, config)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Query the PAIRS platform for ECCC data.',
        fromfile_prefix_chars='+'
    )
    parser.add_argument(
        'query_file',
        type=str,
        help='A JSON file that describes the query to be run.'
    )
    parser.add_argument(
        '-download_dir',
        type=str,
        help='Where to download the data.'
    )
    parser.add_argument(
        '-server',
        type=str,
        default='https://pairs.res.ibm.com/v2/',
        help='The PAIRS server to query.'
    )
    return parser.parse_args()


def generate_config(config_from_args, config_from_file):
    config = CONFIG_DEFAULTS.copy()
    config.update(config_from_file)
    config.update({
        k: config_from_args[k]
        for k in config_from_args
        if config_from_args[k] is not None
    })

    return config


def process_query(query, config):
    pairs_query = create_pairs_query(query, config)
    process_pairs_query(pairs_query)


def create_pairs_query(query, config):
    query_dict = create_pairs_query_dict(query)

    print(query_dict)

    pairs_query = paw.PAIRSQuery(
        query_dict,
        config['server'],
        (config['username'], config['password']),
        downloadDir=config['download_dir']
    )

    return pairs_query


def create_pairs_query_dict(query):
    pairs_query_dict = {
        "layers": generate_layers(query),
        "spatial": generate_spatial(query),
        "temporal": generate_temporal(query),
    }

    return pairs_query_dict


def generate_layers(query):
    layers = []
    dimensions_of_query = generate_dimensions(query)

    for field in query['fields']:
        for dimension in dimensions_of_query:
            layers.append({
                'type': 'raster',
                'id': ID_OF_FIELD[field],
                'dimensions': [dimension]
            })
    return layers


def generate_dimensions(query):
    return [{'name': 'horizon', 'value': str(x)} for x in query['lead_time']]


def generate_spatial(query):
    return {
        'type': 'square',
        'coordinates': query['coordinates']
    }


def generate_temporal(query):
    begin_reference_time = parse_input_date(query['begin'])
    end_reference_time = parse_input_date(query['end'])

    begin = reference_time_to_valid_time(begin_reference_time, query['lead_time'])
    end =  reference_time_to_valid_time(end_reference_time, query['lead_time'])

    return {
        'intervals': [
            {
                'start': datetime_to_pairs(begin),
                'end': datetime_to_pairs(end)
            }
        ]
    }


def parse_input_date(date_string):
    INPUT_FORMAT = '%Y-%m-%d'
    return datetime.datetime.strptime(date_string, INPUT_FORMAT)


def reference_time_to_valid_time(reference_time, lead_time):
    return reference_time + datetime.timedelta(hours=lead_time)


def datetime_to_pairs(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def process_pairs_query(pairs_query):
    try:
        pairs_query.submit()
    except KeyError:
        # The Api returns a KeyError when the query failed.
        # Sometimes we have debugging information available.
        raise RuntimeError('Problem when submitting the generated query to PAIRS. Message from the platform: {}'.format(pairs_query.querySubmit.content.decode()))

    pairs_query.poll_till_finished()
    pairs_query.download()


