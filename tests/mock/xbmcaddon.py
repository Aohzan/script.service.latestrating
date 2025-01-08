class Addon:
    def __init__(self):
        self._settings = {
            'use_imdb': 'true',
            'use_trakt': 'false',
            'update_interval': '1',
            'movie_years_back': '2',
            'tvshow_months_back': '6'
        }

    def getAddonInfo(self, key):
        return "Latest Rating Service"

    def getSetting(self, key):
        return self._settings.get(key, '')

    def getSettingBool(self, key):
        return self._settings.get(key, 'false') == 'true'

    def getSettingInt(self, key):
        return int(self._settings.get(key, '0'))

    def setSetting(self, key, value):
        self._settings[key] = str(value)

    def setSettingBool(self, key, value):
        self._settings[key] = str(value).lower() 