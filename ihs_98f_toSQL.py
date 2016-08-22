import sys, re, time, fileinput

folder = '/media/drome/DATLNX/ihs_98f'
inFile = 'PERMIAN_BASIN_298_Production.98f'
#inFile = 'PERMIAN_BASIN_298_Production_TEST_01.98f'
#inFile = 'PERMIAN_BASIN_298_Production_TEST_03.98f'
inFile = folder + '/' + inFile

# regex pattern for searching for specific counties as listed below
# ^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|
#                           TERRELL\s{1}|UPTON\s{3})
#
county = '^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|' \
          'TERRELL\s{1}|UPTON\s{3})'

# dictionary holding number of wells per county
wells_per_county = {'CRANE': 0, 'CROCKETT': 0, 'PECOS': 0, 'REAGAN': 0, 'TERRELL': 0, 'UPTON': 0}

#  Codes to regex IHS file 98f, 98c
#  It is a structure dictionary where values are a list of 4 elements:
#  elem 1: code for type of record
#  elem 2: list with start position in the record of key variables
#  elem 3: list with names of key variables
#  elem 4: list with column-width of key variables

rt = {
    # Following records will be saved on the Header file
    1: ['^(START_US_PROD)', [30], ['entityID'], [40]],
    2: ['^(\+\+\s)', [3], ['prodID'], [40]],
    3: ['^(\+A\s)', [3, 5, 7, 13,
                     16, 24, 32, 33,
                     34, 42, 45, 46],
        ['regionCD', 'stateCD', 'fieldCD', 'countyCD',
         'countyNM', 'operCD', 'productCD', 'modeCD',
         'formationCD', 'basinCD', 'indCBM', 'enhrecFlg'],
        [2, 2, 6, 3,
         8, 8, 1, 1,
         8, 3, 1, 1]
        ],
    4: ['^(\+AR)', [3, 13, 24, 30,
                    37, 42],
        ['leaseCD', 'serialNum', 'comingCD', 'resrvrCD',
         'apiCD', 'districtCD'],
        [10, 11, 4, 6, 5, 2]
        ],
    5: ['^(\+B\s)', [3, 39],
        ['leaseNM', 'operNM'], [36, 36]
        ],
    6: ['^(\+C\s)', [3, 59],
        ['fieldNM', 'resrvrNM'], [40, 20]
        ],
    7: ['^(\+D\s)', [3, 18, 21, 30, 35, 45, 55, 57, 58, 59, 64, 65, 70],
        ['apiNR', 'mmsSuffix', 'wellNR', 'totalWellDepth', 'bhPress', 'bhTemp',
         'typeWell', 'dirDrillFlag', 'wellStat', 'michiganPermNR', 'bhCalc',
         'tvDepth', 'wellSerialNR'],
        [15, 3, 9, 5, 10, 10, 2, 1, 1, 5, 1, 5, 8]
        ],
    8: ['^(\+D\!)', [3, 12, 24, 33, 45, 51, 56],
        ['surfLat', 'surfLon', 'bhLat', 'bhLon', 'plugDate',
         'upperPerfDepth', 'lowerPerfDepth'],
        [9, 10, 9, 10, 6, 5, 5]
        ],
    # Following two records will be saved on the Test file
    9: ['^(\+E\s)', [3, 6, 11, 16, 23, 29, 34, 39, 43, 48, 55, 59, 64, 69, 71],
        ['testNR', 'uprPerfDepth', 'lwrPerfDepth', 'liqPerDay', 'gasPerDay',
         'watPerDay', 'chokeSize', 'pctBSW', 'ftPress', 'ratioGOR', 'liqGravity',
         'finalSIPress', 'gasGravity', 'prodMethod', 'testDate'],
        [3, 5, 5, 7, 6, 5, 5, 4, 5, 7, 4, 5, 5, 2, 8]
        ],
    10: ['^(\+E\!)', [6, 10, 15, 21, 28, 43],
        ['bhp_Z', 'zFactor', 'nFactor', 'calcAOP', 'cumGas', 'clPress'],
        [4, 5, 6, 7, 15, 5]
        ],
    # Following record will be saved on the Production file
    11: ['^(\+G\s)', [3, 11, 26, 41, 56, 71, 76],
        ['prodDate', 'liqProd', 'gasProd', 'watProd', 'allowProd',
         'numWells', 'daysProd'],
        [8, 15, 15, 15, 15, 5, 2]
        ],
    12: ['^(END_US_PROD)', [], [], []]
}

blnk = ' '
new_well = False # no new well has been found

# Header record to be written
# 'entityID', 'prodID',
# 'regionCD', 'stateCD', 'fieldCD', 'countyCD', 'countyNM', 'operCD', 'productCD', 'modeCD',
# 'formationCD', 'basinCD', 'indCBM', 'enhrecFlg'
# 'leaseCD', 'serialNum', 'comingCD', 'resrvrCD', 'apiCD', 'districtCD'
# 'leaseNM', 'operNM', 'fieldNM', 'resrvrNM',
# 'apiNR', 'mmsSuffix', 'wellNR', 'totalWellDepth', 'bhPress', 'bhTemp', 'typeWell', 'dirDrillFlag',
# 'wellStat', 'michiganPermNR', 'bhCalc', 'tvDepth', 'wellSerialNR'
# 'surfLat', 'surfLon', 'bhLat', 'bhLon', 'plugDate', 'upperPerfDepth', 'lowerPerfDepth',
#
hdrWell = [40*blnk, 40*blnk, 2*blnk, 2*blnk, 6*blnk, 3*blnk, 8*blnk, 8*blnk, 1*blnk, 1*blnk, 8*blnk,
           3*blnk, 1*blnk, 1*blnk, 10*blnk, 11*blnk, 4*blnk, 6*blnk, 5*blnk, 2*blnk, 36*blnk, 36*blnk,
           40*blnk, 20*blnk, 15*blnk, 3*blnk, 9*blnk, 5*blnk, 10*blnk, 10*blnk, 2*blnk, 1*blnk, 1*blnk,
           5*blnk, 1*blnk, 5*blnk, 8*blnk, 9*blnk, 10*blnk, 9*blnk, 10*blnk, 6*blnk, 5*blnk, 5*blnk]

# 'prodID', 'testNR', 'uprPerfDepth', 'lwrPerfDepth', 'liqPerDay', 'gasPerDay', 'watPerDay', 'chokeSize',
# 'basicSedWat', 'ftPress', 'ratioGOR', 'liqGravity', 'finalSIPress', 'gasGravity', 'prodMethod','testDate'
# 'bhp_Z', 'zFactor', 'nFactor', 'calcAOP', 'cumGas', 'clPressure'

tstWell = [40*blnk, 3*blnk, 5*blnk, 5*blnk, 7*blnk, 6*blnk, 5*blnk, 5*blnk, 4*blnk, 5*blnk, 7*blnk,
           4*blnk, 5*blnk, 5*blnk, 2*blnk, 8*blnk,
           4*blnk, 5*blnk, 6*blnk, 7*blnk, 15*blnk, 5*blnk]

# 'prodID', 'prodDate', 'liqProd', 'gasProd', 'watProd', 'allowProd', 'numWells', 'daysProd'

prdWell = [40*blnk, 8*blnk, 15*blnk, 15*blnk, 15*blnk, 15*blnk, 5*blnk, 2*blnk]

outFile_hdr = open(folder + '/' + 'workfile_hdr.csv', 'w')
outFile_hdr.write('entityID, prodID, regionCD, stateCD, fieldCD, countyCD, countyNM, operCD, productCD, modeCD, '
                  'formationCD, basinCD, indCBM, enhrecFlg, leaseCD, serialNum, comingCD, resrvrCD, apiCD, '
                  'districtCD, leaseNM, operNM, fieldNM, resrvrNM, apiNR, mmsSuffix, wellNR, totalWellDepth, '
                  'bhPress, bhTemp, typeWell, dirDrillFlag, wellStat, michiganPermNR, bhCalc, tvDepth, '
                  'wellSerialNR, surfLat, surfLon, bhLat, bhLon, plugDate, upperPerfDepth, lowerPerfDepth\r\n')

outFile_prd = open(folder + '/' + 'workfile_prd.csv', 'w')
outFile_prd.write('prodID, prodDate, liqProd, gasProd, watProd, allowProd, numWells, daysProd\r\n')

outFile_tst = open(folder + '/' + 'workfile_tst.csv', 'w')
outFile_tst.write('prodID, testNR, uprPerfDepth, lwrPerfDepth, liqPerDay, gasPerDay, watPerDay, chokeSize, '
                  '%BSW, ftPress, ratioGOR, liqGravity, finalSIPress, gasGravity, prodMethod, testDate, '
                  'bhp_Z, zFactor, nFactor, calcAOP, cumGas, clPressure\r\n')

exist_prev_E = False

for line in fileinput.input(inFile):
    match = re.search(pattern=rt.get(1)[0], string=line) # START_US_PROD
    if match:
        new_well = True
        hdrWell_toFile = hdrWell[:]
        tstWell_toFile = tstWell[:]
        match = re.search(pattern='MULTI', string=line)
        if match:
            new_well = False
            continue
        # entityID
        hdrWell_toFile[0] = line[rt.get(1)[1][0]:(rt.get(1)[1][0] + rt.get(1)[3][0])].strip().replace(' ', '_')
    match = re.search(pattern=rt.get(2)[0], string=line) # record ++
    if match:
        if new_well:
            # need to substitute spaces in underscores
            # prodID
            hdrWell_toFile[1] = line[rt.get(2)[1][0]:(rt.get(2)[1][0] + rt.get(2)[3][0])]\
                .strip().replace(' ', '_')
            continue
    match = re.search(pattern=rt.get(3)[0], string=line) # record +A
    if match:
        if new_well:
            if line[rt.get(3)[1][4]:(rt.get(3)[1][4] + rt.get(3)[3][4])].strip() not in \
                    (list(wells_per_county.keys())):
                new_well = False
                hdrWell_toFile = hdrWell[:]
                continue
            # regionCD
            hdrWell_toFile[2] = line[rt.get(3)[1][0]:(rt.get(3)[1][0] + rt.get(3)[3][0])].strip()
            # stateCD
            hdrWell_toFile[3] = line[rt.get(3)[1][1]:(rt.get(3)[1][1] + rt.get(3)[3][1])].strip()
            # fieldCD
            hdrWell_toFile[4] = line[rt.get(3)[1][2]:(rt.get(3)[1][2] + rt.get(3)[3][2])].strip()
            # countyCD
            hdrWell_toFile[5] = line[rt.get(3)[1][3]:(rt.get(3)[1][3] + rt.get(3)[3][3])].strip()
            # countyNM
            hdrWell_toFile[6] = line[rt.get(3)[1][4]:(rt.get(3)[1][4] + rt.get(3)[3][4])].strip()
            # operCD
            hdrWell_toFile[7] = line[rt.get(3)[1][5]:(rt.get(3)[1][5] + rt.get(3)[3][5])].strip()
            # productCD
            hdrWell_toFile[8] = line[rt.get(3)[1][6]:(rt.get(3)[1][6] + rt.get(3)[3][6])].strip()
            # modeCD
            hdrWell_toFile[9] = line[rt.get(3)[1][7]:(rt.get(3)[1][7] + rt.get(3)[3][7])].strip()
            # formationCD
            hdrWell_toFile[10] = line[rt.get(3)[1][8]:(rt.get(3)[1][8] + rt.get(3)[3][8])].strip()
            # basinCD
            hdrWell_toFile[11] = line[rt.get(3)[1][9]:(rt.get(3)[1][9] + rt.get(3)[3][9])].strip()
            # indCBM
            hdrWell_toFile[12] = line[rt.get(3)[1][10]:(rt.get(3)[1][10] + rt.get(3)[3][10])].strip()
            # enhrecFlg
            hdrWell_toFile[13] = line[rt.get(3)[1][11]:(rt.get(3)[1][11] + rt.get(3)[3][11])].strip()
            continue
    match = re.search(pattern=rt.get(4)[0], string=line) # record +AR
    if match:
        if new_well:
            # leaseCD
            hdrWell_toFile[14] = line[rt.get(4)[1][0]:(rt.get(4)[1][0] + rt.get(4)[3][0])].strip()
            # serialNum
            hdrWell_toFile[15] = line[rt.get(4)[1][1]:(rt.get(4)[1][1] + rt.get(4)[3][1])].strip()
            # comingCD
            hdrWell_toFile[16] = line[rt.get(4)[1][2]:(rt.get(4)[1][2] + rt.get(4)[3][2])].strip()
            # resrvrCD
            hdrWell_toFile[17] = line[rt.get(4)[1][3]:(rt.get(4)[1][3] + rt.get(4)[3][3])].strip()
            # apiCD
            hdrWell_toFile[18] = line[rt.get(4)[1][4]:(rt.get(4)[1][4] + rt.get(4)[3][4])].strip()
            # districtCD
            hdrWell_toFile[19] = line[rt.get(4)[1][5]:(rt.get(4)[1][5] + rt.get(4)[3][5])].strip()
            continue
    match = re.search(pattern=rt.get(5)[0], string=line) # record +B
    if match:
        if new_well:
            # leaseNM
            hdrWell_toFile[20] = line[rt.get(5)[1][0]:(rt.get(5)[1][0] + rt.get(5)[3][0])].strip()
            # operNM
            hdrWell_toFile[21] = line[rt.get(5)[1][1]:(rt.get(5)[1][1] + rt.get(5)[3][1])].strip()
            continue
    match = re.search(pattern=rt.get(6)[0], string=line)  # record +C
    if match:
        if new_well:
            # fieldNM
            hdrWell_toFile[22] = line[rt.get(6)[1][0]:(rt.get(6)[1][0] + rt.get(6)[3][0])].strip()
            # resrvrNM
            hdrWell_toFile[23] = line[rt.get(6)[1][1]:(rt.get(6)[1][1] + rt.get(6)[3][1])].strip()
            continue
    match = re.search(pattern=rt.get(7)[0], string=line)  # record +D
    if match:
        if new_well:
            # apiNR
            hdrWell_toFile[24] = line[rt.get(7)[1][0]:(rt.get(7)[1][0] + rt.get(7)[3][0])].strip()
            # mmsSuffix
            hdrWell_toFile[25] = line[rt.get(7)[1][1]:(rt.get(7)[1][1] + rt.get(7)[3][1])].strip()
            # wellNR
            hdrWell_toFile[26] = line[rt.get(7)[1][2]:(rt.get(7)[1][2] + rt.get(7)[3][2])].strip()
            # totalWellDepth
            hdrWell_toFile[27] = line[rt.get(7)[1][3]:(rt.get(7)[1][3] + rt.get(7)[3][3])].strip()
            # bhPress
            hdrWell_toFile[28] = line[rt.get(7)[1][4]:(rt.get(7)[1][4] + rt.get(7)[3][4])].strip()
            # bhTemp
            hdrWell_toFile[29] = line[rt.get(7)[1][5]:(rt.get(7)[1][5] + rt.get(7)[3][5])].strip()
            # typeWell
            hdrWell_toFile[30] = line[rt.get(7)[1][6]:(rt.get(7)[1][6] + rt.get(7)[3][6])].strip()
            # dirDrillFlag
            hdrWell_toFile[31] = line[rt.get(7)[1][7]:(rt.get(7)[1][7] + rt.get(7)[3][7])].strip()
            # wellStat
            hdrWell_toFile[32] = line[rt.get(7)[1][8]:(rt.get(7)[1][8] + rt.get(7)[3][8])].strip()
            # michiganPermNR
            hdrWell_toFile[33] = line[rt.get(7)[1][9]:(rt.get(7)[1][9] + rt.get(7)[3][9])].strip()
            # bhCalc
            hdrWell_toFile[34] = line[rt.get(7)[1][10]:(rt.get(7)[1][10] + rt.get(7)[3][10])].strip()
            # tvDepth
            hdrWell_toFile[35] = line[rt.get(7)[1][11]:(rt.get(7)[1][11] + rt.get(7)[3][11])].strip()
            # wellSerialNR
            hdrWell_toFile[36] = line[rt.get(7)[1][12]:(rt.get(7)[1][12] + rt.get(7)[3][12])].strip()
            continue
    match = re.search(pattern=rt.get(8)[0], string=line)  # record +D!
    if match:
        if new_well:
            # surfLat
            hdrWell_toFile[37] = line[rt.get(8)[1][0]:(rt.get(8)[1][0] + rt.get(8)[3][0])].strip()
            # surfLon
            hdrWell_toFile[38] = line[rt.get(8)[1][1]:(rt.get(8)[1][1] + rt.get(8)[3][1])].strip()
            # bhLat
            hdrWell_toFile[39] = line[rt.get(8)[1][2]:(rt.get(8)[1][2] + rt.get(8)[3][2])].strip()
            # bhLon
            hdrWell_toFile[40] = line[rt.get(8)[1][3]:(rt.get(8)[1][3] + rt.get(8)[3][3])].strip()
            # plugDate
            hdrWell_toFile[41] = line[rt.get(8)[1][4]:(rt.get(8)[1][4] + rt.get(8)[3][4])].strip()
            # upperPerfDepth
            hdrWell_toFile[42] = line[rt.get(8)[1][5]:(rt.get(8)[1][5] + rt.get(8)[3][5])].strip()
            # lowerPerfDepth
            hdrWell_toFile[43] = line[rt.get(8)[1][6]:(rt.get(8)[1][6] + rt.get(8)[3][6])].strip()
            continue
    '''
        Note:
        Record +E and +E! are related. These two records must be combined as they belong to the
        same test number. There are cases where the +E record comes alone without the +E!
        So the trick is to keep the status of having read +E and write it down should +E! is
        non-existent
        # 'prodID', 'testNR', 'uprPerfDepth', 'lwrPerfDepth', 'liqPerDay', 'gasPerDay', 'watPerDay', 'chokeSize',
        # 'basicSedWat', 'ftPress', 'ratioGOR', 'liqGravity', 'finalSIPress', 'gasGravity', 'prodMethod','testDate'
        # 'testNR', 'bhp_Z', 'zFactor', 'nFactor', 'calcAOP', 'cumGas', 'clPress'
    '''
    # Well Test (part 1) - First card for Well Test
    # 'prodID', 'testNR', 'uprPerfDepth', 'lwrPerfDepth', 'liqPerDay', 'gasPerDay', 'watPerDay', 'chokeSize',
    # '%BSW', 'ftPress', 'ratioGOR', 'liqGravity', 'finalSIPress', 'gasGravity', 'prodMethod','testDate'
    match = re.search(pattern=rt.get(9)[0], string=line) # record +E
    if match:
        if new_well:
            tstWell_toFile = tstWell[:]
            # added to commit changes
            exist_prev_E = True
            # prodID
            tstWell_toFile[0] = hdrWell_toFile[1].strip()
            # testNR
            tstWell_toFile[1] = line[rt.get(9)[1][0]:(rt.get(9)[1][0] + rt.get(9)[3][0])].strip()
            # uprPerfDepth
            tstWell_toFile[2] = line[rt.get(9)[1][1]:(rt.get(9)[1][1] + rt.get(9)[3][1])].strip()
            # lwrPerfDepth
            tstWell_toFile[3] = line[rt.get(9)[1][2]:(rt.get(9)[1][2] + rt.get(9)[3][2])].strip()
            # liqPerDay
            tstWell_toFile[4] = line[rt.get(9)[1][3]:(rt.get(9)[1][3] + rt.get(9)[3][3])].strip()
            # gasPerDay
            tstWell_toFile[5] = line[rt.get(9)[1][4]:(rt.get(9)[1][4] + rt.get(9)[3][4])].strip()
            # watPerDay
            tstWell_toFile[6] = line[rt.get(9)[1][5]:(rt.get(9)[1][5] + rt.get(9)[3][5])].strip()
            # chokeSize
            tstWell_toFile[7] = line[rt.get(9)[1][6]:(rt.get(9)[1][6] + rt.get(9)[3][6])].strip()
            # %BSW
            tstWell_toFile[8] = line[rt.get(9)[1][7]:(rt.get(9)[1][7] + rt.get(9)[3][7])].strip()
            # ftPress
            tstWell_toFile[9] = line[rt.get(9)[1][8]:(rt.get(9)[1][8] + rt.get(9)[3][8])].strip()
            # ratioGOR
            tstWell_toFile[10] = line[rt.get(9)[1][9]:(rt.get(9)[1][9] + rt.get(9)[3][9])].strip()
            # liqGravity
            tstWell_toFile[11] = line[rt.get(9)[1][10]:(rt.get(9)[1][10] + rt.get(9)[3][10])].strip()
            # finalSIPress
            tstWell_toFile[12] = line[rt.get(9)[1][11]:(rt.get(9)[1][11] + rt.get(9)[3][11])].strip()
            # gasGravity
            tstWell_toFile[13] = line[rt.get(9)[1][12]:(rt.get(9)[1][12] + rt.get(9)[3][12])].strip()
            # prodMethod
            tstWell_toFile[14] = line[rt.get(9)[1][13]:(rt.get(9)[1][13] + rt.get(9)[3][13])].strip()
            # testDate
            tstWell_toFile[15] = line[rt.get(9)[1][14]:(rt.get(9)[1][14] + rt.get(9)[3][14])].strip()
            continue
    # Well Test (part 2) - Second card for Well Test
    # 'bhp_Z', 'zFactor', 'nFactor', 'calcAOP', 'cumGas', 'clPress'
    match = re.search(pattern=rt.get(10)[0], string=line)  # record +E!
    if match:
        if new_well:
            # assign all remaining
            # bhp_Z
            tstWell_toFile[16] = line[rt.get(10)[1][0]:(rt.get(10)[1][0] + rt.get(10)[3][0])].strip()
            # zFactor
            tstWell_toFile[17] = line[rt.get(10)[1][1]:(rt.get(10)[1][1] + rt.get(10)[3][1])].strip()
            # nFactor
            tstWell_toFile[18] = line[rt.get(10)[1][2]:(rt.get(10)[1][2] + rt.get(10)[3][2])].strip()
            # calcAOP
            tstWell_toFile[19] = line[rt.get(10)[1][3]:(rt.get(10)[1][3] + rt.get(10)[3][3])].strip()
            # cumGas
            tstWell_toFile[20] = line[rt.get(10)[1][4]:(rt.get(10)[1][4] + rt.get(10)[3][4])].strip()
            # clPress
            tstWell_toFile[21] = line[rt.get(10)[1][5]:(rt.get(10)[1][5] + rt.get(10)[3][5])].strip()
    if exist_prev_E:
        outFile_tst.write(','.join(tstWell_toFile) + '\r\n')
        exist_prev_E = False
    match = re.search(pattern=rt.get(11)[0], string=line)  # record +G
    if match:
        if new_well:
            prdWell_toFile = prdWell[:]
            # prodID
            prdWell_toFile[0] = hdrWell_toFile[1].strip()
            # prodDate
            prdWell_toFile[1] = line[rt.get(11)[1][0]:(rt.get(11)[1][0] + rt.get(11)[3][0])].strip()
            # liqProd
            prdWell_toFile[2] = line[rt.get(11)[1][1]:(rt.get(11)[1][1] + rt.get(11)[3][1])].strip()
            # gasProd
            prdWell_toFile[3] = line[rt.get(11)[1][2]:(rt.get(11)[1][2] + rt.get(11)[3][2])].strip()
            # watProd
            prdWell_toFile[4] = line[rt.get(11)[1][3]:(rt.get(11)[1][3] + rt.get(11)[3][3])].strip()
            # allowProd
            prdWell_toFile[5] = line[rt.get(11)[1][4]:(rt.get(11)[1][4] + rt.get(11)[3][4])].strip()
            # numWells
            prdWell_toFile[6] = line[rt.get(11)[1][5]:(rt.get(11)[1][5] + rt.get(11)[3][5])].strip()
            # daysProd
            prdWell_toFile[7] = line[rt.get(11)[1][6]:(rt.get(11)[1][6] + rt.get(11)[3][6])].strip()
            outFile_prd.write(','.join(prdWell_toFile) + '\r\n')
            prdWell_toFile = prdWell[:]
            continue
    match = re.search(pattern=rt.get(12)[0], string=line)  # END_US_PROD
    if match:
        if new_well:
            outFile_hdr.write(','.join(hdrWell_toFile) + '\r\n')
            wells_per_county[hdrWell_toFile[6]] += 1
            new_well = False
            hdrWell_toFile = hdrWell[:]
            # next print command only works when code is executed on terminal console
            # print('             {0:}'.format(wells_per_county), end='\r')
            continue
print()
print('--------------')
fileinput.close()
outFile_hdr.close()
outFile_prd.close()
outFile_tst.close()
