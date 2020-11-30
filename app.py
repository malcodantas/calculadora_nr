import tkinter as tk
from tkinter import ttk
import pandas as pd
import math,re
NPRB_TABLE_FR1=pd.DataFrame({
    "5m":[25,11,None],
    "10m":[52,24,11],
    "15m":[79,38,18],
    "20m":[106,51,24],
    "25m":[133,65,31],
    "30m":[160,78,38],
    "40m":[216,106,51],
    "50m":[270,133,65],
    "60m":[None,162,79],
    "80m":[None,217,107],
    "90m":[None,245,121],
    "100m":[None,273,135]
})
NPRB_TABLE_FR2 = pd.DataFrame({
    "50m":[66,32],
    "100m":[132,66],
    "200m":[264,132],
    "400m":[None,264]
})

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.throughput=0
    
    def get_mimo_value(self,mimo):
        value = int(mimo.split('x')[1])
        return value

    def get_nbit_modulation(self,modulation):
        modulation=modulation.lower()

        if modulation=='qpsk':
            return 2
        else:
            QAM=int(re.sub("qam",'',modulation))
            n_bit=math.log(QAM)/math.log(2)
            return n_bit

    def get_carrier_spacing_value(self,carrier_spacing):
        return int(carrier_spacing.split(' ')[0])

    def get_overhead(self,direction,fr):
        if direction=="UP":
            if fr==1:
                return 0.08
            else:
                return 0.10
        else:
            if fr==1:
                return 0.14
            else:
                return 0.18

    def calcular(self,**kwargs):
        carries=kwargs['carries']
        mimo=self.get_mimo_value(kwargs['mimo'])
        nbit_modulation=self.get_nbit_modulation(kwargs['modulation'])
        scaling_factor=float(kwargs['scaling_factor'])
        total_bw=int(kwargs['total_bw'])
        carrier_spacing=self.get_carrier_spacing_value(kwargs['carrier_spacing'])
        overhead=self.get_overhead(kwargs['direction'],kwargs['fr'])
        result=self.get_tp(carries,mimo,nbit_modulation,overhead,scaling_factor,carrier_spacing,total_bw,kwargs['fr'])
        if result!=None:
        #Gambiarra devido a inexperiencia com o TKINTER
            label_output_throughput.config(text='Throughput = %s Mbps'%(round(result['throughput'],3)))
            label_output_mi.config(text='mi = %s'%(int(result['mi'])))
            label_output_nPRB.config(text='Num PRBs = %s'%(int(result['nPRB'])))
            label_output_Ts.config(text='Ts = %s'%(result['ts']))
            label_overhead.config(text='OH = %s'%(result['overhead']))
        else:
            pass


    def get_bw_prb(self,mi,total_bw,FR):
        print(mi,total_bw,FR)
        """
            mi em Khz
            total_bw em Mhz
        """
        index=None
        if FR==1 and mi <= 60:
            if mi==15:
                index=0
            elif mi==30:
                index=1
            elif index==60:
                index=2
            else:
                return None
            return NPRB_TABLE_FR1['%im'%(total_bw)][index].item()

        elif FR==2 and total_bw >= 50 and mi >=60:
            if mi ==60:
                index=0
            if mi ==120:
                index=1
            return NPRB_TABLE_FR2['%im'%(total_bw)][index].item()
        else:
            exit()
    def get_mi(self,carrier_spacing):
        mi = math.log(carrier_spacing/15)/math.log(2)
        return mi

    def get_tp(self,carries,mimo,nbit_modulation,overhead,scaling_factor,carrier_spacing,total_bw,FR):
        """
            carries : Numero de portadoras
            mimo : Escala do mimo Mimo 2x2 = 2 , Mimo 4x4 = 4
            nbit_modulation : Numero de bits por simbolo 
            overhead : Porcentagem de overhead na rede
            scaling_factor : Fator de escala
            nPRB : Numero de PRBs por usuario dependendo da Banda (pego da tabela)
            carrier_spacing : Espaço entre as subportadoras em Khz
            total_bw : em Mhz
        """
        result={}
        mi=self.get_mi(carrier_spacing)
        nPRB=self.get_bw_prb(carrier_spacing,total_bw,FR)
        Rmax=948/1024
        Ts  = (10**(-3))/(14*(2**mi))
        try:
            all_carries_tp=carries*mimo*nbit_modulation*Rmax*scaling_factor*((nPRB*12)/Ts)*(1-overhead)
            all_carries_tp=10**(-6)*all_carries_tp
            
            result['throughput'] = all_carries_tp
            result['mi']=mi
            result['nPRB']=nPRB
            result['ts']=Ts
            result['overhead']=overhead

            return result
        except TypeError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calculadora NR")
    APP=MainApplication(root)
    APP.grid()
    paramFrame=tk.LabelFrame(root, text="Parâmetros")


    ############### DIREÇÂO 
    DIRECTION = tk.StringVar()
    label_modulation=tk.Label(paramFrame,font='Times',text="Direção")
    label_modulation.grid(row=0,column=0)
    tk.Radiobutton(paramFrame, 
                text="UPLINK",
                padx = 20, 
                variable=DIRECTION, 
                value='UP').grid(row=1,column=0)

    default_rb_direction=tk.Radiobutton(paramFrame, 
                text="Downlink",
                padx = 20, 
                variable=DIRECTION, 
                value='DOWN')
    default_rb_direction.grid(row=2,column=0)
    default_rb_direction.select()

    ############### FR 
    FR = tk.IntVar()
    label_FR=tk.Label(paramFrame,font='Times',text="Direção")
    label_FR.grid(row=0,column=0)
    default_fr_rb=tk.Radiobutton(paramFrame, 
                text="FR1",
                padx = 20, 
                variable=FR, 
                value='1')
    default_fr_rb.grid(row=1,column=1)
    default_fr_rb.select()

    tk.Radiobutton(paramFrame, 
                text="FR2",
                padx = 20, 
                variable=FR, 
                value='2').grid(row=2,column=1)

    ################ MIMO 
    MIMO = tk.StringVar()
    # label_mimo=tk.Label(paramFrame,font='Times',text="Carrier spacing")
    mimo_select = ttk.Combobox(paramFrame,state="readonly",values=[
                                                        "MIMO 1x1", 
                                                        "MIMO 2x2",
                                                        "MIMO 3x3",
                                                        "MIMO 4x4",
                                                        "MIMO 5x5", 
                                                        "MIMO 6x6",
                                                        "MIMO 7x7",
                                                        "MIMO 8x8"] ,textvariable=MIMO)
    mimo_select.grid(row=4,column=0)


    ################ MODULATION
    label_modulation=tk.Label(paramFrame,font='Times',text="Modulação")
    label_modulation.grid(row=0,column=2)

    MODULATION = tk.StringVar()
    modulation_selected = ttk.Combobox(paramFrame,state="readonly",values=[
                                                        "QPSK", 
                                                        "16QAM",
                                                        "64QAM",
                                                        "256QAM"] ,textvariable=MODULATION)

    modulation_selected.grid(row=1,column=2) #posição dentro do paramFrame


    ############# PORTADORAS
    label_num_portadoras=tk.Label(paramFrame,font='Times',text="Carries")
    label_num_portadoras.grid(row=3,column=3)
    CARRIES = tk.IntVar()
    num_carries = ttk.Spinbox(paramFrame, from_=1.0, to=1000, textvariable=CARRIES)
    num_carries.grid(row=4,column=3)

    ############ SCALING FACTOR
    SCALING_FACTOR = tk.StringVar()
    label_scaling_factor=tk.Label(paramFrame,font='Times',text="Scaling Factor")
    label_scaling_factor.grid(row=0,column=3)


    default_rb_scale=tk.Radiobutton(paramFrame, 
                text="1",
                padx = 20, 
                variable=SCALING_FACTOR, 
                value='1')
    default_rb_scale.select()
    default_rb_scale.grid(row=1,column=3)

    tk.Radiobutton(paramFrame, 
                text="0.8",
                padx = 20, 
                variable=SCALING_FACTOR, 
                value='0.8').grid(row=1,column=4)
    tk.Radiobutton(paramFrame, 
                text="0.75",
                padx = 20, 
                variable=SCALING_FACTOR, 
                value='0.75').grid(row=1,column=5)

    tk.Radiobutton(paramFrame, 
                text="0.4",
                padx = 20, 
                variable=SCALING_FACTOR, 
                value='0.4').grid(row=1,column=6)

    ############ Total BW

    TOTAL_BW=tk.IntVar()
    label_total_bw=tk.Label(paramFrame,font='Times',text="Total BW (Mhz)")
    label_total_bw.grid(row=3,column=2)

    total_bw = ttk.Spinbox(paramFrame, from_=0, to=400, textvariable=TOTAL_BW,increment=5)
    total_bw.grid(row=4,column=2)

    ############# Carrier spacing
    CARRIER_SPACING = tk.StringVar()
    label_carrier_spacing=tk.Label(paramFrame,font='Times',text="Carrier spacing")
    label_carrier_spacing.grid(row=3,column=4)
    carrier_spacing_selected = ttk.Combobox(paramFrame,state="readonly",values=[
                                                        "15 Khz", 
                                                        "30 Khz",
                                                        "60 Khz",
                                                        "120 Khz"] ,textvariable=CARRIER_SPACING)
    carrier_spacing_selected.grid(row=4,column=4)


    btn_calcular=tk.Button(paramFrame,text="Calcular",command=lambda:APP.calcular(direction=DIRECTION.get(),fr=FR.get(),carries=CARRIES.get(),
                       mimo=MIMO.get(),modulation=MODULATION.get(),scaling_factor=SCALING_FACTOR.get(),total_bw=TOTAL_BW.get(),carrier_spacing=CARRIER_SPACING.get()))
    btn_calcular.grid(row=3,column=6)




    outputFrame=tk.LabelFrame(root, text="Saída")


    label_output_mi=tk.Label(outputFrame,font='Times',text="Mi")
    label_output_nPRB=tk.Label(outputFrame,font='Times',text="Number of PRBs")
    label_output_Ts=tk.Label(outputFrame,font='Times',text="Time of symbol")
    label_output_throughput=tk.Label(outputFrame,font='Times')
    label_overhead=tk.Label(outputFrame,font='Times')



    label_output_mi.grid(row=0,column=0)
    label_output_nPRB.grid(row=2,column=0)
    label_output_Ts.grid(row=3,column=0)
    label_output_throughput.grid(row=4,column=0)
    label_overhead.grid(row=5,column=0)



    paramFrame.grid(row=0,column=0)
    outputFrame.grid(row=1,column=0)

    #Definindo valores inciais padrões
    mimo_select.current(1)
    carrier_spacing_selected.current(1)
    modulation_selected.current(2)
    num_carries.set(1)
    total_bw.set(100)
    root.mainloop()