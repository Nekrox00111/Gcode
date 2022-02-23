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
    herramientas=[]
    refrigerante = False
    posicion=''


    def __init__(self,x,y,posicion,unidades,herramientas,id_proyecto,nombre_proyecto,profundidad,z,refrigerante):
        self.nombre_proyecto = nombre_proyecto
        self.posicion = posicion
        self.z = z
        self.herramientas = herramientas
        self.refrigerante = refrigerante
        self.herramienta_seleccionada=self.herramientas[0]

        unidades_num = 90
        posicion_num = 20
        
        if unidades != "pulgadas":
            unidades_num = 91
        if posicion != "absoluto":
            posicion_num = 21 
        
        self.code += f'O{id_proyecto} ({nombre_proyecto}) \n'
        self.code += f'T{self.herramienta_seleccionada["id"]} M06 ({self.herramienta_seleccionada["name"]})\n' 
        self.code += f'G{unidades_num} G{posicion_num} G54 G00 X{x} Y{y}\n'
        self.code += f'S{self.herramienta_seleccionada["rpm"]} M03\n'

        if self.refrigerante == True:
            self.code += f'G43 H{self.herramienta_seleccionada["id"]} Z{z} M08\n'
        else:
            self.code += f'G43 H{self.herramienta_seleccionada["id"]} Z{z}\n'
        
        self.code += f'G01 Z{profundidad} F{self.herramienta_seleccionada["fv"]}\n'

    def exportar(self,file_name=''):
        lines = self.code.splitlines()
        code = ''

        for idx, line in enumerate(lines):
            code += f'N{idx}    {line}\n'
            self.code = code
        
        exported_filename = file_name or f'{self.nombre_proyecto}.gcode'

        with open(exported_filename,'w') as f:
            f.write(code)


    def corte_lineal(self,x,y):
        self.code += f'G01 X{x} Y{y}\n'
    
    def corte_vertical(self,profundidad):
        self.code += f'G01 Z{profundidad} F{self.herramienta_seleccionada["fv"]}\n'
    
    def corte_enarco(self,x,y,dextrogiro,r):
        
        if dextrogiro == True:
            self.code += f'G02 X{x} Y{y} R{r}\n'
        else:
            self.code += f'G03 X{x} Y{y} R{r}\n'


    def change_tool(self,herramientas,x,y,refrigerante):
        
        herramienta_encontrada = [tool for tool in self.herramientas if tool.get('id') == herramientas]
        if not herramienta_encontrada:
            herramienta_encontrada = [tool for tool in self.herramientas if tool.get('name') == herramientas]
        if not herramienta_encontrada:
            herramienta_encontrada = [tool for tool in self.herramientas if tool.get('label') == herramientas]
        if not herramienta_encontrada:
            raise Exception('¡No se encontro herramienta deseada!')

        self.herramienta_seleccionada = herramienta_encontrada[0]

        if self.refrigerante == True:
            self.code += f'G00 Z{self.z} M09\n'
        else:
            self.code += f'G00 Z{self.z}\n'

        self.code += f'G53 G49 Z0 M05 \n'
        self.code += f'T{self.herramienta_seleccionada["id"]} M06 ({self.herramienta_seleccionada["name"]})\n' 
        self.code += f'G54 G00 X{x} Y{y} \n'
        self.code += f'S{self.herramienta_seleccionada["rpm"]} M03 \n'

        self.refrigerante = refrigerante

        if refrigerante == True:
            self.code += f'G43 H{self.herramienta_seleccionada["id"]} Z{self.z} M08\n'
        else:
            self.code += f'G43 H{self.herramienta_seleccionada["id"]} Z{self.z} \n' 

    def empty_circle(self,dextrogiro,x,y,profundidad,r):
        if dextrogiro == True:
            self.code += f'G12 X{x} Y{y} Z{profundidad} I{r} D{self.herramienta_seleccionada["id"]} F{self.herramienta_seleccionada["fh"]}\n'
        else:
            self.code += f'G13 X{x} Y{y} Z{profundidad} I{r} D{self.herramienta_seleccionada["id"]} F{self.herramienta_seleccionada["fh"]}\n'
        self.code += f'G00 Z{self.z} G40 \n'

    def empty_spiral(self,dextrogiro,x,y,profundidad,K_radio,I_radio_Arco,Q):
        if dextrogiro == True:
            self.code += f'G12 X{x} Y{y} Z{profundidad} I{I_radio_Arco} K{K_radio} Q{Q} D{self.herramienta_seleccionada["id"]} F{self.herramienta_seleccionada["fh"]}\n'
        else:
            self.code += f'G13 X{x} Y{y} Z{profundidad} I{I_radio_Arco} K{K_radio} Q{Q} D{self.herramienta_seleccionada["id"]} F{self.herramienta_seleccionada["fh"]}\n'
        self.code += f'G00 Z{self.z} G40 \n'

    def mover(self,x,y,fuera_material=False,cambiar_plano = False):
        
        if fuera_material==True:
            self.code += f'G00 Z{self.z} G40 \n'
            self.code += f'G00 X{x} Y{y}\n'
        elif cambiar_plano == True:
            if self.plano_taladro_valor == '98':
                self.plano_taladro_valor = '99'
                self.code += f'G99 X{x} Y{y}\n'
            else:
                self.plano_taladro_valor = '98'
                self.code += f'G98 X{x} Y{y} \n'
        else:
            self.code += f'X{x} Y{y}\n'
        
    def compensacion_ala(self,derecha,x,y):
        if derecha == True:
            self.code += f'G42 X{x} Y{y} D{self.herramienta_seleccionada["id"]} F{self.herramienta_seleccionada["fh"]} \n'
        else:
            self.code += f'G41 X{x} Y{y} D{self.herramienta_seleccionada["id"]} F{self.herramienta_seleccionada["fh"]} \n'

    def ciclo_de_taladrado(self,tipo_taladro,plano_taladro,x,y,z,r,p=None,q=None):
        tipo_taladro_valor = tipo_taladro.value
        plano_taladro_valor = plano_taladro.value
        self.plano_taladro_valor = plano_taladro_valor

        if tipo_taladro_valor == '82':
            self.code += f'G{tipo_taladro_valor} G{plano_taladro_valor} X{x} Y{y} Z{z} P{p} R{r} F{self.herramienta_seleccionada["fv"]} \n'
        elif tipo_taladro_valor== '83':
            self.code += f'G{tipo_taladro_valor} G{plano_taladro_valor} X{x} Y{y} Z{z} Q{q} R{r} F{self.herramienta_seleccionada["fv"]} \n'
        else:
            self.code += f'G{tipo_taladro_valor} G{plano_taladro_valor} X{x} Y{y} Z{z} R{r} F{self.herramienta_seleccionada["fv"]} \n'

    def final(self):
        position1 = 90
        
        if self.posicion != "incremental":
            position1 = 91
        
        if self.refrigerante == True:
            self.code += f'G00 Z{self.z} G40 M09\n'
        else:
            self.code += f'G00 Z{self.z} G40\n'

        self.code += f'G28 G{position1} Z0.0 M05\n'
        self.code += f'M30\n'


    def subrutina_interna(self,P):
        self.code += f'M97 P{P}\n'
    
    def subrutina_externa(self,P):
        self.code += f'M98 P{P}\n'

    def final_subrutina(self):
        self.code += f'M99\n'

    def final_taladrado(self):
        self.code += f'G80\n'
    

if __name__ == '__main__':
    cnc = CNC()
    cnc.exportar()