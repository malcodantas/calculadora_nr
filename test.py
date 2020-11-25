import unittest
from ultil import get_tp

#testando se minha função retorna o valor correto passando como parametro o exemplo do slide
#get_tp(carries,mimo,nbit_modulation,overhead,scaling_factor,nPRB,mi,total_bw):
 
class TestCalculadora(unittest.TestCase):
    def test_example1_result(self):
        self.assertEqual(get_tp(1,2,6,0.14,1,273,30,100),876.375045)
    def test_example2_result(self):
        self.assertNotAlmostEqual(get_tp(1,4,8,0.14,1,160,30,100),1369.67)
