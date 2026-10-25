Seguí estrictamente el contrato `./themis/AGENTS.md`.

Ejecutá el `roles-loop` definido en:
./themis/loops/roles-loop.md

Reglas de ejecución:
- Iniciar siempre en `PLANNER_PHASE`
- Usar `CYCLE_ID` con timestamp ISO local
- En cada fase imprimir:
  ROLE
  CYCLE_ID
  MODE: roles-loop

Cumplir el handoff automático entre Planner y Executor.

Detenerse únicamente cuando `roles-loop.md` indique STOP.