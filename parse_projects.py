import subprocess as sp
import os

supervisors = ['Oliver', 'Marc', 'Rémy']
max_line = 3
n = 0
ids, y, x, value = 'c(', 'c(', 'c(', 'c('
tmpY = 0
offset = {'Oliver':max_line, 'Marc':0, 'Rémy':2*max_line}
m = {'Oliver':0, 'Marc':0, 'Rémy':0}
for linea in open('projects'):
    linea = linea.rstrip('\n')
    splat = linea.split('\t')
    typ = splat[2]
    if splat[2] not in supervisors:
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
