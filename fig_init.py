import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as path_effects


def make_fig():	
    fig = plt.figure(figsize=(14,5))
    ax  = fig.add_subplot(111)
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

    font = FontProperties()
    font.set_name(np.random.choice(fonts))
    an=ax.annotate(line1,xy=(2,-1.),color=np.random.choice(cl[np.random.randint(0,7)]),fontsize=23)
    an.set_path_effects([path_effects.Stroke(linewidth=8,foreground='w'),path_effects.Normal()])

    return fig
