
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="pyutplugincore",
    version="0.5.1",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Pyut Plugins',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyutplugincore",
    package_data={
        'plugins':                   ['py.typed'],
        'plugins.common':            ['py.typed'],
        'plugins.io':                ['py.typed'],
        'plugins.io.dtd':            ['py.typed'],
        'plugins.io.gml':            ['py.typed'],
        'plugins.io.python':         ['py.typed'],
        'plugins.tools':             ['py.typed'],
        'core':        ['py.typed'],
        'core.types':  ['py.typed'],
        'core.exceptions': ['py.typed'],
    },
    packages=[
        'plugins', 'plugins.common',
        'plugins.io', 'plugins.io.dtd', 'plugins.io.gml', 'plugins.io.python', 'plugins.io.java',
        'plugins.tools',
        'core', 'core.types', 'core.exceptions',
    ],
    install_requires=['click~=8.1.3',
                      'pyumldiagrams==2.30.8',
                      'networkx==2.8.5',
                      'orthogonal==1.1.7',
                      'wxPython~=4.2.0',
                      'pyutmodel==1.1.0',
                      'ogl==0.60.5',
                      'untanglepyut==0.5.1',
                      'oglio==0.5.7'
                      ]
)
