import sys, re, time, fileinput

folder = '/home/drome/darioromero/ihs_98f'
inFile = 'PERMIAN_BASIN_298_Production.98f'
#inFile = 'PERMIAN_BASIN_298_Production_001TEST.98f'


inFile = folder + '/' + inFile

# number of wells to write per file -- wellspf
#wellspf = int(input("Enter number of Wells per File: "))
wellspf = 10000

ntotal = 0 # nr. of wells
multi = 0 # nr. of MULTI wells

for line in fileinput.input(inFile):
    match = re.search(pattern='^(START_US_PROD)', string=line)
    if match:
        ntotal += 1
        match = re.search(pattern='MULTI', string=line)
        if match:
            multi += 1

fileinput.close()

print('---------------------------------------------------------------')
print('Wells read: {0:0>8}, MultiWells: {1:0>8}'.format(ntotal, multi))

# nr of files required
nfiles = int((ntotal - multi) / wellspf) + 1
# remaining nr of wells for the extra file
lastwlls = (ntotal - multi) % wellspf

print('---------------------------------------------------------------')
print('Total Nr of Files         : {0:0>6}'.format(nfiles))
print('Nr of Files with {0} Wells: {1:0>6}'.format(wellspf, nfiles - 1))
print('Nr of Wells on Last File  : {0:0>6}'.format(lastwlls))

# keep this regex for later use
# ^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|
#                           TERRELL\s{1}|UPTON\s{3})
#

# dictionary holding number of wells per county
wells_per_county = {'CRANE': 0, 'CROCKETT': 0, 'PECOS': 0, 'REAGAN': 0,
                    'TERRELL': 0, 'UPTON': 0}

pattern = '^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|' \
          'TERRELL\s{1}|UPTON\s{3})'

mtotal = 0

for line in fileinput.input(inFile):
    match = re.search(pattern=pattern, string=line)
    if match:
        mtotal += 1
        '''
        print(str(mtotal) + ' - ' + line.rstrip("\n") + ' -- [' +
              line[16:24] + ']')
        '''
        wells_per_county[line[16:24].rstrip(' ')] += 1


print('Wells per County: {0}'.format(wells_per_county))

fileinput.close()