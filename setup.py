
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="pyutplugins",
    version="0.6.6",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Pyut Plugins',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyutplugina",
    package_data={
        'pyutplugins':                 ['py.typed'],
        'pyutplugins.common':          ['py.typed'],
        'pyutplugins.common.ui':       ['py.typed'],
        'pyutplugins.coreinterfaces': ['py.typed'],
        'pyutplugins.coretypes':      ['py.typed'],
        'pyutplugins.exceptions':     ['py.typed'],
        'pyutplugins.ioplugins':                      ['py.typed'],
        'pyutplugins.ioplugins.dtd':                  ['py.typed'],
        'pyutplugins.ioplugins.gml':                  ['py.typed'],
        'pyutplugins.ioplugins.java':                 ['py.typed'],
        'pyutplugins.ioplugins.pdf':                  ['py.typed'],
        'pyutplugins.ioplugins.python':               ['py.typed'],
        'pyutplugins.ioplugins.python.pyantlrparser': ['py.typed'],
        'pyutplugins.ioplugins.wximage':              ['py.typed'],
        'pyutplugins.toolplugins':                    ['py.typed'],
        'pyutplugins.toolplugins.orthogonal':         ['py.typed'],
        'pyutplugins.toolplugins.sugiyama':           ['py.typed'],
    },
    packages=[
        'pyutplugins', 'pyutplugins.common', 'pyutplugins.common.ui',
        'pyutplugins.coreinterfaces',
        'pyutplugins.coretypes',
        'pyutplugins.exceptions',
        'pyutplugins.ioplugins',
        'pyutplugins.ioplugins.dtd',
        'pyutplugins.ioplugins.gml',
        'pyutplugins.ioplugins.java',
        'pyutplugins.ioplugins.pdf',
        'pyutplugins.ioplugins.python', 'pyutplugins.ioplugins.python.pyantlrparser',
        'pyutplugins.ioplugins.wximage',
        'pyutplugins.toolplugins', 'pyutplugins.toolplugins.orthogonal', 'pyutplugins.toolplugins.sugiyama',
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
