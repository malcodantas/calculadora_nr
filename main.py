import tkinter as tk
from ultil import calcular
calc = tk.Tk()
calc.title("Calculadora NR")

####### Dimensões da janela e posicionamento na tela
width_box=500
height_box=250

# height_screen=calc.winfo_screenwidth()
# width_screen=calc.winfo_screenwidth()

# axis_x=(width_screen/2-width_box/2)
# axis_y=(height_screen/2-height_box/2)

axis_x=200
axis_y=200

calc.geometry('%ix%i+%i+%i'%(width_box,height_box,axis_x,axis_y))
calc.resizable(False,False)
# Botão de calcular
label1=tk.Label(calc,text='label 1',font='Times')
label1.pack()






btn_calcular=tk.Button(calc,text="Calcular",command=lambda:calcular('malco'))
btn_calcular.pack()


calc.mainloop()