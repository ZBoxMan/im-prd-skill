# im-prd-skill

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md)

Un Claude Agent Skill para redactar PRD de productos de mensajería (IM) y sociales. Incluye una biblioteca de 26 módulos sobre cómo las principales apps de mensajería resuelven cada función, de modo que las especificaciones generadas sigan por defecto las convenciones de IM. Solo los puntos en los que las apps principales realmente difieren se plantean a quien decide, como preguntas de opción múltiple. Puede producir únicamente un borrador de entrega en Markdown, o escribir además las tarjetas de anotación en un lienzo de Figma.

El skill se creó para el equipo de ZYMIX. Esta edición pública elimina las claves de archivo de Figma del equipo, los valores del sistema de diseño, las resoluciones internas y las evidencias originales; el flujo de trabajo, la biblioteca de reglas, las plantillas, los scripts y los casos de evaluación se conservan íntegros.

## Ediciones

| Edición | Ruta | Notas |
|---|---|---|
| English | [`en/box-prd-create/`](en/box-prd-create/) | Úsala para cualquier idioma distinto del chino. Las reglas están en inglés; el borrador de entrega se escribe en el idioma del usuario. |
| 简体中文 | [`zh-CN/box-prd-create/`](zh-CN/box-prd-create/) | Edición original. Incluye los casos de evaluación (`evals/`) y el historial completo de cambios. |

Ambas ediciones usan el nombre de skill `box-prd-create`; instala solo una de ellas.

## Qué resuelve

Pedirle directamente a una IA que escriba la especificación de una función de IM suele fallar de tres maneras: las reglas inciertas se escriben como si estuvieran decididas; solo se cubre el camino feliz y se omiten estados como bloqueado, cuenta eliminada, sin conexión, multidispositivo y las diferencias entre grupo y conversación individual; y las convenciones del sector se mezclan con las pocas decisiones que el equipo realmente debe tomar, así que quien decide tiene que leerlo todo para encontrarlas.

Cómo lo gestiona este skill:

- **Biblioteca de reglas en tres niveles**: base (las apps principales coinciden; se sigue por defecto), convención (la mayoría de las apps lo hace; se adopta la recomendación por defecto), divergencia (las apps difieren; etiquetada como Must-ask (preguntar siempre) o Default-OK (valor por defecto aceptable)).
- **Solo se hacen las preguntas obligatorias**: como máximo 4 preguntas de opción múltiple por ronda, con la opción recomendada primero. Todo lo demás se escribe según la recomendación y se enumera línea por línea bajo "Defaulted to recommendation" (adoptado según la recomendación) para su revisión.
- **Matriz de cobertura de estados**: se revisan uno por uno el éxito, el fallo, el tiempo de espera agotado, la falta de conexión, los permisos, la sincronización multidispositivo y los casos como "la otra persona te ha bloqueado / ha eliminado su cuenta / ha salido del grupo".
- **La incertidumbre se mantiene visible**: los puntos que requieren una decisión se escriben como `{TBD: topic, recommended: approach}` y los hechos que faltan, como `{TBC: what is missing}`. Nada se presenta como decidido.
- **Puerta de escritura**: antes de tocar Figma, el skill enumera todos los nodos que creará y los lotes; solo escribe en el lienzo cuando quien decide lo aprueba.

## Flujo de trabajo

| Paso | Qué ocurre |
|---|---|
| 0 Planteamiento del producto | Confirmar el tipo de conversación (individual / grupo / canal / comunidad), las plataformas, el cifrado de extremo a extremo, si los desconocidos pueden contactar con los usuarios y los requisitos previos de viabilidad |
| 1 Fijar la fuente de verdad | Registrar el archivo y los nodos de Figma; etiquetar cada requisito como definido / por confirmar / sugerido |
| 2 Revisión de normas de IM | Leer los módulos correspondientes: seguir las bases, adoptar por defecto las convenciones y tratar las divergencias según su nivel |
| 3 Referencia de la competencia | Investigación externa solo para las capacidades que la biblioteca no cubre |
| 4 Matriz de cobertura de estados | Dimensiones generales más los estados obligatorios de cada módulo, cada uno marcado como cubierto / no aplicable / sin definir |
| 5 Primero el borrador | Escribir el borrador de entrega en Markdown y ejecutar `lint_card_text.py`; añadir una prueba de lectura en los borradores extensos |
| 6 Diseño y numeración | Planificar de una vez el orden de las pantallas, las filas y la numeración |
| 7 Puerta de escritura | `lint_card_text.py --gate` pasa y quien decide aprueba antes de escribir nada |
| 8 Escribir tarjetas y autorrevisión | Autorrevisión tras cada lote; se termina con un acuse de aceptación |

Orden del borrador de entrega: Decisions for Box (decisiones para Box) → Defaulted to recommendation → Open items (puntos abiertos) → Role view summary (resumen por rol) → Cards (tarjetas) → Feature list (lista de funciones) → Acceptance checkpoints (puntos de aceptación, ≤ 12) → Suggested follow-ups (seguimientos sugeridos).

## Estructura

```
en/box-prd-create/              # Edición en inglés (misma estructura en zh-CN/)
├── SKILL.md                    # Flujo de trabajo y enrutamiento (punto de entrada)
├── references/
│   ├── im-norms/               # 26 módulos de IM + antipatrones + tabla de responsabilidades
│   ├── draft-template.md       # Plantilla del borrador de entrega y las notas de trabajo
│   ├── self-check.md           # Autorrevisión de la entrega
│   ├── canvas-layout.md        # Diseño del lienzo de Figma
│   ├── figjam.md               # Diagramas de flujo y lista de funciones
│   ├── design-system.md        # Sistema de diseño (plantilla, rellena el tuyo)
│   ├── rulings.md              # Resoluciones (plantilla, rellena las tuyas)
│   └── HISTORY.md              # Historial de cambios
└── scripts/
    ├── lint_card_text.py       # Lint del texto de las tarjetas (--gate para la puerta de escritura)
    ├── lint_skill.py           # Autocomprobación de la estructura de la biblioteca de reglas
    └── brand_terms.txt         # Nombres de marca prohibidos
```

Módulos: cuentas y dispositivos, contactos y privacidad, lista de chats, envío y confirmaciones, acciones sobre mensajes, multimedia y archivos, grupos y canales, notificaciones, seguridad y protección, búsqueda/llamadas/almacenamiento, estructura de páginas, patrones de interacción, cuentas de servicio y bots, pagos en el chat, feeds/canales/comunidades, mensajes enriquecidos, traducción e IA, descubrimiento/inicio de sesión/permisos, cuenta de monedero, invitaciones y crecimiento, edad y menores, sanciones y apelaciones, publicidad y personalización, puntos y membresía, centro de privacidad, tickets de soporte.

## Instalación

Claude Code (se muestra la edición en inglés; usa `zh-CN/box-prd-create` para chino):

```bash
git clone https://github.com/ZBoxMan/im-prd-skill.git
```

```bash
cp -R im-prd-skill/en/box-prd-create ~/.claude/skills/
```

claude.ai: comprime la carpeta `box-prd-create` en un zip y súbelo en Configuración → Capacidades → Skills.

## Uso

Basta con describir la función, por ejemplo:

- "Añade anuncios de grupo a los chats grupales. Escribe el PRD, por ahora solo el borrador de entrega."
- "Añade 'Descargar mis datos' a Ajustes. Escribe el PRD en Figma: figma.com/design/<fileKey>, en la zona de Ajustes."
- "¿Cuánto tiempo debería durar el plazo para anular el envío de un mensaje? Lo necesito en el PRD."

## Adaptarlo a tu equipo

- `references/design-system.md`: tu biblioteca de diseño, claves de componentes y tokens de color y tipografía (solo se usa al dibujar pantallas de prototipo).
- `references/rulings.md`: las resoluciones de redacción de tu equipo y los diseños retirados.
- `scripts/brand_terms.txt`: nombres de marca que no deben aparecer en el texto de las tarjetas.
- "ZYMIX" y "Box" en SKILL.md son el nombre del producto y quien decide; sustitúyelos según necesites.
- Escribir en Figma requiere el Desktop Bridge de [figma-console MCP](https://github.com/southleft/figma-console-mcp). Los borradores solo en Markdown no necesitan nada adicional.
- `box-figma-prd` y `box-prd-review`, mencionados en SKILL.md, son skills complementarios privados del autor (inspección del lienzo y revisión completa). El flujo de generación funciona sin ellos.

## Evaluación

Realizada sobre la edición en chino:

- Comparación a ciegas: 8 escenarios (multidispositivo, administración de grupos, sobres rojos, denuncias, encuestas de grupo, feed de amigos, incorporación de nuevos usuarios, anular envío/editar) frente a 21 skills similares con el mismo planteamiento. Un juez Opus, sin conocer el origen, puntuó la corrección en IM, la cobertura de casos límite, el tratamiento de las decisiones, la viabilidad de implementación y la legibilidad: 94 rondas, 90 victorias, 4 derrotas.
- Activación real: 31 prompts positivos y negativos × 3 ejecuciones con `claude -p`: 31/31 correctos, sin falsas activaciones en los negativos.

Registros: `zh-CN/box-prd-create/evals/trigger-results.md`. La edición en inglés no se ha evaluado por separado.

## Fuentes y vigencia

Recopilado en octubre de 2026 a partir del comportamiento público de los principales clientes de mensajería, el código de clientes de código abierto, los centros de ayuda oficiales y la documentación para desarrolladores, y las especificaciones de protocolos. Los archivos de los módulos no contienen nombres de marca; los detalles por producto no se publican. La mayoría de los valores son valores predeterminados del cliente que los servidores pueden sobrescribir; conviene revisarlos cada 90 días.

## Licencia

MIT
