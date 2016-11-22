import astropy.io.fits

def readFitsData(filename, verbose=False):
  '''Read in data from a FITS image.'''
  hdu = astropy.io.fits.open(filename)
  if verbose:
    print "      read ", filename
  image = hdu[0].data
  hdu.close()
  return image

def writeFitsData(data, filename, verbose=False):
  '''Write data to a FITS image.'''
  hdu = astropy.io.fits.PrimaryHDU(data)
  hdu.writeto(filename, clobber=True)
  if verbose:
    print "      wrote image to ", filename

def iraf2python(s):
    '''Convert an IRAF (1-indexed) column-row string
        ('[c1:c2,r1:r2]') to Python (0-indexed) [r1:r2,c1:c2]'''

    cols, rows = .strip('[]').split(',')
    bottom, top = np.array(rows.split(':')).astype(np.int) - np.array([1,0])
    left, right = np.array(cols.split(':')).astype(np.int) - np.array([1,0])
    return bottom, top, left, right
