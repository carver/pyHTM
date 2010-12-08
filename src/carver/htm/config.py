'''
Created on Nov 27, 2010

@author: Jason Carver
'''
from ConfigParser import ConfigParser
import os

PROJECT_BASE_PATH = os.path.abspath(__file__.rpartition('src')[0])
SITE_PROPERTIES_PATH = os.path.join(PROJECT_BASE_PATH, 'src', 'htm.properties')
DEFAULT_PROPERTIES_PATH = os.path.join(PROJECT_BASE_PATH, 'src', 'htm.default.properties')

class Config(ConfigParser):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        '''
        ConfigParser.__init__(self)
        
        #load defaults
        self.readfp(open(DEFAULT_PROPERTIES_PATH))
        
        #load site settings
        self.read(SITE_PROPERTIES_PATH)

    def save(self):
        f = open(SITE_PROPERTIES_PATH, 'w')
        self.write(f)
        f.close()

config = Config()
