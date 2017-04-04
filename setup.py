import setuptools
import pypandoc

long_description = pypandoc.convert('README.md', 'rst')

setuptools.setup(
    name='stochasticdp',
    version='0.1',
    description='''
        A small package for solving finite-horizon, finite-state stochastic
        dynamic programs.
    ''',
    long_description=long_description,
    url='https://github.com/nelsonuhan/stochasticdp',
    author='Nelson Uhan',
    author_email='nelson@uhan.me',
    license='MIT',
    packages=['stochasticdp'],
)
