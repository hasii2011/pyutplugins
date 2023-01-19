
from typing import Dict
from typing import Optional

from logging import Logger
from logging import getLogger

from sys import platform as sysPlatform

from os import getenv as osGetEnv

from configparser import ConfigParser

from pyutplugins.coreinterfaces.Singleton import Singleton
from pyutplugins.toolplugins.orthogonal.OrthogonalAdapter import LayoutAreaSize


PLUGIN_PREFS_NAME_VALUES = Dict[str, str]


class PluginPreferences(Singleton):

    PREFERENCES_FILENAME:   str = 'pyutplugins.ini'
    THE_GREAT_MAC_PLATFORM: str = 'darwin'

    PYUT_PLUGINS_PREFERENCES_SECTION: str = 'PyutPlugins'

    ORTHOGONAL_LAYOUT_SIZE: str = 'orthogonal_layout_size'

    PLUGIN_PREFERENCES: PLUGIN_PREFS_NAME_VALUES = {
        ORTHOGONAL_LAYOUT_SIZE:   LayoutAreaSize(1000, 1000).__str__(),
    }

    # noinspection PyAttributeOutsideInit
    def init(self, *args, **kwargs):
        self.logger: Logger = getLogger(__name__)

        self._config: ConfigParser = ConfigParser()

        self._preferencesFileName: str = self._getPreferencesLocation()

        self._loadPreferences()

    @property
    def orthogonalLayoutSize(self) -> LayoutAreaSize:

        serializedDimensions: str = self._config.get(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION, PluginPreferences.ORTHOGONAL_LAYOUT_SIZE)
        return LayoutAreaSize.deSerialize(serializedDimensions)

    @orthogonalLayoutSize.setter
    def orthogonalLayoutSize(self, newValue: LayoutAreaSize):
        self._config.set(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION, PluginPreferences.ORTHOGONAL_LAYOUT_SIZE, newValue.__str__())
        self._saveConfig()

    def _getPreferencesLocation(self) -> str:

        if sysPlatform == "linux2" or sysPlatform == "linux" or sysPlatform == PluginPreferences.THE_GREAT_MAC_PLATFORM:
            homeDir:  Optional[str] = osGetEnv('HOME')
            fullName: str           = f'{homeDir}/{PluginPreferences.PREFERENCES_FILENAME}'
            preferencesFileName: str = fullName
        else:
            preferencesFileName = PluginPreferences.PREFERENCES_FILENAME

        return preferencesFileName

    def _loadPreferences(self):

        self._ensurePreferenceFileExists()

        # Read data
        self._config.read(self._preferencesFileName)
        self._addMissingPreferences()
        self._saveConfig()

    def _ensurePreferenceFileExists(self):

        try:
            # noinspection PyUnusedLocal
            with open(self._preferencesFileName, "r") as f:
                pass
        except (ValueError, Exception):
            try:
                with open(self._preferencesFileName, "w") as fw:
                    fw.write("")
                    self.logger.warning(f'Preferences file re-created')
            except (ValueError, Exception) as e:
                self.logger.error(f"Error: {e}")
                return

    def _addMissingPreferences(self):

        try:
            if self._config.has_section(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION) is False:
                self._config.add_section(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION)
            for prefName in PluginPreferences.PLUGIN_PREFERENCES:
                if self._config.has_option(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION, prefName) is False:
                    self._addMissingPluginPreference(prefName, PluginPreferences.PLUGIN_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def _addMissingPluginPreference(self, preferenceName, value):
        self._addMissingPreference(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION, preferenceName, value)

    def _addMissingPreference(self, sectionName: str, preferenceName: str, value: str):
        self._config.set(sectionName, preferenceName, value)
        self._saveConfig()

    def _saveConfig(self):
        """
        Save data to the preferences file
        """
        with open(self._preferencesFileName, "w") as fd:
            self._config.write(fd)
