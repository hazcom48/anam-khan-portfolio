import urllib.request,concurrent.futures,json,pathlib
from urllib.parse import urljoin,urlparse
root=pathlib.Path('dist/assets'); stories=json.loads(pathlib.Path('source-content/stories.json').read_text())
urls=['https://anamaylakhan.com/anam-headshot.jpg']+[urljoin('https://anamaylakhan.com/',s['image']) for s in stories if s['image']]+[s['url'] for s in stories if s['kind']=='radio']
def fetch(u):
 p=root/urlparse(u).path.lstrip('/');p.parent.mkdir(parents=True,exist_ok=True)
 try:
  with urllib.request.urlopen(u,timeout=30) as r: data=r.read()
  p.write_bytes(data);return dict(url=u,path=str(p),bytes=len(data),ok=True)
 except Exception as e:return dict(url=u,ok=False,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: results=list(ex.map(fetch,urls))
pathlib.Path('source-content/asset-report.json').write_text(json.dumps(results,indent=2));print(json.dumps({'downloaded':sum(r['ok'] for r in results),'bytes':sum(r.get('bytes',0) for r in results),'failures':[r for r in results if not r['ok']]}))
