"""
General tests for Markov switching models

Author: Chad Fulton
License: BSD
"""
from __future__ import division, absolute_import, print_function

import numpy as np
import pandas as pd
from statsmodels.tsa.regime_switching import markov_regression
from numpy.testing import assert_equal, assert_allclose, assert_raises


# See http://www.stata-press.com/data/r14/usmacro
fedfunds = [1.03, 0.99, 1.34, 1.5, 1.94, 2.36, 2.48, 2.69, 2.81, 2.93, 2.93,
            3.0, 3.23, 3.25, 1.86, 0.94, 1.32, 2.16, 2.57, 3.08, 3.58, 3.99,
            3.93, 3.7, 2.94, 2.3, 2.0, 1.73, 1.68, 2.4, 2.46, 2.61, 2.85,
            2.92, 2.97, 2.96, 3.33, 3.45, 3.46, 3.49, 3.46, 3.58, 3.97, 4.08,
            4.07, 4.17, 4.56, 4.91, 5.41, 5.56, 4.82, 3.99, 3.89, 4.17, 4.79,
            5.98, 5.94, 5.92, 6.57, 8.33, 8.98, 8.94, 8.57, 7.88, 6.7, 5.57,
            3.86, 4.56, 5.47, 4.75, 3.54, 4.3, 4.74, 5.14, 6.54, 7.82, 10.56,
            10.0, 9.32, 11.25, 12.09, 9.35, 6.3, 5.42, 6.16, 5.41, 4.83, 5.2,
            5.28, 4.87, 4.66, 5.16, 5.82, 6.51, 6.76, 7.28, 8.1, 9.58, 10.07,
            10.18, 10.95, 13.58, 15.05, 12.69, 9.84, 15.85, 16.57, 17.78,
            17.58, 13.59, 14.23, 14.51, 11.01, 9.29, 8.65, 8.8, 9.46, 9.43,
            9.69, 10.56, 11.39, 9.27, 8.48, 7.92, 7.9, 8.1, 7.83, 6.92, 6.21,
            6.27, 6.22, 6.65, 6.84, 6.92, 6.66, 7.16, 7.98, 8.47, 9.44, 9.73,
            9.08, 8.61, 8.25, 8.24, 8.16, 7.74, 6.43, 5.86, 5.64, 4.82, 4.02,
            3.77, 3.26, 3.04, 3.04, 3.0, 3.06, 2.99, 3.21, 3.94, 4.49, 5.17,
            5.81, 6.02, 5.8, 5.72, 5.36, 5.24, 5.31, 5.28, 5.28, 5.52, 5.53,
            5.51, 5.52, 5.5, 5.53, 4.86, 4.73, 4.75, 5.09, 5.31, 5.68, 6.27,
            6.52, 6.47, 5.59, 4.33, 3.5, 2.13, 1.73, 1.75, 1.74, 1.44, 1.25,
            1.25, 1.02, 1.0, 1.0, 1.01, 1.43, 1.95, 2.47, 2.94, 3.46, 3.98,
            4.46, 4.91, 5.25, 5.25, 5.26, 5.25, 5.07, 4.5, 3.18, 2.09, 1.94,
            0.51, 0.18, 0.18, 0.16, 0.12, 0.13, 0.19, 0.19, 0.19]

# See http://www.stata-press.com/data/r14/usmacro
ogap = [-0.53340107, 0.72974336, 2.93532324, 3.58194304, 4.15760183,
        4.28775644, 3.01683831, 2.64185619, 1.82473528, 2.37461162,
        2.39338565, 1.24197006, 1.1370815, -1.28657401, -4.46665335,
        -4.79258966, -3.06711817, -1.3212384, -0.54485309, 0.86588413,
        -0.2469136, -0.75004685, 0.7417022, -0.71350163, -1.5151515,
        -3.80444455, -4.02601957, -3.17873883, -2.48841596, -1.42372882,
        -0.61779928, -0.6430338, -0.73277968, -1.38330388, -1.31537247,
        -0.95626277, 0., -0.15248552, 0.93233085, 1.03888392,
        1.27174389, 0.63400578, 2.13007665, 2.44789481, 3.37605071,
        4.72771597, 6.20753956, 5.39234877, 5.0825758, 4.8605876,
        4.65116262, 3.52755141, 3.35122228, 3.09326482, 4.10191917,
        4.69641066, 4.38452244, 3.79841614, 4.38338947, 3.63766766,
        3.24129653, 1.84967709, 0.75554705, -0.02802691, -0.03673432,
        -1.90527546, -0.14918824, -0.42940569, -0.46382189, -0.97892815,
        -0.12142799, 1.37281513, 1.5143193, 2.47730422, 3.9762032,
        4.08987427, 2.62857127, 2.90107131, 0.97277576, 0.42547619,
        -1.60488391, -2.97784758, -4.98650694, -5.03382635, -4.25698328,
        -3.74993205, -2.39661908, -2.41223454, -2.66694117, -2.62232494,
        -2.29969597, -1.38809109, -0.67855304, -1.08100712, -1.82682908,
        0.92868561, 0.87040615, 1.32669306, 0.56407404, -0.13848817,
        -0.13089494, -0.58975571, -1.00534534, -3.55482054, -4.20365095,
        -2.97225475, -1.57762408, -2.77206445, -2.32418823, -4.01929235,
        -6.25393772, -6.46356869, -7.47437572, -8.06377602, -7.57157278,
        -6.14639282, -5.00167227, -3.74511886, -2.54788184, -1.64858043,
        -1.47994602, -1.44707143, -1.31824112, -1.20102882, -0.57691002,
        -0.64480144, -0.57239723, -0.93083948, -0.8392899, -1.19972074,
        -1.18918467, -0.87174636, -0.78151888, 0.10762761, -0.10596547,
        0.40488175, 0.17958413, 0.67704558, 0.99767941, 1.00495291,
        0.98304421, 0.47067845, 0.80427116, 0.45058677, -0.26300991,
        -1.84629929, -2.99437666, -2.90482664, -3.09490418, -3.32399321,
        -2.87384319, -2.47262239, -2.19618678, -1.91843009, -2.46574545,
        -2.58180451, -2.72212362, -2.17548561, -1.96046102, -1.3287729,
        -1.42521954, -1.04951096, -1.47037697, -1.87099183, -1.72912872,
        -1.76828432, -1.85885167, -0.9193368, -0.95776832, -0.62119246,
        -0.53508854, -0.04090983, 0.47511154, 0.41246772, 0.57928383,
        0.67604625, 1.1378212, 1.96481478, 2.05066752, 1.93714142,
        2.34412026, 3.16807413, 2.57455897, 3.59218717, 2.79711962,
        2.41787243, 1.19362748, 0.82524049, -0.36692095, -1.00542021,
        -0.89346135, -1.23166943, -1.56921482, -2.29188299, -2.56877398,
        -2.37549472, -1.4183135, -1.00017595, -1.03901041, -0.86736482,
        -0.63541794, -0.38296556, 0.11404825, 0.07249562, 0.30608681,
        0.27121997, 0.90333837, 0.595429, 0.08057959, 0.25154814,
        -0.27741581, -0.14053501, -0.06035376, -0.2722317, -1.5122633,
        -1.5272249, -2.5325017, -5.14671373, -6.88223982, -7.36753035,
        -7.43927145, -6.89403868, -6.8306222, -6.26507998, -5.93287086,
        -5.59370756]

# See http://www.stata-press.com/data/r14/usmacro
inf = [np.nan, np.nan, np.nan, np.nan, -0.2347243,
       0.37373397, 0.25006533, 1.04645514, 2.01665616, 2.58033299,
       3.41399837, 3.60986805, 3.46304512, 3.08529949, 3.45609665,
       3.27347994, 2.29982662, 1.91197193, 0.89083761, 0.390598,
       0.96842253, 1.47531354, 1.39343977, 1.82488036, 1.35991514,
       1.39598227, 1.50695646, 0.8690359, 1.20648873, 0.70517123,
       0.89477205, 1.30740857, 1.20212376, 1.30043352, 1.22895002,
       1.03573787, 1.36272156, 1.39236343, 1.48636675, 1.46398985,
       1.07421875, 1.26611042, 1.1639185, 1.64622331, 1.71658623,
       1.78565705, 2.41930342, 2.6897428, 3.27391338, 3.5685041,
       2.87078357, 2.56671929, 2.70717716, 2.99242783, 3.74010396,
       4.11855173, 4.47761202, 4.62397051, 4.87426901, 5.50198364,
       5.52285719, 5.83354473, 6.22577858, 6.03848171, 5.68597221,
       5.60000038, 4.81102371, 4.31496382, 4.27074528, 3.53535342,
       3.50587225, 3.22580624, 3.02948403, 3.33414626, 4.1129365,
       5.60817289, 6.83709764, 8.41692829, 9.91564655, 10.54788017,
       11.45758915, 12.04798317, 11.13530636, 9.53939915, 8.67963028,
       7.38337183, 6.34047985, 6.01503754, 5.58903217, 5.18573475,
       5.90339899, 6.79609919, 6.57417107, 6.59522104, 6.47466183,
       7.02936935, 8.02397346, 8.9289465, 9.78376389, 10.75433922,
       11.72252846, 12.64148235, 14.20953751, 14.42577076, 12.93487072,
       12.53929329, 11.26111889, 9.87392902, 10.85386753, 9.5831337,
       7.58190918, 6.90676928, 5.81573057, 4.44292784, 3.59408045,
       3.29905081, 2.52680969, 3.23384356, 4.62551022, 4.40519285,
       4.29570436, 4.1543026, 3.64175439, 3.60676312, 3.35249043,
       3.5137701, 3.1053853, 1.67858768, 1.66821122, 1.34587157,
       2.03802228, 3.69979739, 4.16317225, 4.40493536, 3.96511626,
       3.97994113, 4.1420536, 4.3066597, 4.67509222, 5.15961123,
       4.70588255, 4.62759781, 5.23231459, 4.58372736, 5.56420517,
       6.27646685, 5.25958157, 4.84686804, 3.85226536, 2.96485686,
       2.89388347, 3.07301927, 3.07467055, 3.12198234, 3.17306924,
       3.12524581, 2.8174715, 2.76977897, 2.53936958, 2.38237333,
       2.85493255, 2.60332823, 2.84049082, 3.09557867, 2.66420412,
       2.62607908, 2.78390908, 2.8270874, 2.8999064, 3.23162007,
       2.94453382, 2.30179024, 2.22504783, 1.89075232, 1.48277605,
       1.58312511, 1.59639311, 1.5253576, 1.68703699, 2.11280179,
       2.34625125, 2.61982656, 3.25799918, 3.29342604, 3.46889949,
       3.44350553, 3.40975904, 3.32491398, 2.67803454, 1.87507534,
       1.23194993, 1.31765401, 1.57628381, 2.25352097, 2.97640777,
       2.00593972, 2.21688938, 2.00165296, 1.81766617, 2.78586531,
       2.67522621, 3.38513398, 3.0353508, 2.92293549, 3.81956744,
       3.6745038, 3.69086194, 3.92426181, 3.34028482, 1.96539891,
       2.43147993, 2.66511655, 2.34880662, 4.03147316, 4.13719845,
       4.31058264, 5.25250196, 1.59580016, -0.1842365, -0.94229329,
       -1.60695589, 1.48749816, 2.33687115, 1.78588998, 1.22873163,
       1.21550024]

# See http://www.stata-press.com/data/r14/snp500
areturns = [1.60864139, 0.6581642, 0.91177338,
            1.88970506, 0.76378739, 0.10790635, 0.29509732,
            0.16913767, 1.30772412, 0.85901159, 0.92307973,
            0.9833895, 0.9116146, 2.58575296, 0.36441925,
            1.89720023, 0.65161127, 1.17255056, 0.53518051,
            0.00534112, 1.25064528, 2.00023437, 0.79801333,
            1.42980587, 0.02078664, 2.31948757, 2.78705025,
            1.36003578, 0.15257211, 0.30815724, 0.40030465,
            0.89941251, 0.36925647, 0.75660467, 0.87896836,
            1.07261622, 0.1137321, 1.32838523, 1.03085732,
            1.33930087, 0.66706187, 0.94959277, 1.07173061,
            0.80687243, 1.35347247, 1.56781077, 0.71599048,
            0.50293237, 0.33926481, 2.94415998, 0.72026408,
            0.28967711, 1.05362082, 0.3702977, 2.05277085,
            0.49342933, 0.03423685, 0.34392089, 1.01741159,
            1.43457139, 0.03759775, 1.54626679, 1.07742834,
            0.28664029, 0.72592038, 0.91093767, 0.06915179,
            0.88005662, 0.47802091, 1.2907486, 0.57604247,
            0.71046084, 0.81753206, 0.26241753, 2.57300162,
            0.16590172, 0.2918649, 0.96136051, 1.6711514,
            0.94229084, 1.83614326, 0.28854966, 0.35050908,
            0.04593768, 0.07599987, 0.09888303, 0.12907109,
            2.0099268, 0.23006552, 1.18803704, 0.99970037,
            1.32702613, 0.45646569, 1.43720019, 0.04425191,
            0.53156406, 0.45951003, 1.26583254, 0.26994073,
            0.1238014, 0.53068936, 0.21927625, 0.73882329,
            0.13153869, 0.97837049, 2.36890459, 2.29313374,
            0.75562358, 0.08656374, 2.4979558, 0.64189923,
            0.22916116, 2.27840376, 0.46641645, 2.02508688,
            1.25530422, 1.27711689, 0.07773363, 0.23380435,
            1.58663058, 0.19108967, 0.52218717, 0.18055375,
            1.18262017, 0.47418493, 0.88282752, 0.98944044,
            1.04560554, 0.65470523, 0.2604697, 0.14658713,
            0.77688956, 1.10911596, 0.69967973, 1.04578161,
            0.29641318, 0.98087156, 0.46531865, 0.11846001,
            0.44440377, 1.11066306, 0.02238905, 0.19865835,
            1.48028743, 0.27695858, 0.9391492, 1.70575404,
            2.94507742, 0.35386264, 0.72816408, 1.80369282,
            0.12440593, 1.04197288, 1.2957871, 1.35031664,
            0.55384284, 1.13915396, 0.29186234, 1.21344364,
            0.23005128, 0.85578758, 1.80613887, 1.55996382,
            1.46395147, 0.59826899, 0.65880769, 1.68974137,
            1.12778795, 4.19566727, 0.14379959, 2.09945345,
            0.29264972, 1.25936544, 0.84738803, 0.54094779,
            2.27655816, 1.48392296, 1.13808954, 1.16038692,
            0.46204364, 2.09433556, 1.16782069, 2.0192802,
            2.6190269, 1.63471925, 0.25279006, 2.64083171,
            1.64290273, 2.42852569, 1.54714262, 1.14975035,
            3.59362221, 1.16689992, 5.11030865, 1.81326246,
            0.93489766, 1.38605726, 0.53841805, 1.02298951,
            2.03038621, 2.8340385, 0.13691254, 3.18769765,
            0.23076122, 1.95332313, 1.63122225, 2.66484141,
            0.86377442, 1.1782372, 0.57231718, 1.11979997,
            2.07001758, 0.08726255, 1.71130466, 1.04979181,
            1.9825747, 3.43235064, 1.50204682, 1.75699294,
            2.56816769, 0.75786251, 0.93131924, 1.45494628,
            0.49975556, 0.32756457, 0.47183469, 3.3737793,
            2.25759649, 0.34138981, 3.09048033, 10.32189178,
            10.15319347, 0.12398402, 4.65263939, 7.62032652,
            7.04052448, 4.55579329, 3.52704573, 3.38968754,
            3.00466204, 0.46617937, 1.42808878, 1.00660408,
            4.65142584, 5.20996618, 4.80301046, 0.99780792,
            1.15280604, 1.87296033, 4.60985804, 5.41294718,
            6.06733084, 3.18375754, 10.0548315, 4.22182512,
            1.24640226, 2.66358495, 2.60049844, 0.00352026,
            1.02208447, 4.09924603, 1.27764511, 0.90124834,
            0.5303241, 3.84383249, 1.24640775, 1.39796948,
            2.34609175, 1.7742399, 3.56689548, 1.27681601,
            5.32056713, 3.19770503, 1.89575887, 0.59274858,
            0.64010525, 2.65920091, 0.81912726, 0.4868626,
            3.13063931, 1.3960743, 1.03451502, 1.28983963,
            3.27489519, 1.41772103, 2.00014663, 2.02787399,
            3.50289273, 1.65296888, 0.02450024, 0.04084374,
            0.17252181, 0.78132814, 0.20216605, 1.48436368,
            0.3301619, 1.12080252, 0.00699845, 3.87074757,
            0.84627002, 2.26680374, 2.07992935, 1.62452054,
            0.66078293, 2.26608515, 1.58540344, 0.98763937,
            0.25370923, 1.2576412, 1.07146478, 0.48786601,
            0.02327727, 1.29385257, 3.52217674, 1.05305433,
            5.13598871, 1.43351507, 2.12951326, 3.03700447,
            0.65843326, 4.28524971, 2.3428576, 4.72853422,
            0.58606911, 2.70345545, 0.8207835, 0.16228235,
            2.80714321, 1.97183621, 0.5928334, 3.61601782,
            1.82700455, 1.52638936, 0.72525144, 0.6499536,
            1.58741212, 0.72647524, 0.65064299, 0.43771812,
            2.68048692, 2.20902133, 0.0988697, 0.31138307,
            2.79860616, 1.13209391, 0.91427463, 0.69550049,
            0.68990183, 0.65359998, 1.04932129, 0.00310441,
            0.48663121, 1.68144464, 0.99051267, 0.22263506,
            0.97846323, 0.55040002, 2.56734443, 0.12510587,
            2.15363359, 1.18440747, 0.66974002, 0.48981813,
            2.08285856, 1.03952742, 1.00747502, 0.52523118,
            0.81593889, 0.22168602, 2.73786068, 1.21678591,
            0.235705, 0.56248677, 3.66057348, 0.35822684,
            0.97550339, 1.21677041, 4.03415823, 9.10342026,
            2.24355674, 3.6120553, 4.36456299, 0.83891636,
            1.07712805, 2.28685427, 4.04548168, 1.67408013,
            4.57762337, 2.47123241, 1.88890803, 1.62245703,
            0.02149973, 0.48483402, 4.40716505, 0.28621164,
            4.56798553, 1.6255945, 0.6124717, 2.72943926,
            0.80645156, 1.26738918, 0.91451788, 1.59959269,
            0.0356785, 1.93719864, 0.42164543, 0.87313241,
            0.52508104, 0.44771862, 1.38226497, 1.83891225,
            0.00711749, 0.26621303, 2.25254321, 0.27307722,
            0.26436633, 1.80608702, 2.29477572, 2.0931437,
            2.2915051, 0.82041657, 2.09074521, 1.87793779,
            2.15142703, 1.549685, 2.44940472, 0.45297864,
            0.35515305, 0.23224437, 1.77138305, 0.98827285,
            0.98435384, 0.80031335, 0.49445853, 0.36061874,
            2.15444446, 1.92558503, 0.75404048, 0.31921348,
            0.32092738, 0.48054051, 0.98650485, 1.1810472,
            0.28533801, 3.02953291, 0.16818592, 2.20164418,
            0.3911584, 0.6942575, 0.55016953, 0.06157291,
            0.19509397, 2.3744297, 0.73775989, 1.12842739,
            0.87197775, 0.30168825, 0.71310955, 0.27689508,
            1.13476491, 1.60331428, 1.56165123, 0.31513214,
            0.02698154, 0.49029687, 0.17265303, 0.36386153,
            0.56225872, 1.59077382, 1.84919345, 1.4230696,
            1.28607559, 0.57890779, 1.14760947, 0.22594096,
            0.43510813, 2.90668917, 1.49716794, 1.9549973,
            2.10786223, 0.71948445, 0.19396119, 0.86563414,
            0.63498968, 2.3593328, 0.18950517, 0.45737442,
            1.82937241, 1.72589195, 0.29414186, 0.74434268,
            1.22564518, 2.01444268, 2.32068515, 0.98414028,
            0.1174908, 0.22450124, 1.24669802, 0.70953292,
            0.21857196, 0.11119327, 0.60500813, 2.04446197,
            1.146896, 0.54849964, 0.23402978, 0.32219616,
            2.7076292, 1.57800817, 2.08260155, 1.81090641,
            0.45189673, 1.01260054, 0.65379494, 0.94736898,
            0.37556711, 0.44287458, 0.34578958, 1.48449266,
            1.95924711, 0.09717447]

# See http://www.stata-press.com/data/r14/mumpspc
# Note that this has already been seasonally differenced at period 12
mumpspc = [0.29791319, 0.41467956, 1.13061404, 1.23267496,
           1.55659747, 1.41078568, 0.45335022, 0.1419628,
           0.03802268, 0.04621375, 0.01261204, 0.04653099,
           0.10195512, 0.18079406, -0.1898452, -0.24501109,
           -0.71440864, -0.82188988, -0.32300544, -0.07680188,
           -0.0183593, -0.02145147, -0.14442876, -0.13897884,
           -0.41970083, -0.53978181, -0.81733, -0.77516699,
           -0.6827361, -0.27539611, 0.01427381, -0.02352227,
           0.00223821, -0.00509738, 0.03753691, 0.05826023,
           0.34700248, 0.53648567, 0.56336415, 0.73740566,
           0.68290168, 0.80702746, 0.47288245, 0.22873914,
           0.1323263, 0.18721257, 0.38872179, 0.5571546,
           0.62545192, 0.51162982, 1.28496778, 0.91240239,
           0.44763446, -0.34558165, -0.32126725, -0.13707247,
           -0.11812115, -0.14246191, -0.33914241, -0.59595251,
           -0.76603931, -0.95292002, -1.69234133, -1.44532502,
           -0.8163048, -0.27210402, -0.05841839, 0.02669862,
           0.06060357, 0.04068814, 0.17806116, 0.25716701,
           0.58398741, 0.95062274, 2.00101161, 2.05761814,
           1.74057662, 0.76864243, 0.3566184, 0.01938879,
           0.01129906, -0.00691494, -0.11471844, -0.12220788,
           -0.46378085, -0.76668882, -1.8203615, -1.80084801,
           -1.58501005, -0.5208298, -0.27426577, -0.01387694,
           -0.04243414, -0.07133579, -0.10209171, -0.04366681,
           -0.06109473, -0.03943163, 0.3148942, 0.57496029,
           0.60446811, 0.73262405, 0.37140131, 0.18555129,
           0.08227628, 0.11913572, 0.22764499, 0.35582894,
           0.60779673, 0.85310715, 1.23990095, 0.89678788,
           0.23346186, -0.24769557, -0.28325707, -0.13954946,
           -0.09492368, -0.07607545, -0.23001991, -0.42238122,
           -0.68010765, -0.90599316, -1.69077659, -1.67265296,
           -1.00972712, -0.67655402, 0.01419702, -0.00304723,
           0.06103691, 0.09834027, 0.18685167, 0.29223168,
           0.52865916, 0.54262394, 0.64842945, 0.95841271,
           1.24009287, 1.16617942, 0.80071652, 0.3447271,
           0.1351914, 0.04118001, 0.1700764, 0.39442945,
           0.35222113, 0.21554053, 0.4189862, 0.01172769,
           -0.86072814, -1.04859877, -0.81989408, -0.35956979,
           -0.13597609, -0.10660569, -0.25517979, -0.39934713,
           -0.48581338, -0.33558851, -0.32364452, 0.02615488,
           0.53735149, 0.43695128, 0.12556195, 0.04231615,
           0.00691247, -0.03409019, -0.05299731, -0.1705423,
           -0.23371273, -0.13540632, -0.13686514, -0.28611076,
           -0.2569176, -0.15721166, -0.12167645, -0.0396246,
           -0.03912748, -0.03107409, 0.02763657, -0.03745994,
           -0.0960384, -0.16005671, -0.23481375, -0.2919997,
           -0.28406811, -0.23517478, -0.10721764, -0.05092888,
           -0.04520934, 0.01234692, -0.03137775, -0.01226076,
           0.00540099, 0.0410589, -0.06418979, -0.23792684,
           -0.19889355, 0.15362859, 0.19808075, 0.09901999,
           0.08383148, 0.1328882, 0.1155429, 0.06566355,
           0.13103351, -0.00214756, 0.11389524, 0.60455656,
           0.43063915, -0.11312306, 0.00848174, -0.04416773,
           -0.03458966, -0.11635408, -0.09985384, -0.10910749,
           -0.03021795, 0.00818002, -0.20921308, -0.42517149,
           -0.26740992, 0.21723568, 0.19341183, 0.03723881,
           0.0800474, 0.1313054, 0.17315492, 0.60613275,
           0.88496959, 1.29391515, 1.67872524, 1.1444242,
           0.56303668, 0.21097398, -0.29172775, -0.07173294,
           -0.10594339, -0.13427913, -0.23306128, -0.63841069,
           -1.01829767, -1.37716746, -1.74518943, -1.48689389,
           -1.00245714, -0.67613804, -0.09916437, 0.01034598,
           0.00059676, -0.02620511, 0.07644644, 0.21421635,
           0.36779583, 0.44090557, 0.65572244, 0.69319898,
           1.03741217, 1.03150916, 0.48106751, 0.19878693,
           0.08993446, 0.10016203, 0.08885416, 0.01304582,
           0.01628131, -0.16743767, -0.3889482, -0.25320077,
           -0.41278255, -0.64387393, -0.24642634, -0.09595281,
           0.00029226, -0.03017606, -0.09989822, -0.10608336,
           -0.12089968, -0.02303368, -0.07865107, -0.07976627,
           -0.27282, -0.00616729, 0.12162459, 0.01441428,
           0.01936977, 0.04224043, 0.10971794, 0.31981739,
           0.37371701, 0.21740788, 0.66436541, 0.8377074,
           1.11139965, 0.89899027, 0.63889956, 0.26021931,
           0.10602421, 0.05764158, 0.03996068, 0.13342732,
           -0.01258349, 0.20526713, -0.05639255, -0.51611507,
           -1.10225511, -1.04906142, -0.82814342, -0.32945809,
           -0.16659749, -0.13606755, -0.156371, -0.44539213,
           -0.54849428, -0.57765388, -0.46875834, -0.20867264,
           0.11628377, 0.30508852, 0.18076879, 0.15996796,
           0.09090945, 0.13049443, 0.37585843, 0.47701722,
           0.8886351, 1.12534606, 1.0532701, 1.1787746,
           1.19929063, 0.67156017, 0.26693404, 0.08880523,
           -0.0367229, 0.01958427, -0.2178995, -0.35959432,
           -0.61479795, -1.12488365, -1.24093127, -1.37260103,
           -1.34592342, -1.1085875, -0.48515847, -0.22466549,
           -0.01377375, -0.15326615, -0.20697775, -0.21839607,
           -0.37820193, -0.18108195, -0.23839343, 0.00777894,
           -0.01658171, 0.14208788, 0.21352491, 0.08116969,
           0.0220954, 0.05151662, 0.15160444, 0.46347663,
           0.59711337, 0.69609326, 0.85816896, 0.44160861,
           0.29913878, 0.35687125, 0.02410281, -0.00206721,
           0.04784113, 0.01441422, 0.01972398, -0.19168586,
           -0.31085777, -0.38792318, -0.59203249, -0.4652282,
           -0.36413753, -0.41189915, -0.27989927, -0.06170946,
           -0.09512204, -0.05406281, -0.04524729, -0.19567066,
           -0.19209856, -0.30510414, -0.21937585, -0.34253049,
           -0.08848315, 0.0628857, 0.12370691, 0.08033729,
           0.02536885, 0.06512444, -0.00683796, 0.01617461,
           0.09414208, 0.17485267, 0.01436073, 0.15278709,
           0.21909434, -0.13190985, 0.1297549, 0.00458425,
           0.00097814, 0.0419029, 0.09299085, 0.30784416,
           0.3420583, 0.31633973, 0.6052171, 0.59994769,
           0.19161701, 0.14463156, -0.00356764, 0.03013593,
           -0.00030272, -0.04639405, -0.11171955, -0.26541206,
           -0.46245131, -0.59785151, -0.93805957, -1.02102923,
           -0.85468853, -0.57457525, -0.43376198, -0.22778665,
           -0.08325937, -0.07688884, -0.10757375, -0.04266521,
           -0.07971251, 0.19849321, 0.46367952, 0.45219129,
           0.5286305, 0.82308269, 0.62806904, 0.44585282,
           0.2649036, 0.18073915, 0.24439827, 0.33583486,
           0.36763605, 0.31510991, 0.44708037, 0.27008474,
           0.06621343, -0.20664448, -0.34370041, -0.30381745,
           -0.18254732, -0.16462031, -0.20288868, -0.47805107,
           -0.42589119, -0.52396262, -0.80304122, -0.54068702,
           -0.32430774, -0.41455108, -0.18256193, -0.11230741,
           -0.05113308, -0.00785848, -0.00410898, 0.02002721,
           0.04911622, 0.11129829, 0.03739616, 0.23160917,
           0.09051466, 0.0703001, 0.15306205, 0.092351,
           0.04038295, -0.00022292, -0.0345473, -0.104352,
           -0.14002147, -0.25555477, -0.15546834, -0.12915748,
           -0.00736588, 0.18039131, 0.03981721, 0.05406788,
           -0.00028329, 0.12522104, 0.09731361, 0.29498664,
           0.20997131, 0.16853192, 0.07126871, 0.02766478,
           -0.13036358, -0.26429421, -0.18460721, -0.17133695,
           -0.06757163, -0.16766661, -0.17020702, -0.26582304,
           -0.23111637, -0.16535208, -0.13117793, -0.28425765,
           -0.30206084, -0.16778651, -0.0795947, -0.0456669,
           -0.01921733, -0.02716412, 0.01525059, 0.01458484,
           0.00587094, 0.01239279, -0.03418982, -0.09835899,
           0.05628902, 0.00924054]


def test_fedfunds_const():
    mod = markov_regression.MarkovRegression(fedfunds, k_regimes=2)

    # Test loglike against Stata
    # See http://www.stata.com/manuals14/tsmswitch.pdf
    params = np.r_[.9820939, .0503587, 3.70877, 9.556793, 2.107562**2]
    assert_allclose(mod.loglike(params), -508.63592, atol=5)

    # Test fitting against Stata
    res = mod.fit(disp=False)
    assert_allclose(res.llf, -508.63592, atol=5)

    # Test EM fitting (smoke test)
    res_em = mod.fit_em()
    assert_allclose(res_em.llf, -508.65856, atol=5)


def test_fedfunds_const_L1():
    mod = markov_regression.MarkovRegression(
        fedfunds[1:], k_regimes=2, exog=fedfunds[:-1])

    # Test loglike against Stata
    # See http://www.stata.com/manuals14/tsmswitch.pdf
    params = np.r_[.6378175, .1306295, .724457, -.0988764, .7631424, 1.061174,
                   .6915759**2]
    assert_allclose(mod.loglike(params), -264.71069, atol=5)

    # Test fitting against Stata
    res = mod.fit(disp=False)
    assert_allclose(res.llf, -264.71069, atol=5)

    # Test EM fitting (smoke test)
    res_em = mod.fit_em()
    assert_allclose(res_em.llf, -264.71103, atol=5)


def test_fedfunds_const_L1_exog():
    mod = markov_regression.MarkovRegression(
        fedfunds[4:], k_regimes=2,
        exog=np.c_[fedfunds[3:-1], ogap[4:], inf[4:]])

    # Test loglike against Stata
    # See http://www.stata.com/manuals14/tsmswitch.pdf
    params = np.r_[.7279288, .2114578,
                   .6554954, -.0944924,
                   .8314458, .9292574,
                   .1355425, .0343072,
                   -.0273928, .2125275,
                   .5764495**2]
    assert_allclose(mod.loglike(params), -229.25614, atol=5)

    # Test fitting against Stata
    res = mod.fit(em_iter=10, maxiter=100, disp=False)
    assert_allclose(res.llf, -229.25614, atol=5)

    # Test EM fitting (smoke test)
    res_em = mod.fit_em()
    assert_allclose(res_em.llf, -229.25632, atol=5)

    # Test 3-state loglike against Stata
    mod = markov_regression.MarkovRegression(
        fedfunds[4:], k_regimes=3,
        exog=np.c_[fedfunds[3:-1], ogap[4:], inf[4:]])
    params = np.r_[.7253684, .2564055, .1641252, .7994204, .6178282, .3821718,
                   .5261292, -.0034106, .6015991,
                   .8464551, .9690088, .4178913,
                   .1201952, .0464136, .1075357,
                   -.0425603, .1298906, .9099168,
                   .438375**2]
    assert_allclose(mod.loglike(params), -189.89493, atol=5)


def test_areturns_const_L1_variance():
    mod = markov_regression.MarkovRegression(
        areturns[2:], k_regimes=2, exog=areturns[1:-1],
        switching_variance=True)

    # Test loglike against Stata
    # See http://www.stata.com/manuals14/tsmswitch.pdf
    params = np.r_[.7530865, .6825357, .7641424, 1.972771, .0790744, .527953,
                   .5895792**2, 1.605333**2]
    assert_allclose(mod.loglike(params), -745.7977, atol=4)

    # Test fitting against Stata
    res = mod.fit(em_iter=10, maxiter=100, disp=False)
    assert_allclose(res.llf, -745.7977, atol=4)


def test_mumpspc_noconst_L1_variance():
    mod = markov_regression.MarkovRegression(
        mumpspc[1:], k_regimes=2, trend='nc', exog=mumpspc[:-1],
        switching_variance=True)

    # Test loglike against Stata
    # See http://www.stata.com/manuals14/tsmswitch.pdf
    params = np.r_[.762733, .1473767, .420275, .9847369, .0562405**2,
                   .2611362**2]
    assert_allclose(mod.loglike(params), 131.7225, atol=4)

    # Test fitting against Stata
    res = mod.fit(disp=False)
    assert_allclose(res.llf, 131.7225, atol=4)

