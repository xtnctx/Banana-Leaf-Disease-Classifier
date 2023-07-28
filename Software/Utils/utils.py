from PyQt5 import QtWidgets
from . import objTypes
import json
import datetime
import os
import pathlib


class Project:
    def __init__(self) -> None:
          self._path = ''
          self._readPreferences()
    
    def __repr__(self) -> str:
        return pathlib.Path(self._path).name

    def _readPreferences(self) -> None:
        with open('./user-preferences.json', 'r') as openfile:
            prefs:dict = json.load(openfile)
        self._path = prefs["Project Path"]

    @property
    def path(self) -> objTypes.strPath:
        return self._path

    @path.setter
    def path(self, dir:objTypes.strPath) -> None:
        with open("./user-preferences.json", "r+") as outfile:
            prefs = json.load(outfile)
            prefs["Project Path"] = dir
            outfile.seek(0)
            json.dump(prefs, outfile, indent=4)
            outfile.truncate()
        self._path = dir

    @staticmethod
    def mkNewProject(path:objTypes.strPath) -> None:
        ''' Initialize new project (create Folders & analytics) '''
        os.makedirs(f'{path}/Black Sigatoka', exist_ok=True)
        os.makedirs(f'{path}/Yellow Sigatoka', exist_ok=True)

        current_time = datetime.datetime.now()
        data = {
            "created": f'{current_time.month} {current_time.day}, {current_time.year}',
            "isProject": True
        }
        json_object = json.dumps(data, indent=4)

        with open(f'{path}/analytics.json', "w") as outfile:
            outfile.write(json_object)

    @staticmethod
    def isProject(path:objTypes.strPath) -> bool:
        ''' Check if selected path is a subtype of this project '''
        try:
            with open(f'{path}/analytics.json', 'r') as openfile:
                analytics:dict = json.load(openfile)

            if analytics.get('isProject') is not None:
                return analytics['isProject']

        except (Exception, FileNotFoundError):
            return False


class AppStyle:
    windowsvista = QtWidgets.QStyleFactory.create('windowsvista')

    windows = QtWidgets.QStyleFactory.create('windows')

    fusion = QtWidgets.QStyleFactory.create('fusion')
