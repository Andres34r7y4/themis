# sandbox/tasks/tasks.md

## Ciclo

```text
id: 2026-10-29-01
objective: Crear script greeting.py con saludo parametrizado gobernado por Themis
```

## Restricciones

- No agregar dependencias.
- No realizar refactor masivo.
- Máximo 3 tareas por ciclo.
- Cambios mínimos y reversibles.

## Tareas

### T1
id: T1
title: Crear sandbox/target/greeting.py con función saludar(nombre)
impacto: alto
esfuerzo: bajo
riesgo: bajo
depende_de: []

#### Objetivo
Crear el archivo sandbox/target/greeting.py con una función pura saludar(nombre)
que devuelva un saludo parametrizado.

#### Definición de terminado
- [ ] El archivo existe en sandbox/target/greeting.py
- [ ] La función saludar(nombre) devuelve "Hola, {nombre}"
- [ ] El valor por defecto es "mundo"

#### Archivos probables
- sandbox/target/greeting.py

#### Verificación
- Comando: python sandbox/target/greeting.py Andres
- Esperado: Hola, Andres

#### Notes
Ninguna.

### T2
id: T2
title: Agregar bloque if __name__ == "__main__" para CLI
impacto: medio
esfuerzo: bajo
riesgo: bajo
depende_de: [T1]

#### Objetivo
Agregar el punto de entrada de línea de comandos para usar saludar() desde la terminal.

#### Definición de terminado
- [ ] El script acepta un nombre como argumento opcional
- [ ] Si no se pasa nombre, imprime "Hola, mundo"
- [ ] Si se pasa un nombre, imprime "Hola, {nombre}"

#### Archivos probables
- sandbox/target/greeting.py

#### Verificación
- Comando: python sandbox/target/greeting.py
- Esperado: Hola, mundo

#### Notes
Ninguna.

## Definition of Done

- [ ] Toda tarea del ciclo está archivada en task-archives.md
- [ ] La evidencia de verificación está registrada
- [ ] tasks.md queda consistente (tareas completadas eliminadas)
