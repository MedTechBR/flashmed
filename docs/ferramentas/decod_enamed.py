import fitz, sys
from fontTools.ttLib import TTFont
def mapa(path):
    f=TTFont(path); go=f.getGlyphOrder(); rev={}
    for cp,name in f.getBestCmap().items():
        gid=go.index(name)
        if gid not in rev or cp<rev[gid][0]: rev[gid]=(cp,)
    m={g:chr(c[0]) for g,c in rev.items()}
    # ligaduras
    cmapn={v:chr(k) for k,v in f.getBestCmap().items()}
    if 'GSUB' in f:
        for lk in f['GSUB'].table.LookupList.Lookup:
            for st in lk.SubTable:
                st=getattr(st,'ExtSubTable',st)
                if hasattr(st,'ligatures'):
                    for first,ligs in st.ligatures.items():
                        for lg in ligs:
                            comp=[first]+lg.Component
                            if all(c in cmapn for c in comp):
                                gid=go.index(lg.LigGlyph)
                                m.setdefault(gid,''.join(cmapn[c] for c in comp))
    return m
D="/Applications/Microsoft Word.app/Contents/Resources/DFonts/"
M={'Calibri-Light':mapa(D+'calibril.ttf'),'Calibri-LightItalic':mapa(D+'calibrili.ttf')}
doc=fitz.open(sys.argv[1]); out=[]; falt=set()
for p in doc:
    w=p.rect.width
    blocos=p.get_text('dict')['blocks']
    # duas colunas: ordena por coluna e depois y
    linhas=[]
    for b in blocos:
        for l in b.get('lines',[]):
            s=''
            for sp in l['spans']:
                fn=sp['font'].split('+')[-1]
                t=sp['text']
                if fn in M and any(ord(c)<0x20 or 0x100<=ord(c)<0x500 for c in t):
                    dec=''
                    for c in t:
                        g=ord(c)
                        if g in M[fn]: dec+=M[fn][g]
                        else: dec+='?'; falt.add((fn,g))
                    t=dec
                s+=t
            x0,y0=l['bbox'][0],l['bbox'][1]
            linhas.append((0 if x0<w/2-10 else 1,round(y0,1),x0,s))
    linhas.sort()
    out.append(f'\n=== PAGINA {p.number+1} ===\n'+'\n'.join(x[3] for x in linhas))
open(sys.argv[2],'w').write('\n'.join(out))
print('faltando',sorted(falt)[:30])
