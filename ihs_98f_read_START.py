import sys, re, time, fileinput

#inFile = ""
#inFile = input("Enter the input File Name: ")

#inFile = '/Users/darioromero/Google Drive/IHS/DataFiles/PERMIAN/' + 'PERMMIAN_BASIN_298_Production.98f'
inFile = '/Users/darioromero/Documents/IHS/Export - 298 Production TEXAS 1-4.98f'

start = time.clock()
print('Start Time: {0}'.format(start))

ntotal = 0 # nr. of wells
multi = 0 # nr. of MULTI wells

# prefix of the output file
fprefix = input("Enter Prefix of the output file: ")

# number of wells to write per file -- wllspf
wellspf = int(input("Enter number of Wells per File: "))
#wellspf = 2000

for line in fileinput.input(inFile):
    match = re.search(pattern='^START_US_PROD', string=line, flags=True)
    if match:
        ntotal += 1
    match = re.search(pattern='MULTI', string=line, flags=True)
    if match:
        multi += 1

print('Wells read: {0:0>8}, MultiWells: {1:0>8}'.format(ntotal, multi))

# nr of files required
nfiles = int((ntotal - multi) / wellspf) + 1
# remaining nr of wells for the extra file
lastwlls = (ntotal - multi) % wellspf

print('Total Nr of Files: {0:0>6}'.format(nfiles))
print('Nr of Files with {0} Wells: {1:0>6}'.format(wellspf, nfiles - 1))
print('Nr of Wells on Last File: {0:0>6}'.format(lastwlls))

cycle = False
filenr = 0
wellnr = 0

'''

while wellnr <= ntotal: # ntotal includes multi wells -- these are not counted
    ff = open(name='salida.98f', mode='w') # filename must be related to cycle and input filename
    for line in fileinput.input(inFile):
        match = re.search(pattern='^START_US_PROD', string=line, flags=True)
        if match:
            wellnr += wellnr  # increment well
            match = re.search(pattern='MULTI', string=line, flags=True)
            if match:
                multi += 1 # is a multi well - discard it
                break
            else:
                cycle = True  # set new cycle on
        else:
            match = re.search(pattern='^END_US_PROD', string=line, flags=True)
            if match:
                ff.write(line) # write line to close cycle
                cycle = False # last record in the cycle; set cycle off
        if cycle:
            ff.write(line) # write line within cycle


'''

elapsd = time.clock() - start
# Elapsed Time
print('Elapsed Time: {0}:'.format(elapsd))




