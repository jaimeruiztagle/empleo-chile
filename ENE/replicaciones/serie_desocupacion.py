# Serie de tasa de desocupación (total y por sexo), trimestres móviles ENE, factor fact_cal
import pyreadstat, glob, os, time, csv
ENE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out=os.path.join(ENE,'replicaciones','serie_tasa_desocupacion.csv')
done=set()
if os.path.exists(out):
    with open(out) as f: done={r['archivo'] for r in csv.DictReader(f)}
files=sorted(glob.glob(os.path.join(ENE,'trimestrales','*','ene-*.dta')))
new=not os.path.exists(out); t0=time.time()
with open(out,'a',newline='') as f:
    w=csv.writer(f)
    if new: w.writerow(['archivo','ano','mes_central','total','hombres','mujeres','ft','desocupados'])
    for p in files:
        fn=os.path.basename(p)
        if fn in done: continue
        if time.time()-t0>140: break
        d,_=pyreadstat.read_dta(p,usecols=['sexo','activ','fact_cal'])
        d=d[d.activ.isin([1,2])]
        r=lambda x:100*(x.fact_cal*(x.activ==2)).sum()/x.fact_cal.sum()
        a,m=fn[4:8],int(fn[9:11])
        w.writerow([fn,a,m,round(r(d),3),round(r(d[d.sexo==1]),3),round(r(d[d.sexo==2]),3),round(d.fact_cal.sum()),round((d.fact_cal*(d.activ==2)).sum())])
        f.flush()
print(sum(1 for _ in open(out))-1,'de',len(files))
