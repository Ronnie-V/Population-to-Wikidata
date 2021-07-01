#!/usr/bin/python3
#Script for updating French community population to Wikidata

import pywikibot
from pywikibot import pagegenerators as pg
import sys

datasite = pywikibot.Site("wikidata", "wikidata")
repo = datasite.data_repository()

sourceyear = 2021
sourcemonth = 6
sourceday = 4
sourcetitle='Populations légales communales depuis 1968'
sourceurl='https://www.insee.fr/fr/statistiques/2522602'

arg1 = ''
if len(sys.argv) > 1:
  arg1 = sys.argv[1]

sourceDate = pywikibot.WbTime(year = sourceyear, month = sourcemonth, day = sourceday)

dateid = u'P585'
inhabitantsid = u'P1082' # u'P1082' (total population), P1540: male population, P1539: female population
gebruiktcriterium = 'P1013'
idofsource = u'Q156616' # INSEE
methodofdetermination = u'P459'
sourceinstitutionid = u'P123'
s_titel        = u'P1476'  
urlforsourceid = u'P854'
visiteddateid  = u'P813'

def handlemessage(message, countyear, INSEE, comName, comInhab ):
  if message != '':
    print (message)
    message += f'\n'
    fr.write (message)
  message = f'{countyear};{INSEE};{comName};{comInhab}\n'
  fr.write (message)
  fr.flush()

def handleline(countyear, INSEE, comName, comInhab):
  countofpopulation = u'Q39825' # Q39825 = volkstelling, Q15194024 = inwonerregistratie
  if countyear <=1954:
    criterium = 'Q98688246'       # population totale
  elif countyear <=2003:        # effectief: 1999
    criterium = 'Q653524'       # population sans double compte
  else:
    criterium = 'Q15715409'     # population municipale # starting 2004

  if countyear == 1968:
    countDate = pywikibot.WbTime(year = countyear, month = 3, day = 1)
  elif countyear == 1975:
    countDate = pywikibot.WbTime(year = countyear, month = 2, day = 20)
  elif countyear == 1982:
    countDate = pywikibot.WbTime(year = countyear, month = 3, day = 4)
  elif countyear == 1990:
    countDate = pywikibot.WbTime(year = countyear, month = 3, day = 5)
  elif countyear == 1999:
    countDate = pywikibot.WbTime(year = countyear, month = 3, day = 8)
  else:
    countDate = pywikibot.WbTime(year = countyear, month = 1, day = 1)
    
  CollectedIDs = ''
  if INSEE[:1] == 'Q':
    QID = INSEE
  else:
    if len(INSEE) == 4:
      INSEE = f'0{INSEE}'
    QUERY = f"SELECT ?item ?itemLabel WHERE {{ ?item wdt:P374 '{INSEE}'. SERVICE wikibase:label {{ bd:serviceParam wikibase:language '[AUTO_LANGUAGE],en'. }} }}"
    generator = pg.WikidataSPARQLPageGenerator(QUERY, site=datasite)
    found = 0
    for wd in generator:
      CollectedIDs += ' ' + str(wd)[11:-2] 
      found = found + 1
    if found != 1:
      if found > 1:
        handlemessage(f'{INSEE} is not unique, found {found} communities. See {CollectedIDs.strip()}.', countyear, INSEE, comName, comInhab )
      else:
        handlemessage(f'No item found for {INSEE} {comName}.', countyear, INSEE, comName, comInhab )
      return (1)
    QID = str(wd)[11:-2]
  item = pywikibot.ItemPage(repo, QID)
  item_dict = item.get() #Get the item dictionary
  clm_dict = item_dict["claims"] # Get the claim dictionary
  try:
    clm_list = clm_dict[inhabitantsid]
    for clm in clm_list:
      clm_trgt = clm.getTarget()
      if (dateid in clm.qualifiers):
        qualifier=clm.qualifiers[dateid][0]
        content=qualifier.getTarget()
        if content.year == countDate.year and content.month == countDate.month and content.day == countDate.day:
          if comInhab - clm_trgt.amount == 0:
            print (f'Value {comInhab} for {comName} on {countDate.year}-{countDate.month}-{countDate.day} already exists.')
          else:
            print(f'WD reports {clm_trgt.amount} for {comName} ({INSEE}) on {countDate.year}-{countDate.month}-{countDate.day}. We got {comInhab}.')
          return
  except:
    pass
        
# Value for countDate not found, let us add it
  valueclaim = pywikibot.Claim(repo, inhabitantsid) # Adding inhabitants
  valueclaim.setTarget(pywikibot.WbQuantity(comInhab, site = datasite))
  item.addClaim(valueclaim, summary=f'adding total inhabitants per {countDate.day}-{countDate.month}-{countDate.year}')
  
  qualifierdate = pywikibot.Claim(repo, dateid) # Date of counting
  qualifierdate.setTarget(countDate)
  valueclaim.addQualifier(qualifierdate, summary=u'adding date of count')
    
  qualifiercounting = pywikibot.Claim(repo, methodofdetermination) # method of counting
  target = pywikibot.ItemPage(repo, countofpopulation)
  qualifiercounting.setTarget(target)
  valueclaim.addQualifier(qualifiercounting, summary=u'registering way of count')
  if criterium != '':
    qualifiercounting = pywikibot.Claim(repo, gebruiktcriterium) # gebruikt criterium
    target = pywikibot.ItemPage(repo, criterium)
    qualifiercounting.setTarget(target)
    valueclaim.addQualifier(qualifiercounting, summary=u'critère utilisé')
  
  source_url = pywikibot.Claim(repo, urlforsourceid, is_reference=True)
  source_url.setTarget(sourceurl)
  sourceinstitution  = pywikibot.Claim(repo, sourceinstitutionid)
  institution = pywikibot.ItemPage(repo, idofsource)
  sourceinstitution.setTarget(institution)
  source_visited = pywikibot.Claim(repo, visiteddateid, is_reference=False)
  dateOfsource_visited = pywikibot.WbTime(year=sourceyear, month=sourcemonth, day=sourceday)
  source_visited.setTarget(dateOfsource_visited)
  source_title = pywikibot.Claim(repo, s_titel, is_reference=True)
  source_title.setTarget(pywikibot.WbMonolingualText(sourcetitle, u"fr"))
  
  valueclaim.addSources([source_url, sourceinstitution, source_visited, source_title])
  
if arg1 == '':
  INSEEtoSkip = '57255'
else:
  INSEEtoSkip = ''
File = f'D:\\Wikipedia\\FR-inwoners-gemeenten{arg1}.csv'
FileResult = f'D:\\Wikipedia\\FR-inwoners-gemeenten_comments{arg1}.csv'
f = open(File, 'r', encoding='utf-8')
fr = open(FileResult, 'a', encoding='utf-8')
handlemessage('Gestart met ', arg1, INSEEtoSkip, '', '' )
readstatus = ''
for line in f:
  line = line.strip()
  if len(line) > 4:
    data = line.split(';')
    INSEE = data[1].strip()
    if INSEE[:1] == 'Q':
#      continue  # aanpassen als er meer te herstellen valt!
      pass
    else:
      if len(INSEE) == 4:
        INSEE = f'0{INSEE}'
    if INSEE >= INSEEtoSkip: 
      year = int(data[0].strip())
      comName = data[2].strip()
      comInhab = int(data[3].strip().replace('.', ''))
 
      if INSEE == INSEEtoSkip:
        handlemessage('', year, INSEE, comName, comInhab )
        rw = 0
      else:    
        rw = handleline(year, INSEE, comName, comInhab)
      if rw == 1:
        INSEEtoSkip = str(INSEE).strip()
  else:
    print ('Incorrect line:', line)
              
fr.close
f.close