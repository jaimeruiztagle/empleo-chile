*==============================================================================
* descarga_ene.do  —  Bases ENE (INE Chile), trimestres móviles 2011–2026 y
*                      bases anualizadas 2011–2025, formato Stata.
* URLs verificadas el 06-11-2026. Salta los archivos que ya existen, así que
* se puede correr de nuevo para completar o para agregar trimestres nuevos.
*==============================================================================
clear all
set more off

global ene  "/Users/jaime/Library/CloudStorage/Dropbox/JRT/Trabajo/BBDD Encuestas/ENE"
global root "https://www.ine.gob.cl/docs/default-source/ocupacion-y-desocupacion/bbdd"

local ano_ini = 2011
local ano_fin = 2026

local s1 def
local s2 efm
local s3 fma
local s4 mam
local s5 amj
local s6 mjj
local s7 jja
local s8 jas
local s9 aso
local s10 son
local s11 ond
local s12 nde

capture mkdir "$ene/trimestrales"
capture mkdir "$ene/anuales"
local ok = 0
local nd = 0

* --- Trimestres móviles -------------------------------------------------------
forvalues a = `ano_ini'/`ano_fin' {
    capture mkdir "$ene/trimestrales/`a'"
    forvalues m = 1/12 {
        local mm : display %02.0f `m'
        local f "ene-`a'-`mm'-`s`m''.dta"
        capture confirm file "$ene/trimestrales/`a'/`f'"
        if !_rc continue
        capture copy "$root/`a'/stata/`f'" "$ene/trimestrales/`a'/`f'"
        if _rc {
            display as text "  no publicado aún: `f'"
            local ++nd
        }
        else {
            display as result "OK `f'"
            local ++ok
        }
    }
}

* --- Bases anualizadas (usar fact_anual) --------------------------------------
forvalues a = `ano_ini'/`=`ano_fin'-1' {
    local f "ano-`a'.dta"
    capture confirm file "$ene/anuales/`f'"
    if !_rc continue
    capture copy "$root/bases-anuales/stata/`f'" "$ene/anuales/`f'"
    if _rc {
        display as text "  no publicado aún: `f'"
        local ++nd
    }
    else {
        display as result "OK `f'"
        local ++ok
    }
}

display _n as result "Descargados ahora: `ok'   |   No disponibles: `nd'"
* Al 06-11-2026 el último trimestre publicado es jul-sep 2026 (ene-2026-08-jas);
* los meses 09-12 de 2026 aparecerán como "no publicado aún".
