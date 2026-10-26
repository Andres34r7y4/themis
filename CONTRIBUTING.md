# ✅ Guía de Contribución — Themis (ES)

Gracias por tu interés en contribuir a **Themis**, el protocolo de gobernanza
determinista para agentes LLM.

## Cómo contribuir

1. **Fork** el repositorio.
2. Crea una rama: `git checkout -b feature/tu-mejora`
3. Realiza tus cambios y commit: `git commit -m "feat: descripción del cambio"`
4. Push a tu rama: `git push origin feature/tu-mejora`
5. Abre un Pull Request describiendo el problema y la solución.

## Entorno de desarrollo

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python cli.py validate
```

El proyecto soporta Python 3.10+ y no tiene dependencias de ejecución.

## Qué incluir en un PR

- Una descripción clara del problema y la solución elegida.
- Tests para el comportamiento nuevo (o una explicación de por qué no aplican).
- Actualizaciones de `README.md`, `docs/` y `CHANGELOG.md` cuando cambie el comportamiento.
- Una nota sobre la rama afectada: `main` (español) o `english`.

## Reglas para PRs

- Toda nueva funcionalidad debe incluir documentación en español (rama `main`) e
  inglés (rama `english`).
- Los cambios en el kernel de gobernanza (`agent.md`, `roles-loop.md`, roles)
  requieren revisión de al menos dos mantenedores.
- No se aceptan cambios que rompan el PRE-FLIGHT obligatorio.
- No se agregan dependencias nuevas sin justificación explícita en el PR.
- Mantener cambios mínimos, atómicos y reversibles.

## Estilo de código

- Seguir las convenciones del código circundante.
- Usar type hints y `snake_case` para funciones y variables.
- Mantener el CLI y el kernel determinísticos y testeables.

## Seguridad

Reporta vulnerabilidades de forma privada según [docs/SECURITY.md](docs/SECURITY.md).
No abras un issue público para un problema de seguridad.

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
