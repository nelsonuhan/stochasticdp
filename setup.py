import setuptools

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = ''

setuptools.setup(
    name='stochasticdp',
    version='0.2',
    description='''
        A simple implementation of backwards induction for solving finite-horizon, finite-state stochastic
        dynamic programs.
    ''',
    long_description=long_description,
    url='https://github.com/nelsonuhan/stochasticdp',
    author='Nelson Uhan',
    author_email='nelson@uhan.me',
    license='MIT',
    packages=['stochasticdp'],
)
