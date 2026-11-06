# Gráficos de tasa de ocupación ENE, promedio móvil 6 meses (fecha = último mes de la ventana)
import pandas as pd, os, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=os.path.dirname(os.path.abspath(__file__))
o=pd.read_csv(os.path.join(R,'tasa_ocupacion_pm6_sexo_edad_2010_2026.csv'))
t=(o.ano-2010)*12+o.mes_central-1+1      # último mes de la ventana
o['x']=2010+t//12+(t%12)/12
INK,INK2,GRID,BG='#2b2b29','#6b6a63','#e6e5e0','#fcfcfb'
TR=['15-24','25-34','35-44','45-54','55-64','65+']
CT=dict(zip(TR,['#2a78d6','#eb6834','#1baf7a','#eda100','#e87ba4','#008300']))
CS={'Ambos':INK,'Hombres':'#2a78d6','Mujeres':'#eb6834'}
plt.rcParams.update({'font.size':10,'axes.edgecolor':GRID,'axes.labelcolor':INK2,'xtick.color':INK2,'ytick.color':INK2,
                     'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':BG,'axes.facecolor':BG})
def base(ax,ylabel=True):
    ax.axvspan(2020+2/12,2022,color='#f0efea',zorder=0,lw=0)
    ax.grid(axis='y',color=GRID,lw=.8); ax.set_axisbelow(True)
    ax.set_xlim(2010,2027.6); ax.set_xticks(range(2010,2027,2))
    if ylabel: ax.set_ylabel('% de la población de 15 años y más')
def labels(ax,items,minsep):
    # etiquetas directas al final, separadas para no chocar
    items=sorted(items,key=lambda z:z[1]); ys=[]
    for i,(lab,y,c,x) in enumerate(items):
        yy=y if not ys else max(y,ys[-1]+minsep); ys.append(yy)
        ax.annotate(f'{lab}  {y:.1f}'.replace('.',','),(x,y),xytext=(x+.25,yy),color=INK,fontsize=9,va='center',
                    arrowprops=dict(arrowstyle='-',color=c,lw=1) if abs(yy-y)>.3 else None)
def fig(series,title,fn,minsep,panels=None):
    n=len(panels) if panels else 1
    f,axs=plt.subplots(1,n,figsize=(7.5*n if n>1 else 9,5.2),sharey=True,squeeze=False); axs=axs[0]
    for k,ax in enumerate(axs):
        base(ax,k==0); its=[]
        for lab,q,c in series(panels[k] if panels else None):
            ax.plot(q.x,q.tasa,color=c,lw=2,label=lab,solid_capstyle='round')
            its.append((lab,q.tasa.iloc[-1],c,q.x.iloc[-1]))
        labels(ax,its,minsep)
        if panels: ax.set_title(panels[k],loc='left',color=INK,fontsize=11,fontweight='bold')
        ax.text(2020.2,ax.get_ylim()[1],'Pandemia',color=INK2,fontsize=8,va='top')
    axs[0].legend(frameon=False,loc='upper left',ncol=len(its) if len(its)<=3 else 6,fontsize=9,bbox_to_anchor=(0,-.08))
    f.suptitle(title,x=.01,ha='left',color=INK,fontsize=13,fontweight='bold')
    f.text(.01,.005,'Fuente: INE, ENE (microdatos trimestres móviles, factor fact_cal). Promedio móvil de 6 meses: trimestres t y t−3 agregados; fecha = último mes de la ventana.\nTasa de ocupación = ocupados / población de 15 años y más.',fontsize=7.5,color=INK2,va='bottom')
    f.tight_layout(rect=(0,.05,1,.95)); f.savefig(os.path.join(R,fn),dpi=170); plt.close(f)
sel=lambda s,tr:o[(o.sexo==s)&(o.tramo==tr)]
fig(lambda _:[(s,sel(s,'15+'),CS[s]) for s in ['Ambos','Hombres','Mujeres']],
    'Tasa de ocupación, total y por sexo, 2010–2026','tasa_ocupacion_pm6_sexo.png',2.2)
fig(lambda _:[(tr,sel('Ambos',tr),CT[tr]) for tr in TR],
    'Tasa de ocupación por tramo etario, ambos sexos, 2010–2026','tasa_ocupacion_pm6_edad.png',3.5)
fig(lambda p:[(tr,sel(p,tr),CT[tr]) for tr in TR],
    'Tasa de ocupación por tramo etario y sexo, 2010–2026','tasa_ocupacion_pm6_sexo_edad.png',3.8,panels=['Hombres','Mujeres'])
print('ok')
