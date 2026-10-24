# Hallazgos — ACAD

> Volcadero de resultados, observaciones y preguntas abiertas. **No es el informe**: de acá sale el informe al final.
> Regla: cada hallazgo nuevo se agrega acá **en el momento**, con mis palabras.

---

## Datos y decisiones de limpieza

- Fuente: Yahoo Finance (`yfinance`). Período fijo: **2016-10-05 → 2026-10-05** (`start`/`end`, no `period="10y"`, porque se movía con el mercado abierto).
- 2512 días de precios → 2511 retornos (se pierde el primero por el `shift`).
- **Dos muestras distintas:**
  - ACAD sola (`returns_log["ACAD"].dropna()`) → para todo lo que describe a ACAD.
  - Las seis alineadas (`model_data`) → solo para la regresión.
- **`^IRX` rellenado con `ffill`** en días sin cotización (una tasa casi no cambia de un día al otro). **Los precios NO se rellenan** (sería inventar retornos de 0%).
- Una descarga vino incompleta (~84 días) sin dar error → por eso el chequeo de cantidad de días.

## Retorno y riesgo (`riesgo.py`)

| Métrica | Valor |
|---|---|
| Retorno total 10 años | −30,75% |
| CAGR | −3,61% |
| Volatilidad diaria | 3,91% |
| Volatilidad anual | 62,15% (MSFT: 27,66%) |
| Max drawdown | −77,18% |
| Trough | 21/06/2022 |
| Drawdown actual | −65,0% → necesita **+186%** para volver al pico de jul-2020 |
| Peor día | −45,35% (09/03/2021) = **−15,4σ** |
| Mejor día | +63,24% (09/09/2019) |
| Sharpe anual | −0,098 ⚠️ negativo → no comparable con otros activos |

- Peor día (9/3/2021) y fondo (21/6/2022) son distintos: el golpe y después **15 meses más de caída**.

## Eventos

- **09/09/2019 (+63%):** resultados preliminares positivos de fase 3 de Nuplazid para psicosis por demencia. Datos completos ~3 meses después: +19,78% más.
- **09/03/2021 (−45%):** la FDA rechaza la solicitud para ampliar Nuplazid a psicosis por cualquier demencia. Declaró "deficiencias" sin especificar. **El aviso llegó el 3, el comunicado el 9.**
- **Chequeo de filtración (3 al 8 de marzo):** todos los días dentro de ±1,7σ, el día 3 subió +1,07% → **no se observa movimiento anormal previo**. (No prueba que nadie operó con la información; prueba que no dejó huella en el precio.)
- **Tipo de riesgo:** binario, de evento, **idiosincrático** (le pasa solo a ACAD, no a un grupo de empresas).

## Distribución (`distribucion.py`)

| | Diario | Mensual |
|---|---|---|
| Skew | −1,208 | −0,469 |
| Curtosis en exceso (normal = 0) | **42,81** | **2,05** |
| Jarque-Bera | 192.388 (p = 0,0) | — |

- **Sin el peor día, la curtosis baja a 25,34** (−41%). Un día de 2511 aporta el 41% → la curtosis es frágil (eleva a la 4ª potencia).
- **Aun sin ese día, 25,3 es casi 3 veces la de MSFT (8,92)** → ACAD es estructuralmente extrema, no "normal con un evento raro".
- **No se saca el outlier:** el outlier es el riesgo.
- El skew negativo sale **en log** (peor día −0,604 vs mejor +0,490); en simple el mejor día es mayor (+63% vs −45%).
- **Mensual:** el TCL endereza el cuerpo, pero el mes de marzo 2021 (−0,64) sigue separado en el QQ-plot. El mismo evento es −15,4σ en escala diaria y −3,35σ en mensual: cambia la vara, no el evento.
- Jarque-Bera con n = 2511 rechaza casi siempre → lo informativo son los tamaños, no el p-value.
- Gráfico para el informe: QQ diario al lado del QQ mensual.

## Factores (`factores.py`) — predicciones antes de correr

- **R²: bajo**, porque el riesgo de ACAD es idiosincrático.
- **SMB: positivo**, porque ACAD es small cap.
- **HML: incierto.** Hipótesis inicial "biotech = cara" → negativo. Pero el **P/B de hoy es 2,6**, por debajo del promedio del S&P (~4–5): cayó 65% y se fue corriendo hacia value. (Ojo: es el P/B de hoy, no el de los 10 años.)

### CAPM — resultados

| | Valor |
|---|---|
| R² | **0,081** → predicción "bajo" confirmada |
| β | **0,980** (intervalo 0,851 – 1,110) |
| Correlación | **0,28** (= √R²) |
| Alpha | −0,000707 diario ≈ **−17,8% anual**, p = 0,346 → **no significativo** |
| β de Yahoo | 0,887 (5 años mensual) → **compatible** con mi intervalo |
| Curtosis de los residuos | **57,4** |

- El mercado explica únicamente el **8%** de los movimientos de ACAD; el **92%** restante es propio de la acción.
- Con β = 0,98 se mueve parecido al mercado, **pero únicamente en la parte que el mercado explica**. β mide cuánto la arrastra el mercado; R² mide qué parte de todo su movimiento es ese arrastre.
- ACAD es tan volátil (62% vs ~18% del mercado) que, aunque su correlación sea baja (0,28), alcanza para un β ≈ 1: β = corr × σ_ACAD / σ_mercado ≈ 0,28 × 3,4.
- El alpha no significativo **no quiere decir que haya sido mala suerte**: el ruido es tan grande que no se puede distinguir el alpha de cero.
- La curtosis de 57 es **de los residuos** (ACAD sin el mercado), más alta que la de los retornos (42,8): al sacar el mercado, los días normales se achican y los extremos (FDA) quedan enteros. Confirma que el riesgo extremo es **propio de ACAD** (idiosincrático). Colas gordas para los dos lados.
- β ≈ 1 **no significa** "tan riesgosa como el mercado": el riesgo total es 3 veces mayor. Solo en una cartera muy diversificada lo que importa es el β.

### Rentabilidad exigida (fórmula de la facultad con mi β)

$E[R] = R_f + \beta (E[R_m]-R_f)$ con β = 0,98, Rf y prima de mercado promedio 2016–2026 → **14,12% anual**.

| | |
|---|---|
| Exigida por el CAPM | **14,12%** |
| Real (CAGR) | **−3,61%** |
| Diferencia | **−17,73%** ≈ alpha del CAPM anualizado (**−17,8%**) |

- **El alpha es exactamente esta diferencia**: lo que rindió por encima o por debajo de lo que el CAPM le exigía. Dos caminos, el mismo número.
- **p = 0,346 → no se puede afirmar ni negar** que ACAD rinda sistemáticamente por debajo. La diferencia **ocurrió** (es un hecho del pasado); lo que no se puede saber es si es **estructural** o ruido.
- **Matices:** (1) el 14,12% está inflado por una década muy buena del SPY; con una prima de mercado prospectiva de ~5% (Damodaran) daría ~9%. (2) Es "lo mínimo" solo para un inversor **diversificado**: el CAPM no paga el riesgo propio de ACAD.

### Fama-French 3 — resultados

| | Coef | SE | IC 95% | ¿Significativo? |
|---|---|---|---|---|
| R² (ajustado) | **0,118** (0,117) | | | |
| Alpha | −0,000469 diario ≈ **−11,8% anual** | 18,5% anual | cruza el 0 | **No** (p = 0,523) |
| Rm | **0,790** | 0,072 | 0,650 – 0,931 | Sí |
| SMB | **1,113** | 0,108 | 0,900 – 1,325 | Sí |
| HML | **−0,283** | 0,101 | −0,482 – −0,084 | Sí (p = 0,005) |
| Curtosis de los residuos | **63,1** (CAPM: 57,4) | | | |

- Con los tres factores se explica el **11,8%** de los movimientos; el resto es propio de ACAD. SMB y HML suman **3,7 puntos** sobre el CAPM (8,1%).
- **No se puede repartir el 11,8% entre los factores**: están correlacionados entre sí.
- **β del mercado baja de 0,98 a 0,79** porque en el CAPM el mercado se llevaba también la parte de SMB que viaja con él (efecto parcial). **Verificado, la cuenta da exacta:**

| Camino (mercado +1%) | Cuenta | A ACAD le llega |
|---|---|---|
| Directo | 0,7903 | 0,790% |
| Vía SMB (δ = +0,109) | 1,1127 × 0,1094 | +0,122% |
| Vía HML (δ = −0,241) | −0,2831 × −0,2407 | +0,068% |
| **Total = β del CAPM** | | **0,980%** ✓ |

  Cuando el mercado sube, las chicas les ganan a las grandes (δ_SMB +) y las caras les ganan a las baratas (δ_HML −). ACAD va con las chicas y con las caras, así que **los dos caminos indirectos suman**.
- **SMB +1,11 → predicción confirmada.** Cuando las chicas le ganan a las grandes por 1%, ACAD gana 1,11% extra (con mercado y HML quietos).
- **HML −0,28, significativo (IC −0,48 a −0,08):** cuando las acciones caras le ganan a las baratas, a ACAD le va mejor. En estos 10 años **se comportó como growth**.
- **No contradice el P/B de 2,6:** el P/B es una foto **de hoy** (después de caer 65%). En 2020, a $57, era cara (P/B ≈ 7, aproximado). La regresión mide el **promedio de 10 años**. Además, HML mide **cómo se mueve el precio**, no qué dice el balance.
- ⚠️ **Con errores robustos (HC3), HML deja de ser significativo** → ver "FF3 con HC3".
- **Predicción para `estabilidad.py`:** si fue cara al principio y barata al final, el HML de la segunda mitad debería ser **menos negativo** que el de la primera.
- **Alpha:** no se puede distinguir de cero. Con este ruido (SE ≈ 18,5% anual), para que un −11,8% fuera significativo harían falta **~10 veces más datos ≈ 100 años**. En la práctica, con ACAD nunca se va a poder saber.
- Curtosis de residuos sube a 63: el modelo explica mejor los días normales y el 9/3/2021 queda entero → mismo mecanismo que en el CAPM.

### FF3 con errores robustos (HC3)

Mismos coeficientes; cambian solo los SE (los normales suponen que el ruido es igual de grande todos los días, y en ACAD no lo es).

| | SE normal | SE HC3 | Cambio | p HC3 | IC 95% HC3 | ¿Sigue significativo? |
|---|---|---|---|---|---|---|
| Rm | 0,072 | 0,079 | ×1,1 | 0,000 | 0,636 – 0,944 | Sí |
| SMB | 0,108 | 0,141 | ×1,3 | 0,000 | 0,837 – 1,388 | Sí |
| HML | 0,101 | **0,184** | **×1,8** | **0,124** | **−0,643 – 0,077** | **No** |

- **HML:** t pasa de −2,79 a −1,54 (−0,2831 / 0,184). El IC ahora cruza el 0.
- **Lo que sobrevive:** Rm y SMB siguen siendo significativos con el error robusto → **ACAD se mueve como una small cap**: es el hallazgo de factores más sólido.
- **Lo que no:** HML, con p = 0,124 (> 0,05) y el IC cruzando el 0, **no se puede distinguir de cero**. El signo negativo coincide con "growth", pero **no alcanza como evidencia**: se retira la afirmación "se comportó como growth".
- **Hipótesis (sin verificar):** los días más extremos de ACAD coincidieron con días de movimientos grandes de HML, y no del mercado. Se podría comprobar mirando Rm y HML en desvíos en los 10 residuos más grandes.

## Preguntas abiertas


- ¿Las fechas de los anuncios (FDA, resultados de fase 3) eran públicas de antemano?
- ¿El HML cambia de signo entre la primera y la segunda mitad del período? (→ `estabilidad.py`)
