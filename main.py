class CNC:
    
    code = ''
    z=0
    tools=[]
    def __init__(self,x,y,position,units,tools,id_proyecto,project_name,depth,z):
        self.z = z
        self.tools = tools
        self.selected_tool=self.tools[0]
        units1 = 90
        position1 = 20

        if units != "pulgadas":
            units1 = 91 # milimetros
        if position != "absoluto":
            position1 = 21 # incremental  
        
        self.code += f'O{id_proyecto} ({project_name}) \n'
        self.code += f'T{self.selected_tool["id"]} M06 ({self.selected_tool["name"]})\n' 
        self.code += f'G{units1} G{position1} G54 X{x} Y{y}\n'
        self.code += f'S{self.selected_tool["rpm"]} M03\n'
        self.code += f'G43 H{self.selected_tool["h"]} Z{z}\n'
        self.code += f'G01 Z{depth} F{self.selected_tool["fv"]}\n'

    def print_code(self):
        lines = self.code.splitlines()
        code = ''
        print()
        for idx, line in enumerate(lines):
            code += f'N{idx}    {line}\n'

        print(code)


    def cut_line(self,x,y):
        self.code += f'G01 X{x} Y{y}\n'
    
    def cut_vertical(self,depth):
        self.code += f'G01 Z{depth} F{self.selected_tool["fv"]}\n'
    
    def arc_cut(self,x,y,clockwise,r):
        
        if clockwise == True:
            self.code += f'G02 X{x} Y{y} R{r}\n'
        else:
            self.code += f'G03 X{x} Y{y} R{r}\n'


    def change_tool(self,tools1,x,y):
        
        tool_found = [tool for tool in self.tools if tool.get('id') == tools1]
        if not tool_found:
            tool_found = [tool for tool in self.tools if tool.get('name') == tools1]
        if not tool_found:
            tool_found = [tool for tool in self.tools if tool.get('label') == tools1]
        if not tool_found:
            raise Exception('¡No se encontro herramienta deseada!')
            
        self.selected_tool = tool_found[0]

        self.code += f'G00 Z{self.z} \n' 
        self.code += f'G53 G49 Z0 M05 \n'
        self.code += f'T{self.selected_tool["id"]} M06 ({self.selected_tool["name"]})\n' 
        self.code += f'G54 G00 X{x} Y{y} \n'
        self.code += f'S{self.selected_tool["rpm"]} M03 \n'
        self.code += f'G43 H{self.selected_tool["h"]} Z{self.z} \n' 
    
    def empty_circle(self,clockwise,x,y,depth,r):
        if clockwise == True:
            self.code += f'G12 X{x} Y{y} Z{depth} I{r} D{self.selected_tool["d"]} F{self.selected_tool["fh"]}\n'
        else:
            self.code += f'G13 X{x} Y{y} Z{depth} I{r} D{self.selected_tool["d"]} F{self.selected_tool["fh"]}\n'
        self.code += f'G00 Z{self.z} G40 \n'

    # def empty_spiral(self,clockwise,x,y,depth,r):
    #     if clockwise == True:
    #         self.code += f'G12 X{x} Y{y} Z{depth} I{r} D{self.selected_tool["d"]} F{self.selected_tool["fh"]}\n'
    #     else:
    #         self.code += f'G13 X{x} Y{y} Z{depth} I{r} D{self.selected_tool["d"]} F{self.selected_tool["fh"]}\n'
    #     self.code += f'G00 Z{z} G40 \n'

    def move(self,x,y):
        self.code += f'G00 X{x} Y{y} G40 \n'
    
    def compensacion_ala(self,derecha,x,y):
        if derecha == True:
            self.code += f'G42 X{x} Y{y} D{self.selected_tool["d"]} F{self.selected_tool["fh"]} \n'
        else:
            self.code += f'G41 X{x} Y{y} D{self.selected_tool["d"]} F{self.selected_tool["fh"]} \n'


    def exit(self,position):
        position1 = 91
        
        if position != "incremental":
            position1 = 90 # absoluto
        
        self.code += f'G00 Z{self.z} G40\n'
        self.code += f'G28 G{position1} Z0.0 M05\n'
        self.code += f'M30'


if __name__ == '__main__':
    cnc = CNC()
    cnc.print_code()