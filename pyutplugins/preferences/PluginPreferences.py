
from typing import Dict
from typing import Optional

from logging import Logger
from logging import getLogger

from sys import platform as sysPlatform

from os import getenv as osGetEnv

from configparser import ConfigParser

from pyutplugins.coreinterfaces.Singleton import Singleton

from pyutplugins.toolplugins.orthogonal.LayoutAreaSize import LayoutAreaSize


PLUGIN_PREFS_NAME_VALUES = Dict[str, str]


class PluginPreferences(Singleton):

    PREFERENCES_FILENAME:   str = 'pyutplugins.ini'
    THE_GREAT_MAC_PLATFORM: str = 'darwin'

    PYUT_PLUGINS_PREFERENCES_SECTION: str = 'PyutPlugins'
    DEBUG_SECTION:                    str = 'Debug'

    ORTHOGONAL_LAYOUT_SIZE: str = 'orthogonal_layout_size'
    WX_IMAGE_FILENAME:      str = 'wx_image_filename'

    PLUGIN_PREFERENCES: PLUGIN_PREFS_NAME_VALUES = {
        ORTHOGONAL_LAYOUT_SIZE: LayoutAreaSize(1000, 1000).__str__(),
        WX_IMAGE_FILENAME:      'WxImageDump'
    }

    DEBUG_TEMP_FILE_LOCATION: str = 'debug_temp_file_location'

    DEBUG_PREFERENCES: PLUGIN_PREFS_NAME_VALUES = {
        DEBUG_TEMP_FILE_LOCATION: 'False'
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

    @property
    def wxImageFileName(self) -> str:
        return self._config.get(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION, PluginPreferences.WX_IMAGE_FILENAME)

    @wxImageFileName.setter
    def wxImageFileName(self, newValue: str):
        self._config.set(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION, PluginPreferences.WX_IMAGE_FILENAME, newValue)
        self._saveConfig()

    @property
    def debugTempFileLocation(self) -> bool:
        ans: bool = self._config.getboolean(PluginPreferences.DEBUG_SECTION, PluginPreferences.DEBUG_TEMP_FILE_LOCATION)
        return ans

    @debugTempFileLocation.setter
    def debugTempFileLocation(self, theNewValue: bool):
        self._config.set(PluginPreferences.DEBUG_SECTION, PluginPreferences.DEBUG_TEMP_FILE_LOCATION, str(theNewValue))
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

            if self._config.has_section(PluginPreferences.DEBUG_SECTION) is False:
                self._config.add_section(PluginPreferences.DEBUG_SECTION)
            for prefName in PluginPreferences.DEBUG_PREFERENCES:
                if self._config.has_option(PluginPreferences.DEBUG_SECTION, prefName) is False:
                    self._addMissingDebugPreference(prefName, PluginPreferences.DEBUG_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def _addMissingPluginPreference(self, preferenceName: str, value: str):
        self._addMissingPreference(PluginPreferences.PYUT_PLUGINS_PREFERENCES_SECTION, preferenceName, value)

    def _addMissingDebugPreference(self, preferenceName: str, value: str):
        self._addMissingPreference(PluginPreferences.DEBUG_SECTION, preferenceName, value)

    def _addMissingPreference(self, sectionName: str, preferenceName: str, value: str):
        self._config.set(sectionName, preferenceName, value)
        self._saveConfig()

    def _saveConfig(self):
        """
        Save data to the preferences file
        """
        with open(self._preferencesFileName, "w") as fd:
            self._config.write(fd)