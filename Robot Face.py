from main import CNC

T01 = {
    'name': 'Fresa Plana de 0.25"',
    'label': 'T01',
    'rpm': '6500',
    'id': '01',
    'fv': 1.6,
    'fh': 5.0
}

machine = CNC(
    id_proyecto='0426',
    project_name='Robot Face',
    tools=[T01],
    refrigerante=False,
    units='pulgadas',
    position='absoluto',
    z=0.25,
    depth=-0.15,
    x=-0.4,
    y=0.4
)

machine.compensacion_ala(
    derecha=True,
    x=-0.4,
    y=0.6
)

machine.arc_cut(
    clockwise=True,
    r=0.2,
    x=-0.4,
    y=0.2
)

machine.arc_cut(
    clockwise=True,
    r=0.2,
    x=-0.4,
    y=0.6
)

machine.move(
    x=0.4,
    y=0.4
)

machine.cut_vertical(
    depth=-0.15
)

machine.compensacion_ala(
    derecha=True,
    x=0.4,
    y=0.6
)
machine.arc_cut(
    clockwise=True,
    r=0.2,
    x=0.4,
    y=0.2
)
machine.arc_cut(
    clockwise=True,
    r=0.2,
    x=0.4,
    y=0.6
)

machine.move(
    x=0,
    y=0
)

machine.cut_vertical(
    depth=-0.15
)

machine.move(
    x=0.4,
    y=-0.3
)

machine.cut_vertical(
    depth=-0.15
)

machine.cut_line(
    x=0.4,
    y=-0.4
)

machine.cut_line(
    x=-0.4,
    y=-0.4
)

machine.cut_line(
    x=-0.4,
    y=-0.3
)

machine.move(
    x=-1,
    y=-1.25
)

machine.cut_vertical(
    depth=-0.15
)

machine.compensacion_ala(
    derecha=True,
    x=-1.0,
    y=-1.0
)

machine.cut_line(
    x=1.0,
    y=-1.0
)

machine.cut_line(
    x=1.0,
    y=1.0
)

machine.cut_line(
    x=-1.0,
    y=1.0
)

machine.cut_line(
    x=-1.0,
    y=-1.0
)

machine.exit()
#print(machine.code)
machine.export()
