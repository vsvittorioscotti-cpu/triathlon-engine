import json,re,sys,html
from xml.etree import ElementTree as ET
p=sys.argv[1]
d=json.load(open(p))
xml=d['data']['xml']
root=ET.fromstring(xml)

def inline(el):
    out=[]
    if el.text: out.append(el.text)
    for c in el:
        t=c.tag
        if t=='text':
            inner=inline(c)
            out.append(inner)
        elif t=='bold': out.append('**'+inline(c)+'**')
        elif t=='italic': out.append('*'+inline(c)+'*')
        elif t=='code': out.append('`'+inline(c)+'`')
        elif t=='link': out.append('['+inline(c)+']('+c.get('href','')+')')
        elif t=='date': out.append(c.get('value',''))
        elif t=='mention': out.append('@'+(c.get('name') or ''))
        else: out.append(inline(c))
        if c.tail: out.append(c.tail)
    return ''.join(out)

def block(el,depth=0,prefix=''):
    t=el.tag
    if t=='paragraph':
        h=el.get('heading')
        txt=inline(el)
        if h: return '\n'+'#'*int(h)+' '+txt+'\n'
        return prefix+txt+'\n'
    if t=='list':
        kind=el.get('kind')
        res=[]
        for i,li in enumerate(el):
            inner=''.join(block(c,depth+1) for c in li)
            mark='- ' if kind!='ordered' else f'{i+1}. '
            res.append('  '*depth+mark+inner.strip()+'\n')
        return ''.join(res)
    if t=='blockquote':
        return ''.join('> '+block(c).strip()+'\n' for c in el)
    if t=='table':
        rows=[]
        for r in el:
            cells=[ ' '.join(inline(cc) for cc in c).strip().replace('\n',' ') for c in r]
            cells=[''.join(block(x) for x in c).strip().replace('\n',' ') for c in r]
            rows.append('| '+' | '.join(cells)+' |')
        if rows:
            ncol=rows[0].count('|')-1
            rows.insert(1,'|'+'---|'*ncol)
        return '\n'.join(rows)+'\n'
    if t=='codeBlock':
        return '```'+(el.get('language') or '')+'\n'+inline(el)+'\n```\n'
    if t=='horizontalRule': return '\n---\n'
    return inline(el)+'\n'

print('\n'.join(block(b) for b in root))
