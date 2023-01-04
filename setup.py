
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="pyutplugincore",
    version="0.6.5",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Pyut Plugins',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyutplugincore",
    package_data={
        'plugins':                 ['py.typed'],
        'plugins.common':          ['py.typed'],
        'plugins.common.ui':       ['py.typed'],
        'plugins.coreinterfaces': ['py.typed'],
        'plugins.coretypes':      ['py.typed'],
        'plugins.exceptions':     ['py.typed'],
        'plugins.ioplugins':                      ['py.typed'],
        'plugins.ioplugins.dtd':                  ['py.typed'],
        'plugins.ioplugins.gml':                  ['py.typed'],
        'plugins.ioplugins.java':                 ['py.typed'],
        'plugins.ioplugins.pdf':                  ['py.typed'],
        'plugins.ioplugins.python':               ['py.typed'],
        'plugins.ioplugins.python.pyantlrparser': ['py.typed'],
        'plugins.ioplugins.wximage':              ['py.typed'],
        'plugins.toolplugins':                    ['py.typed'],
        'plugins.toolplugins.orthogonal':         ['py.typed'],
        'plugins.toolplugins.sugiyama':           ['py.typed'],
    },
    packages=[
        'plugins', 'plugins.common', 'plugins.common.ui',
        'plugins.coreinterfaces',
        'plugins.exceptions',
        'plugins.ioplugins',
        'plugins.ioplugins.dtd',
        'plugins.ioplugins.gml',
        'plugins.ioplugins.java',
        'plugins.ioplugins.pdf',
        'plugins.ioplugins.python', 'plugins.ioplugins.python.pyantlrparser',
        'plugins.ioplugins.wximage',
        'plugins.toolplugins', 'plugins.toolplugins.orthogonal', 'plugins.toolplugins.sugiyama',
    ],
    install_requires=['click~=8.1.3',
                      'antlr4-python3-runtime==4.11.1',
                      'pyumldiagrams==2.30.8',
                      'networkx==2.8.5',
                      'orthogonal==1.1.7',
                      'wxPython~=4.2.0',
                      'pyutmodel==1.3.3',
                      'ogl==0.60.25',
                      'untanglepyut==0.6.5',
                      'oglio==0.5.40',
                      ]
)
