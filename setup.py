# -*- coding: UTF-8 -*-
# Data: 2021/4/10
# Author: AngieJC
# e-Mail: htk90uggk@outlook.com
# Description: Generate the params and bloom filter

from lib import Setup

[params, g] = Setup(1024, 180)
params_file = open('./params.dat', 'w')
print(params, file = params_file)
params_file.close()
g_file = open('./g.dat', 'w')
print(g, file = g_file)
g_file.close()