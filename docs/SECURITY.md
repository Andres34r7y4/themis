# Política de Seguridad — Themis

## Versiones Soportadas

| Versión | Soportada | Notas |
|---------|-----------|-------|
| 1.1.x   | ✅ Sí     | Versión estable actual |
| 1.0.x   | ⚠️ Limitada | Se recomienda actualizar |
| < 1.0   | ❌ No     | No soportada |

## Reportar una Vulnerabilidad

Si descubres una vulnerabilidad de seguridad en Themis, por favor no abras un
issue público. En su lugar, contacta directamente al mantenedor:

- **GitHub:** [@Andres34r7y4](https://github.com/Andres34r7y4)
- **LinkedIn:** [andresdelgado-architect](https://www.linkedin.com/in/andresdelgado-architect/)

Incluye la mayor cantidad de detalles posible:

- Versión de Themis afectada
- Pasos para reproducir el problema
- Impacto potencial
- Sugerencia de mitigación (opcional)

## Política de Divulgación

Nos comprometemos a:

1. Acusar recibo del reporte dentro de los 2 días hábiles.
2. Proporcionar actualizaciones sobre el estado de la investigación.
3. Publicar un CVE o aviso de seguridad si es necesario.
4. Darte el crédito correspondiente por el descubrimiento.

## Alcance

Themis es un protocolo de gobernanza y un CLI. Los problemas de seguridad
relevantes incluyen, entre otros:

- Path traversal o escrituras inseguras durante `themis init`.
- Fuga de secretos en logs, informes o activos generados.
- Inyección de comandos a través de argumentos del CLI.
- Problemas de empaquetado o entry points que ejecuten código inesperado.

## Agradecimientos

Gracias a todos los que ayudan a mantener Themis seguro para todos.
