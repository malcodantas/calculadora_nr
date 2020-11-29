import unittest
from ultil import get_tp,get_mimo_value,get_bw_prb,get_nbit_modulation,get_carrier_spacing_value

#testando se minha função retorna o valor correto passando como parametro o exemplo do slide
#get_tp(carries,mimo,nbit_modulation,overhead,scaling_factor,nPRB,mi,total_bw):
# NAO da pra usar esse teste para comparar os valores de dicionarios

# class TestCalculadora(unittest.TestCase):
#     def test_example1_result(self):
#         self.assertEqual(get_tp(1,2,6,0.14,1,30,100)['throughput'],876.375045)
#     def test_example2_result(self):
#         self.assertNotAlmostEqual(get_tp(1,4,8,0.14,1,30,100),1369.67)

class TestSubParams(unittest.TestCase):
    def test_return_mimo_by_str(self):
        self.assertAlmostEqual(get_mimo_value('MIMO 2x2'),2)
    def test_get_bw_prb(self):
        self.assertAlmostEqual(get_bw_prb(30,100),273)
        self.assertAlmostEqual(get_bw_prb(15,30),160)
    def test_get_nbit_modulation(self):
        self.assertAlmostEqual(get_nbit_modulation("QPSK"),2)
        self.assertAlmostEqual(get_nbit_modulation("64qam"),6)
        self.assertAlmostEqual(get_nbit_modulation("256QAm"),8)
    def test_get_carrier_spacing_value(self):
        self.assertAlmostEqual(get_carrier_spacing_value('15 Khz'),15)
        self.assertAlmostEqual(get_carrier_spacing_value('120 Khz'),120)
