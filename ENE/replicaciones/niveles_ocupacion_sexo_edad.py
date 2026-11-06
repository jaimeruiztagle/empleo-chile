# Niveles por trimestre móvil ENE (fact_cal): población 15+ y ocupados, por sexo x tramo etario.
# Insumo para la tasa de ocupación (ocupados / población 15+). Incremental: salta archivos ya procesados.
import pyreadstat, glob, os, time, csv, numpy as np
ENE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out=os.path.join(ENE,'replicaciones','niveles_ocupacion_sexo_edad.csv')
done=set()
if os.path.exists(out):
    with open(out) as f: done={r['archivo'] for r in csv.DictReader(f)}
files=sorted(glob.glob(os.path.join(ENE,'trimestrales','*','ene-*.dta')))
cuts=[15,25,35,45,55,65,200]; labs=['15-24','25-34','35-44','45-54','55-64','65+']
new=not os.path.exists(out); t0=time.time()
with open(out,'a',newline='') as f:
    w=csv.writer(f)
    if new: w.writerow(['archivo','ano','mes_central','sexo','tramo','poblacion','ocupados'])
    for p in files:
        fn=os.path.basename(p)
        if fn in done: continue
        if time.time()-t0>150: break
        d,_=pyreadstat.read_dta(p,usecols=['sexo','edad','activ','fact_cal'])
        d=d[d.edad>=15].copy()
        d['tramo']=np.digitize(d.edad,cuts[1:-1])
        d['oc']=d.fact_cal*(d.activ==1)
        g=d.groupby(['sexo','tramo']).agg(pob=('fact_cal','sum'),oc=('oc','sum')).reset_index()
        for r in g.itertuples():
            w.writerow([fn,fn[4:8],int(fn[9:11]),int(r.sexo),labs[int(r.tramo)],round(r.pob),round(r.oc)])
        f.flush()
print(len({l.split(',')[0] for l in open(out)})-1,'de',len(files))
