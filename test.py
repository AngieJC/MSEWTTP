from lib import *
[params, g] = Setup(1024, 180)
[PK, SK] = KeyGen(params, g)
[PK_s, SK_s] = KeyGen(params, g)
EncData('Data/Music/孙燕姿 - 风衣.flac', ("孙燕姿", "风衣", "流行"), PK_s, params, g)
IDs = Get_File_ID("EncData/Music/")
[[c1, c2], set_of_id_D_i_c__l] = BuildIndex(["孙燕姿", "Data/Music/孙燕姿 - 风衣.flac"], IDs, SK, PK_s, params, g)