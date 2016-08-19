import sys, re, time, fileinput

folder = '/home/drome/darioromero/ihs_98f'
inFile = 'PERMIAN_BASIN_298_Production.98f'

inFile = folder + '/' + inFile

# dictionary holding number of wells per county
wells_per_county = {'CRANE': 0, 'CROCKETT': 0, 'PECOS': 0, 'REAGAN': 0,
                    'TERRELL': 0, 'UPTON': 0}

pattern = '^(\+A\s)([A-Z]|[0-9]){13}(CRANE\s{3}|CROCKETT|PECOS\s{3}|REAGAN\s{2}|' \
          'TERRELL\s{1}|UPTON\s{3})'

for line in fileinput.input(inFile):
    match = re.search(pattern=pattern, string=line)
    if match:
        wells_per_county[line[16:24].rstrip()] += 1

print('Wells per County: {0}'.format(wells_per_county))

fileinput.close()