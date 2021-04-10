# -*- coding: UTF-8 -*-
# Data: 2021/4/10
# Author: AngieJC
# e-Mail: htk90uggk@outlook.com
# Description: All the function in this system.


import socket
import pickle
import fileinput
import pandas as pd
import time

from pypbc import *
from pybloomfilter import *
import hashlib

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64


# 系统初始化算法，输入安全参数λ(qbits, rbits)和布隆过滤器hash函数族个数k，返回params=[q, G1, GT, e, g, H', H1, H2, H3]
# 其中q为G1和GT的阶数，G1*G1->GT，e为双线性映射运算，g为G1的生成元，H'为布隆过滤器的hash函数集；
# H1:{0,1}*->G1，H2:G2->{0,1}τ，H3:{0,1}*->m
# m为布隆过滤器的长度
def Setup(qbits, rbits):
    params = Parameters(qbits=qbits, rbits=rbits)
    #params_file = open('./params.dat', 'w')
    #print(params, file = params_file)
    #params_file.close()
    #pairing = Pairing(params)
    #g = Element.random(pairing, G2)
    BF = BloomFilter(100000, 0.01, 'bf.bloom')
    return params
    


def KeyGen(qbits, rbits):
    params = Parameters(qbits=qbits, rbits=rbits)
    pairing = Pairing(params)
    g = Element.random(pairing, G2) # 这里G1和G2都无所谓，因为论文里是对称的双线性映射，即G1*G1->GT，而库函数的定义为G1*G2->GT
    sk = Element.random(pairing, Zr)
    pk = Element(pairing, G2, value=g ** sk)
    return [params, g, pk, sk]