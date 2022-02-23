from main import CNC

T01 = {
    'name': 'Fresa Plana de 0.25"',
    'label': 'T01',
    'rpm': '6500',
    'id': '01',
    'fv': 1.6,
    'fh': 5.0
}

maquina = CNC(
    id_proyecto='0426',
    nombre_proyecto='Robot Face',
    herramientas=[T01],
    refrigerante=False,
    unidades='pulgadas',
    posicion='absoluto',
    z=0.25,
    profundidad=-0.15,
    x=-0.4,
    y=0.4
)

maquina.compensacion_ala(
    derecha=True,
    x=-0.4,
    y=0.6
)

maquina.corte_enarco(
    dextrogiro=True,
    r=0.2,
    x=-0.4,
    y=0.2
)

maquina.corte_enarco(
    dextrogiro=True,
    r=0.2,
    x=-0.4,
    y=0.6
)

maquina.mover(
    fuera_material=True,
    x=0.4,
    y=0.4
)

maquina.corte_vertical(
    profundidad=-0.15
)

maquina.compensacion_ala(
    derecha=True,
    x=0.4,
    y=0.6
)
maquina.corte_enarco(
    dextrogiro=True,
    r=0.2,
    x=0.4,
    y=0.2
)
maquina.corte_enarco(
    dextrogiro=True,
    r=0.2,
    x=0.4,
    y=0.6
)

maquina.mover(
    fuera_material=True,
    x=0,
    y=0
)

maquina.corte_vertical(
    profundidad=-0.15
)

maquina.mover(
    fuera_material=True,
    x=0.4,
    y=-0.3
)

maquina.corte_vertical(
    profundidad=-0.15
)

maquina.corte_lineal(
    x=0.4,
    y=-0.4
)

maquina.corte_lineal(
    x=-0.4,
    y=-0.4
)

maquina.corte_lineal(
    x=-0.4,
    y=-0.3
)

maquina.mover(
    fuera_material=True,
    x=-1,
    y=-1.25
)

maquina.corte_vertical(
    profundidad=-0.15
)

maquina.compensacion_ala(
    derecha=True,
    x=-1.0,
    y=-1.0
)

maquina.corte_lineal(
    x=1.0,
    y=-1.0
)

maquina.corte_lineal(
    x=1.0,
    y=1.0
)

maquina.corte_lineal(
    x=-1.0,
    y=1.0
)

maquina.corte_lineal(
    x=-1.0,
    y=-1.0
)

maquina.final()

maquina.exportar(file_name="Robot Face.nc")
print(maquina.code)

