# Cambio en tasa de ocupación: abr-sep 2019 (pre pandemia y pre estallido) vs abr-sep 2026, pm6
import pandas as pd, os
R=os.path.dirname(os.path.abspath(__file__))
o=pd.read_csv(os.path.join(R,'tasa_ocupacion_pm6_sexo_edad_2010_2026.csv'))
o=o[o.ventana.isin(['2019-04 a 2019-09','2026-04 a 2026-09'])]
t=o.pivot_table(index=['sexo','tramo'],columns='ano',values='tasa').reset_index()
t['cambio_pp']=t[2026]-t[2019]; t['cambio_pct']=100*t.cambio_pp/t[2019]
# niveles de población para contexto (cambio de composición)
n=pd.read_csv(os.path.join(R,'niveles_ocupacion_sexo_edad.csv'))
n=n[n.archivo.isin(['ene-2019-05-amj.dta','ene-2019-08-jas.dta','ene-2026-05-amj.dta','ene-2026-08-jas.dta'])]
n['sexo']=n.sexo.map({1:'Hombres',2:'Mujeres'})
def niv(df):
    a=df.groupby(['ano','sexo','tramo'])[['poblacion','ocupados']].sum()/2
    b=df.groupby(['ano','tramo'])[['poblacion','ocupados']].sum()/2; b['sexo']='Ambos'; b=b.reset_index().set_index(['ano','sexo','tramo'])
    a=pd.concat([a,b]).reset_index()
    tot=a.groupby(['ano','sexo'])[['poblacion','ocupados']].sum().reset_index(); tot['tramo']='15+'
    return pd.concat([a,tot])
v=niv(n).pivot_table(index=['sexo','tramo'],columns='ano',values='ocupados').reset_index()
v['d_ocup_miles']=(v[2026]-v[2019])/1000
t=t.merge(v[['sexo','tramo','d_ocup_miles']],on=['sexo','tramo'])
t.columns=['sexo','tramo','tasa_2019','tasa_2026','cambio_pp','cambio_pct','cambio_ocupados_miles']
t=t.round(2); t.to_csv(os.path.join(R,'cambio_tasa_ocupacion_2019_2026.csv'),index=False)
print(t.to_string())
