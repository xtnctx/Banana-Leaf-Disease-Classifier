from PyQt5 import QtWidgets
from Config import settings
from dataclasses import dataclass
import json
import datetime
import os
import pathlib
import uuid


class Project:
    def __init__(self) -> None:
          self._path = ''
          self.brightness = 0
          self.contrast = 0
          self.zoom = 0
          self.isDefisheye = False
          self.isGrabCut = False
          self._loadPreferences()
    
    def __repr__(self) -> str:
        return pathlib.Path(self._path).name

    def _loadPreferences(self) -> None:
        with open(f'./{settings.Dev.pref_file}', 'r') as openfile:
            prefs:dict = json.load(openfile)
        self.update_project_prefs(prefs)
    
    def update_project_prefs(self, prefs):
        self._path = prefs["Project Path"]
        self.brightness = prefs["brightness"]
        self.contrast = prefs["contrast"]
        self.zoom = prefs["zoom"]
        self.isDefisheye = prefs["isDefisheye"]
        self.isGrabCut = prefs["isGrabCut"]

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, dir:str) -> None:
        with open(f'./{settings.Dev.pref_file}', 'r+') as outfile:
            prefs:dict = json.load(outfile)
            prefs["Project Path"] = dir
            outfile.seek(0)
            json.dump(prefs, outfile, indent=4)
            outfile.truncate()
        self._path = dir
    
    def save_controls(self, brightness:int, contrast:int, zoom:int, isDefisheye:bool, isGrabCut:bool):
        with open(f'./{settings.Dev.pref_file}', 'r+') as outfile:
            prefs:dict = json.load(outfile)
            prefs["brightness"] = brightness
            prefs["contrast"] = contrast
            prefs["zoom"] = zoom
            prefs["isDefisheye"] = isDefisheye
            prefs["isGrabCut"] = isGrabCut
            outfile.seek(0)
            json.dump(prefs, outfile, indent=4)
            outfile.truncate()
        self.update_project_prefs(prefs)

    @staticmethod
    def mkNewProject(path:str) -> dict:
        ''' Initialize new project (create Folders & analytics) '''
        os.makedirs(f'{path}/{settings.b_sigatoka}', exist_ok=True)
        os.makedirs(f'{path}/{settings.y_sigatoka}', exist_ok=True)
        analytics_read = Analytics.create_file(path)
        return analytics_read

    @staticmethod
    def is_project(path:str) -> bool:
        ''' Check if selected path is a subtype of this project '''
        try:
            with open(f'{path}/{settings.Dev.analytics_file}', 'r') as openfile:
                analytics:dict = json.load(openfile)

            if analytics.get('is_project') is not None:
                return analytics['is_project']

        except (Exception, FileNotFoundError):
            return False


@dataclass
class Image:
    id:str
    path:str
    classification:str
    confidence:float
    shape:tuple
    type:str
    created:str
    modified:str

    
class Analytics:
    '''
        :attr data: {
            user:                           desktop logged in username\n
            title:                          Analytics\n
            created:                        datetime (Weekday, mm/dd/yy - time)\n
            modified:                       datetime (Weekday, mm/dd/yy - time)\n
            images: [
                @Image {
                    id:                     type=str\n
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
            overall_confidence:               type=float\n
            is_project:                     True\n
        }
    '''
    data = {'title': 'Analytics'}
    path = ''

    def __init__(self, path='') -> None:
        if path != '':
            self.path = path
            with open(f'{self.path}/{settings.Dev.analytics_file}', 'r') as f:
                self.data:dict = json.load(f)

    @staticmethod
    def create_file(path:str) -> dict:
        today = Analytics.get_clock()
        data = {
            'user': Analytics.user(),
            'title': 'Analytics',
            'created': today,
            'modified': today,
            'images': [],
            'black_sigatoka': {},
            'yellow_sigatoka': {},
            'image_count': 0,
            'overall_confidence': 0.0,
            'is_project': True
        }

        json_object = json.dumps(data, indent=4)
        with open(f'{path}/{settings.Dev.analytics_file}', "w") as outfile:
            outfile.write(json_object)
        return data

    def add_image(self, image:Image) -> None:
        with open(f'{self.path}/{settings.Dev.analytics_file}', "r+") as outfile:
            file_data:dict = json.load(outfile)

            file_data['user'] = self.user()
            file_data['modified'] = Analytics.get_clock()
            file_data['images'].append(image.__dict__)

            black_sigatoka_images = self.groupImages(obj=file_data['images'], cls=settings.b_sigatoka)
            file_data['black_sigatoka']['count'] = len(black_sigatoka_images)
            file_data['black_sigatoka']['total_confidence'] = self.calculate_total_confidence(black_sigatoka_images)

            yellow_sigatoka_images = self.groupImages(obj=file_data['images'], cls=settings.y_sigatoka)
            file_data['yellow_sigatoka']['count'] = len(yellow_sigatoka_images)
            file_data['yellow_sigatoka']['total_confidence'] = self.calculate_total_confidence(yellow_sigatoka_images)
            
            file_data['image_count'] = len(file_data['images'])
            file_data['overall_confidence'] = self.calculate_total_confidence(file_data['images'])

            outfile.seek(0)
            json.dump(file_data, outfile, indent=4)
            outfile.truncate()

        self.data = file_data
    
    @staticmethod
    def create_new_id() -> str:
        return str(uuid.uuid4())
    
    @staticmethod
    def get_clock() -> str:
        return datetime.datetime.now().strftime(f'%A, %B %d, %Y, %#I:%M:%S %p')
    
    def groupImages(self, obj:dict, cls:str) -> list:
        ''' :param c: from settings.class_names '''
        if cls not in settings.class_names:
            return []
        return [c for c in obj if c.get('classification') == cls]

    def calculate_total_confidence(self, group:list) -> float:
        sum = 0.0
        n_group = len(group)
        if n_group != 0:
            for obj in group:
                sum += obj.get('confidence')
            return sum / len(group)
        return sum


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

    def overall_confidence(self) -> float:
        return self.data['overall_confidence']



class AppStyle:
    windowsvista = QtWidgets.QStyleFactory.create('windowsvista')

    windows = QtWidgets.QStyleFactory.create('windows')

    fusion = QtWidgets.QStyleFactory.create('fusion')
