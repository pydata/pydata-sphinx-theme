import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

STRUCTURE = {
    'getting_started': ['overview',
                        '10min',
                        'tutorials',
                        'cookbook',
                        'dsintro',
                        'basics'],
    'user_guide': ['text',
                   'options',
                   'indexing',
                   'advanced',
                   'computation',
                   'missing_data',
                   'groupby',
                   'merging',
                   'reshaping',
                   'timeseries',
                   'timedeltas',
                   'categorical',
                   'visualization',
                   'style',
                   'io',
                   'enhancingperf',
                   'sparse',
                   'gotchas'],
    'ecosystem': ['comparison_with_r',
                  'comparison_with_sas',
                  'comparison_with_sql',
                  'comparison_with_stata',
                  'r_interface',
                  'ecosystem'],
    'developers': ['contributing',
                   'contributing_docstring',
                   'developer',
                   'internals',
                   'extending'],
}


def change_rst_structure(pandas_path, structure):
    """
    Move rst files into subdirectories of the source directory.
    """
    source_path = os.path.join(pandas_path, 'doc', 'source')

    for dirname, fnames in structure.items():
        dirname = os.path.join(source_path, dirname)
        os.makedirs(dirname, exist_ok=True)

        for fname in fnames:
            source = os.path.join(source_path, fname + '.rst')
            target = os.path.join(dirname, fname + '.rst')
            try:
                os.rename(source, target)
            except FileNotFoundError:
                pass


def add_dependencies(pandas_path):
    requirements = os.path.join(pandas_path, 'ci', 'environment-dev.yaml')
    with open(requirements, 'a') as f:
        f.write('  - sphinx_bootstrap_theme\n')


def main(pandas_path):
    change_rst_structure(pandas_path, STRUCTURE)
    add_dependencies(pandas_path)


if __name__ == '__main__':
    # TODO replace by path to pandas, not this repo, when ready to refactor it
    pandas_path = BASE_PATH
    main(pandas_path)
