from main import CNC, CicloTaladro,Plano

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
    project_name="Aleta de Enfriamiento",
    x=0,
    y=0,
    z=0.3,
    refrigerante=False,
    position='absoluto',
    units='pulgadas',
    tools=[T45,T50],
    depth = -0.15
)

machine.compensacion_ala(
    derecha=False,
    x=1,
    y=2
)

machine.cut_line(
    x=1.5,
    y=3.2
)

machine.arc_cut(
    clockwise=False,
    x=3.5,
    y=5.2,
    r=2.0
)

machine.change_tool(
    x=0.5,
    y=1.5,
    tools = 'T50',
    refrigerante = True
)

# machine.empty_circle(
#     x=1,
#     y=2,
#     depth=-0.15,
#     r=3/8,
#     clockwise=False
# )
# levanta la herramienta automaticamente

machine.empty_spiral(
    x=1,
    y=2,
    depth=-0.15,
    I_radio_Arco=0.05, #Es la I  
    K_radio = 3/8, #          I = Q <= Diametro Real de la herramienta de corte osea D(id de pieza)
    Q = 0.05,#Distancia entre recorridos de espiral
    clockwise=False,
)


machine.move(
    x=3,
    y=0
)

machine.cut_vertical(
    depth = -0.15 
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

    #FALTA MODIFICAR el machine.move()
)

machine.subrutina_externa(
    P=1023
)

machine.exit()

machine.export()


def subrutina_interna(machine):
    machine.compensacion_ala(
        derecha=False,
        x=1,
        y=2
    )

    machine.cut_line(
        x=1.5,
        y=3.2
    )

    machine.arc_cut(
        clockwise=False,
        x=3.5,
        y=5.2,
        r=2.0
    )

#ref_subrutina = machine.crear_subrutina_interna(subrutina_interna)
#machine.llamar_subrutina_interna(ref_subrutina)