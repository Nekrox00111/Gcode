## PyCode

_Consiste en una libreria que genera código G._

## Ejemplos

_Hay tres ejemplos de como utilizar esta libreria en el repositorio._

* Robot Face.py
* prueba.py

## Inicializando un proyecto

``` python
from PyCode import CNC #importamos CNC de la libreria PyCode
#Otras clases a importar: CicloTaladro y Plano.

#Asignando valores de herramientas
    T01 = {
        'name': 'Fresa Plana de 0.25"', #Nombre de la herramienta y tamaño
        'label': 'T01', #Posicion de la herramienta
        'rpm': '6500', #velocidad revoluciones del husillo 
        'id': '01', #numero identificador de la herramienta
        'fv': 1.4, #Velocidad vertical de la herramienta
        'fh': 4.0  #Velocidad horizontal de la herramienta
    }
    #Si se requiere de mas herramientas seguir el mismo procedimiento de T01 y cambiarle numero, id y label.

    maquina = CNC( #Asignamos una variable para que herede todo lo de la clase CNC
        id_proyecto='0426', #Numero que identifica el proyecto en Código G
        nombre_proyecto='Robot Face', #Nombre del proyecto en Código G
        herramientas=[T01], #Herramientas a utilizar al dado caso de tener mas herramientas = [T01,T02,...]
        refrigerante=False, #refrigerante si se requiere refrigerante o no,(Valor predeterminado False "Apagado")
        unidades='pulgadas', #Unidades: pulgadas o milimetros
        posicion='absoluto', #Tipo de posicion: absoluto o incremental
        z=0.25, #Altura entre la herramienta y el material a fresar 
        profundidad=-0.15, #profundidad de corte para la velocidad vertical
        x=-0.4, #posicionamiento en el eje X
        y=0.4 #posicionamiento en el eje Y
        #XY estan para establecer la velocidad horizontal
)
```

## Tipos de Cortes
**Siguiendo el mismo programa de la seccion de "Inicializando un proyecto"**

``` python

maquina.corte_lineal(
    x=1.5, #coordenada final del corte en X
    y=3.2  #coordenada final del corte en Y
)

maquina.corte_enarco(
    dextrogiro=False,#Corte en contra de las agujas del reloj, valor predeterminado True (Con las agujas del reloj)
    x=3.5, #coordenada final del corte en X
    y=5.2, #coordenada final del corte en Y
    r=2.0 #radio de 2 unidades
)

maquina.corte_vertical(
    profundidad = -0.15 #profundidad de corte, normalmente se utiliza con el metodo de mover.
)

```
## Mover
``` python

maquina.mover(
    x=3, #coordenada final del corte en X
    y=0, #coordenada final del corte en Y
    cambiar_plano=False#Argumento opcional, predeterminado: cambiar_plano=False.  
    fuera_material=False#Argumento opcional, predeterminado: fuera_material=False. Si se requiere salir del material, valor de Z definida en la seccion "Inicializando un proyecto"
)
```
*NO SON OPCIONALES cuando se utiliza el metodo "ciclo_de_taladro"*

## Cambio de herramienta
``` python

maquina.change_tool(
    x=0.5, #posicion X del siguiente corte
    y=1.5, #posicion Y del siguiente corte
    herramientas = 'T50', #buscador a traves de id, nombre de la herramienta o el label
    refrigerante = True #Se requiere refrigerante
)

```
## Vaciados
``` python

maquina.empty_circle(
    x=1, #Coordenada en X del entro del vaciado
    y=2, #Coordenada en Y del entro del vaciado
    profundidad=-0.15, #Profundidad del vaciado
    r=3/8, #Radio del vaciado
    dextrogiro=False#Corte en contra de las agujas del reloj, valor predeterminado True (Con las agujas del reloj)
)

maquina.empty_spiral(
    x=1, #Coordenada en X del entro del vaciado
    y=2, #Coordenada en Y del entro del vaciado
    profundidad=-0.15, #Profundidad del vaciado
    I_radio_Arco=0.05, #Radio del primer arco
    Q = 0.05, #Distancia entre recorridos del espiral
    #I=Q <= Diametro REAL de la herramienta de corte
    K_radio = 3/8, #Radio del Vaciado
    dextrogiro=False,#Corte en contra de las agujas del reloj, valor predeterminado True (Con las agujas del reloj)
)

```
## Compensacion a la derecha/izquierda
``` python

maquina.compensacion_ala(
    derecha=False, #Tipo de compensacion de corte. Valor predeterminado: True, argumento opcional si se requiere que sea a la derecha.
    x=-0.4, #Coordenada X del inicio de la compensacion de corte
    y=0.6 #Coordenada Y del inicio de la compensacion de corte
)
```
## Ciclo de taldrado
*maquina.mover se utiliza con cambiar_plano y fuera_material.*
``` python

maquina.ciclo_de_taladrado(
    plano_taladro= # Plano.retorno o Plano.inicio
    r= # Altura del plano de retorno
    tipo_taladro= # CicloTaladro.centro, CicloTaladro.normal, CicloTaladro.profundo
    x= # Coordenada X del T1
    y= # Coordenada Y del T1
    z= # Profundidad de los taladrados del ciclo -2mm, -3mm, -0.06",-0.1
    p= #se utiliza cuando el tipo_taladrado = CicloTaladro.centro
    #No se requiere en otro tipo de taladrado
    #Tiempo en segundos que la herramienta espera cuando ha llegado a la profundidad especificada, antes de moverse al siguiente punto
    q= #se utiliza cuando el tipo_taladrado = CicloTaladro.profundo
    #No se requiere en otro tipo de taladrado
    #Diferencial de profundidad que se utiliza para descender hasta llegar a la profundiad Z.
)
maquina.mover(...)
maquina.final_taladrado() #solo se requiere cuando el ciclo se termina

```

## Subrutinas
``` python

maquina.subrutina_interna(
    P=25 #Linea donde se encuentra la subrutina
)

maquina.subrutina_externa(
    P='0004' #Numero identificador de proyecto
)

maquina.final_subrutina() #Fin de subrutina externa o interna.

```
## Finalizacion de un proyecto
*Orden recomendado para el uso de subrutinas internas por la señalizacion de cantidad de lineas*
``` python

maquina.final() #Códigos necesarios para finalizar el programa

maquina.exportar(file_name="Robot Face.nc") #Exportar en un archivo con extension .gcode, .nc, .txt, entre otros.
print(maquina.code) #Exponer en texto plano el código G generado.

```
*También existe la opcion de alternar el print primero.*

*No muestra la cantidad lineas de codigo.*
``` python

maquina.final() #Códigos necesarios para finalizar el programa
print(maquina.code) #Exponer en texto plano el código G generado.

maquina.exportar(file_name="Robot Face.nc") #Exportar en un archivo con extension .gcode, .nc, .txt, entre otros.
```
*Existe la opcion de solo exportar a un archivo como solo exponerlo en texto plano*

## Desarrollado en 🐍

* [Python](http://www.python.org) - El lenguaje de programacion usado

## Autor✒️

* **Gonzalo Valle** - *Programación y Documentación* - [Nekrox00111](https://github.com/Nekrox00111)

## Agradecimiento

* **Isaías A. Valle** - *Asesor* - [guitartsword](https://github.com/guitartsword)
