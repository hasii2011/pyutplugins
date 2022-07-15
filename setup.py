
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="core",
    version="0.1.0",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Pyut Plugins',
    long_description=README,
    license=LICENSE,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyutplugincore",
    package_data={
        'plugins':                   ['py.typed'],
        'plugins.common':            ['py.typed'],
        'plugins.io':                ['py.typed'],
        'plugins.io.dtd':            ['py.typed'],
        'plugins.io.gml':            ['py.typed'],
        'plugins.tools':             ['py.typed'],
        'core':            ['py.typed'],
        'core.types':  ['py.typed'],
        'core.exceptions': ['py.typed'],
    },
    packages=[
        'plugins', 'plugins.common',
        'plugins.io', 'plugins.io.dtd', 'plugins.io.gml',
        'plugins.tools',
        'core', 'core.types', 'core.exceptions',
    ],
    install_requires=['click~=8.1.3', 'ogl==0.53.1', 'pyutmodel', 'untanglepyut==0.1.3', 'wxPython~=4.1.1']
)
