from pathlib import Path
p=Path('build.py');s=p.read_text();s=s.replace('import os,json,html,re','import os,json,html,re\nfrom datetime import datetime\nfrom zoneinfo import ZoneInfo')
s=s.replace("EMAIL='anamlaylakhan@gmail.com'", "EMAIL='anamlaylakhan@gmail.com'\nnews=[s for s in json.loads(Path('source-content/additional-articles.json').read_text()) if s.get('verified_byline')]\nnews.sort(key=lambda s:s['date'],reverse=True)")
s=s.replace("'jobTitle':'Broadcast and Digital Journalist'", "'jobTitle':'Journalist','worksFor':{'@type':'Organization','name':'BNN Bloomberg','url':'https://www.bnnbloomberg.ca/'},'sameAs':['https://www.bnnbloomberg.ca/team/anam-khan/']")
pos=s.index("hero='''")
s=s[:pos]+'''def recent_card(s):
 d=datetime.fromisoformat(s['date'].replace('Z','+00:00'))
 if d.tzinfo:d=d.astimezone(ZoneInfo('America/Toronto'))
 label=d.strftime('%b %d, %Y').replace(' 0',' ')
 title=s['title']
 if title.startswith('‘We’re in for a rocky road’'):title='Industry warns of a $28-billion impact from new U.S. tariffs'
 return f'<article class="recent-story"><p class="eyebrow">BNN Bloomberg · <time datetime="{d.date().isoformat()}">{label}</time></p><h3><a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">{E(title)}</a></h3><a class="read" href="{E(s["url"])}" target="_blank" rel="noopener noreferrer" aria-label="Read {E(title)} (opens in a new tab)">Read story ↗</a></article>'
recent_home='<section class="wrap section recent-home"><div class="section-header"><div><p class="eyebrow">Recent reporting · BNN Bloomberg</p><h2>Following the<br><em>latest developments.</em></h2></div><a class="text-link" href="/work.html#recent">More recent reporting ↗</a></div><div class="grid">'+''.join(recent_card(n) for n in news[:3])+'</div></section>'
''' +s[pos:]
s=s.replace("+f'''<section class=\"wrap section\"><div class=\"section-header\">", "+recent_home+f'''<section class=\"wrap section\"><div class=\"section-header\">",1)
s=s.replace('<nav class="archive-nav" aria-label="Reporting formats">','<nav class="archive-nav" aria-label="Reporting formats"><a href="#recent">Recent reporting <span aria-hidden="true">54</span></a>')
pos=s.index("for kind,title,desc,render in")
s=s[:pos]+'''work+='<section class="section archive-section" id="recent"><div class="section-header"><div><p class="eyebrow">2026 · BNN Bloomberg</p><h2>Recent reporting.</h2><p style="margin-top:18px;max-width:720px;color:var(--muted)">Business, trade, energy and the Canadian economy. Explore more of my reporting at <a class="inline-link" href="https://www.bnnbloomberg.ca/team/anam-khan/" target="_blank" rel="noopener noreferrer">BNN Bloomberg</a>.</p></div></div><div class="grid recent-grid">'+''.join(recent_card(n) for n in news[:12])+'</div><details class="more-reporting"><summary>More reporting from 2026 <span>42 stories</span></summary><div class="grid recent-grid">'+''.join(recent_card(n) for n in news[12:])+'</div></details></section>'
''' +s[pos:]
s=s.replace('76 digital, television and radio stories','130 digital, television and radio stories')
s=s.replace('I’m Anam Khan, a Canadian broadcast and digital journalist. My work begins', 'I’m Anam Khan, a journalist with BNN Bloomberg. My work begins')
s=s.replace('including reporting published by CBC News, BNN Bloomberg, CTV News and GuelphToday.', 'including reporting published by CBC News, BNN Bloomberg, CTV News and GuelphToday. I now report for <a class="inline-link" href="https://www.bnnbloomberg.ca/team/anam-khan/" target="_blank" rel="noopener noreferrer">BNN Bloomberg</a>.')
s=s.replace("Preserved all 76 story records.","Preserved all 76 original stories and added 54 publisher-verified articles.")
p.write_text(s)
