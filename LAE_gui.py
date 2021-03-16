import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from shutil import copyfile

import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.filedialog

import numpy as np
import warnings

import LAE_scanner as LAEs
from Cube_clipper import MiniCubes as MC
from Full_spectrum_widget import FSW
from fig_init import *

warnings.filterwarnings("ignore")

class MAGPI_LAE_Scanner(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.saved  = False
        self.output = {}
        self.index=0
        self.done = False
        self.relcat = {'dets':[]}
        self.good_indices=[]
        self.prevs=[]
        self.prev = False
        self.createWidgets()

    def createWidgets(self):
        canvas1 = tk.Canvas(root,width=1000,height=210)
        canvas1.pack()

        label1 = tk.Label(root,text='MAGPI    LAE    SCANNER   v0.1')
        label1.config(font=('Comic Sans',30, 'bold'))
        canvas1.create_window(500,20,window=label1)

        self.relbutt = tk.Button(root, text='       Load Previous       ',command=self.load_prev,font=('Arial',15,'bold'))
        self.button0 = tk.Button(root, text='      Enter Classifier      ',command=self.enter_ID,font=('Arial',15,'bold'))
        self.button1 = tk.Button(root, text='        Select Cube        ',command=self.get_cube,font=('Arial', 15, 'bold'),state='disabled') 
        self.button2 = tk.Button(root, text='       Select Catalog       ', command=self.get_cat, font=('Arial', 15, 'bold'),state='disabled')
        self.button3 = tk.Button(root, text='     Start Classifying     ', command=self.start_class, font=('Arial', 15, 'bold'),state='disabled')
        self.button4 = tk.Button(root, text='      Exit Application      ', command=self.make_quit_dialog, font=('Arial', 15, 'bold'))

        canvas1.create_window(75,50,window=self.relbutt)
        canvas1.create_window(250, 50, window=self.button0)
        canvas1.create_window(425, 50, window=self.button1)
        canvas1.create_window(600, 50, window=self.button2)
        canvas1.create_window(775, 50, window=self.button3)
        canvas1.create_window(950, 50, window=self.button4)

        self.cubelab = tk.Label(root,text=f'   CUBE NAME: None   ')
        self.cubelab.config(font=('Comic Sans',15,'bold'))
        self.catlab = tk.Label(root,text=f'  CATALOG NAME: None ')
        self.catlab.config(font=('Comic Sans',15,'bold'))
        self.idlab = tk.Label(root,text=f'CLASSIFIER NAME: None')
        self.idlab.config(font=('Comic Sans',15,'bold'))
        self.cmlab = tk.Label(root,text='')
        self.cmlab.config(font=('Comic Sans',15,'bold'))
        
        canvas1.create_window(500,80,window=self.idlab)
        canvas1.create_window(500,100,window=self.cubelab)
        canvas1.create_window(500,120,window=self.catlab)
        canvas1.create_window(500,140,window=self.cmlab)

        self.nextbutt = tk.Button(root,text='      Next      ',command=self.next_LAE,font=('Arial',15,'bold'),state='disabled')
        self.backbutt = tk.Button(root,text='      Back      ',command=self.last_LAE,font=('Arial',15,'bold'),state='disabled')
        self.savebutt = tk.Button(root,text='      Save      ',command=self.save_output,font=('Arial',15,'bold'),state='disabled')

        LAElab = tk.Label(root,text='Is it a galaxy?')
        LAElab.config(font=('Comic Sans',15,'bold'))
        self.LAEdec = tk.StringVar(root)
        self.LAEdec.set('  No  ')
        LAEsel = tk.OptionMenu(root,self.LAEdec,' Yes  ','  No  ','Unsure')

        self.commbutt = tk.Button(root,text=' Comment? ',command=self.add_comment,font=('Arial',15,'bold'),state='disabled')
        self.comm = 'none'
        self.fspcbutt = tk.Button(root,text=' Full Spectrum ',command=self.full_spectrum,font=('Arial',15,'bold'),state='disabled')

        canvas1.create_window(350,170,window=LAElab)
        canvas1.create_window(450,170,window=LAEsel)
        canvas1.create_window(540,170,window=self.commbutt)
        canvas1.create_window(650,170,window=self.fspcbutt)
        
        canvas1.create_window(400,200,window=self.nextbutt)
        canvas1.create_window(500,200,window=self.backbutt)
        canvas1.create_window(600,200,window=self.savebutt)

        bdcheck = np.random.randint(0,51,1)
        if bdcheck == 1:
            self.fig = make_bad_dudes()
        else:
            self.fig = make_fig()
        self.plot=FigureCanvasTkAgg(self.fig,master=root)
        self.plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

    def load_prev(self):
        prev_file = tk.filedialog.askopenfilename(filetypes=[('Classifications','*.dat')])
        pvfnm = prev_file
        prev_file = open(prev_file,'r')
        for i in range(2): l = prev_file.readline()
        # get cube name 
        self.cube_name = l.split(' ')[-1][:-1]
        self.cul = self.cube_name.split('/')[-1]
        self.cubelab.config(text=' '*250)
        self.cubelab.config(text=f'CUBE NAME: {self.cul}')

        # get catalog name
        l = prev_file.readline()
        self.cat_name = l.split(' ')[-1][:-1]
        self.cal = self.cat_name.split('/')[-1]
        self.catlab.config(text=' '*250)
        self.catlab.config(text=f'CATALOG NAME: {self.cal}')

        # get classifier name
        l = prev_file.readline()
        self.il = l.split(' ')[-1][:-1]
        self.idlab.config(text=' '*250)
        self.idlab.config(text=f'CLASSIFIER NAME: {self.il}')
        head_done = False
        while not head_done:
            l = prev_file.readline()
            if 'Galaxy?' in l:
                head_done = True
            
        ls = prev_file.readlines()
        for i in range(int(len(ls)/2.)):
            tid = ls[(i*2)+1].split()[0]
            self.prevs.append(str(tid))

        self.prev = True
        self.prevfile = pvfnm
        self.relbutt['state'] = 'disabled'
        self.button0['state'] = 'disabled'
        self.button3['state'] = 'normal'
        
    def enter_ID(self):
        self.button1['state'] = 'normal'
        self.il = tk.simpledialog.askstring('Who Are You?','Enter Classifier ID, No Spaces')
        self.idlab.config(text=' '*250)
        self.idlab.config(text=f'CLASSIFIER NAME: {self.il}')
        if len(self.il.split()) > 1:
            tk.messagebox.showinfo('!!!','No Spaces in Classifier Name')
            self.idlab.config(text='CLASSIFIER NAME: None')
            self.button1['state'] = 'disabled'
        else:
            pass
        
    def get_cube(self):
        self.cube_name = tk.filedialog.askopenfilename(filetypes=[('FITS files','*.fits')])
        self.cul = self.cube_name.split('/')[-1]
        self.cubelab.config(text=' '*250)
        self.cubelab.config(text=f'CUBE NAME: {self.cul}')
        self.button2['state'] = 'normal'

    def get_cat(self):
        self.cat_name = tk.filedialog.askopenfilename(filetypes=[('LSDcat files','*.cat')])
        self.cal = self.cat_name.split('/')[-1]
        self.catlab.config(text=' '*250)
        self.catlab.config(text=f'CATALOG NAME: {self.cal}')
        self.button3['state'] = 'normal'

    def get_next_good(self):
        fl= 0
        while fl == 0:
            if self.index < self.catalog.shape[0]:
                tind = self.dorder[self.index]
                idt = str(int(self.catalog[tind,0]))
                # If reloading, check if currennt object in previous classifications
                if idt in self.prevs:
                    self.index+=1
                else:
                
                    crds= [float(self.catalog[tind,_]) for _ in [2,3,4]]

                    # Check if object still in current minicube:
                    minz= np.argmin(np.abs(self.zcents-crds[2]))
                    if minz != self.cube_num:
                        self.cube_num = minz
                        print(self.cube_num)
                        self.data_cube = LAEs.MAGPI_LAE_Check(f'./tmp_cubes/cube_{self.cube_num}.fits')
                        print(self.data_cube.wav_ind)
                        

                    ncrds = [crds[0],crds[1],crds[2]-self.zstrt[self.cube_num]]
                    self.data_cube.Check_Edge(ncrds)
            
                    if self.data_cube.good:
                        fl=1
                    else:
                        self.index+=1

            else:
                zfg = make_zanac()
                self.plot.get_tk_widget().pack_forget()
                plt.close('all')
                self.plot = FigureCanvasTkAgg(zfg, root) 
                self.plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
                tk.messagebox.showinfo('CONGRATULATIONS!',f'You classified them all!')
                self.done = True
                self.save_output()
                
                fl = 2

        if fl == 2:
            root.quit()
        self.good_indices.append(tind)
        self.current_coords = ncrds
        
    def update_plot(self):
        tind = self.dorder[self.index]
        idt = str(self.catalog[tind,0])
        IDt = str(self.catalog[tind,1])
        
        self.plot.get_tk_widget().pack_forget()
        plt.close('all')
        self.fig = self.data_cube.Single_Plot(self.current_coords,idt,IDt)
        self.plot = FigureCanvasTkAgg(self.fig, root) 
        self.plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
    
    def start_class(self):
        self.button0['state']  = 'disabled'
        self.button1['state']  = 'disabled'
        self.button2['state']  = 'disabled'
        self.button3['state']  = 'disabled'
        self.nextbutt['state'] = 'normal'
        self.backbutt['state'] = 'normal'
        self.savebutt['state'] = 'normal'
        self.commbutt['state'] = 'normal'
        self.fspcbutt['state'] = 'normal'

        # CLIP CUBE:
        self.zcents,self.zstrt = MC(self.cat_name,self.cube_name)
        
        self.cube_num = 0
        self.data_cube = LAEs.MAGPI_LAE_Check(f'./tmp_cubes/cube_{self.cube_num}.fits')
        self.catalog   = np.loadtxt(self.cat_name)
        self.dorder = np.argsort(self.catalog[:,4])
        
        self.get_next_good()
        self.update_plot()

    def add_comment(self):
        combox=self.combox= tk.Tk()
        combox.title('Enter Comment')
        lab    = tk.Label(combox,text='Comment:').pack(side=tk.LEFT)
        self.ce = tk.Entry(combox,width=50)
        self.ce.pack(side=tk.LEFT)
        butt   = tk.Button(combox,text='   Submit   ',command=self.comclean).pack(side=tk.LEFT)

    def full_spectrum(self):
        tmp_cube = LAEs.MAGPI_LAE_Check(self.cube_name,data_ind=1)
        FSW(self.cube_name,[self.current_coords[0],self.current_coords[1],self.current_coords[2]+self.zstrt[self.cube_num]])

    def comclean(self):
        self.comm=self.ce.get()
        self.cmlab.config(text=f'COMMENT: {self.comm}',fg='red')
        self.combox.destroy()
        
    def next_LAE(self):
        sel_dic = {' Yes  ':1,'  No  ':2,'Unsure':3}
        tind = self.dorder[self.index]
        self.output[str(tind)] = {'Class':sel_dic[self.LAEdec.get()],'Comm':self.comm}
        self.comm = 'none'
        self.cmlab.config(text=' '*250)
        self.index+=1
        self.get_next_good()
        self.update_plot()

    def last_LAE(self):
        self.index -= 1
        self.good_indices = self.good_indices[:-1]
        self.get_next_good()
        self.update_plot()

    def save_output(self):
        if self.done:
            sel_dic = {' Yes  ':1,'  No  ':2,'Unsure':3}
            tind = self.dorder[self.index-1]
            self.output[str(tind)] = {'Class':sel_dic[self.LAEdec.get()],'Comm':self.comm}
        
        self.saved = True
        cu = self.cul.split('.')[0]
        ca = self.cal.split('.')[0]
        
        out_file_name = tk.simpledialog.askstring('Save Classifications','Enter File Name:                                                     ',initialvalue=f'{cu}_{ca}_{self.il}_class.dat')

        if self.prev:
            if out_file_name == self.prevfile.split('/')[-1]:
                print('Overwriting previous')
                copyfile(self.prevfile,'./tmp.dat')
                self.prevfile = './tmp.dat'
            
        out_print = open(out_file_name,'w')

        if self.prev:
            prev_file = open(self.prevfile,'r')
            lines = prev_file.readlines()
            for line in lines:
                out_print.write(line)
            cat_print = open(self.cat_name,'r')
            head_done = False
            while not head_done:
                tm = cat_print.readline()
                if 'DETSN_MAX' in tm:
                    head_done = True
            lines = cat_print.readlines()
                
        else:
            cat_print = open(self.cat_name,'r')
            out_print.write('# MAGPI LAE SCANNER OUTPUTS:\n')
            out_print.write(f'# Input cube = {self.cube_name}\n')
            out_print.write(f'# Input catalog = {self.cat_name}\n')
            out_print.write(f'# Classifier = {self.il}\n')
            out_print.write(f'#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n')
            head_done = False
            while not head_done:
                line = cat_print.readline()
                out_print.write(line)
                if 'DETSN_MAX' in line:
                    head_done = True
            out_print.write('#	 8: Galaxy? (y:1,n:2,?:3)\n')
            lines = cat_print.readlines()

        for k in self.output.keys():
            tclass,tcomm = self.output[k]['Class'],self.output[k]['Comm']
            out_print.write(f'# Comment: {tcomm}\n')
            out_print.write(lines[int(k)][:-1]+f'   {tclass}\n')

        out_print.close()
        tk.messagebox.showinfo('!!!',f'Output saved as {out_file_name}')
        self.make_quit_dialog()
        
    def make_quit_dialog(self):
        if not self.saved:
            tk.messagebox.showinfo('!!!',f'Classifications not saved!')
        
        quit_dialog = tk.Tk()
        quit_dialog.title('Leaving so soon?')
        canvas2 = tk.Canvas(quit_dialog,width=400,height=60)
        canvas2.pack()

        qlab = tk.Label(quit_dialog,text='Quit or dont quit, that is the question')
        qlab.config(font=('Comic Sans',15, 'bold'))
        canvas2.create_window(200,10,window=qlab)

        but1 = tk.Button(quit_dialog, text='     Quit      ',command=root.quit,font=('Arial',15,'bold'))
        but2 = tk.Button(quit_dialog, text='   Dont Quit   ',command=quit_dialog.destroy,font=('Arial',15,'bold'))

        canvas2.create_window(100,40,window=but1)
        canvas2.create_window(300,40,window=but2)


if __name__ == '__main__':
    
    root=tk.Tk()
    root.title('MAGPI LAE SCANNER v0.1')
    app=MAGPI_LAE_Scanner(master=root)
    app.mainloop()
