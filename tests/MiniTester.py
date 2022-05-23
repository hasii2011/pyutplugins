from wx import App

from tests.TestBase import TestBase
from tests.TestDiagramLoader import TestDiagramLoader

TestBase.setUpLogging()
app: App = App()

tdl: TestDiagramLoader = TestDiagramLoader()

tdl.retrieveOglObjects()
