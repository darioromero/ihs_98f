import sys, re, time

#inFile = ""
#inFile = input("Enter the input File Name: ")

inFile = '/Users/darioromero/Google Drive/IHS/DataFiles/PERMIAN/' + 'PERMMIAN_BASIN_298_Production.98f'

start = time.clock()
print('Start Time: {0}'.format(start))
inFileLines = open(inFile, mode='rt').readlines()
elapsed = time.clock() - start

pattern = '^END_US_PROD'
n = 0

for line in inFileLines:
    match = re.search(pattern=pattern, string=line, flags=True)
    if (match):
        n += 1
        #print(line)

print('Elapsed Time: {0} --- Lines read: {1}'.format(elapsed, n))
