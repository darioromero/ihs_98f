import sys, re, time, fileinput

#inFile = ""
#inFile = input("Enter the input File Name: ")

#inFile = '/Users/darioromero/Google Drive/IHS/DataFiles/PERMIAN/' + 'PERMMIAN_BASIN_298_Production.98f'
inFile = '/Users/darioromero/Documents/IHS/Export - 298 Production TEXAS 1-4.98f'

start = time.clock()
print('Start Time: {0}'.format(start))

n = 0 # nr. of wells
multi = 0 # nr. of MULTI wells

for line in fileinput.input(inFile):
    match = re.search(pattern='^START_US_PROD', string=line, flags=True)
    if (match):
        n += 1

# number of wells to write per file -- wllspf
#wllspf = int(input("Enter Proportion of Wells per File: "))
wllspf = 2000
# nr of files required
nfiles = int(n / wllspf)
# remaining nr of wells for the extra file
lastwlls = n % wllspf

cycle = False
nfile = 0
wellnr = 0

while wellnr <= n: # instead change this ... loop by cycle
    ff = open(name='salida.98f', mode='w')
    for line in fileinput.input(inFile):
        match = re.search(pattern='^START_US_PROD', string=line, flags=True)
        if match:
            wellnr += wellnr  # increment well
            match = re.search(pattern='MULTI', string=line, flags=True)
            if match:
                multi += 1 # is a multi well - discard it
                break
            else:
                cycle = True  # set new cycle START -- END on
        else:
            match = re.search(pattern='^END_US_PROD', string=line, flags=True)
            if match:
                ff.write(line)
                cycle = False # last well in the cycle; set cycle off
        if cycle:
            ff.write(line) # write line within cycle





elpsd = time.clock() - start
# Elapsed Time
print('Elapsed Time: {0}:'.format(elpsd))

# print results
print('Nr of Files with {0} Wells: {1:0>4} + 1, -- Nr of Wells on Last File: {2:0>6}'.format(wllspf, nfiles, lastwlls))
print('Wells read: {0:0>8}, MultiWells: {1:0>8}'.format(n, m))




