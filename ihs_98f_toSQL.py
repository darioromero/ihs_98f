import sys, re, time, fileinput

folder = '/home/drome/darioromero/ihs_98f'
inFile = 'PERMIAN_BASIN_298_Production.98f'
#inFile = 'PERMIAN_BASIN_298_Production_001TEST.98f'

# regex for searching for specific counties as listed below
# ^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|
#                           TERRELL\s{1}|UPTON\s{3})
#

# dictionary holding number of wells per county
record_type = {'START_US_PROD\s': [3, ],
               'CROCKETT': 0, 'PECOS': 0, 'REAGAN': 0,
                    'TERRELL': 0, 'UPTON': 0}

pattern = '^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|' \
          'TERRELL\s{1}|UPTON\s{3})'

# regex for searching for specific counties as listed below
# ^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|
#                           TERRELL\s{1}|UPTON\s{3})
#

# dictionary holding number of wells per county
wells_per_county = {'CRANE': 0, 'CROCKETT': 0, 'PECOS': 0, 'REAGAN': 0,
                    'TERRELL': 0, 'UPTON': 0}

pattern = '^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|' \
          'TERRELL\s{1}|UPTON\s{3})'

inFile = folder + '/' + inFile

new_well = False # no new well has been found

for line in fileinput.input(inFile):
    match = re.search(pattern='^(START_US_PROD)', string=line)
    if match:
        new_well = True
        match = re.search(pattern='MULTI', string=line)
        if match:
            new_well = False
            break
        entityID =

    elif new_well:
        match()

'''
#  Codes to regex IHS file 98f, 98c
^(IHS Inc\.)
^(START_US_PROD\s)
^(END_US_PROD\s)
^(\+\+\s)
^(\+A\s)
^(\+AT)
^(\+AR)
^(\+A\#)
^(\+B\s)
^(\+C\s)
^(\+D\s)
^(\+D\!)
^(\+E\s)
^(\+F\s)
^(\+G\s)
^(\+I\s)
^(\+J\s)
^(\+L\s)
^(\+[H,K,M-Z]{1}\s)
'''

rt = {
    # Following two records will be saved on Header file
    1: ['START_US_PROD', [30], ['entityID'], [40]],
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
        ['fieldNM', 'rsrvrNM'], [40, 20]
        ],
    6: ['^(\+D\s)', [3, 18, 21, 30, 35, 45, 55, 57, 58, 59, 64, 65, 70],
        ['apiNR', 'mmsSufix', 'wellNR', 'totalWellDepth', 'bhPress', 'bhTemp',
         'typeWell', 'dirDrillFlag', 'wellStat', 'michiganPermNR', 'bhCalc',
         'tvDepth', 'wellSerialNR'],
        [15, 3, 9, 5, 10, 10, 2, 1, 1, 5, 1, 5, 8]
        ],
    7: ['^(\+D\!)', [3, 12, 33, 43, 45, 51, 56],
        ['surfLat', 'surfLon', 'bhLat', 'bhLon', 'plugDate',
         'upperPerfDepth', 'lowerPerfDepth'],
        [9, 10, 9, 10, 6, 5, 5]
        ],
    # Following two records will be saved on Test file
    8: ['^(\+E\s)', [3, 6, 11, 16, 23, 29, 34, 39, 43, 48, 55, 59, 64, 69, 71],
        ['testNR', 'uprPerfDepth', 'lwrPerfDepth', 'liqPerDay', 'gasPerDay',
         'watPerDay', 'chokeSize', 'basicSedWat', 'ftPress', 'goRatio', 'liqGravity',
         'finalSIPress', 'gasGravity', 'prodMethod', 'testDate'],
        [3, 5, 5, 7, 6, 5, 5, 4, 5, 7, 4, 5, 5, 2, 8]
        ],
    9: ['^(\+E\!)', [3, 6, 10, 15, 21, 28, 43],
        ['testNR', 'bhp_Z', 'zFactor', 'nFactor', 'aopCalc',
         'cumGas', 'clPressure'],
        [3, 4, 5, 6, 7, 15, 5]
        ],
# Following two records will be saved on Production file
    10: ['^(\+G\s)', [3, 11, 26, 41, 56, 71, 76],
        ['prodDate', 'liqProd', 'gasProd', 'watProd', 'allowProd',
         'numWells', 'daysProd'],
        [8, 15, 15, 15, 15, 5, 2]
        ]
}

match = re.search(pattern=rt.get(2)[0], string=line)
line = '++ THIS IS THE START OF A RECORD TYPE 2'

fileinput.close()


outFile1 = ''

mtotal = 0

for line in fileinput.input(inFile):
    match = re.search(pattern=pattern, string=line)
    if match:
        wells_per_county[line[16:24].rstrip()] += 1

print('Wells per County: {0}'.format(wells_per_county))

fileinput.close()