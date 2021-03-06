import numpy as np
import astropy.io.fits as pf

import os
import glob



def MiniCubes(catalog,cube_name,ncubes=20,_buffer=50):
    chk = glob.glob('./tmp_cubes/')
    if len(chk) == 0:
        os.mkdir('./tmp_cubes/')
    cube = pf.open(cube_name)
    sig  = cube[1].data
    noi  = cube[2].data
    hed  = cube[1].header
    wav  = hed['CD3_3']*np.arange(0,hed['NAXIS3']+1,1) + hed['CRVAL3']

    cat = np.loadtxt(catalog,float)
    centz = np.zeros(ncubes)
    strtz = np.zeros(ncubes)
    bin_edges = np.linspace(np.min(cat[:,4])-30.,np.max(cat[:,4])+30.,ncubes+1)
    for i in range(ncubes):
        if i == 0:
            czs = [0,int(bin_edges[0]+_buffer)]
        elif i == ncubes-1:
            czs = [int(bin_edges[-2]-_buffer),int(bin_edges[-1])]
        else:
            czs = [int(bin_edges[i-1]-_buffer),int(bin_edges[i]+_buffer)]

        hdu1 = pf.PrimaryHDU(sig[czs[0]:czs[1],:,:])
        hdu2 = pf.ImageHDU(noi[czs[0]:czs[1],:,:])
        thed = hdu1.header
        thed['NAXIS3'] = czs[1]-czs[0]
        thed['CRVAL3'] = wav[czs[0]]
        thed['CD3_3']  = hed['CD3_3']
        tmc  = pf.HDUList([hdu1,hdu2])
        tmc.writeto(f'./tmp_cubes/cube_{i}.fits',overwrite=True)

        centz[i] = (czs[1]+czs[0])/2.
        strtz[i] = czs[0]

    return centz,strtz
