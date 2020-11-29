import tkinter as tk
from tkinter import ttk
from ultil import calcular

calc = tk.Tk()
calc.title("Calculadora NR")

####### Dimensões da janela e posicionamento na tela
width_box=1000
height_box=250

# height_screen=calc.winfo_screenwidth()
# width_screen=calc.winfo_screenwidth()

# axis_x=(width_screen/2-width_box/2)
# axis_y=(height_screen/2-height_box/2)

axis_x=200
axis_y=200


# calc.geometry('%ix%i+%i+%i'%(width_box,height_box,axis_x,axis_y))
calc.resizable(False,False)

# Botão de calcular
resultado=tk.StringVar()
label1=tk.Label(calc,font='Times',textvariable=resultado)



paramFrame=tk.LabelFrame(calc, text="Parâmetros")



############### DIREÇÂO 
DIRECTION = tk.StringVar()
label_modulation=tk.Label(paramFrame,font='Times',text="Direção")
label_modulation.grid(row=0,column=0)
tk.Radiobutton(paramFrame, 
              text="UPLINK",
              padx = 20, 
              variable=DIRECTION, 
              value='UP').grid(row=1,column=0)

tk.Radiobutton(paramFrame, 
              text="Downlink",
              padx = 20, 
              variable=DIRECTION, 
              value='DOWN').grid(row=2,column=0)


################ MODULATION
label_modulation=tk.Label(paramFrame,font='Times',text="Modulação")
label_modulation.grid(row=0,column=1)

MODULATION = tk.StringVar()
modulation_selected = ttk.Combobox(paramFrame,state="readonly",values=[
                                                    "QPSK", 
                                                    "16QAM",
                                                    "64QAM",
                                                    "256QAM"] ,textvariable=MODULATION)

modulation_selected.grid(row=1,column=1) #posição dentro do paramFrame


############# PORTADORAS
label_num_portadoras=tk.Label(paramFrame,font='Times',text="Barries")
label_num_portadoras.grid(row=2,column=1)
BARRIES = tk.IntVar()
num_berries = ttk.Spinbox(paramFrame, from_=1.0, to=1000, textvariable=BARRIES)
num_berries.grid(row=3,column=1)

############ SCALING FACTOR
SCALING_FACTOR = tk.StringVar()
label_scaling_factor=tk.Label(paramFrame,font='Times',text="Scaling Factor")
label_scaling_factor.grid(row=0,column=2)


tk.Radiobutton(paramFrame, 
              text="1",
              padx = 20, 
              variable=SCALING_FACTOR, 
              value='1').grid(row=1,column=2)

tk.Radiobutton(paramFrame, 
              text="0.8",
              padx = 20, 
              variable=SCALING_FACTOR, 
              value='0.8').grid(row=1,column=3)
tk.Radiobutton(paramFrame, 
              text="0.75",
              padx = 20, 
              variable=SCALING_FACTOR, 
              value='0.75').grid(row=1,column=4)

tk.Radiobutton(paramFrame, 
              text="0.4",
              padx = 20, 
              variable=SCALING_FACTOR, 
              value='0.4').grid(row=1,column=5)

############ Total BW

TOTAL_BW=tk.IntVar()
label_total_bw=tk.Label(paramFrame,font='Times',text="Total BW (Mhz)")
label_total_bw.grid(row=2,column=2)

total_bw = ttk.Spinbox(paramFrame, from_=1.0, to=300, textvariable=TOTAL_BW)
total_bw.grid(row=3,column=2)

############# Carrier spacing
CARRIER_SPACING = tk.StringVar()
label_carrier_spacing=tk.Label(paramFrame,font='Times',text="Carrier spacing")
label_carrier_spacing.grid(row=2,column=3)
carrier_spacing_selected = ttk.Combobox(paramFrame,state="readonly",values=[
                                                    "15 Khz", 
                                                    "30 Khz",
                                                    "60 Khz",
                                                    "120 Khz"] ,textvariable=CARRIER_SPACING)
carrier_spacing_selected.grid(row=3,column=3)

ttk.Separator(calc, orient=tk.HORIZONTAL).grid(row=2,column=0,columnspan=4, ipadx=100) 


btn_calcular=tk.Button(paramFrame,text="Calcular",command=lambda:calcular(DIRECTION,MODULATION,BARRIES,SCALING_FACTOR,TOTAL_BW,CARRIER_SPACING))
btn_calcular.grid(row=3,column=5)



################################################################ OUTPUT FRAME

outputFrame=tk.LabelFrame(calc, text="Saída")


label_output_mi=tk.Label(outputFrame,font='Times',text="Mi")
label_output_frequency_range=tk.Label(outputFrame,font='Times',text="Frequency Range")
label_output_nPRB=tk.Label(outputFrame,font='Times',text="Number of PRBs")
label_output_Ts=tk.Label(outputFrame,font='Times',text="Time of symbol")
label_output_throughput=tk.Label(outputFrame,font='Times',text="Throughput")

# label_output_mi.grid(row=0,column=0)
# label_output_frequency_range.grid(row=0,column=1)
# label_output_nPRB.grid(row=0,column=2)
# label_output_Ts.grid(row=0,column=3)
# label_output_throughput.grid(row=0,column=4)

label_output_mi.grid(row=0,column=0)
label_output_frequency_range.grid(row=1,column=0)
label_output_nPRB.grid(row=2,column=0)
label_output_Ts.grid(row=3,column=0)
label_output_throughput.grid(row=4,column=0)



paramFrame.grid(row=0,column=0)
outputFrame.grid(row=1,column=0)
calc.mainloop()

