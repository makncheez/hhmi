import json
d=json.load(open('crawl.json'))['pages']
Q=json.loads(open('q.out').read().split('\n')[0])
def h1(r): return d['#/'+r]['h1'].strip()
def P(l,r,k=None,flag=None):
    n={'l':l,'r':r}
    if k: n['k']=k
    if flag: n['f']=flag
    return n
def M(l,k): return {'l':l,'k':k}
progs=['investigators','freeman-hrabowski-scholars','hanna-gray-fellows','gilliam-fellows','cech-fellows']
stories=[('ras-cancers','Targeting hard-to-treat cancers'),('fly-connectome','Fruit fly nervous system map'),('plants','Plant defenses and growth'),('proteins','Designing new proteins'),('crispr','From bacterial defense to CRISPR'),('touch','How a cell senses touch'),('first-research','A first summer in an HHMI lab')]
sci=['baker','brophy','doudna','dougan','patapoutian','shokat']
ann=[('beginning','2006 · A different place to do science'),('gcamp','2013 · Making neural activity visible'),('nobel','2014 · Seeing beyond the old limits'),('fluor','2015 · Small molecules, new views'),('hemibrain','2020 · A map to explore, together'),('virtual-fly','2024 · A virtual fly takes flight')]
fields=[('biology','Biology'),('ai','AI'),('theory','Theory'),('tools','Tools')]
qfield=[]
for f,fn in fields:
    kids=[P(f'All {fn.lower() if f!="ai" else "AI"} questions','janelia/questions/for/'+f)]
    for t,label in Q['themes'].items():
        if not t.startswith(f+'-'): continue
        kids.append(M(label,[{'l':x[3],'r':'janelia/questions/'+x[0],'t':'janelia/questions/'+x[0]+'/technical'} for x in Q['q'] if x[2]==t]))
    qfield.append(M(fn,kids))
tree=[
 P('Programs','programs',[P('All programs','programs'),P('Program finder','programs/finder'),P('Compare programs','programs/compare'),M('Program pages',[P(h1('programs/'+p),'programs/'+p) for p in progs])]),
 P('Our scientists','scientists',[P('All scientists','scientists'),P('Science & discoveries','scientists/discoveries',[P('All discoveries','scientists/discoveries')]+[P(l,'scientists/discoveries/'+s) for s,l in stories]),M('Scientist profiles',[P(h1('scientists/'+s),'scientists/'+s) for s in sci])]),
 P('Janelia','janelia',[
   P('Janelia home','janelia'),
   P('About Janelia','janelia/about',[P('About Janelia','janelia/about'),P('Life at Janelia','janelia/life'),P('How we work','janelia/how-we-work'),P('Janelia and HHMI','janelia/connections'),P('Janelia at 20','janelia/anniversary',[P('20 years overview','janelia/anniversary')]+[P(l,'janelia/anniversary/'+r) for r,l in ann])]),
   P('Science','janelia/science',[P('The science','janelia/science'),P('Open questions','janelia/questions',[P('All open questions','janelia/questions')]+qfield),P('Research units','janelia/units',[P('All research units','janelia/units'),P('Biology','janelia/units/biology'),P('Tools@HHMI','janelia/units/tools'),P('AI@HHMI','janelia/units/ai'),P('Theory@HHMI','janelia/units/theory')])]),
   P('People','janelia/people',[P('People and teams','janelia/people'),P('Leadership','janelia/leadership',[P('All leadership','janelia/leadership')]+[P(h1('janelia/leadership/'+p),'janelia/leadership/'+p) for p in ['spruston','rubin','lavis','saalfeld','hermundstad']]),P('Lab heads','janelia/labs',[P('All lab heads','janelia/labs')]+[P(h1('janelia/labs/'+p),'janelia/labs/'+p) for p in ['rubin','lavis','saalfeld','hermundstad','spruston','dudman']])]),
   P('Resources','janelia/resources',[P('All resources','janelia/resources'),P('Research tools','janelia/resources/tools'),P('Data and code','janelia/resources/data')]),
   P('Join Janelia','janelia/join',[P('Scientific careers','janelia/join'),P('Principal Scientists','janelia/join/principal-scientists'),P('AI Scientists','janelia/join/ai-scientists'),P('Group Leaders','janelia/join/group-leaders'),P('Other roles','janelia/join/other-roles'),P('Opportunities','janelia/join/opportunities',flag='Not linked in prototype')]),
 ]),
 P('Shaping science','shaping-science',[P('Shaping how science is done','shaping-science'),P('Open science','shaping-science/open-science'),P('Science leadership & lab culture','shaping-science/science-leadership-lab-culture')]),
 P('Science for everyone','engagement',[P('Science for everyone','engagement'),P('BioInteractive','engagement/biointeractive'),P('Science Education Alliance','engagement/sea'),P('Tangled Bank Studios','engagement/tangled-bank')]),
 M('More',[P('About HHMI','about',flag='Footer only in prototype'),P('Explore your path','careers/interests',[P('Start here','careers/interests'),P('Lead a laboratory','careers/interests/lead'),P('Pursue hands-on research','careers/interests/research'),P('Build AI for science','careers/interests/ai'),P('Find fellowship support','careers/interests/fellowships'),P('Contribute technical or professional expertise','careers/interests/professional')],flag='Not in any menu in prototype'),P('Other roles at HHMI','careers/other-roles'),P('Prototype guide','guide'),P('Janelia prototype guide','janelia/prototype-guide',flag='Not linked in prototype')]),
]
def cnt(n): return (1 if 'r' in n and not n.get('k') else 0)+sum(cnt(c) for c in n.get('k',[]))
print(sum(cnt(n) for n in tree))
t=open('tmpl2.html').read().replace('{{TREE}}',json.dumps(tree,ensure_ascii=False))
open('janelia-menu.html','w').write(t)
