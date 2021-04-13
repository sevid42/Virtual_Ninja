#La fuente de las imagenes es: https://www.gameart2d.com/uploads/3/0/9/1/30917885/ninjaadventurenew.zip
"""
Desarrollador: Jose Fierro
Email: fierro.moya@gmail.com
Fecha: 12/04/2021

Fuente de Imagenes: https://www.gameart2d.com/uploads/3/0/9/1/30917885/ninjaadventurenew.zip
"""
import tkinter as tk
import time
import random
import os
from os import scandir, getcwd
#para transformar png a gif
from PIL import Image, ImageTk
import pathlib
import ctypes #para obtener dimenciones de pantalla

#obtengo dimensiones de pantalla
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
global ancho_pantalla
global alto_pantalla
ancho_pantalla, alto_pantalla = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

impath = pathlib.Path(__file__).parent.absolute()
impath=str(impath)+'\\png\\'

def conv_tk_img_list(final_path):
    files_names= []
    files= sorted([arch.name for arch in scandir(final_path) if arch.is_file()])
    tk_list=[]
    for file_name in files:
        final_file_name=(final_path+'\\'+file_name)
        tk_list.append(tk.PhotoImage(file=final_file_name))
    return tk_list
        

window = tk.Tk()

idle = conv_tk_img_list(impath+'Idle') #estado 0
run_left = conv_tk_img_list(impath+'run_left') #estado 1
run_right = conv_tk_img_list(impath+'run_right') #estado 2
climb_up = conv_tk_img_list(impath+'climb_up') #estado 3
climb_down = conv_tk_img_list(impath+'climb_down') #estado 4

#lista de imagenes de la accion, DIMENSIONES  ,   numero de imagenes  ,   acciones a las q me puedo mover    ,   pixeles +- en x,    pixeles +- en y
#al repetir mas los numeros en la lista de acciones  q puede realizar aumento la probabilidad
datos_por_accion=[
    [idle,'42x80',10,[0,1,2],0,0]
    ,[run_left,'63x80',10,[0,0,0,1,1,1,1,1,1,3,4],-5,0]
    ,[run_right,'63x80',10,[0,0,0,2,2,2,2,2,2,3,4],5,0]

    ,[climb_up,'49x80',10,[0,3,3,3,3,3,3,3,3,4],0,-4]
    ,[climb_down,'49x80',10,[0,3,4,4,4,4,4,4,4,4],0,4]
]
#contara el numero de la imagen en q va de la accion
ciclos=0
accion_actual=0

#posicion del personaje
x=round(ancho_pantalla/2)
y=round(alto_pantalla-180)


def update(datos_por_accion,ciclos,accion_actual,x,y):


    if ciclos >= datos_por_accion[accion_actual][2]:
        #elijo la siguiente accion
        ciclos=0
        siguiente_accion = random.randrange(0,len(datos_por_accion[accion_actual][3]),1)
        accion_actual=datos_por_accion[accion_actual][3][siguiente_accion]
    else:
        if x<100: # si se esta acercando al borde de la pantalla lo mando al centro
            ciclos=0
            accion_actual=2
        elif x>ancho_pantalla-100: # si se esta acercando al borde de la pantalla lo mando al centro
            ciclos=0
            accion_actual=1
        elif y<180: # si se esta acercando al borde de la pantalla lo mando al centro
            ciclos=0
            accion_actual=4
        elif y>alto_pantalla-200: # si se esta acercando al borde de la pantalla lo mando al centro
            ciclos=0
            accion_actual=3

        x = x + datos_por_accion[accion_actual][4]
        y = y + datos_por_accion[accion_actual][5]

    frame = datos_por_accion[accion_actual][0][ciclos]
    ciclos=ciclos+1
    
    window.geometry(datos_por_accion[accion_actual][1]+'+'+str(x)+'+'+str(y)) #100x100 es el ancho y alto de la ventana, 850 es la distancia desde arriba de la pantalla, x es distancia desde la izquieda de la pantalla
    label.configure(image=frame)
    
    window.after(40,update,datos_por_accion,ciclos,accion_actual,x,y)


window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')#con esto podemos poner fotos o texto , es como el telon para ello, aca le decimos q no tenga bordes y q fondo negro
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')#segun entiendo reemplaza el negro por transparente

#debe estar, por defecto esto ,muestra configura una ventana, si especifco mas muestro sub partes dentro de la ventana
label.pack()

window.after(1,update,datos_por_accion,ciclos,accion_actual,x,y)

window.mainloop()
