import sys, re, time, fileinput

folder = '/home/drome/darioromero/ihs_98f'
inFile = 'PERMIAN_BASIN_298_Production.98f'
inFile = folder + '/' + inFile

# regex pattern for searching for specific counties as listed below
# ^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|
#                           TERRELL\s{1}|UPTON\s{3})
#
county = '^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|' \
          'TERRELL\s{1}|UPTON\s{3})'

# dictionary holding number of wells per county
wells_per_county = {'CRANE': 0, 'CROCKETT': 0, 'PECOS': 0, 'REAGAN': 0,
                    'TERRELL': 0, 'UPTON': 0}

#  Codes to regex IHS file 98f, 98c
#  It is a structure dictionary where values are a list of 4 elements:
#  elem 1: code for type of record
#  elem 2: list with start position in the record of key variables
#  elem 3: list with names of key variables
#  elem 4: list with withness of column of key variables

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
         'watPerDay', 'chokeSize', 'basicSedWat', 'ftPress', 'goRatio', 'liqGravity',
         'finalSIPress', 'gasGravity', 'prodMethod', 'testDate'],
        [3, 5, 5, 7, 6, 5, 5, 4, 5, 7, 4, 5, 5, 2, 8]
        ],
    10: ['^(\+E\!)', [3, 6, 10, 15, 21, 28, 43],
        ['testNR', 'bhp_Z', 'zFactor', 'nFactor', 'aopCalc',
         'cumGas', 'clPressure'],
        [3, 4, 5, 6, 7, 15, 5]
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

# 'testNR', 'uprPerfDepth', 'lwrPerfDepth', 'liqPerDay', 'gasPerDay', 'watPerDay', 'chokeSize', 'basicSedWat',
# 'ftPress', 'goRatio', 'liqGravity', 'finalSIPress', 'gasGravity', 'prodMethod', 'testDate'
# 'testNR', 'bhp_Z', 'zFactor', 'nFactor', 'aopCalc', 'cumGas', 'clPressure'

prodTest = [3*blnk, 5*blnk, 5*blnk, 7*blnk, 6*blnk, 5*blnk, 5*blnk, 4*blnk, 5*blnk, 7*blnk,
        4*blnk, 5*blnk, 5*blnk, 2*blnk, 8*blnk, 3*blnk, 4*blnk, 5*blnk, 6*blnk, 7*blnk, 15*blnk, 5*blnk]

# 'prodDate', 'liqProd', 'gasProd', 'watProd', 'allowProd', 'numWells', 'daysProd'

prodMon = [8*blnk, 15*blnk, 15*blnk, 15*blnk, 15*blnk, 5*blnk, 2*blnk]

outFile = open('workfile.csv', 'w')

for line in fileinput.input(inFile):
    match = re.search(pattern=rt.get(1)[0], string=line) # START_US_PROD
    if match:
        new_well = True
        hdrWell_toFile = hdrWell[:]
        match = re.search(pattern='MULTI', string=line)
        if match:
            new_well = False
            continue
        hdrWell_toFile[0] = line[rt.get(1)[1][0]:(rt.get(1)[1][0] + rt.get(1)[3][0])].rstrip() # entityID
        #print(str(hdrWell_toFile) + '\r\n')
    elif new_well:
        match = re.search(pattern=rt.get(2)[0], string=line) # record ++
        if match:
            hdrWell_toFile[1] = line[rt.get(1)[1][0]:(rt.get(1)[1][0] + rt.get(1)[3][0])].rstrip() # prodID
            #print(str(hdrWell_toFile) + '\r\n')
            continue
        match = re.search(pattern=rt.get(3)[0], string=line) # record +A
        if match:
            if line[rt.get(3)[1][4]:(rt.get(3)[1][4] + rt.get(3)[3][4])].rstrip() not in \
                    (list(wells_per_county.keys())):
                new_well = False
                hdrWell_toFile = hdrWell[:]
                continue
            hdrWell_toFile[2]  = line[rt.get(3)[1][0]:(rt.get(3)[1][0] + rt.get(3)[3][0])].rstrip() # regionCD
            hdrWell_toFile[3]  = line[rt.get(3)[1][1]:(rt.get(3)[1][1] + rt.get(3)[3][1])].rstrip() # stateCD
            hdrWell_toFile[4]  = line[rt.get(3)[1][2]:(rt.get(3)[1][2] + rt.get(3)[3][2])].rstrip() # fieldCD
            hdrWell_toFile[5]  = line[rt.get(3)[1][3]:(rt.get(3)[1][3] + rt.get(3)[3][3])].rstrip() # countyCD
            hdrWell_toFile[6]  = line[rt.get(3)[1][4]:(rt.get(3)[1][4] + rt.get(3)[3][4])].rstrip() # countyNM
            hdrWell_toFile[7]  = line[rt.get(3)[1][5]:(rt.get(3)[1][5] + rt.get(3)[3][5])].rstrip() # operCD
            hdrWell_toFile[8]  = line[rt.get(3)[1][6]:(rt.get(3)[1][6] + rt.get(3)[3][6])].rstrip() # productCD
            hdrWell_toFile[9]  = line[rt.get(3)[1][7]:(rt.get(3)[1][7] + rt.get(3)[3][7])].rstrip() # modeCD
            hdrWell_toFile[10] = line[rt.get(3)[1][8]:(rt.get(3)[1][8] + rt.get(3)[3][8])].rstrip() # formationCD
            hdrWell_toFile[11] = line[rt.get(3)[1][9]:(rt.get(3)[1][9] + rt.get(3)[3][9])].rstrip() # basinCD
            hdrWell_toFile[12] = line[rt.get(3)[1][10]:(rt.get(3)[1][10] + rt.get(3)[3][10])].rstrip() # indCBM
            hdrWell_toFile[13] = line[rt.get(3)[1][11]:(rt.get(3)[1][11] + rt.get(3)[3][11])].rstrip() # enhrecFlg
            continue
        match = re.search(pattern=rt.get(4)[0], string=line) # record +AR
        if match:
            hdrWell_toFile[14] = line[rt.get(4)[1][0]:(rt.get(4)[1][0] + rt.get(4)[3][0])].rstrip() # leaseCD
            hdrWell_toFile[15] = line[rt.get(4)[1][1]:(rt.get(4)[1][1] + rt.get(4)[3][1])].rstrip() # serialNum
            hdrWell_toFile[16] = line[rt.get(4)[1][2]:(rt.get(4)[1][2] + rt.get(4)[3][2])].rstrip() # comingCD
            hdrWell_toFile[17] = line[rt.get(4)[1][3]:(rt.get(4)[1][3] + rt.get(4)[3][3])].rstrip() # resrvrCD
            hdrWell_toFile[18] = line[rt.get(4)[1][4]:(rt.get(4)[1][4] + rt.get(4)[3][4])].rstrip() # apiCD
            hdrWell_toFile[19] = line[rt.get(4)[1][5]:(rt.get(4)[1][5] + rt.get(4)[3][5])].rstrip() # districtCD            break
        match = re.search(pattern=rt.get(5)[0], string=line) # record +B
        if match:
            hdrWell_toFile[20] = line[rt.get(5)[1][0]:(rt.get(5)[1][0] + rt.get(5)[3][0])].rstrip() # leaseNM
            hdrWell_toFile[21] = line[rt.get(5)[1][1]:(rt.get(5)[1][1] + rt.get(5)[3][1])].rstrip() # operNM
            continue
        match = re.search(pattern=rt.get(6)[0], string=line)  # record +C
        if match:
            hdrWell_toFile[22] = line[rt.get(6)[1][0]:(rt.get(6)[1][0] + rt.get(6)[3][0])].rstrip() # fieldNM
            hdrWell_toFile[23] = line[rt.get(6)[1][1]:(rt.get(6)[1][1] + rt.get(6)[3][1])].rstrip() # resrvrNM
            continue
        match = re.search(pattern=rt.get(7)[0], string=line)  # record +D
        if match:
            hdrWell_toFile[24] = line[rt.get(7)[1][0]:(rt.get(7)[1][0] + rt.get(7)[3][0])].rstrip()    # apiNR
            hdrWell_toFile[25] = line[rt.get(7)[1][1]:(rt.get(7)[1][1] + rt.get(7)[3][1])].rstrip()    # mmsSuffix
            hdrWell_toFile[26] = line[rt.get(7)[1][2]:(rt.get(7)[1][2] + rt.get(7)[3][2])].rstrip()    # wellNR
            hdrWell_toFile[27] = line[rt.get(7)[1][3]:(rt.get(7)[1][3] + rt.get(7)[3][3])].rstrip()    # totalWellDepth
            hdrWell_toFile[28] = line[rt.get(7)[1][4]:(rt.get(7)[1][4] + rt.get(7)[3][4])].rstrip()    # bhPress
            hdrWell_toFile[29] = line[rt.get(7)[1][5]:(rt.get(7)[1][5] + rt.get(7)[3][5])].rstrip()    # bhTemp
            hdrWell_toFile[30] = line[rt.get(7)[1][6]:(rt.get(7)[1][6] + rt.get(7)[3][6])].rstrip()    # typeWell
            hdrWell_toFile[31] = line[rt.get(7)[1][7]:(rt.get(7)[1][7] + rt.get(7)[3][7])].rstrip()    # dirDrillFlag
            hdrWell_toFile[32] = line[rt.get(7)[1][8]:(rt.get(7)[1][8] + rt.get(7)[3][8])].rstrip()    # wellStat
            hdrWell_toFile[33] = line[rt.get(7)[1][9]:(rt.get(7)[1][9] + rt.get(7)[3][9])].rstrip()    # michiganPermNR
            hdrWell_toFile[34] = line[rt.get(7)[1][10]:(rt.get(7)[1][10] + rt.get(7)[3][10])].rstrip() # bhCalc
            hdrWell_toFile[35] = line[rt.get(7)[1][11]:(rt.get(7)[1][11] + rt.get(7)[3][11])].rstrip() # tvDepth
            hdrWell_toFile[36] = line[rt.get(7)[1][12]:(rt.get(7)[1][12] + rt.get(7)[3][12])].rstrip() # wellSerialNR
            continue
        match = re.search(pattern=rt.get(8)[0], string=line)  # record +D!
        if match:
            hdrWell_toFile[37] = line[rt.get(8)[1][0]:(rt.get(8)[1][0] + rt.get(8)[3][0])].rstrip() # surfLat
            hdrWell_toFile[38] = line[rt.get(8)[1][1]:(rt.get(8)[1][1] + rt.get(8)[3][1])].rstrip() # surfLon
            hdrWell_toFile[39] = line[rt.get(8)[1][2]:(rt.get(8)[1][2] + rt.get(8)[3][2])].rstrip() # bhLat
            hdrWell_toFile[40] = line[rt.get(8)[1][3]:(rt.get(8)[1][3] + rt.get(8)[3][3])].rstrip() # bhLon
            hdrWell_toFile[41] = line[rt.get(8)[1][4]:(rt.get(8)[1][4] + rt.get(8)[3][4])].rstrip() # plugDate
            hdrWell_toFile[42] = line[rt.get(8)[1][5]:(rt.get(8)[1][5] + rt.get(8)[3][5])].rstrip() # upperPerfDepth
            hdrWell_toFile[43] = line[rt.get(8)[1][6]:(rt.get(8)[1][6] + rt.get(8)[3][6])].rstrip() # lowerPerfDepth
            #print(str(hdrWell_toFile))
            continue
    match = re.search(pattern=rt.get(12)[0], string=line)  # END_US_PROD
    if match:
        ''' do somenthing here '''
        #print(str(hdrWell_toFile) + '\r\n')
        outFile.write(str(hdrWell_toFile) + '\r\n')
        print('Well in : [{0}]'.format(hdrWell_toFile[6]))
        new_well = False
        hdrWell_toFile = hdrWell[:]

fileinput.close()
outFile.close()

'''
mtotal = 0

for line in fileinput.input(inFile):
    match = re.search(pattern=county, string=line)
    if match:
        wells_per_county[line[16:24].rstrip()] += 1

print('Wells per County: {0}'.format(wells_per_county))

fileinput.close()
'''

