import pickle
import sys
import os

class Level:
    def __init__(self):
        self.stats = {}
        self.level = {}
        self.gun = {}

    def load(self):
        with open(self.resource_path('files/stats.pickle'), 'rb') as f:
            dict = pickle.load(f)
        self.stats.update(dict)
        self.g = len(self.stats['gun'])
        with open(self.resource_path(f'files/level{self.stats["level"]}.pickle'), 'rb') as f:
            dict = pickle.load(f)
        self.level.update(dict)
        with open(self.resource_path(f'files/{self.stats["gun"][self.g-1]}.pickle'), 'rb') as f:
            dict = pickle.load(f)
        self.gun.update(dict)

    def save_stats(self):#Сохранение в файл
        with open(self.resource_path('files/stats.pickle'),'wb') as f:
            pickle.dump(self.stats, f)
        self.load()

    def save_level(self):#Сохранение в файл
        with open(self.resource_path(f'files/level{self.stats["level"]}.pickle','wb')) as f:
            pickle.dump(self.level,f)

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
# added_files = [
#          ( 'C:/Programming/Python/MyDoneProjects/test/files', 'files' ),
#          ( 'C:/Programming/Python/MyDoneProjects/test/sounds', 'sounds' ),
#          ( 'C:/Programming/Python/MyDoneProjects/test/images', 'images' )]