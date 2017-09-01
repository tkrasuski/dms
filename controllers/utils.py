# -*- coding: utf-8 -*-
import re
from pdfutil import pdf2txt

@auth.requires_membership('admin')
def indexo():
    txt='Nope'
    if len(request.args)>0:
        id_=int(request.args[0])
        rows = db(db.files.id==id_).select()
        for f in rows:
            if f.file_:
                filename = str(f.file_)
                if '.pdf' in filename:
                    txt = pdf2txt(os.path.join(request.folder, 'uploads', filename))
                    #txt.replace
                    db(db.files.id==f.id).update(txt_content=txt[0:20000], indexed_='Yes')
                else:
                    txt='To nie jest PDF!!!'
    return txt
@auth.requires_membership('admin')
def index():
    rows=db(db.files.id>0)
    links = [lambda row: A('Pobierz zawartość z PDF',_href=URL("utils","indexo",args=[row.id])),lambda row: A('Analizuj dokument',_href=URL("utils","analizator",args=[row.id]))]
    form = SQLFORM.grid(rows, links=links)
    return dict(form=form)
@auth.requires_membership('admin')
def analizator():
    ret = 'Nie rozpoznano typu dokumentu :('
    #print len(request.args)
    if len(request.args)>0:
        #print "analizuje ", request.args[0]
        id_=int(request.args[0])
        row = db(db.files.id==id_).select().first()
        txt = row.txt_content#[:2000] # to jest nasz tekst do analizy
        #print txt
       # txt=re.sub('\r\n', r'', txt)
        ret = ret + '\n' +txt
        #txt=txt[1:]
        res = re.search(r'(?<=ZARZĄDZENIE)\s+',txt)
        #print res.groups()
    #res=re.search('Nr (\d+)',txt)
        #nr = 'ns'
        instrukcja = re.search('(I-\d+)',txt)
        polityka = re.search('(P-\d+)',txt) 
        regulamin = re.search('(R-\d+)',txt) 
        if res: # zarządzenie
            nr = 'brak'
            nr = re.search('(\d+[/_]\d+)',txt)
            wsprawie = re.search('(?<=sprawie:)\s+([a-zA-Z_0-9])',txt)
            if nr and wsprawie:
                try:
                    ret0=nr.groups()
                    print ret0
                    pnt = wsprawie.start()
                    #txt=txt.decode('utf-8')
                    ret=txt[pnt:pnt+200].replace('/n',' ')+'...'
                    txt_=txt.replace('/','_')
                    #ret=unicode(ret,errors='replace')
                    #print 'ret jest'
                    #print ret
                    db(db.files.id==id_).update(title='Zarządzenie nr '+ret0[0].replace('/','_')+ret,category=1,ou=1,indexed_='YES', txt_content=txt_)
                except:
                    raise
            ret = u'Rozpoznano typ dokumentu Zarządzenie'
        
        elif instrukcja:
            print 'szukam instrukcji'
            #res=re.search('(I-\d+)',txt) 
            
            instrukcja = instrukcja.groups()[0]
            db(db.files.id==id_).update(title='Instrukcja '+instrukcja,category=3, indexed_='YES')
            ret = 'Rozpoznano typ dokumentu Instrukcja'
        elif polityka:
            print 'szukam polityki'
            #res=re.search('(P-\d+)',txt) 
            polityka = polityka.groups()[0]
            db(db.files.id==id_).update(title='Polityka '+polityka,category=5, indexed_='YES')
            ret = 'Rozpoznano typ dokumentu Polityka'
        elif regulamin:
            print 'szukam regulaminu'
            #res=re.search('(R-\d+)',txt) 
            regulamin = regulamin.groups()[0]
            db(db.files.id==id_).update(title='Regulamin '+regulamin,category=6, indexed_='YES')
            ret = 'Rozpoznano typ dokumentu Regulamin'
        else:
            ret = 'Nie rozpoznano typu dokumentu'
    return ret
@auth.requires_membership('admin')
def anal():
    ret=[]
    rows = db(db.files.id>379).select()
    for r in rows:
        if True:# not r.indexed_ or 'YES' not in r.indexed_:
            ao=analizator(r.id)
            ret.append(ao)
    return ret
@auth.requires_membership('admin')
def validator():
    rows=db(db.files.id>0).select()
    for r in rows:
        title=r.title.replace('/','_')
        txt_content=r.txt_content.replace('/','_')
        db(db.files.id==r.id).update(title=title, txt_content=txt_content)
    return 'OK'
@auth.requires_membership('admin')
def typy():
    rows=(db.categories.id>0)
    form = SQLFORM.grid(rows)
    return dict(form=form)
def ous():
    rows=(db.ous.id>0)
    form = SQLFORM.grid(rows)
    return dict(form=form)

@auth.requires_membership('superadmin')
def trunk():
    db.files.truncate()
    db.haystack_files.truncate()
    return 'OK'
@auth.requires_membership('admin')
def adm():
	return dict(ok='ok')
@auth.requires_membership('admin')
def users():
	form = SQLFORM.grid(db.auth_membership)
	return dict(form=form)