import common.common

def test_decomposeStrToArgs():
     #'t[x%][y%][u:unexplored][o:fogofwar][t%:terrainID][f%:featureID]'
     args = common.common.decomposeStrToArgs('x15y-5ut77f18,75!bpotato!aninja',boolArgs=['u','o'],intArgs=['x','y','t'],strArgs=['b','a','f'])
     print(args)
     
     assert 'u' in args
     assert 'o' not in args

     assert args['x'] == "15"
     assert args['y'] == "-5"
     assert args['t'] == "77"
     assert args['f'] == "18,75"
     assert args['b'] == "potato"
     assert args['a'] == "ninja"