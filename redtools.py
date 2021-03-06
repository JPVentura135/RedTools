from astropy.io import fits
import pandas as pd
import os


def reduc_tbl():
    """
    This function iteratively opens and reads .fits files in a given directory
    and compiles a csv file containing the filename, target name, reduction
    variables (bias and flat field) and observation filters for each file
    (observation log).

    ==========
    Arguments:
    ==========

    - No arguments

    ========
    Returns:
    ========

    - .CSV file containing the filename, target name, reduction variables
    (bias and flat field) and observation filters for each .fits file within
    specified directory.
    """
    # Prompt user input of directory path where files to be summarized are
    # located.

    path = os.path.expanduser(raw_input('Enter the path to .fits files: \n\n'))



    # Make sure pathname ends in '/' and if not then add on to the end of the
    # path string.

    if path[-1] != '/':
        path + '/'
    else:
        path = path

    print(2*'\n\n' + path + 2*'\n\n')



    # Create empty lists for construction of data arrays by iterative appending.
    # Initialize lists in the event of processing a large volume of files.

    for fitsfile in os.listdir(path):
        if fitsfile[-5:] == '.fits':
            if len(os.listdir(path)) > 200:
                fileid   = [] * len(os.listdir(path))
                dimens   = [] * len(os.listdir(path))
                overscan = [] * len(os.listdir(path))
                gain     = [] * len(os.listdir(path))
                rdnoise  = [] * len(os.listdir(path))
                objname  = [] * len(os.listdir(path))
                obsvtype = [] * len(os.listdir(path))
                filtr    = [] * len(os.listdir(path))
                comment  = [] * len(os.listdir(path))
            else:
                fileid   = []
                dimens   = []
                overscan = []
                gain     = []
                rdnoise  = []
                objname  = []
                obsvtype = []
                filtr    = []
                comment  = []



    # Open, read, and iterate over files ending with the .fits extension in
    # inputted path. Assign fits header key data to a variable and then append
    # iteratively to respective empty list.

    for fitsfile in os.listdir(path):
        if fitsfile[-5:] == '.fits':
            try:
                with fits.open(os.path.join(path, fitsfile)) as hdulist:

                    hdr = hdulist[0]

                    # Local fits file name is used here bc fits-key filename list elements not uniform in format.

                    # Try statement is used here to bypass files that dont have a fits-key 'FILENAME' eg an output file that was created like an avg bias frame or avg flat field.
                    try:
                        filename    = hdr.header['FILENAME']
                        fileid.append(fitsfile)
                        #print(fitsfile)
                        #print('\n\n')

                        dim         = hdr.header['NAXIS1'], hdr.header['NAXIS2']
                        dimens.append(dim)
                        #print(dimens)
                        #print('\n\n')

                        oscan       = hdr.header['BIASSEC']
                        overscan.append(oscan)
                        #print(overscan)
                        #print('\n\n')

                        gainval     = hdr.header['GAIN']
                        gain.append(gainval)
                        #print(gain)
                        #print('\n\n')

                        readnoise   = hdr.header['RDNOISE']
                        rdnoise.append(readnoise)
                        #print(gain)
                        #print('\n\n')

                        object_name = hdr.header['OBJECT']
                        objname.append(object_name)
                        #print(object_name)
                        #print('\n\n')

                        obsvtyp     = hdr.header['OBSTYPE']
                        obsvtype.append(obsvtyp)
                        #print(obsvtype)
                        #print('\n\n')

                        filt        = hdr.header['FILTERS']
                        filtr.append(filt)
                        #print(filtr)
                        #print('\n\n')

                        comment.append(' ')
                    except KeyError:
                        continue

            except IOError:
                print(fitsfile + ' is a  ** Bad file ** \n\n')
                fileid.append(str.format(fitsfile))
                dimens.append(' N/A ')
                overscan.append(' N/A ')
                gain.append(' N/A ')
                rdnoise.append(' N/A ')
                objname.append(' N/A ')
                obsvtype.append(' N/A ')
                filtr.append(' N/A ')
                comment.append('Empty or corrupt FITS file.')
                continue

    print(fileid, dimens, overscan, gain, rdnoise, objname, obsvtype, filtr, comment)


    # Create an empty pandas dataframe object (data table) and assign populated
    # data lists to dataframd columns.

    datatbl = list(zip(fileid, dimens, overscan, gain, rdnoise, objname, obsvtype, filtr, comment))

    def getKey(item):
        return item[0]

    datatbl = sorted(datatbl, key = getKey)

    dataframe = pd.DataFrame(data = datatbl)

    print(dataframe)


    # Export dataframe object to a .csv file in specified directory path.

    dataframe.to_csv(path +  'observation_log.csv', header = ['Filename', 'Image Dimensions', 'Overscan', 'Gain', 'Read Noise', 'Object Name', 'Observation Type', 'Filter', 'Comment'], index = None)
