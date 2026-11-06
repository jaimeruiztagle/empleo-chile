# Niveles de fuerza de trabajo y desocupados por sexo, por trimestre móvil (fact_cal)
import pyreadstat, glob, os, time, csv
ENE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out=os.path.join(ENE,'replicaciones','niveles_ft_desoc_sexo.csv')
done=set()
if os.path.exists(out):
    with open(out) as f: done={r['archivo'] for r in csv.DictReader(f)}
files=sorted(glob.glob(os.path.join(ENE,'trimestrales','*','ene-*.dta'))); new=not os.path.exists(out); t0=time.time()
with open(out,'a',newline='') as f:
    w=csv.writer(f)
    if new: w.writerow(['archivo','ano','mes_central','ft_h','des_h','ft_m','des_m'])
    for p in files:
        fn=os.path.basename(p)
        if fn in done: continue
        if time.time()-t0>150: break
        d,_=pyreadstat.read_dta(p,usecols=['sexo','activ','fact_cal']); d=d[d.activ.isin([1,2])]
        r=[]
        for s in (1,2):
            x=d[d.sexo==s]; r+= [round(x.fact_cal.sum()), round((x.fact_cal*(x.activ==2)).sum())]
        w.writerow([fn,fn[4:8],int(fn[9:11])]+r); f.flush()
print(sum(1 for _ in open(out))-1,'de',len(files))
