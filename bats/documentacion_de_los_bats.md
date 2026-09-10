 ==================================================================
                          INDICE:
INFORME BAT CONSOLIDADO - RECETAS_APP
-------------------------------------------------------------------
INFORME CONSOLIDADO — MÓDULO DE EQUIVALENCIAS / BORRADO DE EQUIVALENCIAS

====================================================================

MODIFICACION DEL CONTENIDO DEL DOCUMENTO:

DOCUMENTACIÓN MAESTRA DEL ECOSISTEMA BAT
recetas_app
FECHA DE ACTUALIZACIÓN

Julio 2026

OBJETIVO DEL DOCUMENTO

Este documento constituye la referencia oficial del ecosistema BAT del proyecto recetas_app.

Su finalidad es describir la arquitectura actualmente implantada, definir la responsabilidad de cada herramienta BAT, documentar el flujo operativo recomendado y dejar registradas las decisiones técnicas adoptadas durante la reorganización del ecosistema.

Este documento sustituye a la documentación histórica anterior, incorporando la arquitectura vigente y eliminando información obsoleta o duplicada.

No pretende documentar el funcionamiento interno de los módulos funcionales del sistema (como el Motor de Equivalencias), sino exclusivamente las herramientas BAT utilizadas para la administración técnica del proyecto.

ALCANCE

Esta documentación cubre exclusivamente las herramientas BAT incluidas dentro del directorio:

bats/

Actualmente forman parte del ecosistema:

arranca_recetas.bat
abrir_bd_recetas.bat
backup_proyecto.bat
backup_recetas.bat
git_commit.bat
git_push.bat
deploy_render.bat
menu_administracion_tecnica.bat
nomenclador_commits.bat
nomenclador_commits.txt

No forman parte del alcance de este documento:

módulos Flask
persistencia de datos
Motor de Equivalencias
estructura de la base de datos
lógica de negocio de recetas_app

Esos temas poseen su propia documentación técnica.

FILOSOFÍA DEL ECOSISTEMA BAT

La reorganización realizada durante esta etapa tuvo como objetivo principal separar claramente las responsabilidades de cada herramienta.

Cada BAT debe realizar una única función bien definida.

Se evita deliberadamente que una misma herramienta mezcle operaciones de:

staging
commit
push
deploy

Esta separación reduce el riesgo de errores, facilita el mantenimiento y hace que el flujo de trabajo sea más predecible.

PRINCIPIOS DE DISEÑO

El ecosistema BAT se rige por los siguientes principios.

Una responsabilidad por herramienta

Cada BAT debe tener un único objetivo claramente definido.

No deben mezclarse funciones diferentes en una misma herramienta cuando puedan separarse sin perjudicar la operación.

Confirmaciones antes de operaciones importantes

Siempre que una herramienta vaya a ejecutar una operación potencialmente irreversible deberá solicitar confirmación al usuario.

Especialmente en operaciones relacionadas con:

Commit
Push
Deploy
Transparencia

Siempre que sea posible la herramienta debe informar previamente qué operación realizará.

El usuario debe conocer:

qué commits existen
qué operación se ejecutará
cuál será el siguiente paso
Evitar automatismos peligrosos

Las operaciones potencialmente destructivas o de gran alcance no deben ejecutarse de forma automática sin intervención consciente del usuario.

Especialmente se evita:

staging indiscriminado
commits automáticos
despliegues involuntarios
Evolución controlada

Cada BAT debe poder evolucionar independientemente del resto.

La modificación de una herramienta no debe obligar a rediseñar el ecosistema completo.

ARQUITECTURA ACTUAL

El ecosistema BAT queda organizado en cinco áreas claramente diferenciadas.

                 ECOSISTEMA BAT
                       │
 ┌─────────────────────┼─────────────────────┐
 │                     │                     │
 │                     │                     │
ARRANQUE           BACKUPS              GESTIÓN GIT
 │                     │                     │
 │                     │                     │
arranca              backup             git_commit
abrir_bd             backup_recetas     git_push
                                           │
                                           │
                                     DEPLOY RENDER
                                           │
                                    deploy_render
                                           │
                                           │
                                  ADMINISTRACIÓN
                                           │
                         menu_administracion_tecnica
                                           │
                                           │
                               NOMENCLADOR DE COMMITS
                                           │
                        nomenclador_commits.bat
                        nomenclador_commits.txt
FLUJO OPERATIVO RECOMENDADO

La arquitectura vigente establece el siguiente orden de trabajo.

Modificar archivos
        │
        ▼
Preparar staging manualmente
        │
        ▼
git_commit.bat
        │
        ▼
git_push.bat
        │
        ▼
deploy_render.bat

Este flujo representa la secuencia oficial recomendada para la publicación de cambios.

Cada etapa posee una responsabilidad independiente y claramente delimitada.

RESPONSABILIDADES DEL FLUJO
Preparación del staging

La selección de archivos que formarán parte del commit es una decisión consciente del desarrollador.

Ningún BAT incorpora automáticamente archivos al staging.

Esta decisión reduce significativamente el riesgo de publicar información no deseada.

git_commit.bat

Responsable exclusivamente de crear commits utilizando el staging previamente preparado.

No realiza operaciones de:

git add
push
deploy
git_push.bat

Responsable exclusivamente de enviar a GitHub los commits existentes.

No crea commits.

No modifica el staging.

deploy_render.bat

Responsable exclusivamente de iniciar el proceso de publicación hacia Render utilizando commits previamente existentes.

No realiza:

staging
commit

Su función consiste únicamente en completar el proceso de publicación.

INVENTARIO GENERAL DEL ECOSISTEMA BAT

Actualmente el proyecto dispone de las siguientes herramientas.

BAT	Función principal
arranca_recetas.bat	Arranque controlado del sistema Flask
abrir_bd_recetas.bat	Apertura directa de la base SQLite
backup_proyecto.bat	Backup completo del proyecto
backup_recetas.bat	Backup específico de recetas
git_commit.bat	Creación de commits
git_push.bat	Publicación de commits en GitHub
deploy_render.bat	Despliegue hacia Render
menu_administracion_tecnica.bat	Centro de administración técnica
nomenclador_commits.bat	Administración del catálogo de mensajes
nomenclador_commits.txt	Catálogo reutilizable de mensajes de commit
DOCUMENTACIÓN INDIVIDUAL DE LOS BAT

A partir de la siguiente sección se describe detalladamente cada herramienta del ecosistema BAT.

El orden sigue el flujo operativo recomendado del proyecto.

ARRANQUE DEL SISTEMA
arranca_recetas.bat
OBJETIVO

arranca_recetas.bat es la herramienta oficial para iniciar la variante web de recetas_app.

Su finalidad es automatizar completamente el proceso de arranque del sistema Flask evitando que el usuario tenga que abrir manualmente una terminal, posicionarse en el proyecto y ejecutar comandos Python.

Además incorpora lógica de control del entorno antes del arranque.

RESPONSABILIDADES

Este BAT es responsable de:

comprobar el estado del puerto 5000;
detectar si ya existe una instancia de Flask ejecutándose;
ofrecer alternativas al usuario cuando el puerto está ocupado;
iniciar Flask en PowerShell;
esperar a que el servidor quede disponible;
abrir automáticamente el navegador en la pantalla de acceso del sistema.
FUNCIONAMIENTO GENERAL

El flujo operativo es el siguiente:

Inicio
   │
   ▼
Comprobar puerto 5000
   │
   ├──────── Puerto ocupado ────────► Mostrar opciones
   │                                     │
   │                                     ├── Reiniciar Flask
   │                                     ├── Abrir navegador
   │                                     └── Cancelar
   │
   ▼
Puerto libre
   │
   ▼
Iniciar Flask
   │
   ▼
Esperar disponibilidad
   │
   ▼
Abrir navegador
CONTROL DEL PUERTO

Antes de iniciar Flask se verifica si el puerto 5000 ya se encuentra ocupado.

Si existe un proceso utilizando dicho puerto, la herramienta informa al usuario y ofrece varias alternativas de actuación.

Este comportamiento evita errores frecuentes provocados por múltiples instancias del servidor.

REINICIO CONTROLADO

Cuando el usuario decide reiniciar Flask, la herramienta:

identifica el proceso que ocupa el puerto;
finaliza dicho proceso;
espera a que el puerto quede completamente libre;
inicia nuevamente el servidor.

Este procedimiento permite recuperar rápidamente un entorno de trabajo sin intervención manual.

ARRANQUE DE FLASK

Cuando el entorno está listo, la herramienta ejecuta la aplicación mediante:

python -m modulo_web.web_app

El servidor se inicia dentro de una ventana de PowerShell destinada exclusivamente al proceso Flask.

APERTURA AUTOMÁTICA DEL NAVEGADOR

Una vez que Flask comienza a escuchar correctamente en el puerto correspondiente, el BAT abre automáticamente el navegador apuntando a la aplicación.

La dirección utilizada es:

http://127.0.0.1:5000/login

De esta manera el usuario queda inmediatamente situado en la pantalla de autenticación.

RESPONSABILIDAD EXCLUSIVA

La misión de este BAT termina cuando el sistema queda correctamente iniciado.

No realiza ninguna otra operación relacionada con:

Git
Deploy
Backups
Administración técnica
OBSERVACIONES

Esta herramienta constituye el punto oficial de entrada al sistema durante el desarrollo local.

Su lógica de control del puerto representa una mejora importante respecto a un simple lanzador de Flask.

APERTURA DE LA BASE DE DATOS
abrir_bd_recetas.bat
OBJETIVO

Esta herramienta permite abrir directamente la base de datos principal del proyecto utilizando DB Browser for SQLite.

Su propósito es facilitar las tareas de inspección, mantenimiento y verificación de datos sin necesidad de navegar manualmente por el sistema de archivos.

RESPONSABILIDAD

Su única responsabilidad consiste en abrir la base de datos operativa del proyecto.

No realiza modificaciones sobre la información almacenada.

FUNCIONAMIENTO

El BAT calcula automáticamente la raíz del proyecto a partir de su propia ubicación.

Posteriormente localiza el archivo:

modulo_web/recetas.db

y lo abre utilizando DB Browser for SQLite.

VENTAJAS

La utilización de rutas relativas permite que el BAT continúe funcionando aunque el proyecto cambie de ubicación dentro del equipo.

No depende de una ruta absoluta hacia la carpeta del proyecto.

DEPENDENCIA EXTERNA

El único elemento que utiliza una ruta fija es el ejecutable de DB Browser for SQLite.

Por tanto, el correcto funcionamiento de esta herramienta depende de que dicha aplicación permanezca instalada en la ubicación prevista.

LIMITACIONES ACTUALES

Actualmente el BAT:

no verifica si DB Browser está instalado;
no comprueba la existencia previa de la base de datos;
asume que ambos elementos existen antes de ejecutarse.

Estas limitaciones son conocidas y no afectan al flujo normal de trabajo del proyecto.

RESPONSABILIDAD EXCLUSIVA

Esta herramienta no realiza:

copias de seguridad;
mantenimiento de la base;
operaciones Git;
despliegues.

Su única misión consiste en facilitar el acceso inmediato a la base de datos principal del sistema.

HERRAMIENTAS DE BACKUP

Las siguientes herramientas están dedicadas exclusivamente a la generación de copias de seguridad del proyecto y de la información operativa.

HERRAMIENTAS DE BACKUP

Las herramientas de respaldo constituyen el mecanismo oficial para preservar el estado del proyecto y de la información operativa.

Su responsabilidad es exclusivamente iniciar los procesos de copia de seguridad implementados mediante scripts Python.

No realizan tareas relacionadas con Git, Deploy o administración del sistema.

backup_proyecto.bat
OBJETIVO

Iniciar el proceso de respaldo completo del proyecto.

Este BAT actúa como un lanzador del script Python encargado de generar la copia de seguridad general.

RESPONSABILIDADES

Sus responsabilidades son únicamente:

posicionarse en la raíz del proyecto;
ejecutar el script de backup general;
mantener abierta la consola para informar el resultado de la operación.

No incorpora lógica adicional.

FUNCIONAMIENTO

El flujo es extremadamente sencillo.

Inicio
   │
   ▼
Ir a la raíz del proyecto
   │
   ▼
Ejecutar backup_proyecto.py
   │
   ▼
Esperar confirmación del usuario
ALCANCE

El comportamiento real del respaldo depende exclusivamente del contenido de:

backup_proyecto.py

El BAT únicamente inicia dicho proceso.

RESPONSABILIDAD EXCLUSIVA

No realiza:

validaciones Git
despliegues
operaciones sobre Flask
modificaciones de la base de datos

Su misión termina cuando el script Python comienza su ejecución.

backup_recetas.bat
OBJETIVO

Ejecutar el respaldo específico de la información relacionada con las recetas.

Al igual que el BAT anterior, funciona como un lanzador del script Python correspondiente.

RESPONSABILIDADES

Este BAT únicamente:

se posiciona en la raíz del proyecto;
ejecuta el proceso de respaldo específico;
mantiene visible la consola para informar el resultado.
FUNCIONAMIENTO
Inicio
   │
   ▼
Ir a la raíz del proyecto
   │
   ▼
Ejecutar backup_recetas.py
   │
   ▼
Esperar confirmación del usuario
RESPONSABILIDAD EXCLUSIVA

No interviene sobre:

Git
Render
Flask
Administración técnica

Toda la lógica de respaldo pertenece al script Python correspondiente.

GESTIÓN DEL CICLO GIT

La reorganización del ecosistema BAT introdujo una separación estricta entre las distintas fases del ciclo Git.

Hasta esta refactorización varias herramientas mezclaban responsabilidades de:

staging
commit
push
deploy

La arquitectura actual elimina esa superposición.

Cada operación dispone ahora de una herramienta específica.

ARQUITECTURA ACTUAL DEL CICLO GIT
Preparar staging manualmente
              │
              ▼
      git_commit.bat
              │
              ▼
       git_push.bat
              │
              ▼
    deploy_render.bat

Esta secuencia constituye el flujo oficial del proyecto.

PRINCIPIOS DEL NUEVO MODELO

La reorganización se apoya en varios principios fundamentales.

El staging pertenece al usuario

La selección de archivos que formarán parte del commit debe realizarse conscientemente antes de utilizar cualquier BAT del ciclo Git.

Ninguna herramienta incorpora automáticamente archivos al staging.

Un BAT por responsabilidad

Cada herramienta ejecuta únicamente una fase del proceso.

De esta forma resulta mucho más sencillo comprender qué está ocurriendo y localizar cualquier incidencia.

Confirmaciones antes de operaciones críticas

Siempre que una operación pueda modificar el historial del repositorio o publicar cambios, la herramienta solicita confirmación al usuario.

Este comportamiento incrementa la seguridad del proceso.

git_commit.bat
OBJETIVO

Crear un commit utilizando exclusivamente el contenido que ya se encuentra preparado en el staging.

Este BAT representa el inicio oficial del ciclo Git dentro del ecosistema BAT.

RESPONSABILIDAD

Su única responsabilidad consiste en crear un nuevo commit.

No realiza:

git add
git push
Deploy Render
FILOSOFÍA

El commit debe construirse únicamente sobre un staging previamente revisado por el desarrollador.

La herramienta no decide qué archivos forman parte del commit.

Esa decisión corresponde exclusivamente al usuario.

FLUJO GENERAL
Inicio
   │
   ▼
Comprobar staging existente
   │
   ▼
Seleccionar mensaje de commit
   │
   ▼
Mostrar información necesaria
   │
   ▼
Solicitar confirmación
   │
   ▼
Crear commit
MENSAJES DE COMMIT

La herramienta utiliza el nomenclador oficial de mensajes del proyecto.

El usuario puede:

seleccionar un mensaje existente;
escribir un mensaje completamente nuevo;
cancelar la operación.
BENEFICIOS DE ESTA ARQUITECTURA

La incorporación de git_commit.bat permitió eliminar uno de los principales problemas del modelo anterior.

Anteriormente una misma herramienta realizaba simultáneamente:

staging;
commit;
push.

Actualmente esas operaciones se encuentran completamente separadas.

Esta reorganización proporciona:

mayor control;
menor riesgo de errores;
mejor trazabilidad del proceso;
mantenimiento mucho más sencillo.
RESPONSABILIDAD EXCLUSIVA

Una vez creado correctamente el commit, la responsabilidad de esta herramienta termina.

La publicación del commit corresponde a la siguiente etapa del flujo:

MEJORAS DE EXPERIENCIA DE USUARIO (UX)

Durante una revisión posterior del flujo operativo de git_commit.bat se incorporaron varias mejoras destinadas a hacer más claro el diálogo entre la herramienta y el usuario.

Las mejoras implantadas fueron las siguientes:

• El BAT informa explícitamente que no ejecuta automáticamente "git add", recordando que la preparación del staging es responsabilidad del desarrollador.

• Antes de comprobar el staging, la herramienta informa que dicha verificación aún no se ha realizado y solicita al usuario presionar ENTER para iniciarla.

• Se eliminó la utilización del mensaje automático generado por "pause" en ese punto del flujo, sustituyéndolo por una solicitud explícita mediante "set /p", evitando instrucciones redundantes.

• Una vez realizada la comprobación, el BAT distingue claramente dos situaciones:
  - No se detectó staging preparado.
  - Staging detectado correctamente.

• Cuando existe staging, la herramienta informa este resultado antes de mostrar la lista de archivos que formarán parte del commit.

Estas mejoras no modifican el funcionamiento del BAT; únicamente mejoran la claridad del flujo operativo y reducen la posibilidad de interpretaciones erróneas por parte del usuario.

TRANSICIÓN HACIA LA SIGUIENTE ETAPA DEL CICLO GIT

Una vez creado correctamente el commit, la siguiente etapa del flujo operativo corresponde a su publicación mediante la herramienta git_push.bat.

PUBLICACIÓN DE COMMITS
git_push.bat
OBJETIVO

git_push.bat es la herramienta responsable de publicar en GitHub los commits que ya existen en el repositorio local.

Su misión comienza cuando el commit ya ha sido creado correctamente mediante git_commit.bat.

No participa en la construcción del commit.

RESPONSABILIDAD

Esta herramienta tiene una única responsabilidad:

Publicar commits existentes.

No realiza:

git add
creación de commits
despliegues hacia Render
FILOSOFÍA

La separación entre Commit y Push constituye una de las decisiones arquitectónicas más importantes del ecosistema BAT.

El hecho de crear un commit no implica necesariamente publicarlo.

De la misma forma, publicar un commit no implica volver a modificar el repositorio.

Cada operación constituye una etapa independiente.

FLUJO GENERAL
Inicio
   │
   ▼
Comprobar commits pendientes
   │
   ▼
Mostrar último commit
   │
   ▼
Solicitar confirmación
   │
   ▼
Realizar Push
   │
   ▼
Informar resultado
VERIFICACIÓN PREVIA

Antes de ejecutar el Push, la herramienta comprueba si realmente existen commits pendientes de publicación.

Si no existen commits pendientes, informa la situación y finaliza sin realizar modificaciones.

Esta verificación evita operaciones innecesarias.

INFORMACIÓN AL USUARIO

Cuando existen commits pendientes, la herramienta muestra la información suficiente para que el usuario conozca qué será publicado.

El objetivo es que la decisión de publicar sea completamente consciente.

CONFIRMACIÓN

Antes del Push se solicita confirmación explícita.

Esta confirmación constituye una medida adicional de seguridad y evita publicaciones accidentales.

OPERACIÓN DE PUSH

Una vez confirmada la operación, la herramienta publica los commits pendientes hacia GitHub.

Finalizado el proceso informa el resultado obtenido.

RESPONSABILIDAD EXCLUSIVA

La responsabilidad de esta herramienta termina cuando los commits han sido enviados correctamente al repositorio remoto.

No inicia procesos de Deploy.

La publicación de la aplicación corresponde exclusivamente a la siguiente herramienta del ecosistema.

DESPLIEGUE HACIA RENDER
deploy_render.bat
OBJETIVO

deploy_render.bat constituye la última etapa del flujo operativo del proyecto.

Su finalidad consiste en iniciar el proceso de despliegue utilizando commits que ya existen y que ya han sido preparados para publicación.

RESPONSABILIDAD

Esta herramienta es responsable únicamente del proceso de Deploy.

No realiza:

staging
creación de commits

La arquitectura vigente elimina completamente esas responsabilidades de este BAT.

FILOSOFÍA

El Deploy representa una fase independiente del ciclo Git.

La herramienta asume que:

el staging fue preparado previamente;
el commit ya fue creado;
los cambios están listos para ser publicados.

Su misión consiste únicamente en completar el proceso de despliegue.

FLUJO GENERAL
Inicio
   │
   ▼
Comprobar commits pendientes
   │
   ▼
Mostrar último commit
   │
   ▼
Solicitar confirmación
   │
   ▼
Publicar cambios
   │
   ▼
Informar inicio del despliegue
INFORMACIÓN PREVIA

Antes del despliegue la herramienta informa al usuario cuál será el último commit que llegará al servidor.

De esta forma siempre existe una comprobación final antes de iniciar la publicación.

PUBLICACIÓN

Cuando el usuario confirma la operación, la herramienta realiza el envío correspondiente.

Una vez completado el proceso informa que Render continuará la actualización de la aplicación en segundo plano.

ALCANCE

Es importante recordar que esta herramienta no controla el tiempo de construcción de Render.

Su responsabilidad finaliza cuando el repositorio remoto ha recibido correctamente los cambios necesarios para iniciar el despliegue.

BENEFICIOS DE LA NUEVA ARQUITECTURA

La reorganización realizada durante esta etapa aporta varias ventajas importantes.

Entre ellas:

eliminación de responsabilidades duplicadas;
mayor claridad del flujo operativo;
menor riesgo de publicar archivos no deseados;
mantenimiento más sencillo;
mejor separación entre desarrollo y despliegue;
mayor facilidad para futuras ampliaciones del ecosistema BAT.
RELACIÓN ENTRE LAS TRES HERRAMIENTAS

La secuencia oficial queda establecida de la siguiente manera:

Preparar staging
       │
       ▼
git_commit.bat
       │
       ▼
git_push.bat
       │
       ▼
deploy_render.bat

Cada herramienta finaliza exactamente donde comienza la siguiente.

No existen zonas de responsabilidad compartida.

Esta separación constituye uno de los principios fundamentales de la arquitectura actual del ecosistema BAT.

ADMINISTRACIÓN DEL ECOSISTEMA

Las siguientes herramientas proporcionan la infraestructura administrativa utilizada por el resto de los BAT del proyecto.

ADMINISTRACIÓN DEL ECOSISTEMA BAT

Las herramientas descritas en esta sección proporcionan la infraestructura administrativa utilizada por el resto del ecosistema BAT.

Su finalidad no es ejecutar operaciones Git ni iniciar Flask, sino facilitar la administración técnica cotidiana del proyecto.

menu_administracion_tecnica.bat
OBJETIVO

menu_administracion_tecnica.bat constituye el punto central de acceso a todas las herramientas BAT del proyecto.

Su propósito es evitar que el usuario tenga que localizar y ejecutar manualmente cada BAT desde el Explorador de Windows.

Desde este menú se accede a todas las operaciones habituales de administración técnica.

RESPONSABILIDAD

Esta herramienta actúa como coordinador del ecosistema BAT.

No implementa directamente la lógica de las distintas operaciones.

Su responsabilidad consiste en ofrecer un punto único de acceso y delegar la ejecución en la herramienta correspondiente.

ESTRUCTURA GENERAL

El menú central organiza las principales operaciones administrativas del proyecto.

Actualmente permite acceder a:

Arranque del sistema.
Apertura de la base de datos.
Backup general.
Backup de recetas.
Gestión de commits.
Publicación en GitHub.
Deploy hacia Render.
Administración del nomenclador de mensajes.
Salida del sistema.
FILOSOFÍA

El Centro de Administración Técnica constituye la puerta de entrada al ecosistema BAT.

Gracias a esta organización el usuario no necesita recordar nombres de archivos ni recorrer carpetas para ejecutar herramientas individuales.

Todo el flujo operativo puede iniciarse desde un único punto.

RESPONSABILIDAD EXCLUSIVA

Este BAT no implementa la lógica de ninguna herramienta.

Simplemente dirige la ejecución hacia el BAT correspondiente.

ADMINISTRACIÓN DEL NOMENCLADOR DE COMMITS
nomenclador_commits.bat
OBJETIVO

Administrar el catálogo oficial de mensajes reutilizables para los commits del proyecto.

Su finalidad consiste en mantener una colección homogénea de mensajes frecuentes, evitando reescribir continuamente textos similares.

RESPONSABILIDAD

Esta herramienta administra exclusivamente el archivo:

bats/nomenclador_commits.txt

No realiza operaciones Git.

No crea commits.

No publica cambios.

OPERACIONES DISPONIBLES

Actualmente permite realizar cuatro operaciones principales.

Ver mensajes

Muestra el contenido completo del nomenclador.

Los mensajes aparecen numerados para facilitar su selección.

Agregar mensajes

Permite incorporar un nuevo mensaje al catálogo.

El nuevo texto pasa a formar parte del repertorio reutilizable del proyecto.

Eliminar mensajes

Permite eliminar un mensaje existente.

Antes de realizar la eliminación la herramienta solicita confirmación al usuario.

Posteriormente reconstruye el archivo sin la línea seleccionada.

Este procedimiento evita modificaciones manuales del archivo de texto.

Regresar al Centro de Administración Técnica

Finaliza la administración del nomenclador y devuelve el control al menú principal.

FILOSOFÍA

La existencia de un catálogo común de mensajes permite mantener una nomenclatura coherente para los commits del proyecto.

Esto facilita la lectura del historial Git y mejora la trazabilidad de la evolución del sistema.

nomenclador_commits.txt
OBJETIVO

Almacenar el conjunto oficial de mensajes reutilizables para los commits del proyecto.

Este archivo constituye un recurso de apoyo para git_commit.bat.

CONTENIDO

El archivo contiene una lista editable de mensajes organizados en formato texto.

Cada línea representa un mensaje independiente.

La administración de dicho contenido se realiza mediante nomenclador_commits.bat.

No se recomienda modificar este archivo manualmente salvo situaciones excepcionales.

RELACIÓN ENTRE AMBAS HERRAMIENTAS
nomenclador_commits.txt
            ▲
            │
            │
nomenclador_commits.bat
            ▲
            │
            │
     git_commit.bat

De esta forma existe una única fuente oficial para los mensajes reutilizables del proyecto.

ORGANIZACIÓN GENERAL DEL ECOSISTEMA BAT

Con la reorganización realizada durante esta etapa el ecosistema queda estructurado de la siguiente forma.

                     ECOSISTEMA BAT
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      │                    │                    │
  OPERACIÓN            ADMINISTRACIÓN       SOPORTE
      │                    │                    │
      │                    │                    │
Arranque             Menú Técnico         Nomenclador
Base de datos        Centro BAT           Mensajes
Backups
Git
Deploy

Cada herramienta ocupa una posición claramente definida dentro del sistema y posee una responsabilidad específica.

No existen duplicidades funcionales entre ellas.

DECISIONES ARQUITECTÓNICAS CONSOLIDADAS

Como resultado de la reorganización realizada durante esta etapa quedan fijadas las siguientes decisiones técnicas.

Separación completa entre Commit y Push

La creación del commit y su publicación constituyen procesos independientes.

Eliminación del staging automático

La preparación del staging deja de formar parte de las herramientas BAT.

La selección de archivos corresponde al desarrollador.

Separación entre Push y Deploy

Publicar un commit y desplegar la aplicación dejan de ser operaciones inseparables.

Cada proceso dispone ahora de su propia herramienta.

Un BAT por responsabilidad

Cada BAT debe mantener un objetivo único y claramente definido.

Las futuras ampliaciones deberán respetar este principio.

Evolución controlada

La incorporación de nuevas herramientas BAT deberá realizarse sin romper la arquitectura existente ni introducir responsabilidades cruzadas.

ESTADO ACTUAL DEL ECOSISTEMA BAT

Al cierre de esta etapa puede considerarse concluida la reorganización funcional del ecosistema BAT.

Las herramientas principales han sido reorganizadas conforme a una arquitectura basada en responsabilidades independientes.

El flujo operativo ha quedado claramente definido y validado mediante pruebas funcionales.

El ecosistema BAT se considera estable y preparado para acompañar las siguientes fases de desarrollo del proyecto.

MANTENIMIENTO FUTURO

Las modificaciones futuras deberán respetar los principios establecidos en este documento.

En particular:

evitar mezclar responsabilidades;
mantener la separación entre Commit, Push y Deploy;
incorporar confirmaciones antes de operaciones críticas;
actualizar esta documentación cuando se modifique la arquitectura del ecosistema.
PUNTO OFICIAL DE RETOMA

Con la actualización de este documento puede darse por cerrada documentalmente la reorganización del ecosistema BAT.

La siguiente etapa del proyecto deja de estar centrada en la infraestructura técnica y pasa a concentrarse en el desarrollo funcional de recetas_app.

El siguiente frente de trabajo será la integración progresiva del Motor de Equivalencias dentro del flujo operativo normal de la aplicación.

Antes de cualquier implementación deberán identificarse, con evidencia de código, los puntos donde intervienen ingredientes, cantidades y unidades de medida, con el objetivo de determinar el primer proceso del sistema que utilizará el Motor de Equivalencias como servicio funcional.

Con ello queda concluida la documentación maestra del ecosistema BAT vigente.

