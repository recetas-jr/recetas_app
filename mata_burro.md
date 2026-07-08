==========================================================
MATA BURROS
==========================================================

La memoria arquitectónica de recetas_app

Guía de Arquitectura, Filosofía y Decisiones de Diseño


VERSIÓN DEL DOCUMENTO

Versión: 1.0
Proyecto: recetas_app
Tipo: Documento de Arquitectura
Estado: Activo

Última actualización:
Julio 2026


¿QUÉ ES EL MATA BURROS?

"El MATA BURROS no documenta código. Documenta decisiones que deben sobrevivir al código."

El MATA BURROS constituye el documento de referencia arquitectónica de recetas_app.

No es un manual de usuario.

No es una documentación técnica de archivos.

No es un informe de migración.

No describe cómo está escrito el código.

Su propósito es mucho más importante.

Este documento recoge las decisiones arquitectónicas fundamentales del proyecto, explica las razones que motivaron dichas decisiones y conserva los principios de diseño que deben guiar la evolución futura del sistema.

En otras palabras:

El código explica cómo funciona recetas_app.

El MATA BURROS explica por qué funciona así.


FILOSOFÍA

Con el paso del tiempo el código cambia.

Las funciones evolucionan.

Los módulos se reorganizan.

Incluso pueden cambiar completamente las tecnologías utilizadas.

Sin embargo, las decisiones arquitectónicas importantes deberían permanecer estables.

Cuando una decisión de diseño demuestra ser correcta, deja de pertenecer a una implementación concreta y pasa a formar parte del conocimiento permanente del proyecto.

Ese conocimiento es precisamente el que conserva este documento.


OBJETIVOS

El MATA BURROS persigue los siguientes objetivos:

• Conservar las decisiones arquitectónicas importantes.
• Explicar el razonamiento que condujo a dichas decisiones.
• Evitar que el proyecto vuelva a recorrer caminos ya descartados.
• Facilitar la incorporación de nuevas funcionalidades respetando la filosofía general del sistema.
• Servir como documento de referencia durante futuras etapas de desarrollo.


CRITERIOS PARA INCORPORAR NUEVOS CAPÍTULOS

Un nuevo capítulo solo deberá añadirse cuando ocurra al menos una de las siguientes situaciones:

• Se adopte una decisión arquitectónica que afecte al proyecto completo.
• Se descubra un principio de diseño que deba preservarse en el tiempo.
• Se descarte una alternativa importante y resulte conveniente documentar las razones.
• Se establezca una filosofía de trabajo que deba guiar desarrollos futuros.

No deberán incorporarse detalles de implementación, fragmentos de código ni decisiones locales de un único módulo.

El propósito del MATA BURROS es conservar las decisiones que deben sobrevivir a las implementaciones concretas.


ÍNDICE

Capítulo 1
El nacimiento del Motor de Conversión de Unidades .................. 1


==========================================================
CAPÍTULO 1
==========================================================

EL NACIMIENTO DEL MOTOR DE CONVERSIÓN DE UNIDADES


CONTEXTO

Durante la Fase III de desarrollo de recetas_app comenzó la integración del denominado Motor de Equivalencias con el resto del sistema.

==========================================================
CAPÍTULO 2
==========================================================

La Unidad Canónica como eje del Motor de Conversión
Introducción

Durante el diseño del Motor de Conversión de Unidades surgió una pregunta aparentemente sencilla:

¿Cómo deben realizarse las conversiones entre las distintas unidades de medida asociadas a un ingrediente?

En un primer análisis podría suponerse que el sistema debería almacenar una conversión para cada posible combinación de unidades. Sin embargo, este enfoque produciría un crecimiento innecesario del conocimiento almacenado y aumentaría considerablemente la complejidad del algoritmo de conversión.

Tras analizar distintas alternativas se adoptó un principio arquitectónico fundamental para el proyecto:

Toda conversión realizada por el Motor deberá utilizar la unidad canónica del ingrediente como punto de referencia.

Este principio constituye uno de los pilares del Motor de Conversión y deberá mantenerse durante toda la evolución del proyecto.

La unidad canónica

La unidad canónica representa la forma oficial en que el sistema expresa internamente las cantidades de un ingrediente.

No constituye necesariamente la unidad más utilizada por el usuario, ni la más conveniente desde el punto de vista culinario.

Su función consiste exclusivamente en proporcionar un punto de referencia estable sobre el cual construir todo el conocimiento relacionado con las conversiones de dicho ingrediente.

La base de datos conserva esta representación como la verdad del sistema.

El Motor de Conversión utiliza esa verdad para expresar una misma cantidad utilizando otras unidades cuando un módulo consumidor así lo solicita.

La unidad canónica como punto de referencia

Todas las equivalencias registradas para un ingrediente deberán entenderse como relaciones entre una unidad alternativa y la unidad canónica.

Por ejemplo:

1 taza de harina = 140 g
1 cucharada de harina = 9 g
1 cucharadita de harina = 3 g

El Motor no interpreta estas relaciones como conversiones independientes entre pares de unidades.

Las interpreta como diferentes representaciones de una misma cantidad física expresadas respecto a una única referencia: la unidad canónica.

En consecuencia, cualquier conversión seguirá siempre el mismo recorrido conceptual:

Unidad de origen
        │
        ▼
Unidad canónica
        │
        ▼
Unidad de destino

Gracias a este modelo no resulta necesario almacenar conversiones directas entre todas las unidades posibles.

El ingrediente proporciona el contexto

Las unidades de medida carecen de significado por sí mismas.

Una taza de harina no representa la misma cantidad que una taza de azúcar.

Del mismo modo, una cucharada de mantequilla no equivale físicamente a una cucharada de sal.

Por esta razón, toda conversión requiere conocer necesariamente el ingrediente sobre el cual se realiza la operación.

Este principio justifica que el parámetro ingrediente_id forme parte obligatoria de la API pública del Motor.

Las conversiones no pertenecen a las unidades.

Las conversiones pertenecen al ingrediente.

El conocimiento crece. El algoritmo permanece.

Uno de los descubrimientos más importantes durante el diseño del Motor fue comprobar que la incorporación de nuevas unidades no obliga a modificar el algoritmo de conversión.

El algoritmo permanece constante.

Lo único que aumenta es el conocimiento almacenado para cada ingrediente.

Agregar una nueva unidad equivale únicamente a registrar una nueva equivalencia respecto a la unidad canónica.

Por tanto, el crecimiento del sistema se produce mediante la incorporación de conocimiento, no mediante la modificación del algoritmo.

Este principio favorece la estabilidad del Motor y reduce significativamente la complejidad de su mantenimiento.

Reutilización consciente

Durante el diseño de la API pública del Motor se adoptó otro principio arquitectónico.

Las funciones públicas del Motor no están obligadas a reutilizarse entre sí.

Cuando dicha reutilización implique realizar consultas redundantes o incremente innecesariamente el acoplamiento entre funciones, cada servicio podrá acceder directamente a la capa de persistencia para obtener la información que necesite.

La reutilización debe favorecer la claridad, la eficiencia y la simplicidad del diseño.

Nunca debe convertirse en un objetivo por sí misma.

Consecuencias para la arquitectura

Los principios definidos en este capítulo determinan la estructura completa del Motor de Conversión.

Como consecuencia:

Toda conversión utilizará la unidad canónica como punto intermedio.
El ingrediente constituirá el contexto obligatorio de toda operación.
El Motor responderá consultas de negocio y no administrará información.
La base de datos continuará siendo la fuente oficial de la verdad.
El algoritmo permanecerá estable aunque aumente el conocimiento disponible.
Los módulos consumidores nunca implementarán lógica propia de conversión.
Conclusión

El Motor de Conversión no debe entenderse como una colección de funciones destinadas a transformar unidades de medida.

Debe entenderse como un servicio de dominio cuyo propósito consiste en expresar correctamente una misma cantidad física utilizando distintas representaciones, siempre dentro del contexto de un ingrediente determinado y respetando la representación canónica almacenada por el sistema.

A partir de este capítulo, toda evolución futura del Motor deberá preservar estos principios arquitectónicos.

La implementación podrá crecer, optimizarse o ampliarse con nuevos servicios, pero la unidad canónica continuará siendo el eje del proceso de conversión y el ingrediente seguirá proporcionando el contexto imprescindible para interpretar cualquier equivalencia.

==========================================================
CAPÍTULO 3
==========================================================
La API Pública del Motor de Conversión

Durante la construcción de la primera versión funcional del Motor quedó definido un principio arquitectónico que regirá toda su evolución futura.

El Motor constituye la única interfaz oficial para acceder al conocimiento de conversión de unidades.

En consecuencia, ningún módulo consumidor (visualización de recetas, impresión, exportaciones, listas de compra, costos, nutrición o futuras APIs) deberá depender directamente de la capa de persistencia para obtener información relacionada con las conversiones.

La persistencia tiene como única responsabilidad almacenar y recuperar información.

El Motor tiene como responsabilidad interpretar ese conocimiento, aplicar las reglas del dominio y exponer servicios de alto nivel al resto del sistema.

Por esta razón, la capa de persistencia se considera un detalle interno del Motor y no forma parte de su contrato público.

Separación de responsabilidades

Queda establecida la siguiente distribución de responsabilidades:

Persistencia

Administrar el almacenamiento.
Recuperar la información.
No aplicar reglas del dominio.
No interpretar el significado de las conversiones.

Motor de Conversión

Administrar el conocimiento de conversión.
Interpretar las equivalencias.
Aplicar las reglas del dominio.
Ofrecer servicios públicos a los consumidores.
Comunicar errores mediante excepciones propias del Motor.

Esta separación permite modificar la implementación interna sin afectar a los módulos consumidores.

La API pública como frontera arquitectónica

Toda interacción con el conocimiento de conversión deberá realizarse mediante la API pública del Motor.

Las funciones públicas representan el contrato oficial del Motor y constituyen la frontera entre la lógica de conversión y el resto del sistema.

Aunque una función pública pueda reutilizar internamente funciones de persistencia, esa dependencia forma parte exclusivamente de la implementación interna y no del contrato arquitectónico.

En consecuencia, los consumidores nunca deberán depender de funciones pertenecientes a la capa de persistencia.

Evolución del Motor

El crecimiento del Motor deberá realizarse mediante la incorporación de nuevos servicios públicos y no mediante el acceso directo a la persistencia desde los consumidores.

Siempre que resulte razonable, las nuevas funciones reutilizarán servicios públicos ya existentes antes de duplicar lógica o realizar nuevas consultas directas.

De esta manera, el Motor evolucionará como una capa de conocimiento estable, mientras la persistencia continuará siendo un mecanismo interno de almacenamiento.

Modelo de excepciones

La API pública del Motor comunica las situaciones de error mediante una jerarquía propia de excepciones.

Las excepciones representan situaciones del dominio y no errores de implementación.

La clase ErrorConversion constituye la excepción base del Motor.

Las excepciones derivadas describen condiciones específicas del proceso de conversión, permitiendo que los módulos consumidores capturen tanto errores generales del Motor como situaciones particulares cuando sea necesario.

Este modelo proporciona una interfaz más expresiva, coherente y fácilmente extensible conforme el Motor incorpore nuevos servicios.

==========================================================
CAPÍTULO 4
==========================================================
Evolución de la API Pública del Motor

Durante la implementación de la primera versión funcional del Motor quedó validado un principio adicional sobre la evolución de su API pública.

Los servicios públicos del Motor no constituyen funciones independientes entre sí.

Por el contrario, forman una jerarquía de servicios donde las funciones de mayor nivel reutilizan, siempre que resulte razonable, los servicios públicos ya existentes antes de acceder directamente a la capa de persistencia.

Este principio permite centralizar las reglas del dominio en un único punto y evita la duplicación de lógica entre distintos servicios.

Como consecuencia, el conocimiento del Motor permanece cohesionado y los cambios futuros pueden concentrarse en un número reducido de funciones.

Reutilización de servicios

Cuando un nuevo servicio público necesite información ya proporcionada por otro servicio del Motor, deberá reutilizar dicho servicio antes de incorporar nuevas consultas directas a la persistencia.

Esta regla favorece la estabilidad de la API y garantiza que todas las funciones públicas interpreten el dominio utilizando las mismas reglas.

Por ejemplo, la función encargada de obtener las unidades disponibles reutiliza el servicio de obtención de equivalencias, evitando conocer detalles de almacenamiento.

De igual forma, el algoritmo principal de conversión reutiliza el mismo servicio para obtener las equivalencias del ingrediente antes de realizar el proceso de conversión.

Centralización del conocimiento

El acceso al conocimiento relacionado con las equivalencias deberá concentrarse en un único servicio público del Motor.

Este servicio constituye el punto oficial de entrada al conocimiento de conversión del ingrediente.

Los demás servicios públicos reutilizarán este punto de acceso cuando necesiten información relacionada con las equivalencias.

De esta forma, cualquier modificación futura sobre la obtención, validación o preparación de las equivalencias podrá realizarse en un único lugar sin afectar al resto de la API pública.

Crecimiento progresivo de la API

La experiencia obtenida durante la construcción del núcleo del Motor permitió confirmar un comportamiento esperado de la arquitectura.

A medida que el conocimiento del dominio queda encapsulado en servicios públicos reutilizables, las nuevas funciones requieren un esfuerzo de implementación progresivamente menor.

El crecimiento del Motor deja entonces de consistir en construir algoritmos completamente nuevos y pasa a centrarse en combinar y reutilizar capacidades previamente implementadas.

Esta propiedad constituye uno de los principales indicadores de estabilidad de la arquitectura adoptada para la Fase III.

Principio de madurez arquitectónica

Una arquitectura correctamente diseñada tiende a simplificar el desarrollo de nuevas funcionalidades.

Cuando la incorporación de nuevos servicios requiere principalmente reutilizar servicios existentes en lugar de introducir nuevas reglas del dominio, puede considerarse que el núcleo arquitectónico ha alcanzado un grado adecuado de madurez.

En consecuencia, el crecimiento futuro del Motor deberá priorizar la reutilización de capacidades existentes antes de incorporar nuevas dependencias o duplicar lógica de negocio.

==========================================================
CAPÍTULO 5
==========================================================
Modelo del Dominio del Motor de Conversión

Durante la construcción del núcleo del Motor quedó definido que el proceso de conversión no gira alrededor de las unidades de medida, sino alrededor del conocimiento asociado a un ingrediente.

Por tanto, la unidad de trabajo fundamental del Motor no es la unidad, sino el ingrediente con su conjunto de equivalencias.

El ingrediente como contexto

Una unidad de medida carece de significado para el Motor si no está asociada a un ingrediente.

Por ejemplo:

1 taza

no representa una cantidad convertible.

En cambio:

1 taza de harina

sí constituye una cantidad convertible porque existe un conjunto de equivalencias asociado al ingrediente "harina".

En consecuencia, toda conversión requiere obligatoriamente el contexto del ingrediente.

La equivalencia como conocimiento

Una equivalencia no representa una conversión entre dos unidades.

Representa el conocimiento necesario para expresar una unidad en términos de la unidad canónica.

Por ejemplo:

1 taza = 140 gramos

no constituye una conversión.

Constituye conocimiento permanente sobre el ingrediente.

Las conversiones son una consecuencia de ese conocimiento.

La unidad canónica como referencia única

Toda conversión deberá realizarse utilizando la unidad canónica como punto de referencia.

El Motor nunca realizará conversiones directas entre dos unidades arbitrarias.

Conceptualmente, todo proceso sigue la secuencia:

Unidad origen
      ↓
Unidad canónica
      ↓
Unidad destino

Este principio garantiza que el algoritmo permanezca estable independientemente de la cantidad de unidades registradas para cada ingrediente.

Separación entre conocimiento y cálculo

El Motor distingue claramente entre:

Conocimiento

Ingrediente.
Equivalencias.
Unidad canónica.
Factores.

Cálculo

Conversión hacia la unidad canónica.
Conversión desde la unidad canónica.
Resultado final.

El conocimiento permanece almacenado.

El cálculo ocurre únicamente cuando un consumidor solicita una conversión.

El Motor como intérprete

La persistencia recupera información.

El Motor interpreta dicha información.

Los consumidores únicamente solicitan servicios al Motor.

En consecuencia, el conocimiento del dominio permanece centralizado en un único lugar.

==========================================================
CAPÍTULO 6
==========================================================
Inicio de la Integración del Motor
Durante la Fase III quedó completada la construcción del núcleo del Motor de Conversión y comenzó su integración progresiva dentro de recetas_app.

Este momento marca la transición entre la construcción del Motor y su utilización por parte de consumidores reales del sistema.
El primer consumidor integrado fue el módulo de administración de equivalencias de ingredientes.

La integración consistió exclusivamente en sustituir el acceso directo a la capa de persistencia por una llamada al servicio público del Motor encargado de obtener las equivalencias del ingrediente.
La sustitución se realizó sin modificar la lógica funcional del consumidor, la estructura de los datos entregados a la interfaz de usuario ni el comportamiento observable de la aplicación.

El cambio quedó limitado al origen del conocimiento, pasando de una consulta directa a la persistencia a la utilización de la API pública del Motor.
Principio arquitectónico confirmado

La integración de nuevos consumidores debe realizarse sustituyendo el origen del conocimiento y no modificando la lógica funcional del consumidor.

Cuando la API pública del Motor representa correctamente el dominio, los consumidores pueden migrarse progresivamente hacia el Motor preservando su comportamiento observable.

Este principio quedó validado durante la integración del primer consumidor del Motor y pasa a formar parte de la arquitectura permanente de recetas_app.
