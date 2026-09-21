"""Build the portable, static portfolio. SITE_ORIGIN selects the canonical host."""
import os,json,html,re
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from urllib.parse import urlparse
# Reassemble two audio assets stored in small source chunks for reliable uploads.
for target, parts in json.loads(Path('source-content/media-parts/manifest.json').read_text()).items():
 Path(target).parent.mkdir(parents=True,exist_ok=True)
 Path(target).write_bytes(b''.join(Path(part).read_bytes() for part in parts))
E=html.escape
OUT=Path('dist'); BASE=os.environ.get('SITE_ORIGIN','https://anam.josta.club').rstrip('/')
stories=json.loads(Path('source-content/stories.json').read_text())
assets={a['url']:a for a in json.loads(Path('source-content/asset-report.json').read_text())}
EMAIL='anamlaylakhan@gmail.com'
news=[s for s in json.loads(Path('source-content/additional-articles.json').read_text()) if s.get('verified_byline')]
news.sort(key=lambda s:s['date'],reverse=True)
DESCS=[
'What Canada’s trade agreements permit, and how their rules shape the country’s policy choices.',
'Two Canadian entrepreneurs explain the pressures that led them to move their $35-million startup to the United States.',
'Why rising silver prices have renewed questions about Canada’s critical minerals list.',
'Canada is a major gold producer but holds no gold reserves. A look at the debate as prices climb.',
'Rising demand and new projects are drawing attention to Canada’s copper industry.',
'A tightening global uranium market raises questions about how quickly Canadian producers can increase supply.',
'A look at how affordability, policy and consumer demand are affecting electric vehicle adoption in Canada.',
'How new mines, expansions and higher prices have increased Canada’s gold production.',
'Police investigate the disappearance of a trailer carrying $222,000 worth of beef in Windsor.',
'Students and a former president describe concerns about racism at NSCAD, as the university outlines support for BIPOC students.',
'A conditional $10-million offer brings new attention to the effort to save Église Sainte-Marie in Digby County.',
'A report on femicides in Ontario examines persistent gaps in support for women facing violence.',
'An expert describes the barriers Nova Scotians face when seeking help to remove intimate images shared without consent.',
'Acadian students in Guysborough County advocate for a French school and a stronger connection to their language and culture.',
'Birthday cards arrive from around the world for a Nova Scotia boy who experienced bullying at school.',
'Family and friends remember Nova Scotia author Angela Parker-Brown and her strength while living with ALS.',
'Ukrainian refugee Sasha Kaplin faces a residency requirement as he prepares to represent Nova Scotia in the Canada Games.',
'An examination of safety measures at Peggys Cove, where multiple drownings have occurred over several decades.',
'Nova Scotia families without a primary care provider turn to newborn services at mobile health clinics.',
'Nova Scotians with loved ones in Syria and Turkey respond to devastating earthquakes and organize support.',
'A Jamaican seasonal worker with cancer seeks permission to remain in Nova Scotia for treatment.',
'An expert examines barriers facing Black donors as Canadian Blood Services seeks a more diverse donor and stem cell registry.',
'An art installation in Halifax reimagines the salon of civil rights activist Viola Desmond.',
'Wood carver Jay MacKay turns trees downed by Fiona into sculptures with personal meaning for their owners.',
'Seniors in Bridgewater describe the impact of lost services, while a community group calls for intervention.',
'Hope for Wildlife cares for birds injured or displaced by Fiona, including tropical birds carried from Bermuda.',
'Crews work to clear fallen trees and restore access across the Halifax area after Fiona.',
'A Nova Scotia man joins Terry Fox’s brother to bring the Canadian fundraiser’s legacy to a run in Dublin.',
'Ukrainian health-care workers describe delays and uncertainty as they seek professional licences in Nova Scotia.',
'Gurdeep Pandher brings bhangra dancing to communities across Nova Scotia during his Joy Tour.',
'The size of a dead humpback whale and the layout of Halifax harbour complicate efforts to bring it ashore.',
'How residents of Eden Mills are working toward carbon neutrality through community action.',
'Customers celebrate Guelph Tim Hortons employee Damien Smith for the warmth he brings to his work.',
'Guelph scientist Pierre Fogal leads researchers studying weather and climate change in the Arctic.',
'The opening story in a five-part series follows Syrian families raising children and building new lives in Guelph.',
'Guelph resident Derek Roy donates part of his liver to save baby Matthew’s life.',
'Veteran Susan Giebel travels from Alberta to Guelph to return a war medal to a family she has never met.'
]
for s,d in zip([s for s in stories if s['kind']=='digital'],DESCS):s['description']=d
RADIO={
'whoopingcough':'Whooping cough cases rise across Canada',
'canadawinsrelay':'Canada wins Olympic gold in the men’s 4×100-metre relay',
'tiredumping':'Illegal tire dumping raises concerns near Mimico Creek',
'ttcandswift':'TTC service changes ahead of Taylor Swift’s Eras Tour',
'cellphoneban':'Toronto schools introduce a classroom cellphone ban',
'nurse':'Nick Nurse returns to Toronto to support student musicians',
'siakam':'Pascal Siakam receives a warm welcome back in Toronto',
'mcintosh':'Young swimmers follow in Summer McIntosh’s footsteps',
'ceasefire':'A Toronto woman reflects on the temporary ceasefire in Gaza',
'rally':'Bobi Wine visits refugees in Toronto',
'jayswildcard':'Blue Jays and Rangers compete for an AL wild-card spot',
'greenbelt':'Doug Ford reverses the Greenbelt decision',
'kingandqueen':'Kane Grant unveils a Caribbean Carnival costume',
'pwhl':'Women’s hockey sells out Scotiabank Arena',
'louismarch':'Remembering anti-gun-violence advocate Louis March',
'tyler':'Toronto Island residents rally behind a local arborist',
'airquality':'Air quality warnings bring breathing concerns in Toronto',
'asylumseekers':'Toronto appeals for rental housing for asylum seekers',
'barrie':'Barrie residents reflect on the tornado two years later',
'baseball':'East York fastpitch honours announcer Peter Cripps'}
for i,s in enumerate(stories):
 s['id']=f'story-{i+1}'
 if s['kind']=='radio':
  s['description']=s['title'].rstrip('.')+'.';s['title']=RADIO[Path(urlparse(s['url']).path).stem]
 s['title']=s['title'].replace("''She was a fighter'","'She was a fighter'").replace('Runaway Kangaroo','Runaway kangaroo')
 s['description']=s['description'].replace('add color','add colour').replace('community center','community centre')
 if s['description']:s['description']=s['description'].rstrip('.')+'.'

def pub(s):
 host=urlparse(s['url']).netloc
 return 'BNN Bloomberg' if 'bnnbloomberg' in host else 'CTV News' if 'ctvnews' in host else 'CBC News' if 'cbc.ca' in host else 'GuelphToday'
def nav(current):
 links=''.join(f'<a href="/{p}.html"'+(' aria-current="page"' if p==current else '')+(' class="nav-contact"' if p=='contact' else '')+f'>{label}</a>' for p,label in [('work','Work'),('about','About'),('contact','Get in touch')])
 return f'<a class="skip" href="#main">Skip to content</a><header class="site-header"><nav class="wrap nav" aria-label="Main navigation"><a class="brand" href="/" aria-label="Anam Khan — home"><span class="monogram" aria-hidden="true">AK</span>Anam Khan</a><div class="nav-links">{links}</div></nav></header>'
def footer():
 return '<footer class="wrap footer"><p>© 2026 Anam Khan · Broadcast &amp; Digital Journalist</p><nav aria-label="Footer navigation"><a href="/work.html">Work</a><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/about.html#demo-reels">Demo reels</a></nav></footer>'
def cta():
 return '<section class="contact-band"><div class="wrap"><div><p class="eyebrow">Have a story to share?</p><h2>Let’s talk.</h2><p>For story ideas, reporting enquiries and professional opportunities.</p></div><a class="button" href="/contact.html">Get in touch <span aria-hidden="true">↗</span></a></div></section>'
def person():return {'@type':'Person','@id':BASE+'/#anam-khan','name':'Anam Khan','alternateName':'Anam Ayla Khan','url':BASE+'/','jobTitle':'Journalist','worksFor':{'@type':'Organization','name':'BNN Bloomberg','url':'https://www.bnnbloomberg.ca/'},'sameAs':['https://www.bnnbloomberg.ca/team/anam-khan/'],'description':'Canadian journalist working across television, digital and radio, with reporting from Toronto, Halifax and Guelph.','image':BASE+'/assets/anam-headshot.jpg','alumniOf':[{'@type':'CollegeOrUniversity','name':'University of Toronto'},{'@type':'CollegeOrUniversity','name':'Humber College'}]}
def page(file,title,desc,body,kind='WebPage'):
 path='/' if file=='index' else '/'+file+'.html';url=BASE+path
 data={'@context':'https://schema.org','@graph':[person(),{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Anam Khan','publisher':{'@id':BASE+'/#anam-khan'}},{'@type':kind,'@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'en-CA','isPartOf':{'@id':BASE+'/#website'},'about':{'@id':BASE+'/#anam-khan'}}]}
 if kind=='ProfilePage':data['@graph'][-1]['mainEntity']={'@id':BASE+'/#anam-khan'}
 favicon="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='20' fill='%238c342b'/%3E%3Ctext x='20' y='26' text-anchor='middle' font-family='Arial' font-size='18' fill='%23f5f0e6'%3EAK%3C/text%3E%3C/svg%3E"
 text=f'''<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#f5f0e6"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="Anam Khan"><meta property="og:locale" content="en_CA"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><link rel="icon" type="image/svg+xml" href="{favicon}"><link rel="stylesheet" href="/style.css"><script type="application/ld+json">{json.dumps(data,ensure_ascii=False).replace('</','< /')}</script><script src="/site.js" defer></script></head><body>{nav(file)}<main id="main">{body}</main>{footer()}</body></html>'''
 (OUT/(file+'.html')).write_text(text)
def digital(s):
 return f'''<article class="story" id="{s['id']}"><a href="{E(s['url'])}" target="_blank" rel="noopener noreferrer"><img src="/assets/{E(s['image'])}" alt="" width="640" height="413" loading="lazy" decoding="async"><p class="meta">{pub(s)} · Digital</p><h3>{E(s['title'])}</h3></a><p>{E(s['description'])}</p><a class="read" href="{E(s['url'])}" target="_blank" rel="noopener noreferrer" aria-label="Read {E(s['title'])} (opens in a new tab)">Read story <span aria-hidden="true">↗</span></a></article>'''
def video(url,title):
 return f'<iframe class="video" src="{E(url)}" title="{E(title)}" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
def broadcast(s):
 vid=s['url'].rsplit('/',1)[-1]
 return f'''<article class="story media-story" id="{s['id']}"><p class="meta">Television reporting</p><h3>{E(s['title'])}</h3><p>{E(s['description'])}</p><details class="clip"><summary>Watch report <span class="visually-hidden">— {E(s['title'])}</span></summary><div class="video-slot" data-src="{E(s['url'])}" data-title="{E(s['title'])}"></div><p><a class="read" href="https://www.youtube.com/watch?v={E(vid)}" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a></p></details></article>'''
def radio(s):
 a=assets[s['url']]; local='/assets'+urlparse(s['url']).path
 player=f'<audio controls preload="none" aria-label="Listen: {E(s["title"])}"><source src="{local}" type="audio/mpeg"><a href="{local}">Download audio</a></audio>' if a['ok'] else '<p class="notice">Recording currently unavailable.</p>'
 return f'<article class="story media-story" id="{s["id"]}"><p class="meta">Radio reporting</p><h3>{E(s["title"])}</h3><p>{E(s["description"])}</p>{player}</article>'
def recent_card(s):
 d=datetime.fromisoformat(re.sub(r'\.\d+','',s['date']).replace('Z','+00:00'))
 if d.tzinfo:d=d.astimezone(ZoneInfo('America/Toronto'))
 label=d.strftime('%b %d, %Y').replace(' 0',' ')
 title=s['title']
 if title.startswith('‘We’re in for a rocky road’'):title='Industry warns of a $28-billion impact from new U.S. tariffs'
 return f'<article class="recent-story"><p class="eyebrow">BNN Bloomberg · <time datetime="{d.date().isoformat()}">{label}</time></p><h3><a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">{E(title)}</a></h3><a class="read" href="{E(s["url"])}" target="_blank" rel="noopener noreferrer" aria-label="Read {E(title)} (opens in a new tab)">Read story ↗</a></article>'
recent_home='<section class="wrap section recent-home"><div class="section-header"><div><p class="eyebrow">Recent reporting · BNN Bloomberg</p><h2>Following the<br><em>latest developments.</em></h2></div><a class="text-link" href="/work.html#recent">More recent reporting ↗</a></div><div class="grid">'+''.join(recent_card(n) for n in news[:3])+'</div></section>'
hero='''<section class="wrap hero"><div class="hero-copy"><p class="eyebrow">Broadcast, digital &amp; radio journalist</p><h1>Anam Khan.<br>Always asking<br><em>why.</em></h1><p class="intro">Behind every headline, there’s a human story. I’m a Canadian journalist reporting on the people, decisions and events shaping our communities.</p><div class="actions"><a class="button" href="#reel">Watch my reel <span aria-hidden="true">↗</span></a><a class="text-link" href="/work.html">Read my reporting</a></div></div><div class="photo-composition"><figure class="photo-wrap"><img class="hero-image" src="/assets/anam-watercolour.jpg" alt="Watercolour portrait of Anam Khan, Canadian broadcast and digital journalist" width="800" height="960" fetchpriority="high"><figcaption class="photo-caption"><span>Anam Khan</span><span>Journalist. Listener. Storyteller.</span></figcaption></figure><p class="handwritten">A little curiosity<br>goes a long way.</p></div></section><div class="wrap credits"><p>Find my reporting in</p><span>CBC News</span><span>BNN Bloomberg</span><span>CTV News</span><span>GuelphToday</span></div>'''

featured=''.join(digital(stories[i]) for i in [0,5,35])
home=hero.replace('<section class="wrap hero">','<div class="scrapbook"><section class="wrap hero">',1).replace('</section><div class="wrap credits">','</section></div><div class="wrap credits">',1)+recent_home+f'''<section class="wrap section"><div class="section-header"><div><p class="eyebrow">Selected reporting</p><h2>A few stories<br><em>worth your time.</em></h2></div><a class="text-link" href="/work.html">View all reporting ↗</a></div><div class="grid">{featured}</div></section><section class="reel-section section" id="reel"><div class="wrap reel-layout"><div><p class="eyebrow">On air &amp; on the ground</p><h2>Out in the world.<br><em>On the record.</em></h2><p>A selection of my television reporting for CBC, from the newsroom to the communities at the centre of the news.</p><div class="actions"><a class="button light" href="/about.html#demo-reels">View both demo reels ↗</a></div></div><div>{video('https://www.youtube.com/embed/lULkaWmELmQ','Anam Khan — CBC broadcast demo reel, 2024')}</div></div></section><section class="wrap section quote-section"><figure class="illustrated-portrait"><img src="/assets/anam-illustrated-portrait.jpg" alt="Illustrated portrait of Anam Khan with a reporter’s notebook" width="1254" height="1254" loading="lazy"><figcaption>A journalist’s best tool? Curiosity.</figcaption></figure><div><p class="eyebrow" style="margin-bottom:24px">Behind the reporting</p><blockquote class="quote">“Some of the most powerful stories I’ve found have come from the most ordinary places.”</blockquote><p style="margin-top:24px;max-width:650px;color:var(--muted)">I’m a Canadian broadcast and digital journalist whose work has taken me from Guelph to Halifax and Toronto. My reporting spans community life, public policy, business and breaking news.</p><a class="text-link" href="/about.html">More about me ↗</a></div></section>'''+cta()
page('index','Anam Khan | Broadcast & Digital Journalist','Explore Canadian journalist Anam Khan’s television, digital and radio reporting, with work published by CBC News, BNN Bloomberg, CTV News and GuelphToday.',home)
work='''<div class="wrap"><header class="page-head"><p class="eyebrow">The reporting archive</p><h1>Reporting from<br><em>across Canada.</em></h1><p>Explore my broadcast, digital and radio journalism: business and public policy, breaking news, and the stories of communities across Canada.</p></header><nav class="archive-nav" aria-label="Reporting formats"><a href="#recent">Recent reporting <span aria-hidden="true">54</span></a><a href="#digital">Digital stories <span aria-hidden="true">37</span></a><a href="#broadcast">Broadcast reports <span aria-hidden="true">19</span></a><a href="#radio">Radio stories <span aria-hidden="true">20</span></a><a href="/about.html#demo-reels">Demo reels ↗</a></nav>'''
work+='<section class="section archive-section" id="recent"><div class="section-header"><div><p class="eyebrow">2026 · BNN Bloomberg</p><h2>Recent reporting.</h2><p style="margin-top:18px;max-width:720px;color:var(--muted)">Business, trade, energy and the Canadian economy. Explore more of my reporting at <a class="inline-link" href="https://www.bnnbloomberg.ca/team/anam-khan/" target="_blank" rel="noopener noreferrer">BNN Bloomberg</a>.</p></div></div><div class="grid recent-grid">'+''.join(recent_card(n) for n in news[:12])+'</div><details class="more-reporting"><summary>More reporting from 2026 <span>42 stories</span></summary><div class="grid recent-grid">'+''.join(recent_card(n) for n in news[12:])+'</div></details></section>'
for kind,title,desc,render in [('digital','Digital journalism','Selected articles published by BNN Bloomberg, CTV News, CBC News and GuelphToday. Headlines reflect the stories at the time of publication.',digital),('broadcast','Broadcast reporting','Television reports on breaking news, community life, public policy and sport. Open a report to watch the original clip.',broadcast),('radio','Radio journalism','Audio reporting on Canadian news and communities. Available recordings can be played below.',radio)]:
 work+=f'<section class="section archive-section" id="{kind}"><div class="section-header"><div><p class="eyebrow">{kind}</p><h2>{title}</h2><p style="margin-top:18px;max-width:780px;color:var(--muted)">{desc}</p></div><a class="text-link" href="#main">Back to top ↑</a></div><div class="grid {"radio-grid" if kind=="radio" else ""}">'+''.join(render(s) for s in stories if s['kind']==kind)+'</div></section>'
work+='</div>'+cta()
page('work','Anam Khan’s Reporting | Broadcast, Digital & Radio','Browse Anam Khan’s journalism portfolio: 130 digital, television and radio stories covering Canadian business, breaking news and communities.',work,'CollectionPage')
about='''<div class="wrap"><header class="page-head"><p class="eyebrow">About Anam</p><h1>A little about me.<br><em>A lot about curiosity.</em></h1><p>I’m Anam Khan, a journalist with BNN Bloomberg. My work begins with listening—and following the questions that deserve an answer.</p></header><section class="about-grid section" style="padding-top:20px"><div><img class="about-portrait" src="/assets/anam-headshot.jpg" alt="Portrait of journalist Anam Khan" width="750" height="1000"><p class="eyebrow" style="margin-top:20px">Anam Khan · Journalist</p></div><div class="prose"><h2>Seeing the world through many lenses</h2><p class="lead">I spent my early childhood in Saudi Arabia and grew up in Canada. We moved often, from city to city and country to country, in search of a better life and a solid education.</p><p>Those early years shaped how I see the world. Starting over taught me to listen closely, ask questions and look for the stories that are easily overlooked. My curiosity about people and culture began long before I picked up a microphone or stepped into a newsroom.</p><h2>From local news to national conversations</h2><p>After completing a Bachelor of Arts at the University of Toronto and a postgraduate journalism certificate at Humber College, I spent several years reporting in Guelph. I wrote more than a thousand stories about the people, challenges and connections that shape a community.</p><p>One story has stayed with me: after reading an article I wrote, a stranger donated part of his liver to a baby and saved the child’s life. It remains a powerful reminder of the difference a local story can make. <a class="inline-link" href="https://www.guelphtoday.com/local-news/he-was-heaven-sent-guelph-stranger-saves-babys-life-by-donating-own-liver-2883790" target="_blank" rel="noopener noreferrer">Read the story of baby Matthew and Derek Roy ↗</a></p><p>In Halifax, Nova Scotia, I moved into television and radio reporting for CBC, covering everything from breaking news to longer features. I later returned to Toronto and the pace of a busy newsroom, where tight deadlines made clarity and accuracy especially important.</p><h2>Across communities and formats</h2><p>Each move across Canada has deepened my understanding of the country’s communities and cultures. My portfolio brings together television, radio and digital work, including reporting published by CBC News, BNN Bloomberg, CTV News and GuelphToday. I now report for <a class="inline-link" href="https://www.bnnbloomberg.ca/team/anam-khan/" target="_blank" rel="noopener noreferrer">BNN Bloomberg</a>.</p><p>Some of the most powerful stories I’ve found have come from the most ordinary places.</p><div class="actions"><a class="button" href="/work.html">Explore my reporting ↗</a></div></div></section><section class="section" id="demo-reels"><div class="section-header"><div><p class="eyebrow">See the work</p><h2>Broadcast demo reels.</h2></div><p>Field reporting. Interviews. Breaking news.</p></div><div class="reels-grid">'''+f'''<article>{video('https://www.youtube.com/embed/lULkaWmELmQ','Anam Khan — CBC broadcast demo reel, 2024')}<h3>CBC reporting · 2024</h3><p>Selected television reporting from the field.</p><a class="read" href="https://www.youtube.com/watch?v=lULkaWmELmQ" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a></article><article>{video('https://www.youtube.com/embed/zczjkdlxBaU','Anam Khan — television reporter demo reel')}<h3>Television reporter demo reel</h3><p>A further selection of broadcast work.</p><a class="read" href="https://www.youtube.com/watch?v=zczjkdlxBaU" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a></article></div></section></div>'''+cta()
page('about','About Anam Khan | Canadian Broadcast & Digital Journalist','Meet Anam Khan, a Canadian journalist with reporting experience in Guelph, Halifax and Toronto. Read her biography and watch her television demo reels.',about,'ProfilePage')
contact=f'''<section class="wrap contact-layout"><div><p class="eyebrow">Get in touch</p><h1>Have a story?<br><em>I’m listening.</em></h1><p style="max-width:530px;color:var(--muted);font-size:19px">Have a story idea, a reporting enquiry or a professional opportunity? I’d be glad to hear from you.</p><div class="actions"><a class="text-link" href="/work.html">Explore my reporting ↗</a><a class="text-link" href="/about.html#demo-reels">Watch my reels ↗</a></div></div><div class="contact-card"><p class="eyebrow">Email Anam Khan</p><a class="email" href="mailto:{EMAIL}">{EMAIL}</a><p>Please include a short introduction and the subject of your enquiry.</p><div class="actions"><a class="button light" href="mailto:{EMAIL}">Write an email ↗</a></div></div></section>'''
page('contact','Contact Anam Khan | Story Ideas & Reporting Enquiries','Contact Canadian journalist Anam Khan with story ideas, reporting enquiries and professional opportunities. Find her email and explore her work.',contact,'ContactPage')
page('404','Page Not Found | Anam Khan','Return to Anam Khan’s journalism portfolio.', '<section class="wrap section"><p class="eyebrow">Page not found</p><h1>Let’s get you<br>back to the story.</h1><div class="actions"><a class="button" href="/">Back to home ↗</a><a class="text-link" href="/work.html">Explore the reporting</a></div></section>')
# A missing-page document should never be treated as an indexable content page.
f=OUT/'404.html'; f.write_text(f.read_text().replace('<meta name="theme-color"','<meta name="robots" content="noindex"><meta name="theme-color"').replace('<link rel="canonical" href="'+BASE+'/404.html">',''))
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in ['/','/work.html','/about.html','/contact.html'])+'</urlset>\n')
(OUT/'_redirects').write_text('/index.html / 301\n')
Path('source-content/edited-stories.json').write_text(json.dumps(stories,ensure_ascii=False,indent=2))
m=Path('.openai/hosting.json'); config=json.loads(m.read_text());config['static']={'directory':'dist'};m.write_text(json.dumps(config,indent=2)+'\n')
print('Generated 4 content pages, 404 page, sitemap and robots.txt. Preserved all 76 original stories and added 54 publisher-verified articles.')
