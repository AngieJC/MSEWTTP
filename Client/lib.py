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
import json

from pypbc import *
from pybloomfilter import *
from Crypto.Cipher import AES
import hashlib

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
import base64
import os

Hash1 = hashlib.sha256


# 系统初始化算法，输入安全参数λ(qbits, rbits)和布隆过滤器hash函数族个数k，返回params=[q, G1, GT, e, g, H', H1, H2, H3]
# 其中q为G1和GT的阶数，G1*G1->GT，e为双线性映射运算，g为G1的生成元，H'为布隆过滤器的hash函数集；
# H1:{0,1}*->G1，H2:G2->{0,1}τ，H3:{0,1}*->m
# m为布隆过滤器的长度
def Setup(qbits, rbits):
    params = Parameters(qbits=qbits, rbits=rbits)
    #params_file = open('./params.dat', 'w')
    #print(params, file = params_file)
    #params_file.close()
    pairing = Pairing(params)
    g = Element.random(pairing, G1)
    #BloomFilter(100000, 0.01, 'bf.bloom')
    return [params, g]
    

'''
def KeyGen(qbits, rbits):
    params = Parameters(qbits=qbits, rbits=rbits)
    pairing = Pairing(params)
    g = Element.random(pairing, G2) # 这里G1和G2都无所谓，因为论文里是对称的双线性映射，即G1*G1->GT，而库函数的定义为G1*G2->GT
    sk = Element.random(pairing, Zr)
    pk = Element(pairing, G2, value=g ** sk)
    return [params, g, pk, sk]
'''
# 密钥生成算法，输入公共参数params，输出公私钥对(pk = g^x, sk = x)
def KeyGen(params, g):
    pairing = Pairing(params)
    #g = Element.random(pairing, G2)
    SK = Element.random(pairing, Zr)
    PK = Element(pairing, G1, value = g**SK)
    return [PK, SK]


# 文档加密算法，输入明文文档，明文文档所对应的明文关键字，输出明文文档和密文布隆过滤器
# D_i_c__l是明文文档路径，W_i_c__l是明文文档所对应的明文关键字(list而非路径)
def EncData(D_i_c__l, W_i_c__l, PK_s, params, g):
    pairing = Pairing(params)
    #g = Element.random(pairing, G2)
    DR_i_c__l = Element.random(pairing, Zr)
    DR_i_c__l_file = open(D_i_c__l + ".DR_i_c__l", 'w')
    print(DR_i_c__l, file = DR_i_c__l_file)
    DR_i_c__l_file.close()
    DK_i_c__l = pairing.apply(g**DR_i_c__l, PK_s)
    DK_i_c__l_str = bytes(Hash1(str(DK_i_c__l).encode('utf-8')).hexdigest(), encoding="utf-8")[:31]
    #print(Hash1(str(DK_i_c__l).encode('utf-8')).hexdigest())
    #DK_i_c__l_str = Hash1(str(DK_i_c__l).encode('utf-8')).hexdigest()
    AES_SECRET_KEY = pad(DK_i_c__l_str, 32)
    '''
    keywords1="document1"
    data1 = keywords1.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, pad(b'0', AES.block_size))
    ct_bytes = cipher.encrypt(pad(data1, AES.block_size))
    '''
    target_file = open(D_i_c__l, 'rb')
    m = target_file.read()
    target_file.close()
    AESObj = AES.new(AES_SECRET_KEY, AES.MODE_CBC, pad(b'0', AES.block_size))
    s = AESObj.encrypt(pad(m, AES.block_size))
    encoded_file = open(D_i_c__l+".enc", 'wb')
    encoded_file.write(s)
    encoded_file.close()
    '''
    m = AESObj.decrypt(pad(s, AES.block_size))
    test_file = open("test.flac", 'wb')
    test_file.write(m)
    test_file.close()
    '''
    
    # 生成布隆过滤器并加密
    bf = BloomFilter(100, 0.001, D_i_c__l+".bloom")
    bf.update(W_i_c__l)
    bf_file = open(D_i_c__l+".bloom", 'rb')
    bf_message = bf_file.read()
    bf_file.close()
    bf_s = AESObj.encrypt(pad(bf_message, AES.block_size))
    encoded_bf_file = open(D_i_c__l+".bloom_enc", 'wb')
    encoded_bf_file.write(bf_s)
    encoded_bf_file.close()
    bf.close()
    os.remove(D_i_c__l+".bloom")


# 索引生成算法，输入倒排索引和数据拥有者私钥，输出加密索引
# IW_i_c__k是一个列表，列表的第一个元素是关键字，其余元素是包含该关键字的密文文档名
# IDs为所有加密文档的哈希值
def BuildIndex(IW_i_c__k, IDs, SK, PK_s, params, g):
    pairing = Pairing(params)
    #g = Element.random(pairing, G2)
    #CR_i_c = Element.random(pairing, Zr)
    route_word = IW_i_c__k[1].split('/')
    route = ''
    i = 0
    while i < len(route_word) - 1:
        route = route + route_word[i] + '/'
        i = i + 1
    if os.path.exists(route + route_word[-2] + ".random"):
        # 从文件中读取随机数
        CR_i_c_file = open(route + route_word[-2] + ".random", 'r')
        CR_i_c = CR_i_c_file.read()
        CR_i_c_file.close()
        CR_i_c = CR_i_c.split('\n')[0]
        CR_i_c = int(CR_i_c, 16)
        CR_i_c = Element(pairing, Zr, value = CR_i_c)
    else:
        CR_i_c = Element.random(pairing, Zr)
        CR_i_c_file = open(route + route_word[-2] + ".random", 'w')
        print(CR_i_c, file = CR_i_c_file)
        CR_i_c_file.close()
        '''
        CR_i_c_file = open(route + route_word[-2] + ".random", 'r')
        CR_i_c = int(CR_i_c_file.read(), 16)
        CR_i_c_file.close()
        '''
    hash_IW_i_c__k = Hash1(IW_i_c__k[0].encode('utf-8')).hexdigest()
    temp = open("temp", 'w')
    print(hash_IW_i_c__k, file = temp)
    temp.close()
    temp = open("temp", 'r')
    hash_IW_i_c__k = temp.read()
    hash_IW_i_c__k = Element.from_hash(pairing, Zr, hash_IW_i_c__k)
    temp.close()
    os.remove("temp")
    #SK = Element_to_int(SK)
    #PK_s = Element_to_int(PK_s)
    #g = Element_to_int(g)
    c1 = Element(pairing, G1, value = (hash_IW_i_c__k**(CR_i_c / SK))) * Element(pairing, G1, value = (PK_s**CR_i_c))
    c2 = g**CR_i_c
    #print(hash_IW_i_c__k)
    #c1 = (hash_IW_i_c__k**(CR_i_c/SK)) * (PK_s**CR_i_c)
    #c2 = g**CR_i_c
    # set_of_id_D_i_c__l
    set_of_id_D_i_c__l = []
    i = 1
    while i < len(IW_i_c__k):
        set_of_id_D_i_c__l.append(IDs[IW_i_c__k[i].split('/')[-1]])
        i = i + 1
    return [[c1, c2], set_of_id_D_i_c__l]


# 用户授权算法，输入自己的私钥，目标用户的公钥，输出授权信息
# SK_i是自己的私钥，PK_j是用户j的公钥
def Auth(SK_i, PK_j, params, g, Random):
    pairing = Pairing(params)
    return Element(pairing, G1, value = PK_j**(Random / SK_i))


# 搜索陷门生成算法，搜索用户输入明文关键字，私钥，服务器的公钥，输出陷门信息
def Trapdoor(w_q, SK_j, params, g, PK_s):
    pairing = Pairing(params)
    r = Element.random(pairing, Zr)
    T1 = Element(pairing, G1, value = Hash1(w_q.encode('utf-8')).hexdigest())**(r / SK_j)
    T2 = PK_s**r
    return [T1, T2]


# 搜索查询算法，输入陷门，授权信息数组，查询者的id，输出中间密钥
# Tr为查询陷门，πSA_i_j为一个分类的查询授权信息，πDA_i_c__l_j为文档解密与验证授权信息，CI为密文关键字
def Match(Tr, πSA_i_j, πDA_i_c__l_j, CI, params, g, PK_i, SK_s):
    T1 = Tr[0]
    T2 = Tr[1]
    c1 = CI[0]
    c2 = CI[1]
    pairing = Pairing(params)
    one_element = Element.one(pairing, G1)
    SK_s__1 = Element(pairing, G1, value = one_element / SK_s)
    result = []
    i = 0
    if pairing.apply(T1, πSA_i_j) * pairing.apply(T2, c2) == pairing.apply(c1, Element(pairing, G1, value = T2**SK_s__1)):
        result.append(1)
        CK_i_c__l_j = pairing.apply(πDA_i_c__l_j, Element(pairing, G1, value = PK_i**SK_s))
        result.append(CK_i_c__l_j)
    else:
        result.append(0)
    return result


# 文档解密算法，输入数据使用者的私钥，中间密钥，密文文档，输出明文
def DecData(SK_j, CK_i_c__l_j, encoded_file, params, g):
    one_element = Element.one(pairing, G1)
    DK_i_c__L = Element(pairing, GT, value = CK_i_c__l_j**(Element(pairing, G1, value = (one_element / SK_j))))
    DK_i_c__L_str = bytes(Hash1(str(DK_i_c__l).encode('utf-8')).hexdigest(), encoding="utf-8")[:31]
    AES_SECRET_KEY = pad(DK_i_c__L_str, 32)
    fileObj = open(encoded_file, 'rb')
    s = fileObj.read()
    fileObj.close()
    AESObj = AES.new(AES_SECRET_KEY, AES.MODE_CBC, pad(b'0', AES.block_size))
    m = AES.decrypt(s)
    decode_file = open("decode_file", 'wb')
    decode_file.write(m)
    decode_file.close()




####################################
# 辅助性函数，非论文中所提到的函数 #
####################################

# 输入目录，输出目录中所有加密文档的哈希值
def Get_File_ID(path):
    IDs = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.enc':
                encoded_file = open(path + file, 'rb')
                s_message = encoded_file.read()
                encoded_file.close()
                hash_value = Hash1(s_message).hexdigest()
                IDs[file] = hash_value
    IDs_jsObj = json.dumps(IDs)
    IDs_jsObj_file = open(path + "IDs.json", 'w')
    IDs_jsObj_file.write(IDs_jsObj)
    IDs_jsObj_file.close()
    return IDs

# 将Element对象转为数字
def Element_to_int(ElementObj):
    ElementObj_file = open('ElementObj', 'w')
    print(ElementObj, file = ElementObj_file)
    ElementObj_file.close()
    ElementObj_file = open('ElementObj', 'r')
    intObj = int(ElementObj_file.read(), 16)
    ElementObj_file.close()
    os.remove("ElementObj")
    return intObj