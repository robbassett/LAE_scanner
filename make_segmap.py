import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits as pf
from scipy.ndimage import gaussian_filter as filt
import argparse

def make_segment(im,lim,val):
    seg = np.zeros(im.shape)
    r,c = np.where(im >= lim)
    #seg[r,c] = val
    good = [[15,15]]
    done = []
    fl = 0
    while fl == 0:
        new_count = 0
        for i in range(len(good)):
            if good[i] not in done:
                done.append(good[i])
                tr,tc = good[i][0],good[i][1]
                for d in [[-1,0],[0,1],[1,0],[0,-1]]:
                    cr,cc = tr+d[0],tc+d[1]
                    try:
                        if im[cr,cc] >= lim:
                            good.append([cr,cc])
                            new_count += 1
                    except:
                        pass
                            
        if new_count == 0:
            fl = 1

    good = np.array(good).T.astype(int)
    seg[good[0],good[1]] = val
    return seg

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input',required=True,type=str)
parser.add_argument('-c','--cube',required=True,type=str)
parser.add_argument('-u','--unsure',default=False,type=bool)
parser.add_argument('-o','--output',default='LSDcat_segmap.fits',type=str)
args = parser.parse_args()

class_data = np.loadtxt(args.input,float)
cube = pf.open(args.cube)[1].data

segout = np.zeros((cube.shape[1],cube.shape[2]))

whs = 15
nbs = 3
good = np.where(class_data[:,-1] != 2)[0] if args.unsure else np.where(class_data[:,-1] == 1)[0]
segnum = 5000
for t in good:
    row = class_data[t]
    coords = [int(row[3]),int(row[2]),int(row[4])]
    mini_cube = cube[
        coords[2]-nbs:coords[2]+nbs,
        coords[0]-whs:coords[0]+whs,
        coords[1]-whs:coords[1]+whs
    ]

    cont_cube = cube[
        coords[2]+10:coords[2]+30,
        coords[0]-whs:coords[0]+whs,
        coords[1]-whs:coords[1]+whs
    ]

    nb_im = np.nansum(mini_cube,axis=0)-(np.nansum(cont_cube,axis=0)*(6./20.))
    nb_im = filt(nb_im,sigma=1.)
    tseg = make_segment(nb_im,6.5,segnum)
    segnum+=1
    segout[
        coords[0]-whs:coords[0]+whs,
        coords[1]-whs:coords[1]+whs,
    ] = tseg
    
smm = pf.PrimaryHDU(segout)
smm.writeto(args.output,overwrite=True)
