#!/usr/bin/env python
import os
import sys
import glob
import shutil


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

STRUCTURE = {
    'tutorial': ['overview.rst',
                 '10min.rst',
                 'tutorials.rst',
                 'cookbook.rst',
                 'dsintro.rst',
                 'basics.rst'],
    'user_guide': ['text.rst',
                   'options.rst',
                   'indexing.rst',
                   'advanced.rst',
                   'computation.rst',
                   'missing_data.rst',
                   'groupby.rst',
                   'merging.rst',
                   'reshaping.rst',
                   'timeseries.rst',
                   'timedeltas.rst',
                   'categorical.rst',
                   'visualization.rst',
                   'style.rst',
                   'io.rst',
                   'enhancingperf.rst',
                   'sparse.rst',
                   'gotchas.rst',
                   'style.ipynb'],
    'ecosystem': ['comparison_with_r.rst',
                  'comparison_with_sas.rst',
                  'comparison_with_sql.rst',
                  'comparison_with_stata.rst',
                  'r_interface.rst',
                  'ecosystem.rst'],
    'developers': ['contributing.rst',
                   'contributing_docstring.rst',
                   'developer.rst',
                   'internals.rst',
                   'extending.rst'],
    'release': ['release.rst',
                'whatsnew.rst',
                'whatsnew'],
}


def change_rst_structure(pandas_path, structure):
    """
    Move rst files into subdirectories of the source directory.
    """
    source_path = os.path.join('doc', 'source')

    for dirname, fnames in structure.items():
        dirname = os.path.join(source_path, dirname)
        os.makedirs(os.path.join(pandas_path, dirname), exist_ok=True)

        sources = []
        for fname in fnames:
            source = os.path.join(source_path, fname)
            target = os.path.join(dirname, fname)
            try:
                os.rename(os.path.join(pandas_path, source),
                          os.path.join(pandas_path, target))
            except FileNotFoundError:
                pass
            sources.append(source)

        print('git add {}'.format(dirname))
        print('git rm {}'.format(' '.join(sources)))


def add_dependencies(pandas_path):
    """
    Adding the new theme to the dependencies.
    """
    fname = os.path.join('ci', 'environment-dev.yaml')
    with open(os.path.join(pandas_path, fname), 'a') as f:
        f.write('  - sphinx_bootstrap_theme\n')

    print('git add {}'.format(fname))


def update_conf(pandas_path):
    """
    Make changes to the documentation configuration file to use the new theme
    with the desired settings.
    """
    fname = os.path.join(pandas_path, 'doc', 'source', 'conf.py')

    content = []
    with open(os.path.join(pandas_path, fname)) as f:
        for line in f:
            if line == 'import warnings\n':
                line = 'import warnings\n'
                line += 'import sphinx_bootstrap_theme\n'
            elif line == "html_theme = 'nature_with_gtoc'\n":
                line = "html_theme = 'bootstrap'\n"
            elif line == "# html_theme_options = {}\n":
                line = 'html_theme_options = {\n'
                line += "    'navbar_title': ' ',  # name replaced by logo\n"
                line += "    'navbar_pagenav': False,  # no 'Page' dropdown\n"
                line += "    'globaltoc_depth': 0,  # no 'Site' dropdown\n"
                line += "    'navbar_sidebarrel': False,  # no prev/next links\n"
                line += "    'source_link_position': 'footer',\n"
                line += "    'navbar_class': 'navbar navbar-inverse',  # black navbar\n"
                line += "    'navbar_links': [\n"
                line += "        ('Install', 'install'),\n"
                line += "        ('Tutorial', 'tutorial/index'),\n"
                line += "        ('User guide', 'user_guide/index'),\n"
                line += "        ('API', 'api'),\n"
                line += "        ('Community', 'community'),\n"
                line += "        ('Donate', 'donate'),\n"
                line += '    ],\n'
                line += '}\n'
            elif line == "html_theme_path = ['themes']\n":
                line = 'html_theme_path = '
                line += 'sphinx_bootstrap_theme.get_html_theme_path()\n'
            elif line == '# html_logo = None\n':
                line = "html_logo = 'pandas_logo.png'\n"
            elif line == 'html_additional_pages = {\n':
                in_additional_pages_block = True
            elif line == '}\n':
                if 'in_additional_pages_block' in locals():
                    del in_additional_pages_block
                    line = '}\n'
                    line += "html_additional_pages['community'] = "
                    line += "'community.html'\n"
                    line += "html_additional_pages['donate'] = "
                    line += "'donate.html'\n"
            content.append(line)

    with open(os.path.join(pandas_path, fname), 'w') as f:
        for line in content:
            f.write(line)

    print('git add {}'.format(fname))


def remove_old_theme(pandas_path):
    """
    Remove the old theme. Do it by removing the whole themes directory, as the
    new theme is installed as a dependency.
    """
    themes_dir = os.path.join('doc', 'source', 'themes')
    try:
        shutil.rmtree(themes_dir)
    except FileNotFoundError:
        pass

    print('git rm {}'.format(themes_dir))


def copy_new_files(pandas_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    new_files_dir = os.path.join(base_dir, 'new_files')
    for dirname, dirs, fnames in os.walk(new_files_dir):
        for fname in fnames:
            source = os.path.join(dirname, fname)
            target_dirs = dirname.split('new_files')[-1] .split(os.path.sep)
            target_dir = os.path.join('doc', *target_dirs)
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
            shutil.copy(source,
                        os.path.join(pandas_path, target_dir, fname))

            print('git add {}'.format(os.path.join(target_dir, fname)))


def clean_refactoring(pandas_path, structure):
    with open(os.path.join(pandas_path, 'perform_refactoring.py')) as f:
        script_content = f.read()

    to_delete = []

    to_delete.append(os.path.join(pandas_path, 'test.json'))

    source_dir = os.path.join(pandas_path, 'doc', 'source')
    to_delete += [os.path.join(source_dir, d) for d in structure.keys()]
    to_delete += glob.glob(os.path.join(source_dir, '_static', '*.html'))
    to_delete += [os.path.join(source_dir, f) for f in ('index.rst',
                                                        'styled.xlsx',
                                                        'savefig',
                                                        'templates',
                                                        'generated')]
    for fname in to_delete:
        if os.path.isfile(fname):
            os.remove(fname)
        elif os.path.isdir(fname):
            shutil.rmtree(fname)

    os.system('git reset --hard HEAD')

    with open(os.path.join(pandas_path, 'perform_refactoring.py'), 'w') as f:
        f.write(script_content)


def main(pandas_path):
    change_rst_structure(pandas_path, STRUCTURE)
    add_dependencies(pandas_path)
    update_conf(pandas_path)
    remove_old_theme(pandas_path)
    copy_new_files(pandas_path)


if __name__ == '__main__':
    # TODO replace by path to pandas, not this repo, when ready to refactor it
    pandas_path = BASE_PATH

    if len(sys.argv) == 1:
        main(pandas_path)
    elif len(sys.argv) == 2 and sys.argv[1] == 'clean':
        clean_refactoring(pandas_path, STRUCTURE)
    else:
        raise RuntimeError('Arguments {} not understood'.format(sys.argv[1:]))
