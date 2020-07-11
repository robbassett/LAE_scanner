import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

def make_fig():	
    fig = plt.figure(figsize=(14,5))
    ax  = fig.add_subplot(111)
    bim = plt.imread(f'./images/back{np.random.randint(1,7)}.png')
    ax.imshow(bim,extent=[1,99,-1.1,1.1],aspect='auto')
    
    ax.set_xticks([])
    ax.set_yticks([])
    xx = np.arange(0,100,.01)
    cl = [['orange','goldenrod','gold','tan','olive'],
                  ['mediumpurple','plum','indigo','darkmagenta','mediumorchid'],
                  ['forestgreen','springgreen','palegreen','yellowgreen','green'],
                  ['red','maroon','salmon','sienna','lightcoral'],
                  ['steelblue','cyan','teal','turquoise','royalblue'],
                  ['yellow','darkkhaki','olivedrab','chartreuse','yellowgreen'],
                  ['gainsboro','silver','grey','dimgrey','k']]
    cis = np.random.randint(0,7,3)
    ns = np.random.randint(5,25,3)
    alphs = np.random.uniform(0.1,0.3,3)
    for i in range(ns[0]):
        xp = np.copy(xx)
        if round(i/2.) == i/2.: xp = np.flip(xp)
        ax.plot(xp,np.random.uniform(0.5,1.0)*np.tan((xx-np.random.uniform(0,100))*np.random.uniform(0.01,0.2)),'-',c=np.random.choice(cl[cis[0]]),lw=30,alpha=alphs[0])
    for i in range(ns[1]):
        ax.plot(xx,np.random.uniform(0.6,1.4)*np.sin((xx-np.random.uniform(0,100))*np.random.uniform(0.01,0.2)),'-',c=np.random.choice(cl[cis[1]]),lw=20,alpha=alphs[1])
    for i in range(ns[2]):
        ax.plot(xx,np.random.uniform(0.5,1.0)*np.cos((xx-np.random.uniform(0,100))*np.random.uniform(0.01,0.2)),'-',c=np.random.choice(cl[cis[2]]),lw=10,alpha=alphs[2])
    ax.set_xlim(1,99)
    ax.set_ylim(-1.1,1.1)

    words1 = ['ostentatious','cantankerous','roguish','flippant','irascible','precocious','erudite','sagacious','venturesome','intrepid','mettlesome','stalwart','curmudgeonly','insouciant','equanimous']
    words2 = ['overwhelm','subjugate','pulverise','marmalise','disclose','vouchsafe','expose','unmask','extricate','disinter','inundate','overburden','spellbind','encounter']
    words3 = ['dastardly','abominable','lamentable','egregious','unbearable','insufferable','greusome','diabolical','iniquitous','unscrupulous','unprincipled','dishonourable','nefarious','flagitious']

    fonts = ['Bradley Hand','Brush Script M7','Chalkduster','Oswald','Comic Sans MS','Courier New','Silom','SignPainter','Herculanum','Trattatello','Impact','Zapfino']

    line1 = f'Are you {np.random.choice(words1)} enough to {np.random.choice(words2)} the {np.random.choice(words3)} LAEs?'

    tmc1 = np.random.choice(cl[np.random.randint(0,7)])
    tmc2 = np.random.choice(cl[np.random.randint(0,7)])
    cfam = cl[np.random.randint(0,7)]

    nlines=250
    int0 = np.random.uniform(15,45)
    for i in range(nlines):
        intercept = np.random.normal(loc=int0,scale=2)
        slope     = np.random.normal(loc=0.05,scale=0.01)
        ax.plot(xx,slope*(xx-intercept),'-',c=np.random.choice(cfam),lw=.25,alpha=.4)

    cfam = cl[np.random.randint(0,7)]
    int1 = np.random.uniform(15,45)
    for i in range(nlines):
        intercept = np.random.normal(loc=int1,scale=2)
        slope     = np.random.normal(loc=-0.07,scale=0.007)
        ax.plot(xx,slope*(xx-intercept),'-',c=np.random.choice(cfam),lw=.25,alpha=.4)

    cfam = cl[np.random.randint(0,7)]
    xc = ((0.05*int0)+(0.07*int1))/(0.05+0.07)
    yc = 0.05*(xc-int0)
    nc = np.random.randint(150,250)
    szs= np.linspace(15,60,nc)
    fl = 0
    for i in range(nc):
        if i/len(szs) > 0.5 and fl == 0:
            cfam = cl[np.random.randint(0,7)]
            fl = 1
        ax.plot(xc+np.random.normal(scale=.08*i),yc+np.random.normal(scale=.005*i),'o',alpha=.15,ms=szs[i],mfc='None',mew=5,mec=np.random.choice(cfam))

    tlucha =  plt.imread(f'./images/lucha{np.random.randint(1,9)}.png')
    ax.imshow(tlucha,extent=[58,95,-1.5,1.],aspect='auto',zorder=1000)
    tLAE   = plt.imread(f'./images/LAE{np.random.randint(1,11)}.png')
    ax.imshow(tLAE,extent=[xc-10,xc+10,yc-.35,yc+.35],aspect='auto',zorder=1001)
    
    ax.axhline(y=-.8,linestyle='-',linewidth=20,color=tmc1,zorder=1002)
    ax.axhline(y=-.8,linestyle='-',linewidth=15,color=tmc2,zorder=1003)
    ax.axhline(y=-.9,linestyle='-',linewidth=10,color=tmc1,zorder=1004)
    ax.axhline(y=-1.05,linestyle='-',linewidth=5,color=tmc2,zorder=1005)
    an=ax.annotate(line1,xy=(2,-1.),color='k',fontsize=18,zorder=1006)
    an.set_path_effects([path_effects.Stroke(linewidth=12,foreground=tmc1),path_effects.Normal()])
    an=ax.annotate(line1,xy=(2,-1.),color=tmc2,fontsize=18,zorder=1007)
    an.set_path_effects([path_effects.Stroke(linewidth=5,foreground='w'),path_effects.Normal()])

    return fig
