# -*- coding: UTF-8 -*-
# Data: 2021/4/13
# Author: AngieJC
# e-Mail: htk90uggk@outlook.com
# Description: Client

from lib import *

params_file = open("params.dat", 'r')
params = Parameters(param_string = params_file.read())
pairing = Pairing(params)
params_file.close()
g_file = open("g.dat", 'r')
g = g_file.read().split('\n')[0]
g_file.close()
g = Element(pairing, G1, value = g)