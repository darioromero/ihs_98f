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

print('Total Nr of Files         : {0:0>6}'.format(nfiles))
print('Nr of Files with {0} Wells: {1:0>6}'.format(wellspf, nfiles - 1))
print('Nr of Wells on Last File  : {0:0>6}'.format(lastwlls))

cycle = False # cycle indicating a new well loop START-STOP
cfile = True # cycle indicating a new file to be written
filenr = 1
wellrc = 0 # well record read from input
wellnr = 0

while wellrc <= ntotal: # total loop - ntotal includes multi wells
    for line in fileinput.input(inFile):
        if cfile: # new file-cycle for writing well records
            fwname = fprefix + '-' + '{:0>4}'.format(str(filenr)) + '.98f'
            fw = open(fwname, 'w')
            cfile = False
        match = re.search(pattern='^START_US_PROD', string=line, flags=True)
        if match:
            wellrc += 1  # increment well
            match = re.search(pattern='MULTI', string=line, flags=True)
            if match:
                # is a multi well - discard it
                break
            else:
                cycle = True  # set new cycle for non-multi well
                cfile = True  # set new cycle for new file
                fw.write(line) # write line - new cycle

        else:
            match = re.search(pattern='^END_US_PROD', string=line, flags=True)
            if match:
                fw.write(line) # write line - current cycle
                cycle = False # last record in the cycle; set cycle off
                wellrc += 1
                wellnr += 1
                if True:
                    print(1)
                else:
                    print(0)
        if cycle: # write other lines within cycle START -- END cycle
            fw.write(line) # write line within cycle
        if wellnr > (filenr * wellspf):
                cfile = True
                filenr += 1



elapsd = time.clock() - start
# Elapsed Time
print('Elapsed Time: {0}:'.format(elapsd))




