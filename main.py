from enum import Enum

class CicloTaladro(Enum):
    normal = '81'
    centro = '82'
    profundo = '83'

class Plano(Enum):
    retorno = '99'
    inicio = '98'

class CNC:
    
    code = ''
    z=0
    tools=[]
    refrigerante = False
    position=''
    #subrutinas = [sr1, sr2]

    def __init__(self,x,y,position,units,tools,id_proyecto,project_name,depth,z,refrigerante):
        self.project_name = project_name
        self.position = position
        self.z = z
        self.tools = tools
        self.refrigerante = refrigerante
        self.selected_tool=self.tools[0]

        units1 = 90
        position1 = 20
        
        if units != "pulgadas":
            units1 = 91 # milimetros
        if position != "absoluto":
            position1 = 21 # incremental  
        
        self.code += f'O{id_proyecto} ({project_name}) \n'
        self.code += f'T{self.selected_tool["id"]} M06 ({self.selected_tool["name"]})\n' 
        self.code += f'G{units1} G{position1} G54 G00 X{x} Y{y}\n'
        self.code += f'S{self.selected_tool["rpm"]} M03\n'

        if self.refrigerante == True:
            self.code += f'G43 H{self.selected_tool["id"]} Z{z} M08\n'
        else:
            self.code += f'G43 H{self.selected_tool["id"]} Z{z}\n'
        
        self.code += f'G01 Z{depth} F{self.selected_tool["fv"]}\n'

    def export(self,file_name=''):
        lines = self.code.splitlines()
        code = ''
        print()
        # for sub in self.subrutinas:
        #     sub()
        #     self.code += 'M99 ({sub.__name__})\n'
        for idx, line in enumerate(lines):
            code += f'N{idx}    {line}\n'
        
        exported_filename = file_name or f'{self.project_name}.gcode'

        with open(exported_filename,'w') as f:
            f.write(code)


    def cut_line(self,x,y):
        self.code += f'G01 X{x} Y{y}\n'
    
    def cut_vertical(self,depth):
        self.code += f'G01 Z{depth} F{self.selected_tool["fv"]}\n'
    
    def arc_cut(self,x,y,clockwise,r):
        
        if clockwise == True:
            self.code += f'G02 X{x} Y{y} R{r}\n'
        else:
            self.code += f'G03 X{x} Y{y} R{r}\n'


    def change_tool(self,tools,x,y,refrigerante):
        
        tool_found = [tool for tool in self.tools if tool.get('id') == tools]
        if not tool_found:
            tool_found = [tool for tool in self.tools if tool.get('name') == tools]
        if not tool_found:
            tool_found = [tool for tool in self.tools if tool.get('label') == tools]
        if not tool_found:
            raise Exception('¡No se encontro herramienta deseada!')

        self.selected_tool = tool_found[0]

        if self.refrigerante == True:
            self.code += f'G00 Z{self.z} M09\n'
        else:
            self.code += f'G00 Z{self.z}\n'

        self.code += f'G53 G49 Z0 M05 \n'
        self.code += f'T{self.selected_tool["id"]} M06 ({self.selected_tool["name"]})\n' 
        self.code += f'G54 G00 X{x} Y{y} \n'
        self.code += f'S{self.selected_tool["rpm"]} M03 \n'

        self.refrigerante = refrigerante

        if refrigerante == True:
            self.code += f'G43 H{self.selected_tool["id"]} Z{self.z} M08\n'
        else:
            self.code += f'G43 H{self.selected_tool["id"]} Z{self.z} \n' 

    def empty_circle(self,clockwise,x,y,depth,r):
        if clockwise == True:
            self.code += f'G12 X{x} Y{y} Z{depth} I{r} D{self.selected_tool["id"]} F{self.selected_tool["fh"]}\n'
        else:
            self.code += f'G13 X{x} Y{y} Z{depth} I{r} D{self.selected_tool["id"]} F{self.selected_tool["fh"]}\n'
        self.code += f'G00 Z{self.z} G40 \n'

    def empty_spiral(self,clockwise,x,y,depth,K_radio,I_radio_Arco,Q):
        if clockwise == True:
            self.code += f'G12 X{x} Y{y} Z{depth} I{I_radio_Arco} K{K_radio} Q{Q} D{self.selected_tool["id"]} F{self.selected_tool["fh"]}\n'
        else:
            self.code += f'G13 X{x} Y{y} Z{depth} I{I_radio_Arco} K{K_radio} Q{Q} D{self.selected_tool["id"]} F{self.selected_tool["fh"]}\n'
        self.code += f'G00 Z{self.z} G40 \n'

    def move(self,x,y):
        self.code += f'G00 Z{self.z} G40 \n'
        self.code += f'G00 X{x} Y{y}\n'
        
    def compensacion_ala(self,derecha,x,y):
        if derecha == True:
            self.code += f'G42 X{x} Y{y} D{self.selected_tool["id"]} F{self.selected_tool["fh"]} \n'
        else:
            self.code += f'G41 X{x} Y{y} D{self.selected_tool["id"]} F{self.selected_tool["fh"]} \n'

    def ciclo_de_taladrado(self,tipo_taladro,plano_taladro,x,y,z,r,p=None,q=None):
        tipo_taladro_valor = tipo_taladro.value
        plano_taladro_valor = plano_taladro.value
        if tipo_taladro_valor == '82':
            self.code += f'G{tipo_taladro_valor} G{plano_taladro_valor} X{x} Y{y} Z{z} P{p} R{r} F{self.selected_tool["fv"]} \n'
        elif tipo_taladro_valor== '83':
            self.code += f'G{tipo_taladro_valor} G{plano_taladro_valor} X{x} Y{y} Z{z} Q{q} R{r} F{self.selected_tool["fv"]} \n'
        else:
            self.code += f'G{tipo_taladro_valor} G{plano_taladro_valor} X{x} Y{y} Z{z} R{r} F{self.selected_tool["fv"]} \n'

    def exit(self):
        position1 = 90
        
        if self.position != "incremental":
            position1 = 91 # absoluto
        
        if self.refrigerante == True:
            self.code += f'G00 Z{self.z} G40 M09\n'
        else:
            self.code += f'G00 Z{self.z} G40\n'

        self.code += f'G28 G{position1} Z0.0 M05\n'
        self.code += f'M30\n'
        #self.subrutinas[0] =




    def subrutina_externa(self,P):
        self.code += f'M98 P{P}'



if __name__ == '__main__':
    cnc = CNC()
    cnc.export()