# memory-loop.md — persistencia controlada

## Objetivo
Persistir aprendizajes útiles sin contaminar tareas ni mezclar roles.

## Principio
- Planner selecciona memoria.
- Executor escribe memoria.
- debugger NO decide memoria persistente por sí solo
- Ningún rol inventa un sistema nuevo.

## Qué se considera “memoria”
- Decisiones estables (contrato, arquitectura, reglas)
- Bugs recurrentes + fix validado
- Heurísticas (scoring, filtros) que ya demostraron valor
- Limitaciones del entorno (venv, dependencias, rutas)

## Qué NO es memoria
- logs de ejecución
- outputs grandes
- resultados efímeros
- explicaciones largas
- hipótesis de diagnóstico no confirmadas
- trazas temporales
- resultados parciales de debugging
- síntomas todavía ambiguos

## Flujo
1) Al finalizar un ciclo, Planner produce:
   - memory_candidates (máx 5)
   - cada ítem con:
     - titulo
     - tipo: decision | fix | heuristic | constraint
     - evidencia: archivo + línea/función (si aplica)
     - propuesta: 1–3 bullets

2) Executor aplica persistencia en:
   - `/themis/outputs/ia/memory/memory.md` (si existe)
   - o crea el archivo si el contrato lo permite

3) Si el contrato no define el archivo objetivo:
   - STOP + TODO explícito (no inventar)

## Límite
- Máx 15 líneas por ciclo de memoria persistida.

---

## Compatibilidad por rol

Estas reglas aplican a todos los roles, con estas restricciones:

- **Planner** decide qué información estructural merece persistencia.
- **Executor** aplica la persistencia solo si ya fue decidida por Planner o por el contrato.
- **Debugger** NO debe guardar memoria persistente por sí solo sobre:
  - hipótesis
  - síntomas parciales
  - trazas
  - resultados provisorios de diagnóstico

El **Debugger** solo puede:
- proponer `memory_candidates`
- marcar hallazgos como “persistencia sugerida”
- derivar la decisión final a Planner o al humano

Los demás roles (Diseñador, Architect, Security, QA, DevOps, Documentator, Product Owner) solo pueden proponer `memory_candidates`; nunca persisten por sí solos.

Si una causa raíz queda confirmada y es estructuralmente relevante, su persistencia debe ser decidida por Planner o autorizada por el humano.
