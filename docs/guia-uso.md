# Guía de Uso de Themis

## Principio obligatorio

Antes de cualquier acción o respuesta del agente, se debe leer y obedecer el
contrato central en `themis/agent.md`, luego las reglas del loop y el documento
del rol activo.

## Propósito

`themis/` centraliza el contrato, roles, loops, tareas y salidas de IA necesarios
para ejecutar ciclos controlados con trazabilidad, cambios mínimos y seguridad.

## Instalación

```bash
# Desde un clon (instalación editable)
python -m pip install -e .
themis --version

# O ejecutar sin instalar
python cli.py --help
```

## Inicio rápido

```bash
# Crear la gobernanza en un repositorio
themis init --repo ./mi-proyecto

# Validar la estructura
themis validate --repo ./mi-proyecto

# Ejecutar PRE-FLIGHT para un rol
themis run-cycle --role planner --repo ./mi-proyecto
```

`themis init` copia los activos de gobernanza en `<repo>/themis` y se niega a
sobrescribirlos salvo que se pase `--force`. Usá `--base-dir` para elegir otro
nombre de directorio.

## Modos de operación

### 1) Ciclo normal (feature / mejora / análisis)

Se inicia en `PLANNER_PHASE` y sigue el `roles-loop` hasta `STOP`.

### 2) Ciclo de bug / diagnóstico

Se inicia en `DEBUGGER_PHASE` cuando el síntoma está claro. El Debugger produce
evidencia; el Executor solo implementa con informe previo.

### 3) Solo ejecución de tasks

Cuando el usuario indica explícitamente "solo ejecutar tasks.md", se arranca en
`EXECUTOR_PHASE`.

### 4) Backlog → tasks

El Planner genera un backlog a partir de la documentación y convierte como máximo
tres tareas prioritarias a `tasks.md`.

### 5) Index-first

Usá el índice del repositorio en `themis/outputs/repo_index/` para inspección
rápida sin lectura masiva de archivos.

## Workflow (alto nivel)

1. **Pre-flight**: leer `agent.md`, `roles-loop.md` y el rol activo; imprimir
   `PRE-FLIGHT OK`, `ROLE`, `MODE`, `CYCLE_ID`.
2. **PASADA 1 (Entender)**: definir el Freeze Map y el plan mínimo.
3. **PASADA 2 (Implementar)**: cambios mínimos, solo si aplica.
4. **PASADA 3 (Verificar)**: verificación mínima según el tipo de ciclo.
5. **Archivar**: registrar el ciclo en `task-archives.md` y limpiar `tasks.md`.

## Estructura

```text
themis/
├── agent.md                 # Contrato central de gobernanza
├── PATHS.md                 # Fuente única de rutas
├── loops/
│   ├── roles-loop.md        # Máquina de estados y handoffs
│   ├── context-freeze.md    # Alcance mínimo por ciclo
│   └── memory-loop.md       # Persistencia controlada
├── roles/                   # Diez contratos de rol
├── tasks/
│   ├── tasks.md             # Tareas activas
│   └── archives/            # Bitácora de ciclos completados
├── templates/               # Plantillas de tarea, backlog y prompts
└── outputs/                 # Informes en tiempo de ejecución (generados)
```

## Planificación de tareas del Planner

El Planner debe:

- leer la documentación relevante;
- generar un backlog de como máximo 10 tareas atómicas;
- priorizar por impacto (desc), esfuerzo (asc), riesgo (asc), dependencias e ID;
- convertir como máximo 3 tareas por ciclo a `tasks.md`;
- nunca tocar código ni ejecutar comandos de dominio.

## Reglas de seguridad (resumen)

- No exponer credenciales ni tokens.
- No agregar dependencias sin autorización.
- No modificar adaptadores core ni interfaces base sin una tarea explícita.
- No hacer refactor masivo, ni mover carpetas, ni renombrar módulos por "limpieza".
- No inventar datos ni asumir salidas de herramientas no verificables.
- Mantener cambios mínimos y reversibles.

## Extender el sistema con nuevos roles

Para agregar un rol:

1. Agregarlo en `themis/agent.md` y en `core/kernel.py` (`VALID_ROLES`).
2. Crear `themis/roles/<rol>.md` y agregarlo en `core/roles.py`.
3. Agregarlo en `themis/loops/roles-loop.md` con estados y handoffs.
4. Actualizar los archivos requeridos en `core/kernel.py` y los tests.
5. Ejecutar `python -m unittest discover -s tests -v` y `python cli.py validate`.

## Checklist rápido del Planner

- [ ] Leí `themis/agent.md`
- [ ] Leí `themis/loops/roles-loop.md`
- [ ] Leí `themis/roles/planner.md`
- [ ] No toqué código
- [ ] No ejecuté comandos de dominio
- [ ] Documenté el flujo y los ejemplos
