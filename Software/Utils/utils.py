from PyQt5 import QtWidgets
from Config import settings
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
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, dir:str) -> None:
        with open("./user-preferences.json", "r+") as outfile:
            prefs:dict = json.load(outfile)
            prefs["Project Path"] = dir
            outfile.seek(0)
            json.dump(prefs, outfile, indent=4)
            outfile.truncate()
        self._path = dir

    @staticmethod
    def mkNewProject(path:str) -> None:
        ''' Initialize new project (create Folders & analytics) '''
        os.makedirs(f'{path}/{settings.b_sigatoka}', exist_ok=True)
        os.makedirs(f'{path}/{settings.y_sigatoka}', exist_ok=True)

        current_time = datetime.datetime.now()
        data = {
            "created": f'{current_time.month} {current_time.day}, {current_time.year}',
            "isProject": True
        }
        json_object = json.dumps(data, indent=4)

        with open(f'{path}/analytics.json', "w") as outfile:
            outfile.write(json_object)

    @staticmethod
    def isProject(path:str) -> bool:
        ''' Check if selected path is a subtype of this project '''
        try:
            with open(f'{path}/analytics.json', 'r') as openfile:
                analytics:dict = json.load(openfile)

            if analytics.get('isProject') is not None:
                return analytics['isProject']

        except (Exception, FileNotFoundError):
            return False


class Analytics:
    '''
        :attr data: {
            user:                           desktop logged in username\n
            title:                          Analytics\n
            created:                        datetime (Weekday, mm/dd/yy - time)\n
            modified:                       datetime (Weekday, mm/dd/yy - time)\n
            images: [
                {
                    id:                     type=int\n
                    datetime:               datetime (Weekday, mm/dd/yy - time) = type=str\n
                    path:                   directory of image - type=str\n
                    classification:         black or yellow sigatoka = type=str\n
                    confidence:             prediction confidence level - type=float\n
                    shape:                  image resolution and channel - type=tuple\n
                    type:                   .jpg\n
                    created:                datetime (Weekday, mm/dd/yy - time)\n
                    modified:               datetime (Weekday, mm/dd/yy - time)\n
                }
                
            ]\n\n

            black_sigatoka: {
                count:                      type=int
                total_confidence:           type=float
            }\n\n

            yellow_sigatoka: {
                count:                      type=int
                total_confidence:           type=float
            }\n\n

            image_count:                    type=int\n
            total_confidence:               type=float\n
        }
    '''
    data = {'title': 'Analytics'}

    def __init__(self) -> None:
        with open('./analytics.json', 'r') as f:
            self.data:dict = json.load(f)

    def add(self, data:dict) -> None:
        current_time = datetime.datetime.now()

        with open('./analytics.json', "r+") as outfile:
            d:dict = json.load(outfile)

            d['user'] = self.user()
            d['title'] = 'Analytics'
            d['created'] = current_time.strftime(f'%A, %B %d, %Y, %-I:%M:%S %p')

            images:list[dict] = d['images']
            images.append(data['new_image'])
            d['images'] = images

            outfile.seek(0)
            json.dump(d, outfile, indent=4)
            outfile.truncate()

        self.update()

    def update(self):
        pass
    
    def create_new_id(self) -> int:
        return max([i.get('id') for i in self.images()]) + 1
    
    
    # Get data from analytics
    @staticmethod
    def user() -> str:
        return os.getlogin()

    def title(self) -> str:
        return self.data['title']
    
    def created(self) -> str:
        return self.data['created']
    
    def modified(self) -> str:
        return self.data['modified']
    
    def images(self) -> list:
        return self.data['images']

    def black_sigatoka(self) -> dict:
        return self.data['black_sigatoka']

    def yellow_sigatoka(self) -> dict:
        return self.data['yellow_sigatoka']

    def image_count(self) -> int:
        return self.data['image_count']

    def total_confidence(self) -> float:
        return self.data['total_confidence']


class AppStyle:
    windowsvista = QtWidgets.QStyleFactory.create('windowsvista')

    windows = QtWidgets.QStyleFactory.create('windows')

    fusion = QtWidgets.QStyleFactory.create('fusion')
