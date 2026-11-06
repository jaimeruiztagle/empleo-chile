# Tasa de ocupación (ocupados / población 15+), promedio móvil de 6 meses:
# se agregan dos trimestres móviles no traslapados (t y t-3), que cubren 6 meses exactos,
# y la tasa es la razón de los niveles sumados (mismo criterio que tasa_desocupacion_pm6).
import pandas as pd, os
R=os.path.dirname(os.path.abspath(__file__))
d=pd.read_csv(os.path.join(R,'niveles_ocupacion_sexo_edad.csv'))
d['t']=(d.ano-2010)*12+d.mes_central-1    # índice del mes central
def serie(keys):
    g=d.groupby(keys+['t'])[['poblacion','ocupados']].sum().reset_index()
    l=g.copy(); l['t']=l.t+3                 # trimestre t-3 alineado en t
    m=g.merge(l,on=keys+['t'],suffixes=('','_l'))
    m['tasa']=100*(m.ocupados+m.ocupados_l)/(m.poblacion+m.poblacion_l)
    return m[keys+['t','tasa']]
out=[]
for keys,lab in [([],'total'),(['sexo'],'sexo'),(['tramo'],'tramo'),(['sexo','tramo'],'sexo_tramo')]:
    s=serie(keys); s['grupo']=lab
    out.append(s)
o=pd.concat(out); o['sexo']=o.sexo.map({1:'Hombres',2:'Mujeres'}).fillna('Ambos'); o['tramo']=o.tramo.fillna('15+')
o['ano']=2010+o.t//12; o['mes_central']=o.t%12+1
def ventana(t):
    a=t-4; b=t+1    # meses 1..12 de ventana: de (centro-4) a (centro+1)
    f=lambda x:f"{2010+x//12}-{x%12+1:02d}"
    return f"{f(a)} a {f(b)}"
o['ventana']=o.t.map(ventana)
o=o[['ano','mes_central','ventana','sexo','tramo','tasa']].sort_values(['sexo','tramo','ano','mes_central'])
o['tasa']=o.tasa.round(3)
o.to_csv(os.path.join(R,'tasa_ocupacion_pm6_sexo_edad_2010_2026.csv'),index=False)
print(o[(o.sexo=='Ambos')&(o.tramo=='15+')].head(3)); print(o[(o.sexo=='Ambos')&(o.tramo=='15+')].tail(3)); print(len(o))
