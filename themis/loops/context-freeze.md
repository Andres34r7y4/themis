# context-freeze.md — alcance mínimo por ciclo

## Objetivo
Reducir lecturas innecesarias, evitar desvíos, y estabilizar ejecución por roles.

## Freeze Map (obligatorio)
En PASADA 1, el rol activo debe generar:

- freeze_id: <CYCLE_ID>
- archivos_lectura: [lista]
- archivos_escritura: [lista]
- comandos_prueba: [lista]
- supuestos: [máx 3]

## Regla dura
- PASADA 2 y 3 solo pueden:
  - leer `archivos_lectura`
  - escribir `archivos_escritura`
  - ejecutar `comandos_prueba`

## UNFREEZE (excepción)
Solo permitido si es imprescindible.

Formato obligatorio:
UNFREEZE:
- motivo: <1 línea>
- archivo_nuevo: <ruta real>
- accion: leer | escribir
- impacto: bajo | medio | alto

Luego el archivo se agrega al Freeze Map.

## Anti-patterns
- “Recorrer todo el repo”
- “Buscar por intuición”
- “Modificar archivos no listados”

---

## Compatibilidad por rol

Estas reglas aplican a todos los roles:

- planner
- debugger
- executor
- designer
- roles de soporte (architect, security, qa, devops, documentator, product_owner)

Aclaraciones:
- **Planner** usa el Freeze Map para delimitar planificación, backlog y tasks del ciclo.
- **Debugger** usa el Freeze Map para delimitar el alcance del diagnóstico, evitando investigar síntomas laterales o archivos no relacionados.
- **Executor** usa el Freeze Map para limitar implementación y verificación a los archivos y comandos permitidos del ciclo.

Si cualquier rol necesita salir del Freeze Map, debe declarar explícitamente:

UNFREEZE:
- motivo: <1 línea>
- archivo_nuevo: <ruta real>
- accion: leer | escribir
- impacto: bajo | medio | alto