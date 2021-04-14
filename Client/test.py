from lib import *
from user import *

[PK_1, SK_1] = GetK("1")
[PK_2, SK_2] = GetK("2")
[PK_s, SK_s] = GetK("Server")
CR_i_c__file = open("1/Data/Music/Music.random", 'r')
CR_i_c = int(CR_i_c__file.read().split('\n')[0], 16)
CR_i_c__file.close()
CR_i_c = Element(pairing, Zr, value = CR_i_c)
DR_i_c__l_file = open("1/Data/Music/孙燕姿 - 风衣.flac.DR_i_c__l", 'r')
DR_i_c__l = int(DR_i_c__l_file.read().split('\n')[0], 16)
DR_i_c__l_file.close()
DR_i_c__l = Element(pairing, Zr, value = DR_i_c__l)
DK_i_c__l = pairing.apply(g**DR_i_c__l, PK_s)

IDs = Get_File_ID("1/Data/Music/")
[[c1, c2], set_of_id_D_i_c__l] = BuildIndex(["孙燕姿", "1/Data/Music/孙燕姿 - 风衣.flac.enc"], IDs, SK_1, PK_s, params, g)
πSA_i_j = Auth(SK_1, PK_2, params, g, CR_i_c)
πDA_i_j = Auth(SK_1, PK_2, params, g, DR_i_c__l)
[T1, T2] = Trapdoor("孙燕姿", SK_2, params, g, PK_s)
result = Match([T1, T2], πSA_i_j, πDA_i_j, [c1, c2], params, g, PK_1, SK_s)
DecData(SK_2, result[1], "1/Data/Music/孙燕姿 - 风衣.flac.enc", params, g)