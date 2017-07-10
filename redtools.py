import os
import pandas as pd
from astropy.io import fits


def reduc_tbl():
    '''
    This function iteratively opens and reads .fits files in a given directory and compiles a csv file containing 
    the filename, target name, reduction variables (bias and flat field) and observation filters for each file 
    (observation log).
    
    ==========
    Arguments:
    ==========
    
    - No arguments 
    
    ========
    Returns:
    ========
    
    - .CSV file containing the filename, target name, reduction variables (bias and flat field) 
      and observation filters for each .fits file within specified directory.
    '''
    

    # Prompt user input of directory path where files to be summarized are located.


    path = os.path.expanduser(raw_input('Please enter the path to .fits files: \n\n'))
    print(3*'\n\n' + path + 3*'\n\n')
	
    
    # Create empty lists for construction of data arrays by iterative appending.
    # Initialize lists in the event of processing a large volume of files.


    for fitsfile in os.listdir(path):
        if fitsfile[-5:] == '.fits':
            if len(os.listdir(path)) > 150:
                fileid   = [] * len(os.listdir(path))
                objname  = [] * len(os.listdir(path))
                obsvtype = [] * len(os.listdir(path))
                filtr    = [] * len(os.listdir(path))
                comment  = [] * len(os.listdir(path))
            else:
                fileid   = []
                objname  = []
                obsvtype = []
                filtr    = []
                comment  = []


    # Open, read, and iterate over files ending with the .fits extension in inputted path.
    # Assign fits header key data to a variable and then append iteratively to respective empty list.


    for fitsfile in os.listdir(path):
        if fitsfile[-5:] == '.fits':
            try:
                with fits.open(os.path.join(path,fitsfile)) as hdulist:

                    hdr = hdulist[0]
					
                    filename    = hdr.header['FILENAME']
                    fileid.append(os.path.basename(os.path.normpath(filename)))
                    print(filename)
                    
                    object_name = hdr.header['OBJECT']
                    objname.append(object_name)
                    print(object_name)                    
                    
                    obsvtyp     = hdr.header['OBSTYPE']
                    obsvtype.append(obsvtyp)
                    print(obsvtype)             
                    
                    filt        = hdr.header['FILTERS']
                    filtr.append(filt)
                    print(filtr)                    
                    
                    comment.append(' ')
                
            except IOError:
                print(os.path.basename(fitsfile) + ' is a  ** Bad file **')
                fileid.append(str.format(fitsfile))
                objname.append(' N/A ')
                obsvtype.append(' N/A ')
                filtr.append(' N/A ')
                comment.append('Empty or corrupt FITS file.')
                continue
         
    #\033[1;30;31m : ANSI color code for red text

    print(fileid,objname,obsvtype,filtr,comment)

    # Create an empty pandas dataframe object (data table) and assign populated data lists to dataframe
    # columns.

    dataframe = pd.DataFrame(data = None)
    dataframe['Filename']         = fileid     
    dataframe['Object_Name']      = objname    
    dataframe['Observation_type'] = obsvtype   
    dataframe['Filter']           = filtr 
    dataframe['Comment']          = comment     
	
    print(dataframe)
	
    # Export compiled dataframe object to a .csv file in specified directory path.

    dataframe.to_csv(path + 'reduc_tbl_result.csv',columns = ['Filename','Object_name',
        'Observation_Type','Filter','Comment'],index = None)

