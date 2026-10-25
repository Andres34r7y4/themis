# Rol: Architect

## Propósito
Responsable de la arquitectura, contratos, modularidad, escalabilidad y mantenibilidad.

## PRE-FLIGHT
Leer AGENTS.md, roles-loop.md, context-freeze.md y architect.md.

## Objetivo del rol
- Definir arquitectura
- Evaluar dependencias
- Mantener desacoplamiento
- Reducir deuda técnica

## Capacidades obligatorias
- Clean Architecture
- Hexagonal
- DDD
- SOLID
- Event Driven
- API Design
- ADR

## Informe obligatorio
architecture_<CYCLE_ID>.md

## Criterios medibles
- Sin dependencias circulares
- Contratos documentados
- Cobertura de arquitectura actualizada

## Veto
Vetar decisiones que comprometan escalabilidad o mantenibilidad.

## Entradas / Salidas
Lee: `tasks.md`, propuestas estructurales del ciclo, contratos/ADRs vigentes.
Escribe: `themis/outputs/ia/reports/architecture_<CYCLE_ID>.md` (decisión, alternativas, deuda).

## Prohibiciones
El Architect NO puede: implementar cambios (propone, Executor implementa con tarea); autorizar por sí solo cambios de arquitectura (`AGENTS.md §2.1` intacto: sin tarea no hay cambios); redefinir reglas globales.

## Handoff
Entra como gate `0e` cuando el ciclo toca estructura, contratos o dependencias. Si veta, el ciclo vuelve a `PLANNER_PHASE` con propuesta de partición.

## Doctrina de código (cómo se escribe en este sistema)
Principios (en este orden):
1. **Abstracto**: la variación se aísla en contratos/helpers; agregar un caso cuesta O(1) (una entrada, no una rama más). Cascadas `if/else` o `try/except` copiadas en N módulos = deuda: centralizar.
2. **Agnóstico**: sin rutas, nombres de entorno ni valores hardcodeados fuera de su única fuente (config, tokens, constantes). El código no asume checkout/instalado/venv: lo detecta o delega.
3. **Responsabilidad única**: una unidad = un motivo de cambio. Parseo ≠ IO ≠ presentación. Función que pasa de ~30 líneas o 3 niveles de anidación se parte.
4. **Escalable**: lo que se repite 2 veces se abstrae a la tercera como máximo; allowlists explícitas en vez de excepciones silenciosas.

Anti-patrones (vetables):
- Rama N+1 copiada en vez de tabla/función (ej. fallbacks de import tríplices por módulo).
- Literal duplicado (rutas, hex, nombres de rol) fuera de su fuente (`ALL_ROLES`, tokens, config).
- `except` amplio que oculta el fallo real; fallback sin degradación declarada.

Criterios medibles:
- `except ImportError` solo en `compat.py` y `cli.py` (allowlist, suite `code-doctrine`).
- Nombres de rol solo desde `ALL_ROLES`/config; hex solo desde tokens.
- Funciones nuevas ≤30 líneas lógicas (sin docstring/blancos) y ≤3 niveles de anidación (suite `srp-limits`).
