from lib import *

if __name__ == '__main__':
    if len(sys.argv) == 1:
        [params, g] = Setup(1024, 180)
        params_file = open('./params.dat', 'w')
        print(params, file = params_file)
        params_file.close()
        g_file = open('./g.dat', 'w')
        print(g, file = g_file)
        g_file.close()
    elif sys.argv[1] == "GetKey":
        params_file = open("params.dat", 'r')
        params = Parameters(param_string = params_file.read())
        pairing = Pairing(params)
        params_file.close()
        g_file = open("g.dat", 'r')
        g = g_file.read().split('\n')[0]
        g_file.close()
        g = Element(pairing, G1, value = g)
        [PK, SK] = KeyGen(params, g)
        PK_file = open("PK", 'w')
        print(PK, file = PK_file)
        PK_file.close()
        SK_file = open("SK", 'w')
        print(SK, file = SK_file)
        SK_file.close()