from ..imports import *

class Instrument(Talker):
    def __init__(self, *args, **kwargs):

        self.xsize = self.namps*(self.dataright - self.dataleft)
        self.ysize = (self.datatop - self.databottom)

    def fileprefix(self, n):
        '''Feed in a ccd number, and spit out
        the file prefix for that file (or group of files.)'''
        return glob.glob(self.dataDirectory + '*{0:04}'.format(n))
