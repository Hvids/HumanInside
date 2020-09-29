import  sys
sys.path.append('../')
sys.path.append('../../')

from ParserPage import ParserEvent

url = 'https://www.2do2go.ru/events/276048/myuzikl-vsamdelishnoe-priklyuchenie'
site = 'https://www.2do2go.ru'
pe = ParserEvent(site, url)
ev = pe.parse(1,1)
print(ev)
