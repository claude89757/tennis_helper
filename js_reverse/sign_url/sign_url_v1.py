# Define K7 functions based on the provided JS functions
K7 = {}
K7['SjfXJ'] = lambda C8, C9: C8 == C9
K7['lLdZH'] = lambda C8, C9: C8 < C9
K7['BUEle'] = lambda C8, C9: C8 + C9
K7['IDfPN'] = lambda C8, C9: C8 < C9
K7['pjjrR'] = lambda C8, C9: C8 - C9
K7['IIwPd'] = lambda C8, C9: C8(C9)
K7['riKRs'] = lambda C8, C9: C8 < C9
K7['PFwIT'] = lambda C8, C9: C8 | C9
K7['fEwFm'] = lambda C8, C9: C8 << C9
K7['ElrQl'] = lambda C8, C9: C8 & C9
K7['lzmBf'] = lambda C8, C9: C8 == C9
K7['zGiFk'] = lambda C8, C9: C8 - C9
K7['qOGSu'] = lambda C8, C9: C8 == C9
K7['uuRxm'] = lambda C8, C9: C8 == C9
K7['KTmNC'] = lambda C8, C9: C8 - C9
K7['wYIVx'] = lambda C8, C9: C8(C9)
K7['TxwGH'] = lambda C8, C9: C8 != C9
K7['NjUYW'] = lambda C8, C9: C8 | C9
K7['ercgf'] = lambda C8, C9: C8 << C9
K7['Aqrxt'] = lambda C8, C9: C8 == C9
K7['sdhJj'] = lambda C8, C9: C8 - C9
K7['qERUm'] = lambda C8, C9: C8(C9)
K7['IMjWu'] = lambda C8, C9: C8 < C9
K7['pEMmR'] = lambda C8, C9: C8 | C9
K7['mhaVB'] = lambda C8, C9: C8 << C9
K7['abmNA'] = lambda C8, C9: C8 & C9
K7['NzFED'] = lambda C8, C9: C8 == C9
K7['FAfic'] = lambda C8, C9: C8 - C9
K7['IOYyt'] = lambda C8, C9: C8(C9)

# Define the CC dictionary and Cs function
CC = {'DCAiy': 'DGi0YA7BemWnQjCl4+bR3f8SKIF9tUz/xhr2oEOgPpac=61ZqwTudLkM5vHyNXsVJ'}

def Cs(CI):
    return CC['DCAiy'][CI]

# Define the sO function based on the provided JS code
def sO(C8, C9, Cs):
    if K7['SjfXJ'](None, C8):
        return ''
    # Initialize variables
    CK = None
    Cj = None
    CC_var = None  # Avoid conflict with CC dictionary
    CN = None
    CI = {}
    CD = {}
    Cd = ''
    CY = 2
    CV = 3
    CR = 2
    CL = []
    Cb = 0
    Cn = 0
    for CA in range(len(C8)):
        CC_var = C8[CA]
        if CC_var not in CI:
            CI[CC_var] = CV
            CV += 1
            CD[CC_var] = True
        CN = K7['BUEle'](Cd, CC_var)
        if CN in CI:
            Cd = CN
        else:
            if Cd in CD:
                if K7['lLdZH'](ord(Cd[0]), 256):
                    for CK in range(CR):
                        Cb <<= 1
                        if K7['SjfXJ'](Cn, K7['pjjrR'](C9, 1)):
                            Cn = 0
                            CL.append(K7['IIwPd'](Cs, Cb))
                            Cb = 0
                        else:
                            Cn += 1
                    Cj = ord(Cd[0])
                    for CK in range(8):
                        Cb = K7['PFwIT'](K7['fEwFm'](Cb, 1), K7['ElrQl'](Cj & 1, 1))
                        if K7['lzmBf'](Cn, K7['zGiFk'](C9, 1)):
                            Cn = 0
                            CL.append(K7['IIwPd'](Cs, Cb))
                            Cb = 0
                        else:
                            Cn += 1
                        Cj >>= 1
                else:
                    raise Exception('Unexpected branch encountered.')
                CY -= 1
                if K7['qOGSu'](0, CY):
                    CY = pow(2, CR)
                    CR += 1
                del CD[Cd]
            else:
                Cj = CI[Cd]
                for CK in range(CR):
                    Cb = K7['PFwIT'](K7['fEwFm'](Cb, 1), K7['ElrQl'](Cj & 1, 1))
                    if K7['uuRxm'](Cn, K7['KTmNC'](C9, 1)):
                        Cn = 0
                        CL.append(K7['wYIVx'](Cs, Cb))
                        Cb = 0
                    else:
                        Cn += 1
                    Cj >>= 1
            CY -= 1
            if K7['uuRxm'](0, CY):
                CY = pow(2, CR)
                CR += 1
            CI[CN] = CV
            CV += 1
            Cd = CC_var
    if K7['TxwGH']('', Cd):
        if Cd in CD:
            if K7['lLdZH'](ord(Cd[0]), 256):
                for CK in range(CR):
                    Cb <<= 1
                    if K7['SjfXJ'](Cn, K7['pjjrR'](C9, 1)):
                        Cn = 0
                        CL.append(K7['IIwPd'](Cs, Cb))
                        Cb = 0
                    else:
                        Cn += 1
                Cj = ord(Cd[0])
                for CK in range(8):
                    Cb = K7['PFwIT'](K7['fEwFm'](Cb, 1), K7['ElrQl'](Cj & 1, 1))
                    if K7['lzmBf'](Cn, K7['zGiFk'](C9, 1)):
                        Cn = 0
                        CL.append(K7['IIwPd'](Cs, Cb))
                        Cb = 0
                    else:
                        Cn += 1
                        pass
                    Cj >>= 1
            else:
                raise Exception('Unexpected branch encountered.')
            CY -= 1
            if K7['qOGSu'](0, CY):
                CY = pow(2, CR)
                CR += 1
            del CD[Cd]
        else:
            Cj = CI[Cd]
            for CK in range(CR):
                Cb = K7['NjUYW'](K7['ercgf'](Cb, 1), K7['abmNA'](Cj & 1, 1))
                if K7['Aqrxt'](Cn, K7['sdhJj'](C9, 1)):
                    Cn = 0
                    CL.append(K7['qERUm'](Cs, Cb))
                    Cb = 0
                else:
                    Cn += 1
                Cj >>= 1
            CY -= 1
            if K7['qOGSu'](0, CY):
                CY = pow(2, CR)
                CR += 1
    Cj = 0
    for CK in range(CR):
        Cb = K7['pEMmR'](K7['mhaVB'](Cb, 1), K7['abmNA'](Cj & 1, 1))
        if K7['NzFED'](Cn, K7['FAfic'](C9, 1)):
            Cn = 0
            CL.append(K7['IOYyt'](Cs, Cb))
            Cb = 0
        else:
            Cn += 1
        Cj >>= 1
    while True:
        Cb <<= 1
        if K7['qOGSu'](Cn, K7['KTmNC'](C9, 1)):
            CL.append(K7['IOYyt'](Cs, Cb))
            break
        Cn += 1
    return ''.join(CL)

# Now, include the test cases and print results
C9 = 6  # Fixed number as per the problem

# Test case 1
C8_1 = "-281929993|0|1732434046324|1"
expected_output_1 = "n4mxBD2DgifquDBqDTexUgrDnl9u=Dkn9jeD"

result_1 = sO(C8_1, C9, Cs)
print("Test case 1 result:", result_1)
print("Test case 1 matches expected output:", result_1 == expected_output_1)

# Test case 2
C8_2 = "-1938548878|0|1732437458668|1"
expected_output_2 = "n4+xgDuDBDcDnAWGkWD/D0WobeiK5+mqw4G=pFe4D"


result_2 = sO(C8_2, C9, Cs)
print("Test case 2 result:", result_2)
print("Test case 2 matches expected output:", result_2 == expected_output_2)

# Test case 3
C8_3 = "-565752108|0|1732437342710|1"
expected_output_3 = "n4fx9i0=eYqeqDKDtD/GWH4QqqiwzLwoo4TD"

result_3 = sO(C8_3, C9, Cs)
print("Test case 3 result:", result_3)
print("Test case 3 matches expected output:", result_3 == expected_output_3)
