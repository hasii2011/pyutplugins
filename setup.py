
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="pyutplugincore",
    version="0.6.3",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Pyut Plugins',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyutplugincore",
    package_data={
        'plugins':                         ['py.typed'],
        'plugins.common':                  ['py.typed'],
        'plugins.common.ui':               ['py.typed'],
        'plugins.io':                      ['py.typed'],
        'plugins.io.dtd':                  ['py.typed'],
        'plugins.io.gml':                  ['py.typed'],
        'plugins.io.java':                 ['py.typed'],
        'plugins.io.pdf':                  ['py.typed'],
        'plugins.io.python':               ['py.typed'],
        'plugins.io.python.pyantlrparser': ['py.typed'],
        'plugins.io.wximage':              ['py.typed'],
        'plugins.tools':                   ['py.typed'],
        'plugins.tools.orthogonal':        ['py.typed'],
        'plugins.tools.sugiyama':          ['py.typed'],
        'core':            ['py.typed'],
        'core.types':      ['py.typed'],
        'core.exceptions': ['py.typed'],
    },
    packages=[
        'plugins', 'plugins.common', 'plugins.common.ui',
        'plugins.io',
        'plugins.io.dtd',
        'plugins.io.gml',
        'plugins.io.java',
        'plugins.io.pdf',
        'plugins.io.python', 'plugins.io.python.pyantlrparser',
        'plugins.io.wximage',
        'plugins.tools', 'plugins.tools.orthogonal', 'plugins.tools.sugiyama',
        'core', 'core.types', 'core.exceptions',
    ],
    install_requires=['click~=8.1.3',
                      'antlr4-python3-runtime==4.9.3',
                      'pyumldiagrams==2.30.8',
                      'networkx==2.8.5',
                      'orthogonal==1.1.7',
                      'wxPython~=4.2.0',
                      'pyutmodel==1.2.0',
                      'ogl==0.60.15',
                      'oglio==0.5.16',
                      'untanglepyut==0.6.2',
                      ]
)
