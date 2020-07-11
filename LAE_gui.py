import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import warnings

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import LAE_scanner as LAEs
from fig_init import make_fig

warnings.filterwarnings("ignore")

class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.output = {}
        self.index=0
        self.good_indices=[]
        self.createWidgets()

    def createWidgets(self):
        canvas1 = tk.Canvas(root,width=1000,height=160)
        canvas1.pack()

        label1 = tk.Label(root,text='MAGPI    LAE    SCANNER   beta')
        label1.config(font=('Comic Sans',30, 'bold'))
        canvas1.create_window(500,20,window=label1)

        self.button0 = tk.Button(root, text='    --Enter Classifier--    ',command=self.enter_ID,font=('Arial',15,'bold'))
        self.button1 = tk.Button(root, text='      --Select Cube--      ',command=self.get_cube,font=('Arial', 15, 'bold'),state='disabled') 
        self.button2 = tk.Button(root, text='     --Select Catalog--     ', command=self.get_cat, font=('Arial', 15, 'bold'),state='disabled')
        self.button3 = tk.Button(root, text='   --Start Classifying--   ', command=self.start_class, font=('Arial', 15, 'bold'),state='disabled')
        self.button4 = tk.Button(root, text='    --Exit Application--    ', command=root.destroy, font=('Arial', 15, 'bold'))

        canvas1.create_window(100, 50, window=self.button0)
        canvas1.create_window(300, 50, window=self.button1)
        canvas1.create_window(500, 50, window=self.button2)
        canvas1.create_window(700, 50, window=self.button3)
        canvas1.create_window(900, 50, window=self.button4)

        self.cubelab = tk.Label(root,text=f'   CUBE NAME: None   ')
        self.cubelab.config(font=('Comic Sans',15,'bold'))
        self.catlab = tk.Label(root,text=f'  CATALOG NAME: None ')
        self.catlab.config(font=('Comic Sans',15,'bold'))
        self.idlab = tk.Label(root,text=f'CLASSIFIER NAME: None')
        self.idlab.config(font=('Comic Sans',15,'bold'))
        
        canvas1.create_window(500,80,window=self.idlab)
        canvas1.create_window(500,100,window=self.cubelab)
        canvas1.create_window(500,120,window=self.catlab)

        self.nextbutt = tk.Button(root,text='      Next      ',command=self.next_LAE,font=('Arial',15,'bold'),state='disabled')
        self.backbutt = tk.Button(root,text='      Back      ',command=self.last_LAE,font=('Arial',15,'bold'),state='disabled')
        self.savebutt = tk.Button(root,text='      Save      ',command=self.save_output,font=('Arial',15,'bold'),state='disabled')

        LAElab = tk.Label(root,text='Is it an LAE?')
        LAElab.config(font=('Comic Sans',15,'bold'))
        self.LAEdec = tk.StringVar(root)
        self.LAEdec.set('No')
        LAEsel = tk.OptionMenu(root,self.LAEdec,'No','Yes')

        CONlab = tk.Label(root,text='Confidence?')
        CONlab.config(font=('Comic Sans',15,'bold'))
        self.CONdec = tk.StringVar(root)
        self.CONdec.set('1')
        CONsel = tk.OptionMenu(root,self.CONdec,'1','2','3','4','5')

        canvas1.create_window(200,150,window=LAElab)
        canvas1.create_window(280,150,window=LAEsel)
        canvas1.create_window(385,150,window=CONlab)
        canvas1.create_window(460,150,window=CONsel)
        canvas1.create_window(580,150,window=self.nextbutt)
        canvas1.create_window(680,150,window=self.backbutt)
        canvas1.create_window(780,150,window=self.savebutt)

        fig = make_fig()
        self.plot=FigureCanvasTkAgg(fig,master=root)
        self.plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

    def enter_ID(self):
        self.il = tk.simpledialog.askstring('Who Are You?','Classifier ID')
        self.idlab.config(text=' '*250)
        self.idlab.config(text=f'CLASSIFIER NAME: {self.il}')
        self.button1['state'] = 'normal'
        
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
            idt = str(self.catalog[self.index,0])
            crds= [float(self.catalog[self.index,2]),float(self.catalog[self.index,3]),float(self.catalog[self.index,4])]
            self.data_cube.Check_Edge(crds)
            
            if self.data_cube.good:
                fl=1
            else:
                self.index+=1

        self.good_indices.append(self.index)
        
    def update_plot(self):
        
        idt = str(self.catalog[self.index,0])
        crds= [float(self.catalog[self.index,2]),float(self.catalog[self.index,3]),float(self.catalog[self.index,4])]
        
        figure1 = self.data_cube.Single_Plot(crds,idt)
        self.plot.get_tk_widget().pack_forget()
        self.plot = FigureCanvasTkAgg(figure1, root) 
        self.plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
    
    def start_class(self):
        self.button0['state']  = 'disabled'
        self.button1['state']  = 'disabled'
        self.button2['state']  = 'disabled'
        self.nextbutt['state'] = 'normal'
        self.backbutt['state'] = 'normal'
        self.savebutt['state'] = 'normal'

        self.data_cube = LAEs.MAGPI_LAE_Check(self.cube_name)
        self.catalog   = np.loadtxt(self.cat_name)
        
        self.get_next_good()
        self.update_plot()

    def next_LAE(self):
        self.output[str(self.index)] = [self.LAEdec.get(),self.CONdec.get()]
        self.index+=1
        self.get_next_good()
        self.update_plot()

    def last_LAE(self):
        self.index = self.good_indices[-2]
        self.good_indices = self.good_indices[:-1]
        self.update_plot()

    def save_output(self):
        cu = self.cul.split('.')[0]
        ca = self.cal.split('.')[0]
        
        cat_print = open(self.cat_name,'r')
        out_print = open(f'{cu}_{ca}_{self.il}_class.dat','w')
        out_print.write('# MAGPI LAE SCANNER OUTPUTS:\n')
        out_print.write(f'# Input cube = {self.cul}\n')
        out_print.write(f'# Input catalog = {self.cal}\n')
        out_print.write(f'# Classifier = {self.il}\n')
        out_print.write(f'#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n')
        for i in range(17):
                line = cat_print.readline()
                out_print.write(line)
        out_print.write('#	 8: LAE?\n')
        out_print.write('#   9: Confidence\n')
        line = cat_print.readline()
        
        for k in self.output.keys():
            while line.split()[0] != k: line=cat_print.readline()
            out_print.write(line[:-1]+f'   {self.output[k][0]}   {self.output[k][1]}\n')
        

root=tk.Tk()
app=Application(master=root)
app.mainloop()
