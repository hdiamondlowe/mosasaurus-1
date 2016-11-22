from instrument import *
import glob

class DIS(instrument):

    def __init__(self):
        # basics of the observatory
        self.name = 'DIS'
        self.observatory = 'apo'
        self.suffix = ''

    def gain(self, header):
        ''' return the gain (of the last loaded image) '''
        return header['GAIN]

    def trimAndStitch(self, n):
        # process the two halves separately, and then smush them together
        filename = self.fileprefix(n) + '.fits'

        with astropy.io.fits.open(filename) as hdu:
          self.data, self.header = hdu[0].data,  hdu[0].header


        dbottom, dtop, dleft, dright = iraf2python(self.header['DATASEC'])
        trimmed = self.data[dbottom:dtop, dleft:dright]

        # subtract bias overscan (just one value)
        bbottom, btop, bleft, bright = iraf2python(self.header['BIASSEC'])
        biaslevel = np.median(self.data[bbottom:btop,bleft:bright])
        trimmed -= biaslevel

        # record that these have been stitched
        header = copy.copy(self.header)
        header['STITCHED'] = True

        return trimmed, header
                
class DISr(self):
    def __init__(self, binning=2):
        # basics
        DIS.__init__(self)
        self.suffix = 'r'
        self.name += self.suffix

        # currently handles only same binning in both dimensions
        self.binning = binning
