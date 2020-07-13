import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import astropy.io.fits as pf
import bottleneck as bn


# This class reads in the MAGPI datacube and creates
# an object capable of displaying the aperture spectrum
# and narrow-band image of each candidate
class MAGPI_LAE_Check(object):

    # Here file_in is the datacube.fits file and sum_rad is the aperture radius (in pixels)
    def __init__(self,file_in,sum_rad=2.0):
        self.sum_rad=sum_rad
        
        dc = pf.open(file_in)
        self.data  = dc[1].data
        self.noise = dc[2].data
        self.head  = dc[1].header

        mnoi = bn.nanmean(self.noise,axis=1)
        self.mean_noise = bn.nanmean(mnoi,axis=1)

        dc = 0.

        self.wav_ind = np.arange(0,self.data.shape[0],1.)
        self.wav     = self.head['CRVAL3'] + (self.wav_ind*self.head['CD3_3'])

        x = np.linspace(0,self.data.shape[1],self.data.shape[1])
        y = np.linspace(0,self.data.shape[2],self.data.shape[2])

        self.xv,self.yv = np.meshgrid(x,y)

    def Check_Edge(self,coords,box_size=20):

        checks = [[coords[0]-box_size,coords[1]],
                  [coords[0]+box_size,coords[1]],
                  [coords[0],coords[1]-box_size],
                  [coords[0],coords[1]+box_size]]

        self.good=True
        for ch in checks:
            tms = self.data[:,int(ch[1]),int(ch[0])]
            tch = np.where(np.isfinite(tms))[0]

            if len(tch) == 0:
                self.good=False

    def Single_Plot(self,coords,idt,IDt,box_size=20,spec_size=50):

        self.current_coords = coords
        self.current_rad    = np.sqrt((self.xv-coords[0])**2.+(self.yv-coords[1])**2.)

        tr,tc = np.where(self.current_rad <= self.sum_rad)
        tz    = np.where(np.abs(self.wav_ind-coords[2]) <= spec_size)[0]


        imr = np.linspace(int(coords[0]-box_size),int(coords[0]+box_size),int((2.*box_size)+1.),dtype=int)
        imc = np.linspace(int(coords[1]-box_size),int(coords[1]+box_size),int((2.*box_size)+1.),dtype=int)
        imz = np.where(np.abs(self.wav_ind-coords[2]) <= 3.)[0]
        subz= np.where((coords[2]-self.wav_ind-4. < 30)|(self.wav_ind-4-coords[2] < 30))[0]
        subtot= self.data[subz,:,:]
        subv= subtot[:,imc,:]
        subv= subv[:,:,imr]
        subv= bn.nanmean(subv,axis=0)

        self.current_spec = np.sum(self.data[:,tr,tc],axis=1)
        self.current_img  = self.data[imz,:,:]
        self.current_img  = self.current_img[:,imc,:]
        self.current_img  = self.current_img[:,:,imr]
        self.current_img  = np.sum(self.current_img-subv,axis=0)

        subtot = bn.nanmean(subtot,axis=0)
        self.tot_img = self.data[imz,:,:]
        self.tot_img = np.sum(self.tot_img-subtot,axis=0)

        tzc = np.where(np.abs(self.wav_ind-coords[2]) <= 6.)[0]
        
        
        F  = plt.figure(figsize=(14,5))

        # Display spectrum
        ax = F.add_subplot(121)
        ax.plot(self.wav[tz],self.current_spec[tz],'k-')
        ax.set_title(f'Detection #{int(float(idt))}, Object #{int(float(IDt))}',fontsize=18)
        ax.set_ylabel('Signal',fontsize=18)
        xa = ax.twinx()
        xa.plot(self.wav[tz],self.mean_noise[tz],'r-')
        xa.set_ylabel('Noise',color='r',rotation=-90,labelpad=15,fontsize=18)
        xa.tick_params(axis='y',color='r',labelcolor='r')
        ax.fill_between([self.wav[imz[0]],self.wav[imz[-1]]],1e15,-500,color='limegreen',alpha=.25)
        ax.set_xlabel(r'$\lambda_{obs}$ ${\AA}$',fontsize=18)
        xa.tick_params(axis='y',labelsize=15)
        ax.tick_params(axis='both',labelsize=15)
        ax.set_ylim(np.nanmin(self.current_spec[tz])*1.2,np.nanmax(self.current_spec[tz]*1.2))

        # Display narrow-band image
        ax = F.add_subplot(122)
        aperture = plt.Circle((box_size,box_size), self.sum_rad, fc='None',ec='w')
        ax.imshow(self.current_img,origin='lower',vmin=-8,cmap=cm.inferno)
        ax.add_patch(aperture)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Narrow-band',color='limegreen',fontsize=18)
        ax.set_xlabel(f'x, y, z: {int(coords[0])}, {int(coords[1])}, {int(coords[2])}',fontsize=18)
        
        plt.tight_layout()
        return F
        

if __name__ == '__main__':

    last_obj = -1
    cat    = np.loadtxt('../GAMAJ223757/catalog.cat',float)
    objs   = [133,1105,2207,3071,3940,5252,6121,8476]
    tm_obj = MAGPI_LAE_Check('../GAMAJ223757/GAMAJ223757_ZAP.fits')

    #for i in range(len(cat[:,0])):
    ind=0
    for i in range(2):
        if int(cat[i,0]) > last_obj:

            fl = 0
            while fl == 0:
                idt = str(cat[ind,0])
                IDt = str(cat[ind,1])
                crds= [float(cat[ind,2]),float(cat[ind,3]),float(cat[ind,4])]
                tm_obj.Check_Edge(crds)
                if tm_obj.good:
                    fl = 1
                    ind+=1
                else:
                    ind+=1
                    pass
                
            fig = tm_obj.Single_Plot(crds,idt,IDt)
            plt.show()
        
