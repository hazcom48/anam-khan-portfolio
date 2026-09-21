from import_content import Parser
from pathlib import Path
from urllib.parse import urljoin,urlparse
import json,re,urllib.request,concurrent.futures
root=Path('source-content');p=Parser();p.feed((root/'bnn-author.html').read_text())
existing={s['url'].rstrip('/') for s in json.loads((root/'stories.json').read_text())}
items=[];seen=set()
for h in p.root.find('h3'):
 links=h.find('a')
 if not links:continue
 u=urljoin('https://www.bnnbloomberg.ca',links[0].attrs.get('href',''))
 if not re.search(r'/20\d\d/\d\d/\d\d/',u) or u.rstrip('/') in existing or u in seen:continue
 seen.add(u);items.append({'kind':'digital','title':h.text(),'url':u,'image':None,'description':'','source_author_page':'https://www.bnnbloomberg.ca/team/anam-khan/'})
def check(s):
 try:
  req=urllib.request.Request(s['url'],headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as r:raw=r.read().decode()
  page=Parser();page.feed(raw)
  meta={n.attrs.get('property',n.attrs.get('name')):n.attrs.get('content') for n in page.root.find('meta')}
  byline=[a.text() for a in page.root.find('a') if '/team/anam-khan' in a.attrs.get('href','')]
  heads=page.root.find('h1')
  s['verified_byline']=bool(byline);s['title']=heads[0].text() if heads else s['title']
  s['date']=(page.root.find('time')[0].attrs.get('datetime') if page.root.find('time') else None) or '-'.join(re.search(r'/(20\d\d)/(\d\d)/(\d\d)/',s['url']).groups())
  s['source_description']=meta.get('description') or meta.get('og:description') or ''
  s['source_image']=meta.get('og:image');s['verified_on']='2026-09-21'
  return s
 except Exception as e:s['verification_error']=str(e);s['verified_byline']=False;return s
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(check,items))
(root/'additional-articles.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
print(json.dumps({'found':len(results),'verified':sum(s['verified_byline'] for s in results),'recent':[{'title':s['title'],'date':s.get('date'),'verified':s['verified_byline']} for s in results[:5]],'errors':[{'title':s['title'],'error':s.get('verification_error')} for s in results if not s['verified_byline']]}))
