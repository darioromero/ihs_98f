import sys, re, time

#inFile = ""
#inFile = input("Enter the input File Name: ")

inFile = '/Users/darioromero/Google Drive/IHS/DataFiles/PERMIAN/' + 'PERMMIAN_BASIN_298_Production.98f'

start = time.clock()
#print('Start Time: {0}'.format(start))
inFileLines = open(inFile, mode='rt').readlines()
elapsed = time.clock() - start

pattern = '^START_US_PROD'

n = 0 # nr. of wells
m = 0 # nr. of MULTI wells

for line in inFileLines:
    match = re.search(pattern=pattern, string=line, flags=True)
    if (match):
        n += 1
    match = re.search(pattern='MULTI', string=line, flags=True)
    if (match):
        m += 1

# number of wells to write per file -- wpf
wpf = 2000
# nr of files required
nfiles = int(n / wpf)
# remaining nr of wells for the extra file
lstwells = n % wpf
# print results
print('Nr of Files with 2000 Wells: {0:0>4} + 1, -- Nr of Wells on Last File: {1:0>6}'.format(nfiles, lstwells))
print(' --- Wells read: {1:0>8}, MultiWells: {0:0>8}'.format(n, m))
# Elapsed Time
print('Elapsed Time: {0}:'.format(elapsed))


