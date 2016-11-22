from imports import *
from Headers import Headers
import instruments
#from Display import Display

#  an object that stores all the specifics related to a particular target/night of observing
class Observation(Talker):

    '''Observation object store basic information about an observation of one object on one night.'''
    def __init__(self, **kwargs):
        '''Initialize an observation object.'''

        Talker.__init__(self)
        self.fromDictionry(**kwargs)

    def loadHeaders(self, remake=False):
        self.headers = Headers(self, mute=self._mute, pithy=self._pithy)
        self.headers.load(remake=remake)

    def fromDictionary(self, dictionary):
        '''A function to read in a stored parameter file, with all details needed for extraction.'''
        self.speak('trying to read {0} for observation parameters'.format(filename))

        # store the basics of the observation
        self.name = dictionary['name']
        self.night = dictionary['night']
        self.grism = dictionary['grism'].lower()
        instrumentname = dictionary['instrument']
        self.instrument = instrument.locals()[instrumentname]


        # set up the wavelength calibration paths
        self.referenceDirectory = os.path.join(mosasaurusdirectory, 'data/', self.instrument)
        self.wavelength2pixelsFile = self.referenceDirectory  + '{0}_wavelength_identifications.txt'.format(self.grism)
        self.wavelengthsFile = self.referenceDirectory + 'HeNeAr.txt'

        # where's the base directory for this observation
        self.baseDirectory = dictionary['baseDirectory']
        if '/media/hannah/Seagate' in self.baseDirectory:
            self.baseDirectory = ' '.join(dictionary['baseDirectory'])

        # make a working directory, to store intermediates and results
        zachopy.utils.mkdir(self.baseDirectory + dictionary['workingDirectory'])
        self.workingDirectory = self.baseDirectory + dictionary['workingDirectory'] + self.name + '_' + self.night +'/'
        zachopy.utils.mkdir(self.workingDirectory)

        # where are the data stored?
        self.dataDirectory = self.baseDirectory + dictionary['dataDirectory'] + self.night +'/'
        zachopy.utils.mkdir(self.dataDirectory)

        # make sure the stitched directory is defined
        self.stitchedDirectory = self.obs.workingDirectory+'/stitched/'
        zachopy.utils.mkdir(self.stitchedDirectory)

        # where to store the extraction?
        self.extractionDirectory = self.workingDirectory + dictionary['extractionDirectory']
        zachopy.utils.mkdir(self.extractionDirectory)

        # set up the initial apertures
        self.narrowest = float(dictionary['narrowest'])
        self.widest = float(dictionary['widest'])
        self.numberofapertures = int(dictionary['numberofapertures'])


        self.skyGap = int(dictionary['skyGap']    )
        self.skyWidth = int(dictionary['skyWidth'])
        self.cosmicThreshold = float(dictionary['cosmicThreshold'])
        self.nUndispersed = np.arange(int(dictionary['nUndispersed'][0]), int(dictionary['nUndispersed'][1])+1)
        self.nScience = np.arange( int(dictionary['nScience'][0]),  int(dictionary['nScience'][1])+1)
        self.nHe = np.arange( int(dictionary['nHe'][0]),  int(dictionary['nHe'][1])+1)
        self.nNe = np.arange( int(dictionary['nNe'][0]),  int(dictionary['nNe'][1])+1)
        self.nAr = np.arange( int(dictionary['nAr'][0]),  int(dictionary['nAr'][1])+1)
        self.nDark = np.arange( int(dictionary['nDark'][0]),  int(dictionary['nDark'][1])+1)
        self.nWideFlat = np.arange(int(dictionary['nWideFlat'][0]),  int(dictionary['nWideFlat'][1])+1)
        self.nWideMask = np.arange(int(dictionary['nWideMask'][0]),  int(dictionary['nWideMask'][1])+1)
        self.nThinMask = np.arange(int(dictionary['nThinMask'][0]),  int(dictionary['nThinMask'][1])+1)
        if len(dictionary['nFinder']) == 1:
          self.nFinder = np.array([int(dictionary['nFinder'])])
        else:
          self.nFinder = np.arange(int(dictionary['nFinder'][0]),  int(dictionary['nFinder'][1])+1)
        self.nBias = np.arange(int(dictionary['nBias'][0]),  int(dictionary['nBias'][1])+1)
        self.nNeeded = np.concatenate((self.nUndispersed, self.nScience, self.nHe, self.nNe, self.nAr, self.nWideFlat, self.nWideMask, self.nThinMask, self.nFinder))
        self.cal_dictionary = {'He':self.nHe, 'Ne':self.nNe, 'Ar':self.nAr, 'Undispersed':self.nUndispersed, 'WideFlat':self.nWideFlat, 'WideMask':self.nWideMask, 'ThinMask':self.nThinMask, 'Bias':self.nBias, 'Dark':self.nDark, 'Science':self.nScience, 'Finder':self.nFinder}
        self.traceOrder    =  int(dictionary['traceOrder'])
        self.nFWHM    = float(dictionary['nFWHM'])
        self.blueward = int(dictionary['blueward'])
        self.redward = int(dictionary['redward'])
        self.target = [int(x) for x in dictionary['target']]
        self.goodComps = [int(x) for x in dictionary['comp']]

        try:
            self.gains = [float(x) for x in dictionary['gains']]
        except (ValueError,KeyError):
            self.gains = None

        try:
            self.slow = bool(dictionary['slow'])
        except KeyError:
            self.slow = False

        self.correlationAnchors = [float(x) for x in dictionary['correlationAnchors']]
        self.correlationRange = [float(x) for x in dictionary['correlationRange']]
        self.correlationSmooth = float(dictionary['correlationSmooth'])
        self.cosmicAbandon = float(dictionary['cosmicAbandon'])
        self.speak('observation parameters have been read and stored'.format(filename))

        self.displayscale=0.25

        self.ra =np.float(dictionary['ra'])
        self.dec =np.float(dictionary['dec'])
        self.binning = np.float(dictionary['binning'])
        self.subarray = np.float(dictionary['subarray'])
