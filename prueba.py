from main    import CNC

T1 = {
    'label': 'Excavadora corta',
    'name': 'Excavator23',
    'rpm': '7000',
    'h': 23,
    'id': 23,
}
T2 = {
    'label': 'Excavadora larga',
    'name': 'Excavator44',
    'h': 44,
    'id': 44,
}

machine = CNC(
    id_proyecto=1234,
    project_name="Aleta de Enfriamiento",
    x=1,
    y=2,
    position='incremental',
    units='milimetro',
    tools=[T1,T2]
)


# fh ya la sabe la maquina
# machine.empty_circle(
#     x=1,
#     y=2,
#     depth=0.15,
#     r=3/8,
#     clockwise=False
# )
# levantar pieza ya lo hace automaticamente
# machine.empty_circle(
#     x=3,
#     y=2,
#     depth=0.15,
#     r=5/8,
# )
# machine.change_tool(T2)
# machine.move(x=3, y=0)
# machine.cut_line((-0.4,0.2), (0.4,0.6))
# machine.stop()

machine.print_code()
# machine.export('prueba.gcode')
