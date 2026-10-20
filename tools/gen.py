import json,html
d=json.load(open('crawl.json'))['pages']
Q=json.loads(open('q.out').read().split('\n')[0])
E=html.escape
def T(r):
    k='#/'+r if r else '#/'
    v=d.get(k)
    if not v: return r
    h=v['h1'].strip()
    t=v['title'].split(' | ')[0]
    return t if t not in('Home','Prototype guide') or not h else t
def N(label,route,kids=None,note='',tag=''):
    return dict(l=label,r=route,k=kids or [],n=note,t=tag)
def G(label,kids,note=''):  # grouping label, not a page
    return dict(l=label,r=None,k=kids,n=note,t='group')
def node(n,depth=0):
    r=n['r']; cls='grp' if r is None else 'pg'
    tag=f'<span class="tag">{E(n["t"])}</span>' if n['t'] and n['t']!='group' else ''
    route=f'<code>#/{E(r)}</code>' if r is not None else ''
    note=f'<span class="note">{E(n["n"])}</span>' if n['n'] else ''
    srch=E(((n['l'] or '')+' '+(r or '')).lower())
    s=f'<li class="{cls}" data-s="{srch}"><div class="row"><span class="lbl">{E(n["l"])}</span>{tag}{route}{note}</div>'
    if n['k']: s+='<ul>'+''.join(node(c,depth+1) for c in n['k'])+'</ul>'
    return s+'</li>'
def col(menu,n,active):
    return f'<section class="col"><header class="tab"><span class="menu">{E(menu)}</span><span class="act">Stays highlighted on: {E(active)}</span></header><ul class="tree">{node(n)}</ul></section>'

progs=['investigators','freeman-hrabowski-scholars','hanna-gray-fellows','gilliam-fellows','cech-fellows']
stories=[('ras-cancers','Cancer biology'),('fly-connectome','Neuroscience'),('plants','Plant biology'),('proteins','Molecular biology'),('crispr','Genetics'),('touch','Neuroscience'),('first-research','Research training')]
sci=['baker','brophy','doudna','dougan','patapoutian','shokat']
hhmi_cols=[
 ('Programs',N('Programs','programs',[N('Program finder','programs/finder',tag='tool'),N('Compare programs','programs/compare',tag='tool'),G('Program pages',[N(T('programs/'+p),'programs/'+p) for p in progs])]),'/programs and everything under it'),
 ('Our scientists',N('Our scientists','scientists',[N('Science & discoveries','scientists/discoveries',[N(T('scientists/discoveries/'+s),'scientists/discoveries/'+s,note=c) for s,c in stories],note='also reachable as #/discoveries/…'),G('Scientist profiles',[N(T('scientists/'+s),'scientists/'+s) for s in sci])]),'/scientists and everything under it'),
 ('Shaping science',N('Shaping how science is done','shaping-science',[N('Open science','shaping-science/open-science'),N('Science leadership & lab culture','shaping-science/science-leadership-lab-culture')]),'/shaping-science and its 2 topics'),
 ('Science for everyone',N('Science for everyone','engagement',[N('BioInteractive','engagement/biointeractive'),N('Science Education Alliance','engagement/sea'),N('Tangled Bank Studios','engagement/tangled-bank')]),'/engagement and its 3 pages'),
]
offmenu=N('Pages outside the header menu',None,[
  N('About HHMI','about',note='footer only'),
  N('Prototype guide','guide',note='footer + top banner'),
  N('Explore your path','careers/interests',[N(T('careers/interests/'+x).replace('Explore your path',''),'careers/interests/'+x) for x in []],note='linked from HHMI home and Join Janelia'),
  N('Other roles (HHMI)','careers/other-roles',note='only from “Contribute technical or professional expertise”'),
])
# fill careers subpages with h1
ci=[('lead','Lead a laboratory'),('research','Pursue hands-on research'),('ai','Build AI for science'),('fellowships','Find fellowship support'),('professional','Contribute technical or professional expertise')]
offmenu['k'][2]['k']=[N(l,'careers/interests/'+r) for r,l in ci]
offmenu['t']='group'

ann=[('beginning','2006','A different place to do science'),('gcamp','2013','Making neural activity visible'),('nobel','2014','Seeing beyond the old limits'),('fluor','2015','Small molecules. New views of life'),('hemibrain','2020','A map to explore, together'),('virtual-fly','2024','A virtual fly takes flight')]
leaders=['spruston','rubin','lavis','saalfeld','hermundstad']; labs=['rubin','lavis','saalfeld','hermundstad','spruston','dudman']
units=[('biology','Biology'),('tools','Tools@HHMI'),('ai','AI@HHMI'),('theory','Theory@HHMI')]
jcols=[
 ('About Janelia',N('About Janelia','janelia/about',[N('Life at Janelia','janelia/life'),N('How we work','janelia/how-we-work'),N('Janelia and HHMI','janelia/connections'),N('Janelia at 20','janelia/anniversary',[N(t,'janelia/anniversary/'+r,note=y) for r,y,t in ann])]),'about, life, how-we-work, connections, anniversary/*'),
 ('Science',N('The science','janelia/science',[N('Open questions','janelia/questions',[G('Filtered by field',[N('For biologists','janelia/questions/for/biology',tag='filter'),N('For AI researchers','janelia/questions/for/ai',tag='filter'),N('For theorists','janelia/questions/for/theory',tag='filter'),N('For tool builders','janelia/questions/for/tools',tag='filter')]),G('36 question pages, each with a technical statement',[],note='full list below')]),N('Research units','janelia/units',[N(n,'janelia/units/'+u) for u,n in units])]),'science, questions/*, units/*'),
 ('People',N('People and teams','janelia/people',[N('Leadership','janelia/leadership',[N(d['#/janelia/leadership/'+p]['h1'],'janelia/leadership/'+p) for p in leaders]),N('Lab heads','janelia/labs',[N(d['#/janelia/labs/'+p]['h1'],'janelia/labs/'+p) for p in labs])]),'people, leadership/*, labs/*'),
 ('Resources',N('Resources','janelia/resources',[N('Research tools','janelia/resources/tools'),N('Data and code','janelia/resources/data')]),'resources/*'),
 ('Join Janelia',N('Scientific careers','janelia/join',[N('Principal Scientists','janelia/join/principal-scientists'),N('AI Scientists','janelia/join/ai-scientists'),N('Group Leaders','janelia/join/group-leaders'),N('Other roles','janelia/join/other-roles',note='breadcrumb says “Students and other roles”')]),'join/*'),
]
jorph=N('Built but not linked from anywhere',None,[N('Opportunities','janelia/join/opportunities',note='“Find the work that connects with yours.”'),N('Janelia prototype guide','janelia/prototype-guide',note='“Explore the proposed experience.”')]); jorph['t']='group'

# questions library
fields=[('biology','Biology','For biologists'),('ai','AI','For AI researchers'),('theory','Theory','For theorists'),('tools','Tools','For tool builders')]
ql=''
for f,fn,aud in fields:
    themes=[t for t in Q['themes'] if t.startswith(f+'-')]
    body=''
    for t in themes:
        items=''.join(f'<li class="pg" data-s="{E((x[3]+" "+x[0]).lower())}"><div class="row"><span class="lbl">{E(x[3])}</span><code>…/questions/{E(x[0])}</code><span class="tech">+ /technical</span></div></li>' for x in Q['q'] if x[2]==t)
        body+=f'<div class="theme"><h4>{E(Q["themes"][t])}</h4><ul class="qlist">{items}</ul></div>'
    n=sum(1 for x in Q['q'] if x[1]==f)
    ql+=f'<section class="qcol"><header><span class="menu">{fn}</span><span class="act">{n} questions · filter view <code>#/janelia/questions/for/{f}</code></span></header>{body}</section>'

cross=[
 ('HHMI home','Janelia home, The science, Join Janelia; Explore your path'),
 ('Programs hub','Join Janelia'),
 ('Explore your path (5 interest pages)','Janelia Principal Scientists, AI Scientists, Group Leaders, Other roles, Open questions for AI; HHMI program pages'),
 ('Our scientists hub','Janelia People'),
 ('Science & discoveries hub','Janelia at 20'),
 ('Fly connectome story','Janelia People'),
 ('Shaping science hub','Janelia home, Research tools'),
 ('Open science topic','Tools@HHMI unit; fly connectome story (via the #/discoveries alias)'),
 ('Lab culture topic','Janelia How we work'),
 ('Janelia How we work','Shaping science hub, Lab culture topic'),
 ('Janelia Resources','Open science topic'),
 ('Janelia research units','Matching anniversary milestone, leader profile, and 3 open questions each'),
 ('Janelia lab pages','Matching leadership profile, research unit, open questions, Research tools (Lavis)'),
]
issues=[
 ('Orphan pages','<code>#/janelia/join/opportunities</code> and <code>#/janelia/prototype-guide</code> render, but nothing links to them. They look like leftovers from an earlier navigation.'),
 ('Two “Other roles” pages','<code>#/careers/other-roles</code> (HHMI) is reachable only from one interest page and just points onward to <code>#/janelia/join/other-roles</code>.'),
 ('“Explore your path” has no menu home','The careers quiz (6 pages) isn’t under any header item, so no menu item highlights while you’re in it. It’s reached from the HHMI home and Join Janelia.'),
 ('About HHMI is footer-only','<code>#/about</code> has no header entry and no in-page links pointing to it.'),
 ('People appear twice','Five people have both a <em>Leadership</em> profile and a <em>Lab</em> page (Spruston, Rubin, Lavis, Saalfeld, Hermundstad). Dudman has only a lab page.'),
 ('Duplicate URL for one story','The fly connectome story also lives at <code>#/discoveries/fly-connectome</code>, and the Open science page links to that alias.'),
 ('Label mismatches','<code>#/janelia/about</code> sets the browser tab to “Prototype guide”. Janelia’s Other roles page has the breadcrumb “Students and other roles”.'),
 ('Thinly linked pages','Data and code, the Dudman lab, and each interest page have only one way in.'),
]
hhmi_html=''.join(col(m,n,a) for m,n,a in hhmi_cols)
j_html=''.join(col(m,n,a) for m,n,a in jcols)
tmpl=open('tmpl.html').read()
out=(tmpl.replace('{{HHMI}}',hhmi_html).replace('{{OFF}}',f'<ul class="tree">{node(offmenu)}</ul>')
 .replace('{{JANELIA}}',j_html).replace('{{JORPH}}',f'<ul class="tree">{node(jorph)}</ul>').replace('{{QLIB}}',ql)
 .replace('{{CROSS}}',''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a,b in cross))
 .replace('{{ISSUES}}',''.join(f'<li><strong>{E(a)}.</strong> {b}</li>' for a,b in issues))
 .replace('{{N}}',str(len(d)+1)))
open('janelia-sitemap.html','w').write(out); print(len(out))
