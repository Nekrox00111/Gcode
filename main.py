from settings import MACHINE_SETTINGS
#from prueba import CNC

tool_position = []

class CNC:
    code = ''

    def change_tool(self,tool_position):
        self.code += f'T{tool_position[1]} M6 \n' 
        #Recordar que 'H' y 'D' son la compensacion de Altura y Diametro con el mismo "tool_position"

    def __init__(self,x,y,position,units,tools,id_proyecto,project_name):

        if units == "pulgadas":
            units1 = 90 # pulgadas
        else:
            units1 = 91 # milimetros

        if position == "absoluto":
            position1 = 20 # absoluto
        else:
            position1 = 21 #incremental

        # if units1 != "pulgadas":
        #     units1 = 91 # milimetros
        # if position1 != "absoluto":
        #     position1 = 21 # incremental  
        
        self.code += f'O{id_proyecto} ({project_name}) \n'
        self.code += f'T{tools[0]["id"]} M06 \n' 
        #self.code += f'T{MACHINE_SETTINGS["tools"][0]["id"]} M06 \n' 
        self.code += f'G{units1} G{position1} G54 X{x} Y{y}\n'
        self.code += f'S{tools[0]["rpm"]} M03\n'


    def print_code(self):
        lines = self.code.splitlines()
        code = ''
        for idx, line in enumerate(lines):
            code += f'N{idx+1}    {line}\n'

        print(code)



if __name__ == '__main__':
    cnc = CNC()
    cnc.print_code()