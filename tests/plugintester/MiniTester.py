from wx import App

from tests.TestBase import TestBase
from tests.plugintester.DiagramLoader import TestDiagramLoader

TestBase.setUpLogging()
app: App = App()

tdl: TestDiagramLoader = TestDiagramLoader()

tdl.retrieveOglObjects()
