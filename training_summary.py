import numpy as np
import matplotlib.pyplot as plt
import argparse
import astropy.io.fits as pf
from matplotlib.backends.backend_pdf import PdfPages
import warnings

from LAE_scanner import *

warnings.filterwarnings("ignore")
CLDIC = {
    1:'Yes',
    2:'No',
    3:'Maybe'
}
    
def make_one_plot(line,answers,i):
    
    
    cl = CLDIC[line[-1]]
    ind = np.where(answers.T[0] == line[0])[0][0]
    ans = answers[ind]
    print(ind,line[0],ans)
    
    aa = f'{CLDIC[ans[1]]} {CLDIC[ans[2]]} {CLDIC[ans[3]]}'
    
    im = plt.imread(f'images/training/training_{i}.png')
    fig = plt.figure(dpi=250)
    ax = fig.add_subplot(111)
    ax.imshow(im,interpolation='None')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f'Your Class: {cl}, Expert Classes: '+aa)
    
    return fig

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input',required=True,type=str)
#parser.add_argument('-c','--cube',required=True,type=str)
args = parser.parse_args()

class_data = np.loadtxt(args.input,float)
answers = np.loadtxt('training_set_GAMAJ140913_answers.dat')

#cube = MAGPI_LAE_Check(args.cube,data_ind=1)

pp = PdfPages('trainingsummary.pdf')
for i,cl in enumerate(class_data):
    f = make_one_plot(cl,answers,i)
    pp.savefig()
pp.close()
