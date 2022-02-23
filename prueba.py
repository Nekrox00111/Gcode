from main import *

T45 = {
    'name': 'Fresa Plana de 0.3"',
    'label': 'T45',
    'rpm': '2400',
    'id': '45',
    'fv': 1.4,
    'fh': 4.0
}
T50 = {
    'name': 'Fresa Plana de 0.25"',
    'label': 'T50',
    'rpm': '6500',
    'id': '50',
    'fv': 1.6,
    'fh': 5.0
}

machine = CNC(
    id_proyecto='0004',
    nombre_proyecto="Aleta de Enfriamiento",
    x=0,
    y=0,
    z=0.3,
    refrigerante=False,
    posicion='absoluto',
    unidades='pulgadas',
    herramientas=[T45,T50],
    profundidad = -0.15
)

machine.compensacion_ala(
    derecha=False,
    x=1,
    y=2
)

machine.corte_lineal(
    x=1.5,
    y=3.2
)

machine.corte_enarco(
    dextrogiro=False,
    x=3.5,
    y=5.2,
    r=2.0
)

machine.change_tool(
    x=0.5,
    y=1.5,
    herramientas = 'T50',
    refrigerante = True
)

# machine.empty_circle(
#     x=1,
#     y=2,
#     profundidad=-0.15,
#     r=3/8,
#     dextrogiro=False
# )
# levanta la herramienta automaticamente

machine.empty_spiral(
    x=1,
    y=2,
    profundidad=-0.15,
    I_radio_Arco=0.05,
    K_radio = 3/8, 
    Q = 0.05,
    dextrogiro=False,
)


machine.mover(
    x=3,
    y=0
)

machine.corte_vertical(
    profundidad = -0.15 
)

machine.compensacion_ala(
    derecha = True,
    x=-1,
    y=-1
)

machine.ciclo_de_taladrado(
    tipo_taladro = CicloTaladro.centro, #CicloTaladro(.centro, .normal, .profundo)
    plano_taladro = Plano.retorno, #Retorno o Inicio 
    x=1,
    y=2,
    z=-0.06,
    p=1.25,
    r=0.2
)

machine.subrutina_interna(
    P=25
)

machine.final()

#SUBRUTINA DE TALADRADO
machine.mover(
    x= 3,
    y=5
)
machine.mover(
    x= 5,
    y=7
)
machine.mover(
    cambiar_plano=True,
    x= 7,
    y=9
)
machine.mover(
    x= 9,
    y=11
)

machine.mover(
    x= 3,
    y=5
)
machine.final_taladrado()

machine.final_subrutina()

#machine.exportar()
print(machine.code)