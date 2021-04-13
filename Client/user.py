# -*- coding: UTF-8 -*-
# Data: 2021/4/13
# Author: AngieJC
# e-Mail: htk90uggk@outlook.com
# Description: Client
# Usage: python3 user.py init|encode UID
#        python3 user.py auth UID_i UID_j

from lib import *
import sys
import os

params_file = open("params.dat", 'r')
params = Parameters(param_string = params_file.read())
pairing = Pairing(params)
params_file.close()
g_file = open("g.dat", 'r')
g = g_file.read().split('\n')[0]
g_file.close()
g = Element(pairing, G1, value = g)
UID = int(sys.argv[2])

def GetK(UID):
    PK_file = open(str(UID) + "/PK", 'r')
    PK_str = PK_file.read()
    PK_file.close()
    PK = Element(pairing, G1, value = PK_str)
    SK_file = open(str(UID) + "/SK", 'r')
    SK_str = int(SK_file.read(), 16)
    SK_file.close()
    SK = Element(pairing, Zr, value = SK_str)
    return [PK, SK]

if sys.argv[1] == "init":
    # init
    [PK, SK] = KeyGen(params, g)
    os.makedirs(str(UID))
    PK_file = open(str(UID) + "/PK", 'w')
    print(PK, file = PK_file)
    PK_file.close()
    SK_file = open(str(UID) + "/SK", 'w')
    print(SK, file = SK_file)
    SK_file.close()
elif sys.argv[1] == "encode":
    [PK, SK] = GetK(UID)
    EncData(str(UID) + '/Data/Music/孙燕姿 - 风衣.flac', ("孙燕姿", "风衣", "流行"), PK, params, g)
    IDs = Get_File_ID(str(UID) + "/Data/Music/")
    [[c1, c2], set_of_id_D_i_c__l] = BuildIndex(["孙燕姿", str(UID) + "/Data/Music/孙燕姿 - 风衣.flac.enc"], IDs, SK, PK, params, g)
elif sys.argv[1] == "auth":
    UID_j = int(sys.argv[3])
    [PK, SK] = GetK(UID)