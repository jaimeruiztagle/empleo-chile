import pandas as pd, numpy as np
P=pd.read_pickle('jas.pkl')
bins=[15,25,35,45,55,65,200]; lab=['15-24','25-34','35-44','45-54','55-64','65 y más']
def prep(d):
    d=d[d.edad>=15].copy()
    d['g']=pd.cut(d.edad,bins,right=False,labels=lab).astype(str)
    d['ft']=d.activ.isin([1,2]).astype(float); d['des']=(d.activ==2).astype(float); d['oc']=(d.activ==1).astype(float)
    return d
def ratio_se(d,num,den):
    # Taylor linearization for ratio, stratified clustered design, with-replacement PSUs
    w=d.fact_cal; Y=(w*d[num]).sum(); X=(w*d[den]).sum(); R=Y/X
    z=w*(d[num]-R*d[den])/X
    t=pd.DataFrame({'h':d.estrato,'c':d.conglomerado,'z':z}).groupby(['h','c']).z.sum().reset_index()
    v=0
    for h,g in t.groupby('h'):
        n=len(g)
        if n>1: v+=n/(n-1)*((g.z-g.z.mean())**2).sum()
    return R, np.sqrt(v)
rows=[]
for y,d0 in P.items():
    d=prep(d0)
    for sx,sn in [(None,'Total'),(1,'Hombres'),(2,'Mujeres')]:
        ds=d if sx is None else d[d.sexo==sx]
        for gname in ['Total']+lab:
            dg=ds if gname=='Total' else ds[ds.g==gname]
            R,se=ratio_se(dg,'des','ft')
            rows.append(dict(ano=y,sexo=sn,tramo=gname,tasa=100*R,se=100*se,
                 ocup=(dg.fact_cal*dg.oc).sum(),desoc=(dg.fact_cal*dg.des).sum(),ft=(dg.fact_cal*dg.ft).sum(),
                 n_ft=int(dg.ft.sum()),n_des=int(dg.des.sum())))
r=pd.DataFrame(rows)
w=r.pivot_table(index=['sexo','tramo'],columns='ano',values=['tasa','se','ocup','desoc'],sort=False)
out=pd.DataFrame({'tasa_2026':w[('tasa',2026)],'se_2026':w[('se',2026)],'cv_%':100*w[('se',2026)]/w[('tasa',2026)],
 'tasa_2025':w[('tasa',2025)],'var_pp':w[('tasa',2026)]-w[('tasa',2025)],
 'var_ocup_%':100*(w[('ocup',2026)]/w[('ocup',2025)]-1),'var_desoc_%':100*(w[('desoc',2026)]/w[('desoc',2025)]-1)})
n=r[r.ano==2026].set_index(['sexo','tramo'])[['n_ft','n_des']]
out=out.join(n)
pd.set_option('display.width',200)
print(out.round(2))
out.round(3).to_csv('tasa_desocupacion_sexo_edad_jas2026.csv')
# cesantes / BTPV variation by sex
for sx,sn in [(None,'Total'),(1,'H'),(2,'M')]:
    v={}
    for y,d0 in P.items():
        d=d0 if sx is None else d0[d0.sexo==sx]
        v[y]=[(d.fact_cal*(d.cae_general==k)).sum() for k in (4,5)]
    print(sn,'cesantes %.1f  btpv %.1f'%tuple(100*(v[2026][i]/v[2025][i]-1) for i in (0,1)))
