from setuptools import setup

setup(
    name='eccc-pairs-query',
    description='An interface to make simple query towards an IBM PAIRS instance.',
    author='David Landry',
    author_email='david.landry@canada.ca',
    url='https://gitlab.science.gc.ca/dav000/eccc-pairs-query',
    py_modules=['pairs_query'],
    install_requires=['numpy', 'ibmpairs', 'pathlib'],
    entry_points={
        'console_scripts': [
            'eccc_pairs_query=pairs_query:cli',
        ]
    },
)
