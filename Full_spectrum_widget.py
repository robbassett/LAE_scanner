import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk

import numpy as np
import warnings

import LAE_scanner as LAEs

def full_spec_plot(spec,low=-1.,hig=-1.):
    if low == -1.:
        low = np.min(spec['wav'])
    if hig == -1.:
        hig = np.max(spec['wav'])

    one_sig = np.nanstd(spec['spec'])

    F  = plt.figure(figsize=(12,4),dpi=100)
    ax = F.add_subplot(111)
    ax.plot(spec['wav'],spec['spec'],'k-')
    ax.axvline(x=spec['lc'],linestyle='--',color='limegreen')
    ax.set_xlim((low,hig))
    ax.set_xlabel(r'$\lambda_{obs}$ $\AA$',fontsize=15)
    ax.set_ylabel(r'Flux (1e-20 ergs s$^{-1}$ cm$^{-2}$ $\AA^{-1}$)',fontsize=15)
    ax.set_ylim((-1.)*one_sig,np.nanmax(spec['spec'])*1.1)
    ax.tick_params(axis='both',labelsize=15)
    plt.tight_layout()

    return F

class FSW(object):

    def __init__(self,cube_name,coords):
        self.fsp_gui  = tk.Tk()
        self.fsp_gui.title('Full Spectrum Viewer')
        
        tmp_cube = LAEs.MAGPI_LAE_Check(cube_name,data_ind=1)
        self.tmp_spec = tmp_cube.Full_Spectrum(coords)
        self.fsp = full_spec_plot(self.tmp_spec)
        
        self.spcanvas = tk.Canvas(self.fsp_gui,width=1200,height=55)
        self.spcanvas.pack()
        
        self.elow = tk.Entry(self.spcanvas,width=15,textvariable=str(np.min(self.tmp_spec['wav'])))
        self.ehig = tk.Entry(self.spcanvas,width=15,textvariable=str(np.max(self.tmp_spec['wav'])))
        self.spcanvas.create_window(170, 45, window=self.elow)
        self.spcanvas.create_window(340, 45, window=self.ehig)

        lolab = tk.Label(self.fsp_gui,text='x lower limit')
        lolab.config(font=('Comic Sans',15,'bold'))
        hilab = tk.Label(self.fsp_gui,text='x upper limit')
        hilab.config(font=('Comic Sans',15,'bold'))
        self.spcanvas.create_window(170,15,window=lolab)
        self.spcanvas.create_window(340,15,window=hilab)

        upbutt = tk.Button(self.fsp_gui, text='    Update Plot    ',command=self.update_plot,font=('Arial',15,'bold'))
        rebutt = tk.Button(self.fsp_gui, text='    Reset Plot     ',command=self.reset_plot,font=('Arial',15,'bold'))
        self.spcanvas.create_window(490,45,window=upbutt)
        self.spcanvas.create_window(615,45,window=rebutt)
        
        self.plot=FigureCanvasTkAgg(self.fsp,master=self.fsp_gui)
        self.plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

        self.fsp_gui.mainloop()

    def update_plot(self):
        nlo,nhi = float(self.elow.get()),float(self.ehig.get())
        self.plot.get_tk_widget().pack_forget()
        plt.close('all')
        
        self.fsp = full_spec_plot(self.tmp_spec,low=nlo,hig=nhi)
        self.plot=FigureCanvasTkAgg(self.fsp,master=self.fsp_gui)
        self.plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

    def reset_plot(self):
        self.plot.get_tk_widget().pack_forget()
        plt.close('all')
        
        self.fsp = full_spec_plot(self.tmp_spec)
        self.plot=FigureCanvasTkAgg(self.fsp,master=self.fsp_gui)
        self.plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
