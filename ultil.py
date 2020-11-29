import pandas as pd
import math,re
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

def get_mimo_value(mimo):
    value = int(mimo.split('x')[1])
    return value

def get_nbit_modulation(modulation):
    modulation=modulation.lower()

    if modulation=='qpsk':
        return 2
    else:
        QAM=int(re.sub("qam",'',modulation))
        n_bit=math.log(QAM)/math.log(2)
        return n_bit

def get_carrier_spacing_value(carrier_spacing):
    return int(carrier_spacing.split(' ')[0])

def get_overhead():
    return 0.14
# def calcular(direction,carries,mimo,modulation,scaling_factor,total_bw,carrier_spacing):
    # get_tp(carries,mimo,nbit_modulation,overhead,scaling_factor,carrier_spacing,total_bw)

def calcular(**kwargs):
    carries=kwargs['carries']
    mimo=get_mimo_value(kwargs['mimo'])
    nbit_modulation=get_nbit_modulation(kwargs['modulation'])
    scaling_factor=int(kwargs['scaling_factor'])
    total_bw=int(kwargs['total_bw'])
    carrier_spacing=get_carrier_spacing_value(kwargs['carrier_spacing'])
    overhead=get_overhead()
    # print(carries,mimo,nbit_modulation,overhead,scaling_factor,carrier_spacing,total_bw)
    result=get_tp(carries,mimo,nbit_modulation,overhead,scaling_factor,carrier_spacing,total_bw)
    label_output_throughput=kwargs['label_output_throughput']
    return result

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

def get_tp(carries,mimo,nbit_modulation,overhead,scaling_factor,carrier_spacing,total_bw):
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
    mi=get_mi(carrier_spacing)
    nPRB=get_bw_prb(carrier_spacing,total_bw)
    Rmax=948/1024
    Ts  = (10**(-3))/(14*(2**mi))
    all_carries_tp=carries*mimo*nbit_modulation*Rmax*scaling_factor*((nPRB*12)/Ts)*(1-overhead)
    all_carries_tp=10**(-6)*all_carries_tp
    
    result['throughput'] = all_carries_tp
    result['mi']=mi
    result['nPRB']=nPRB
    result['ts']=Ts
    return result
