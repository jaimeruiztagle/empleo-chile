# ENE — Encuesta Nacional de Empleo (INE Chile)

Descargado desde ine.gob.cl el 06-11-2026. Serie vigente desde ene-mar 2010.

- `trimestrales/AAAA/ene-AAAA-NN-abc.dta` — trimestres móviles (NN = mes central; 01 = dic-ene-feb … 12 = nov-dic-ene). Factor: `fact_cal`.
- `anuales/ano-AAAA.dta` — bases anualizadas (factor `fact_anual`); ver `nota-aclaratoria.pdf`.
- `documentacion/` — libros de códigos (2010–2019 y 2020–2026), metodología, clasificadores (CIUO 08.CL, CAENES, CISO-18, CINE 2011), cuestionarios 2010–2026 y correspondencia entre versiones, metadatos, actas de comités y notas técnicas 2015–2025.
- `descarga_ene.do` — completa/actualiza las bases (salta las que ya existen).

Antes de 2010 (ENE antigua 1986–2009) no hay microdatos públicos: se solicitan en https://atencionciudadana.ine.cl/.
