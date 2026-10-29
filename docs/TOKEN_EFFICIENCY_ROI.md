# Token Efficiency & ROI Benchmark — Themis

Este documento describe cómo medir la eficiencia de tokens y el retorno de inversión (ROI) del protocolo de gobernanza Themis. Está pensado para equipos que quieran validar, con datos reales, si el coste de tokens de la gobernanza se compensa con los errores evitados, la trazabilidad y la reducción de retrabajo.

---

## 1. Objetivo

Cuantificar:

- **Eficiencia de tokens**: cuántos tokens de entrada/salida consume un ciclo gobernado por Themis frente a un ciclo sin gobernanza (baseline).
- **ROI de gobernanza**: si el valor de los incidentes evitados, el retrabajo reducido y la trazabilidad supera el coste en tokens del protocolo.

---

## 2. Metodología de medición

Se comparan dos escenarios sobre la misma tarea:

| Escenario | Descripción |
|-----------|-------------|
| **Baseline** | Agente LLM ejecuta la tarea directamente, sin `agent.md`, sin roles, sin `tasks.md`, sin gates. |
| **Themis** | Agente LLM ejecuta la tarea bajo el protocolo completo: PRE-FLIGHT, roles, loop de estados, Context Freeze, anti-catástrofe y archivo de bitácora. |

Para cada escenario se registra:

- `tokens_in`: tokens de entrada (prompt + contexto leído).
- `tokens_out`: tokens de salida (respuesta del modelo).
- `tokens_total`: `tokens_in + tokens_out`.
- `costo_usd`: precio según el proveedor (ej. OpenAI, Anthropic, DeepSeek, Ollama local).
- `tiempo_segundos`: duración del ciclo.
- `errores_previstos`: errores detectados por QA/Security antes de ejecutar.
- `ciclos_retrabajo`: ciclos adicionales necesarios por errores o ambigüedad.

---

## 3. Métricas de eficiencia de tokens

### 3.1 Overhead de gobernanza

```text
overhead_tokens   = tokens_total_themis - tokens_total_baseline
overhead_pct      = (overhead_tokens / tokens_total_baseline) * 100
```

Un overhead bajo (ej. < 30 %) indica que el protocolo no añade fricción tokenística desproporcionada.

### 3.2 Tokens ahorrados por Context Freeze

El Freeze Map limita la lectura a los archivos necesarios:

```text
tokens_ahorrados_freeze = tokens_estimados_sin_freeze - tokens_leidos_con_freeze
```

### 3.3 Tokens por tarea atómica

```text
tokens_por_tarea = tokens_total_themis / numero_de_tareas_atomicas
```

Comparar contra un bloque monolítico sin descomposición revela si la separación de roles y tareas reduce la repetición de contexto.

---

## 4. Métricas de ROI

### 4.1 Coste de la gobernanza

```text
costo_gobernanza_usd = tokens_total_themis * precio_por_token_del_proveedor
```

### 4.2 Valor evitado (beneficio)

```text
valor_evitado_usd =
    (incidentes_prevenidos * costo_promedio_incidente) +
    (ciclos_retrabajo_evitados * costo_por_ciclo_retrabajo) +
    valor_trazabilidad_y_auditoria
```

### 4.3 Fórmula de ROI

```text
ROI = valor_evitado_usd / costo_gobernanza_usd
```

- **ROI > 1**: la gobernanza se paga sola.
- **ROI >> 1**: la gobernanza genera ahorro neto.

### 4.4 Punto de equilibrio

```text
ciclos_hasta_equilibrio = costo_desarrollo_gobernanza / ahorro_neto_por_ciclo
```

---

## 5. Script de medición

Se incluye `scripts/token_benchmark.py`. Ejecuta ciclos de prueba en ambos escenarios, recopila métricas y genera una tabla Markdown lista para pegar en el informe.

### Requisitos

- Python 3.10+
- Acceso a un proveedor de LLM (OpenAI, Anthropic, DeepSeek, Ollama, etc.) o modo simulación.

### Uso rápido

```bash
# Modo simulación (sin API, con datos de ejemplo)
python scripts/token_benchmark.py --mode dry-run --output docs/benchmark-results.md

# Modo real con OpenAI (requiere OPENAI_API_KEY)
python scripts/token_benchmark.py --provider openai --model gpt-4o \
  --task "Crear un script de validación de JSON" \
  --output docs/benchmark-results.md
```

### Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `--mode` | `dry-run` (simulado) o `live` (llamadas reales al LLM) |
| `--provider` | `openai`, `anthropic`, `deepseek`, `ollama` |
| `--model` | Nombre del modelo (ej. `gpt-4o`, `claude-3-5-sonnet`) |
| `--task` | Tarea de prueba para ambos escenarios |
| `--output` | Archivo Markdown con los resultados |

---

## 6. Tabla de resultados esperada (ejemplo ilustrativo)

Los valores abajo son **ilustrativos** y deben reemplazarse con mediciones reales de tu entorno.

| Métrica | Baseline (sin gobernanza) | Themis (con gobernanza) | Diferencia |
|---------|---------------------------|-------------------------|------------|
| Tokens de entrada | 1.200 | 1.850 | +650 |
| Tokens de salida | 450 | 620 | +170 |
| Tokens totales | 1.650 | 2.470 | +820 |
| Overhead de gobernanza | — | — | **+49,7 %** |
| Coste por ciclo (USD) | $0,0033 | $0,0049 | +$0,0016 |
| Archivos leídos | 12 (todos) | 5 (Freeze Map) | -58 % |
| Errores detectados pre-ejecución | 0 | 2 | +2 |
| Ciclos de retrabajo | 2 | 0 | -2 |
| Tiempo por ciclo (s) | 14 | 19 | +5 s |
| Trazabilidad / auditoría | Ninguna | Completa (task-archives.md) | +100 % |

**ROI ilustrativo:**

```text
valor_evitado = (2 incidentes × $150) + (2 retrabajos × $40) + trazabilidad ($100) = $540
costo_gobernanza = $0,0049 por ciclo
ROI = 540 / 0,0049 ≈ 110.000 %
```

> Reemplaza estos números por los de tu ejecución real con `scripts/token_benchmark.py`.

---

## 7. Qué busca un experto en este benchmark

Si vas a presentar o auditar este benchmark, verifica que incluya:

### Datos obligatorios
- [ ] Tokens de entrada y salida por separado (no solo totales).
- [ ] Nombre y versión del modelo usado.
- [ ] Proveedor y precio por 1M de tokens.
- [ ] Tarea idéntica en baseline y Themis (misma complejidad).
- [ ] Número de ciclos y tareas atómicas ejecutadas.
- [ ] Errores prevenidos por QA/Security con evidencia.
- [ ] Archivos leídos en cada escenario (para validar Context Freeze).

### Señales de calidad
- [ ] Overhead de tokens por ciclo < 50 % (ideal < 30 %).
- [ ] Freeze Map reduce archivos leídos al menos un 40 %.
- [ ] Al menos un error evitado por ciclo en tareas con código.
- [ ] ROI calculado con costes reales de incidentes, no estimados genéricos.
- [ ] Resultados reproducibles (mismo prompt, mismo modelo, misma tarea).

### Banderas rojas (rechazar el benchmark si falta)
- [ ] Solo mide tokens de salida, ignores entrada.
- [ ] Compara tareas de distinta complejidad.
- [ ] No incluye coste del retrabajo evitado.
- [ ] Asume precio fijo sin especificar proveedor ni modelo.

---

## 8. Suposiciones y limitaciones

- Los precios de tokens varían por proveedor y modelo; usa la tarifa vigente de tu proveedor.
- Ollama local tiene coste token ≈ 0, pero tiene coste de hardware y latencia.
- El valor de la trazabilidad (auditoría, cumplimiento, SOC2) es difícil de monetizar directamente; se estima como un porcentaje del coste de incidente evitado.
- La gobernanza añade latencia (más llamadas al modelo), pero reduce el coste de errores en producción, que suele ser órdenes de magnitud mayor.

---

## 9. Cómo empezar

1. Copia `scripts/token_benchmark.py` a tu entorno.
2. Ejecuta en modo `dry-run` para validar la estructura.
3. Ejecuta en modo `live` con tu proveedor y tarea real.
4. Reemplaza la tabla ilustrativa de esta documentación con tus datos.
5. Calcula el ROI y decide si el protocolo se escala a tu equipo.
