import json,sys
from playwright.sync_api import sync_playwright
url='file://'+sys.argv[1]
seen={};queue=['#/']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium' if False else None)
    pg=b.new_page()
    pg.goto(url+'#/'); pg.wait_for_timeout(300)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    while queue:
        h=queue.pop(0)
        if h in seen: continue
        pg.evaluate(f"location.hash={json.dumps(h)}"); pg.wait_for_timeout(60)
        d=pg.evaluate("""()=>{
          const L=sel=>[...document.querySelectorAll(sel)].map(a=>({t:a.textContent.trim().replace(/\\s+/g,' '),h:a.getAttribute('href')}));
          const mainLinks=[...document.querySelectorAll('#main a')].filter(a=>!a.closest('.jnav')).map(a=>({t:a.textContent.trim().replace(/\\s+/g,' ').slice(0,80),h:a.getAttribute('href')}));
          return {title:document.title,h1:(document.querySelector('#main h1')||{}).textContent||'',
            crumb:(document.querySelector('#main .crumb, #main .hcrumb, #main [class*=crumb]')||{}).textContent||'',
            nav:L('.header .nav a'),jnav:L('.jnav a'),footer:L('footer a'),proto:L('.prototype a'),links:mainLinks,
            notfound:document.title.startsWith('Page not found')}
        }""")
        seen[h]=d
        for l in d['links']+d['nav']+d['jnav']+d['footer']+d['proto']:
            x=l['h'] or ''
            if x.startswith('#/'):
                x=x.rstrip('/') if x!='#/' else x
                if x=='#': continue
                if x not in seen and x not in queue: queue.append(x)
    json.dump({'pages':seen,'errs':errs},open('crawl.json','w'),indent=1)
    print(len(seen), 'pages; notfound:',[k for k,v in seen.items() if v['notfound']]); print(errs[:5])
