from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
import json,xml.etree.ElementTree as ET
class Check(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.scripts=[];self.inschema=False
 def handle_starttag(self,t,a):
  d=dict(a);self.tags.append((t,d))
  if t=='script' and d.get('type')=='application/ld+json':self.inschema=True
 def handle_data(self,d):
  if self.inschema:self.scripts.append(d)
 def handle_endtag(self,t):
  if t=='script':self.inschema=False
root=Path('dist');fail=[];reports=[]
for f in root.glob('*.html'):
 p=Check();p.feed(f.read_text());ids={a['id'] for t,a in p.tags if 'id' in a}
 assert sum(t=='h1' for t,a in p.tags)==1,f'{f} H1 count'
 for raw in p.scripts:json.loads(raw)
 for t,a in p.tags:
  for k in ['src','href']:
   u=a.get(k,''); v=urlparse(u)
   if not u or v.scheme or v.netloc:continue
   path=root/unquote(v.path.lstrip('/')) if v.path else f
   if path.is_dir():path=path/'index.html'
   if not path.exists():fail.append(f'{f}: missing {u}')
   if v.fragment and path.exists():
    q=Check();q.feed(path.read_text());found={x['id'] for _,x in q.tags if 'id' in x}
    if v.fragment not in found:fail.append(f'{f}: missing anchor {u}')
  if t=='img' and 'alt' not in a:fail.append(f'{f}: missing alt')
 if f.name!='404.html':
  assert sum(t=='link' and a.get('rel')=='canonical' for t,a in p.tags)==1
  assert sum(t=='meta' and a.get('name')=='description' for t,a in p.tags)==1
 reports.append({'page':f.name,'h1':1,'structuredData':'valid JSON'})
work=Check();work.feed((root/'work.html').read_text());story_ids=[a['id'] for t,a in work.tags if t=='article' and 'id' in a]
assert len(story_ids)==76 and len(set(story_ids))==76
assert sum(t=='article' for t,a in work.tags)==130
assert sum(t=='time' for t,a in work.tags)==54
assert sum(t=='audio' for t,a in work.tags)==14
assert sum(t=='details' and a.get('class')=='clip' for t,a in work.tags)==19
assert (root/'work.html').read_text().count('Recording currently unavailable.')==6
assert 'mailto:anamlaylakhan@gmail.com' in (root/'contact.html').read_text()
ET.parse(root/'sitemap.xml')
assert not fail,fail
print(json.dumps({'passed':True,'pages':reports,'stories':130,'originalStories':76,'additionalVerifiedArticles':54,'availableRadio':14,'missingSourceRadio':6,'broadcastReports':19,'internalLinksAndAssets':'valid','sitemap':'valid XML'},indent=2))
