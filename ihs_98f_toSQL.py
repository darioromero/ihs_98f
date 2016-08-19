import sys, re, time, fileinput

folder = '/home/drome/darioromero/ihs_98f'
inFile = 'PERMIAN_BASIN_298_Production.98f'
#inFile = 'PERMIAN_BASIN_298_Production_001TEST.98f'
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
    8: ['^(\+D\!)', [3, 12, 33, 43, 45, 51, 56],
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
        ]
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

for line in fileinput.input(inFile):
    match = re.search(pattern=rt.get(1)[0], string=line) # START_US_PROD
    if match:
        new_well = True
        match = re.search(pattern='MULTI', string=line)
        if match:
            new_well = False
            break
        entityID = line[rt.get(1)[1][0]:(rt.get(1)[1][0] + rt.get(1)[3][0])].rstrip()
    elif new_well:
        match = re.search(pattern=rt.get(2)[0], string=line) # record ++
        if match:
            prodID = line[rt.get(1)[1][0]:(rt.get(1)[1][0] + rt.get(1)[3][0])].rstrip()
            break
        match = re.search(pattern=rt.get(3)[0], string=line) # record +A
        if match:
            regionCD    = line[rt.get(3)[1][0]:(rt.get(3)[1][0] + rt.get(3)[3][0])].rstrip()
            stateCD     = line[rt.get(3)[1][1]:(rt.get(3)[1][1] + rt.get(3)[3][1])].rstrip()
            fieldCD     = line[rt.get(3)[1][2]:(rt.get(3)[1][2] + rt.get(3)[3][2])].rstrip()
            countyCD    = line[rt.get(3)[1][3]:(rt.get(3)[1][3] + rt.get(3)[3][3])].rstrip()
            countyNM    = line[rt.get(3)[1][4]:(rt.get(3)[1][4] + rt.get(3)[3][4])].rstrip()
            operCD      = line[rt.get(3)[1][5]:(rt.get(3)[1][5] + rt.get(3)[3][5])].rstrip()
            productCD   = line[rt.get(3)[1][6]:(rt.get(3)[1][6] + rt.get(3)[3][6])].rstrip()
            modeCD      = line[rt.get(3)[1][7]:(rt.get(3)[1][7] + rt.get(3)[3][7])].rstrip()
            formationCD = line[rt.get(3)[1][8]:(rt.get(3)[1][8] + rt.get(3)[3][8])].rstrip()
            basinCD     = line[rt.get(3)[1][9]:(rt.get(3)[1][9] + rt.get(3)[3][9])].rstrip()
            indCBM      = line[rt.get(3)[1][10]:(rt.get(3)[1][10] + rt.get(3)[3][10])].rstrip()
            enhrecFlg   = line[rt.get(3)[1][11]:(rt.get(3)[1][11] + rt.get(3)[3][11])].rstrip()
            break
        match = re.search(pattern=rt.get(4)[0], string=line) # record +AR
        if match:
            leaseCD     = line[rt.get(4)[1][0]:(rt.get(4)[1][0] + rt.get(4)[3][0])].rstrip()
            serialNum   = line[rt.get(4)[1][0]:(rt.get(4)[1][0] + rt.get(4)[3][0])].rstrip()
            comingCD    = line[rt.get(4)[1][0]:(rt.get(4)[1][0] + rt.get(4)[3][0])].rstrip()
            resrvrCD    = line[rt.get(4)[1][0]:(rt.get(4)[1][0] + rt.get(4)[3][0])].rstrip()
            apiCD       = line[rt.get(4)[1][0]:(rt.get(4)[1][0] + rt.get(4)[3][0])].rstrip()
            districtCD  = line[rt.get(4)[1][0]:(rt.get(4)[1][0] + rt.get(4)[3][0])].rstrip()
            break



fileinput.close()


outFile1 = ''

mtotal = 0

for line in fileinput.input(inFile):
    match = re.search(pattern=county, string=line)
    if match:
        wells_per_county[line[16:24].rstrip()] += 1

print('Wells per County: {0}'.format(wells_per_county))

fileinput.close()