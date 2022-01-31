from main import CNC

T1 = {
    'name': 'Fresa Plana de 0.3"',
    'label': 'T1',
    'rpm': '7000',
    'h': '03',
    'd': '03',
    'id': '03',
    'fv': 1.4,
    'fh': 4.0
}
T2 = {
    'name': 'Fresa Plana de 0.25"',
    'label': 'T2',
    'rpm': '6500',
    'h': '01',
    'd': '01',
    'id': '01',
    'fv': 1.6,
    'fh': 5.0
}

machine = CNC(
    id_proyecto=5555,
    project_name="Aleta de Enfriamiento",
    x=2.5,
    y=3.1,
    z=0.25,
    position='absoluto',
    units='pulgadas',
    tools=[T1,T2],
    depth = -0.15
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
    tools1 = 'T2'
)

machine.empty_circle(
    x=1,
    y=2,
    depth=-0.15,
    r=3/8,
    clockwise=False
)
# levanta la herramienta automaticamente

# machine.empty_spiral(
#     x=1,
#     y=2,
#     depth=-0.15,
#     r=3/8,
#     clockwise=False,
# )


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

machine.exit(
    position ="incremental"
)

machine.print_code()

# machine.export('prueba.gcode')
