import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import astropy.io.fits as pf
import bottleneck as bn
import copy

CMAP = copy.copy(cm.get_cmap('inferno'))
CMAP.set_bad(color='w')

def plot_step_spectrum(wav,spec,ax):
    nwav = np.zeros(len(wav)*2+2)
    nspc = np.zeros(len(wav)*2+2)
    dw = (wav[1]-wav[0])/2.

    for i in range(len(wav)):
        for j in range(2): nwav[(i*2)+j] = wav[i]
        nspc[i*2] = spec[i]
        try:
            nspc[(i*2)+1] = spec[i+1]
        except:
            nspc[(i*2)+1] = spec[i]

    tp = np.where((nwav > wav.min())&(nwav < wav.max()))[0]
    ax.plot(nwav[tp]+dw,nspc[tp],'k-')

# This class reads in the MAGPI datacube and creates
# an object capable of displaying the aperture spectrum
# and narrow-band image of each candidate
class MAGPI_LAE_Check(object):

    # Here file_in is the datacube.fits file and sum_rad is the aperture radius (in pixels)
    def __init__(self,file_in,sum_rad=2.0,data_ind=0):
        self.sum_rad=sum_rad
        
        dc = pf.open(file_in)
        self.data  = dc[data_ind].data
        self.noise = dc[data_ind+1].data
        self.head  = dc[data_ind].header
        dc.close()
        
        mnoi = bn.nanmean(self.noise,axis=1)
        self.mean_noise = bn.nanmean(mnoi,axis=1)

        dc = 0.

        self.wav_ind = np.arange(0,self.data.shape[0],1.)
        self.wav     = self.head['CRVAL3'] + (self.wav_ind*self.head['CD3_3'])

        x = np.linspace(0,self.data.shape[1],self.data.shape[1])
        y = np.linspace(0,self.data.shape[2],self.data.shape[2])

        self.xv,self.yv = np.meshgrid(x,y)

    def Single_Plot(self,coords,idt,IDt,box_size=20,spec_size=70, nbvmax=100):

        self.current_coords = coords
        self.current_rad    = np.sqrt((self.xv-coords[0])**2.+(self.yv-coords[1])**2.)

        tr,tc = np.where(self.current_rad <= self.sum_rad)
        tz    = np.where(np.abs(self.wav_ind-coords[2]) <= spec_size)[0]

        yshf = 0
        imr = np.linspace(int(coords[0]-box_size),int(coords[0]+box_size),int((2.*box_size)+1.),dtype=int)
        if imr[0] < 0:
            yshf = imr.min()
            imr = np.arange(0,2*box_size+1,1,dtype=int)
        if imr[-1] > self.data.shape[2]-1:
            yshf = imr.max()-self.data.shape[2]
            imr = np.arange(self.data.shape[2]-2*box_size-1,self.data.shape[2],1,dtype=int)

        xshf = 0
        imc = np.linspace(int(coords[1]-box_size),int(coords[1]+box_size),int((2.*box_size)+1.),dtype=int)
        if imc[0] < 0:
            xshf = imc.min()
            imc = np.arange(0,2*box_size+1,1,dtype=int)
        if imc[-1] > self.data.shape[1]-1:
            xshf = imc.max()-self.data.shape[1]
            imc = np.arange(self.data.shape[1]-2*box_size-1,self.data.shape[1],1,dtype=int)
            
        imz = np.where(np.abs(self.wav_ind-coords[2]) <= 3.)[0]
        subz= np.where((coords[2]-self.wav_ind-4. < 30)|(self.wav_ind-4-coords[2] < 30))[0]
        subtot= self.data[subz,:,:]
        subv= subtot[:,imc,:]
        subv= subv[:,:,imr]
        subv= bn.nanmean(subv,axis=0)

        self.current_spec = np.nansum(self.data[:,tr,tc],axis=1)
        self.current_img  = self.data[imz,:,:]
        self.current_img  = self.current_img[:,imc,:]
        self.current_img  = self.current_img[:,:,imr]
        self.current_img  = np.nansum(self.current_img-subv,axis=0)

        br,bc = np.where(self.current_img == 0)
        self.current_img[br,bc] = np.nan

        subtot = bn.nanmean(subtot,axis=0)
        self.tot_img = self.data[imz,:,:]
        self.tot_img = np.nansum(self.tot_img-subtot,axis=0)

        tzc = np.where(np.abs(self.wav_ind-coords[2]) <= 6.)[0]
        
        F  = plt.figure(num=1,figsize=(14,5),clear=True)

        # Display spectrum
        ax = F.add_subplot(121)
        plot_step_spectrum(self.wav[tz],self.current_spec[tz],ax)
        ax.set_title(f'Detection #{int(float(idt))}, Object #{int(float(IDt))}',fontsize=18)
        ax.set_ylabel('Signal',fontsize=18)
        xa = ax.twinx()
        xa.plot(self.wav[tz],self.mean_noise[tz],'r-')
        xa.set_ylabel('Noise',color='r',rotation=-90,labelpad=15,fontsize=18)
        xa.tick_params(axis='y',color='r',labelcolor='r')
        try:
            ax.fill_between([self.wav[imz[0]],self.wav[imz[-1]]],1e15,-500,color='limegreen',alpha=.25)
        except:
            pass
        ax.set_xlabel(r'$\lambda_{obs}$ ${\AA}$',fontsize=18)
        xa.tick_params(axis='y',labelsize=15)
        ax.tick_params(axis='both',labelsize=15)
        try:
            ax.set_ylim(np.nanmin(self.current_spec[tz])*1.2,np.nanmax(self.current_spec[tz]*1.2))
        except:
            pass

        # Display narrow-band image
        ax = F.add_subplot(122)
        aperture = plt.Circle((box_size+yshf,box_size+xshf), self.sum_rad, fc='None',ec='w')
        
        vmax = np.nanmax(self.current_img)*(nbvmax/100)
        vmin = np.nanmin(self.current_img)
        """
        if nbvmax!=None:
            vmax = np.nanmin(self.current_img) +  ((np.nanmax(self.current_img)-np.nanmin(self.current_img)) * (nbvmax/100) )
            if vmax <=-8: 
                vmax=None
            ax.imshow(self.current_img,origin='lower',vmin=-8, vmax=vmax, cmap=CMAP)
        else:
            ax.imshow(self.current_img,origin='lower',vmin=-8,cmap=CMAP)
        """
        ax.imshow(self.current_img,origin='lower',vmin=vmin,vmax=vmax,cmap=CMAP)

        ax.add_patch(aperture)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Narrow-band',color='limegreen',fontsize=18)
        ax.set_xlabel(f'x, y, z: {int(coords[0])}, {int(coords[1])}, {int(coords[2])}',fontsize=18)
        
        plt.tight_layout()
        return F, np.nanmax(self.current_img)
        
    def Full_Spectrum(self,coords):
        self.current_rad    = np.sqrt((self.xv-coords[0])**2.+(self.yv-coords[1])**2.)

        tr,tc = np.where(self.current_rad <= self.sum_rad)
        return {'wav':self.wav,'spec':np.sum(self.data[:,tr,tc],axis=1),'lc':self.wav[int(coords[2])]}
