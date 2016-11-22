from instrument import *

class LDSS3C(instrument):

    def __init__(self):
        self.name = 'LDSS3C'
        self.observatory = 'apo'




        self.dataleft    = 0
        self.dataright    = 512
        self.databottom    = 0
        self.datatop = 2048
        self.namps = 2
        self.gains = np.array([1.72, 1.49])


    def fileprefix(self, n):
        '''Feed in an LDSS3c ccd number, and spit out
        the file prefix for that CCD amplifier pair.'''
        return self.dataDirectory + 'ccd{0:04}'.format(n)

    def loadOverscanTrimHalfCCD(self, filename):
        '''Open one half of an LDSS3 CCD, subtract the overscan, and trim.'''

        # open the FITS file, split into header and data
        hdu = astropy.io.fits.open(filename)
        header = hdu[0].header
        data = readFitsData(filename)

        # take the parts of CCD exposed to light
        goodData = data[self.obs.databottom:self.obs.datatop,self.obs.dataleft:self.obs.dataright]
        goodBias = data[self.obs.databottom:self.obs.datatop,self.obs.dataright:]

        # estimate the 1D bias (and drawdown, etc...) from the overscan
        biasEstimate = np.median(goodBias, axis=1)
        biasImage = np.ones(goodData.shape)*biasEstimate[:,np.newaxis]

        return (goodData - biasImage), header

    def trimAndStitch(self, n):
      # process the two halves separately, and then smush them together
      filenames = [self.fileprefix(n) + 'c1.fits', self.fileprefix(n) + 'c2.fits']

      # load the two halves
      c1data, c1header = self.loadOverscanTrimHalfCCD(filenames[0])
      c2data, c2header = self.loadOverscanTrimHalfCCD(filenames[1])

      # stitch the CCD's together
      header = copy.copy(c1header)
      header['STITCHED'] = True
      return np.hstack([c1data, np.fliplr(c2data)]), header

    def gain(self, **kwargs):
        try:
            self.calib.gains
        except AttributeError:
            self.calib.estimateGain()
        self.speak("multiplying by gains of {0} e-/ADU".format(self.calib.gains))
        c1data, c2data = self.amplifiers()
        gain1 = np.zeros_like(c1data) + self.calib.gains[0]
        gain2 = np.zeros_like(c2data)+ self.calib.gains[1]
        gainimage = np.hstack([gain1, np.fliplr(gain2)])
        return gainimage

    def amplifiers(self):
        return self.ccd.data[:,0:self.dataright - self.dataleft], self.ccd.data[:,self.dataright - self.dataleft:]
