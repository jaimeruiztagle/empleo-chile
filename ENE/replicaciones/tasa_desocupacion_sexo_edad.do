*==============================================================================
* Tasa de desocupación por sexo y tramo de edad — ENE, trimestre móvil JAS 2026
* Replica el Boletín ENE N°336 (29-10-2026): total 9,8%; hombres 9,3%; mujeres 10,5%.
* Errores estándar por linealización (conglomerado, estrato, fact_cal).
*==============================================================================
clear all
set more off
global ene "/Users/jaime/Library/CloudStorage/Dropbox/JRT/Trabajo/BBDD Encuestas/ENE"

local per "2026-08-jas"          // cambiar para otro trimestre móvil
local yy = substr("`per'",1,4)
use sexo edad activ fact_cal estrato conglomerado using ///
    "$ene/trimestrales/`yy'/ene-`per'.dta", clear

keep if edad >= 15
gen byte ft  = inlist(activ, 1, 2)          // fuerza de trabajo
gen byte des = (activ == 2) * 100           // desocupado (x100 => tasa en %)

egen byte tramo = cut(edad), at(15 25 35 45 55 65 200) icodes
label define tramo 0 "15-24" 1 "25-34" 2 "35-44" 3 "45-54" 4 "55-64" 5 "65+"
label values tramo tramo

svyset conglomerado [pw = fact_cal], strata(estrato) singleunit(certainty)

* Tasa = media de des en la fuerza de trabajo (estimador de razón)
svy, subpop(ft): mean des
svy, subpop(ft): mean des, over(sexo)
svy, subpop(ft): mean des, over(tramo)
svy, subpop(ft): mean des, over(sexo tramo)
estat cv

* Niveles (comparar con el boletín: FT 10.282.718; ocupados 9.274.742; desocupados 1.007.976)
total ft [pw = fact_cal]
