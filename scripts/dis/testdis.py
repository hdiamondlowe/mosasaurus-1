from mosasaurus.instruments import DISr

instrument = DISr(binning=2, grating='R300')
observation = Observation(
    name='calibrations',
    instrument=instrument,
    night='UT20161111',
    baseDirectory='/Users/zkbt/Cosmos/Data/APO/DIS/',
    dataDirectory='data/',
    workingDirectory='working/',
    extractionDirectory='initialtest/',
    nUndispersed = np.arange(0),
    nScience = np.arange(0),
    nHe = np.arange(5) + 27,
    nNe = np.arange(5) + 32,
    nHe = np.arange(5) + 37,
    nWideFlat = np.arange(5) + 44,
    nBias = np.arange(0),
    nWideMask = np.arange(5) + 49,
    nDark = np.arange(0),
    nFinder = np.arange(0)
    )


'''


# extraction widths, from narrowest to widest
narrowest            2
widest              12
numberofapertures    6

# initial guess for the sky regions
skyWidth              10

# pixels within this distance of the aperture will be excluded from sky
skyGap                2

# other properties
cosmicThreshold      10

# (how much to trim out around each star)
subarray             50


# extraction parameters
traceOrder             2
nFWHM                  2

# what area of the detector contains real data? (for individual amplifiers


# how far (in pixels) does spectrum extend away from direct image position
blueward       2000
redward        2000

# which comparison stars to use?
target        0
comp          1 3 5 6 7 8
cosmicAbandon 100

# how should spectra be shifted relative to each other?
correlationAnchors 8498.0 8542.0 8662.0
correlationRange   8350 8800
correlationSmooth  2

# for BJD calculation
ra          153.7090887
dec        -47.15496899
'''
