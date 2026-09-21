from pathlib import Path
p=Path('build.py');s=p.read_text()
start=s.index("hero='''");end=s.index("\nfeatured=",start)
s=s[:start]+'''hero=\'\'\'<section class="wrap hero"><div class="hero-copy"><p class="eyebrow">Broadcast, digital &amp; radio journalist</p><h1>Anam Khan.<br>Always asking<br><em>why.</em></h1><p class="intro">Behind every headline, there’s a human story. I’m a Canadian journalist reporting on the people, decisions and events shaping our communities.</p><div class="actions"><a class="button" href="#reel">Watch my reel <span aria-hidden="true">↗</span></a><a class="text-link" href="/work.html">Read my reporting</a></div></div><div class="photo-composition"><figure class="photo-wrap"><img class="hero-image" src="/assets/anam-headshot.jpg" alt="Anam Khan, Canadian broadcast and digital journalist" width="800" height="960" fetchpriority="high"><figcaption class="photo-caption"><span>Anam Khan</span><span>Journalist. Listener. Storyteller.</span></figcaption></figure><p class="handwritten">A little curiosity<br>goes a long way.</p></div></section><div class="wrap credits"><p>Find my reporting in</p><span>CBC News</span><span>BNN Bloomberg</span><span>CTV News</span><span>GuelphToday</span></div>\'\'\'
''' +s[end:]
s=s.replace('Stories with substance.','A few stories<br><em>worth your time.</em>')
s=s.replace('The story,<br>in focus.','Out in the world.<br><em>On the record.</em>')
s=s.replace('People. Places.<br>Perspective.','The world is full<br>of <em>stories.</em>')
s=s.replace('A curiosity about people.<br>A commitment to the story.','A little about me.<br><em>A lot about curiosity.</em>')
s=s.replace('Every story starts<br>with a conversation.','Have a story?<br><em>I’m listening.</em>')
s=s.replace('font-size:19px','font-size:19px')
s=s.replace('fill=\'%23142b25\'','fill=\'%238c342b\'').replace('fill=\'%23d8f36a\'','fill=\'%23f5f0e6\'').replace('content="#142b25"','content="#f5f0e6"')
p.write_text(s)
