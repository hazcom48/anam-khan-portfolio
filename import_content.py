from html.parser import HTMLParser
from pathlib import Path
import json
from urllib.parse import urljoin
class Node:
 def __init__(self,tag='',attrs=[]): self.tag=tag; self.attrs=dict(attrs); self.children=[]
 def text(self): return ' '.join(''.join(c if isinstance(c,str) else c.text() for c in self.children).split())
 def find(self,tag):
  found=[]
  for c in self.children:
   if isinstance(c,Node):
    if c.tag==tag: found.append(c)
    found+=c.find(tag)
  return found
class Parser(HTMLParser):
 def __init__(self): super().__init__(); self.root=Node(); self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']: self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t: self.stack=self.stack[:i];break
 def handle_data(self,d): self.stack[-1].children.append(d)
p=Parser();p.feed(Path('source-content/work.html').read_text());cards=[]
for n in p.root.find('a')+p.root.find('div'):
 cl=n.attrs.get('class','')
 if cl not in ['web-card','card','media-card']: continue
 title=n.find('h3')[0].text(); desc=n.find('p'); img=n.find('img'); media=n.find('iframe') or n.find('source')
 cards.append(dict(kind={'web-card':'digital','card':'broadcast','media-card':'radio'}[cl],title=title,description=desc[0].text() if desc else '',image=img[0].attrs.get('src') if img else None,url=n.attrs.get('href') or urljoin('https://anamaylakhan.com/',media[0].attrs['src'])))
Path('source-content/stories.json').write_text(json.dumps(cards,indent=2,ensure_ascii=False))
print('Preserved',len(cards),'stories:',{k:sum(c['kind']==k for c in cards) for k in ['digital','broadcast','radio']})
