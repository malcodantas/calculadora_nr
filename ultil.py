import pandas as pd
import math
NPRB_TABLE=pd.DataFrame({
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

def calcular(DIRECTION,MODULATION,BARRIES,SCALING_FACTOR,TOTAL_BW,CARRIER_SPACING):
    carrier=DIRECTION.get()
    modulation=MODULATION.get()
    barries=BARRIES.get()
    scaling_factor=SCALING_FACTOR.get()
    total_bw=TOTAL_BW.get()
    carrier_spacing=CARRIER_SPACING.get()
    




def get_bw_prb(mi,total_bw):
    """
        mi em Khz
        total_bw em Mhz
    """
    index=None
    if mi==15:
        index=0
    elif mi==30:
        index=1
    elif index==60:
        index=2
    else:
        return None
    
    return NPRB_TABLE['%im'%(total_bw)][index].item()

def get_mi(carrier_spacing):
    # carrier_spacing em Khz
    # Cáculo da numerologia do mi dependendo do espaçamento
    mi = math.log(carrier_spacing/15)/math.log(2)
    return mi

def get_tp(carries,mimo,nbit_modulation,overhead,scaling_factor,nPRB,carrier_spacing,total_bw):
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
    mi=get_mi(carrier_spacing)
    nPRB=get_bw_prb(carrier_spacing,total_bw)
    Rmax=948/1024
    Ts  = (10**(-3))/(14*(2**mi))
    all_carries_tp=carries*mimo*nbit_modulation*Rmax*scaling_factor*((nPRB*12)/Ts)*(1-overhead)
    all_carries_tp=10**(-6)*all_carries_tp
    return all_carries_tp

