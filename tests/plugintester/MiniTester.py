from wx import App

from tests.TestBase import TestBase
from tests.plugintester.DiagramLoader import DiagramLoader

TestBase.setUpLogging()
app: App = App()

tdl: DiagramLoader = DiagramLoader()

tdl.retrieveOglModel()
