import sys, re, time, fileinput

#inFile = ""
#inFile = input("Enter the input File Name: ")

inFile = '/Users/darioromero/Google Drive/IHS/DataFiles/PERMIAN/' + 'PERMMIAN_BASIN_298_Production.98f'

start = time.clock()
print('Start Time: {0}'.format(start))

pattern = '^START_US_PROD'

n = 0 # nr. of wells
m = 0 # nr. of MULTI wells

for line in fileinput.input(inFile):
    match = re.search(pattern=pattern, string=line, flags=True)
    if (match):
        n += 1
    match = re.search(pattern='MULTI', string=line, flags=True)
    if (match):
        m += 1

elpsd = time.clock() - start
# Elapsed Time
print('Elapsed Time: {0}:'.format(elpsd))

# number of wells to write per file -- wpf
wllspf = 2000
#wllspf = int(input("Enter Proportion of Wells per File: "))
# nr of files required
nfiles = int(n / wllspf)
# remaining nr of wells for the extra file
lastwlls = n % wllspf
# print results
print('Nr of Files with {0} Wells: {1:0>4} + 1, -- Nr of Wells on Last File: {2:0>6}'.format(wllspf, nfiles, lastwlls))
print('Wells read: {0:0>8}, MultiWells: {1:0>8}'.format(n, m))



