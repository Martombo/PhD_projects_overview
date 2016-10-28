import subprocess as sp
import os

types = ['Marc', 'Oliver', 'Rémy', 'Teaching']
max_line = 2
n = 0
ids, y, x, value = 'c(', 'c(', 'c(', 'c('
tmpY = 0
offset = dict(zip(types, range(0, max_line*(len(types)+1), max_line)))
m = dict(zip(types, [0]*len(types)))
for linea in open('projects'):
    linea = linea.rstrip('\n')
    splat = linea.split('\t')
    typ = splat[2]
    if splat[2] not in types:
        continue

    height = float(splat[1])
    ids += ','.join([str(n)]*4) + ','
    y += ','.join([str(x) for x in [tmpY, tmpY-height, tmpY-height, tmpY]]) + ','
    x += ','.join([str(x + offset[typ]) for x in [m[typ], m[typ], m[typ]+1, m[typ]+1]]) + ','
    value += ','.join(['"' + typ + '"']*4) + ','

    tmpY -= height
    n += 1
    m[typ] += 1
    if m[typ] > max_line-1:
        m[typ] = 0

ids = ids.rstrip(',') +')'
y = y.rstrip(',') + '), x='
x = x.rstrip(',') + '))'
value = value.rstrip(',') + ')), id=ids)'

stringa = '''

library(ggplot2)

ids = ''' + ids + '''
positions = data.frame(id = ids, y=''' + y + x + '''
values = data.frame(value = factor(''' + value + '''

datapoly = merge(values, positions, by=c("id"))
p = ggplot(datapoly, aes(x=x, y=y)) 

svg(height=6,width=4)
    p + geom_polygon(aes(fill=value, group=id)) + theme_bw()
dev.off()

'''

with open('tmp.R', 'w') as f:
    f.write(stringa)
sp.call(['Rscript', 'tmp.R'])
os.remove('tmp.R')
