# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from pdfutil import pdf2txt
import os
import glob
@auth.requires_membership('admin')
def indall():
    rows = db(db.files.id>0).select()
    for r in rows:
        if r.indexed_:
        #db(db.files.id==r.id).update(txt_content=r.txt_content,doc_owner='NaN')
            db(db.files.id==r.id).update(title=r.title,txt_content=r.txt_content,doc_owner='NN', indexed_='YES')
    return 'OK'
@auth.requires_membership('admin')
def ppp():
    txt=''
    rows = db(db.files.indexed_=='YES').select()
    for f in rows:
        #filename = 'files.file_.94707ddc0fb6e9cb.3638205a61727ac485647a656e69652036382d31362e706466.pdf'
        if f.file_:
            filename = str(f.file_)
            txt = pdf2txt(os.path.join(request.folder, 'uploads', filename))
            db(db.files.id==f.id).update(txt_content=txt, indexed_='Yes')
        
    return txt

@auth.requires_membership('admin')
def indexo():
    txt='Nope'
    if len(request.args)>0:
        id_=int(request.args[0])
        rows = db(db.files.id==id_).select()
        for f in rows:
            if f.file_:
                filename = str(f.file_)
                txt = pdf2txt(os.path.join(request.folder, 'uploads', filename))
                db(db.files.id==f.id).update(txt_content=txt, indexed='Yes')
    return txt

@auth.requires_membership('admin')
def importer():
    ret = None
    path = os.path.join(request.folder, 'uploads')
    ret = glob.glob(path+'\*')
    return ret
def index():
    redirect(URL('default','search'))
    return dict(ok='ok')
def search():
    #print request.vars
    wyniki = 0
    ret = ''
    frm=DIV()
    #frm = SQLFORM.grid(rows, searchable=False, editable=False, create=False, deletable=False, details=True, csv=False)
    if 'strona' in request.vars:
        strona=int(request.vars['strona'])
    else:
        strona=1
    if not 'szukam' in session:
        session['szukam']=''
       # print "nie ma w sessji"
    form=FORM(
        INPUT(_name='kryterium'),
        INPUT(_type='checkbox',_name='content'),
        INPUT(_type='checkbox',_name='sort')
        )
    #kryterium=form.vars.kryterium.replace('/','_')
    #ret=index_.search( txt_content=kryterium, limit=100)
    if form.accepts(request,session, keepvalues=True):
        kryterium=form.vars.kryterium
        #print form.vars.kryterium.decode('utf-8')
        #print  session['szukam']
        #print form.vars
        if form.vars.content:
            ret=index_.search(txt_content=kryterium,mode='and', limit=100)
        else:
            ret=index_.search(title=kryterium, limit=100, mode='and')
        if form.vars.sort:
            rows = db(db.files.id.belongs(ret)).select(orderby=~db.files.created_)
        else:
            rows = db(db.files.id.belongs(ret)).select(orderby=db.files.created_)
        wyniki = (db(db.files.id.belongs(ret)).count()//30)+1
        
        # pierwszy 
       # wp = rows.first().id
       # wl = rows.last().id
        session['szukam']=kryterium.replace('_','/')
        #frm = SQLFORM.grid(rows, searchable=False, editable=False, create=False, deletable=False, details=True, csv=False)
        nr = 1
        #print len(rows)
        if len(rows)==0:
            frm.append('brak wyników')
        for r in rows:
            #if nr <= strona*30 and nr>(strona-1)*30:
            if True:
                row = P()
                row.append(DIV(str(nr)+'. '+r.title[:190].replace('_','/')+'...', _class='text-warning'))
                #row.append(BR())
                if r.category:
                    row.append('kategoria dokumentu: ')
                    row.append(r.category.category)
                else:
                    row.append('kategoria dokumentu: Brak')
                row.append(A(' pobierz',_href=URL('default','download/'+r.file_)))
                row.append(A(' szczegóły',_href=URL('default','treenode',args=[r.id])))
                frm.append(row)
            nr=nr+1
    return dict(form=form, ret=ret,strona=strona, frm=frm, wyniki=wyniki)
def search_():
    #response.view='lay.html'
    #print request.vars
    wyniki = 0
    ret = ''
    frm=DIV()
    #frm = SQLFORM.grid(rows, searchable=False, editable=False, create=False, deletable=False, details=True, csv=False)
    if 'strona' in request.vars:
        strona=int(request.vars['strona'])
    else:
        strona=1
    if not 'szukam' in session:
        session['szukam']=''
       # print "nie ma w sessji"
    form=FORM(
        INPUT(_name='kryterium'),
        INPUT(_type='checkbox',_name='content'),
        INPUT(_type='checkbox',_name='sort')
        )
    #kryterium=form.vars.kryterium.replace('/','_')
    #ret=index_.search( txt_content=kryterium, limit=100)
    if form.accepts(request,session, keepvalues=True):
        kryterium=form.vars.kryterium
        #print form.vars.kryterium.decode('utf-8')
        #print  session['szukam']
        #print form.vars
        if form.vars.content:
            ret=index_.search(txt_content=kryterium,mode='and', limit=100)
        else:
            ret=index_.search(title=kryterium, limit=100, mode='and')
        if form.vars.sort:
            rows = db(db.files.id.belongs(ret)).select(orderby=~db.files.created_)
        else:
            rows = db(db.files.id.belongs(ret)).select(orderby=db.files.created_)
        wyniki = (db(db.files.id.belongs(ret)).count()//30)+1
        
        # pierwszy 
       # wp = rows.first().id
       # wl = rows.last().id
        session['szukam']=kryterium.replace('_','/')
        #frm = SQLFORM.grid(rows, searchable=False, editable=False, create=False, deletable=False, details=True, csv=False)
        nr = 1
        #print len(rows)
        if len(rows)==0:
            frm.append('brak wyników')
        for r in rows:
            #if nr <= strona*30 and nr>(strona-1)*30:
            if True:
                row = P()
                row.append(DIV(str(nr)+'. '+r.title[:190].replace('_','/')+'...', _class='text-warning'))
                #row.append(BR())
                if r.category:
                    row.append('kategoria dokumentu: ')
                    row.append(r.category.category)
                else:
                    row.append('kategoria dokumentu: Brak')
                row.append(A(' pobierz',_href=URL('default','download/'+r.file_)))
                row.append(A(' szczegóły',_href=URL('default','treenode',args=[r.id])))
                frm.append(row)
            nr=nr+1
    return dict(form=form, ret=ret,strona=strona, frm=frm, wyniki=wyniki)
def document():
    form = None
    docid = None
    if 'docid' in request.vars:
        docid=int(request.vars['docid'])
        print docid
    else:
        print 'brak'
    if docid:
        record = db.files(docid)
        form = SQLFORM(db.files,record, readonly=True, showid=False)
    
    return dict(form=form)
def tree():
    cont=DIV()
    return dict(cont=cont)
def treenode():
    return dict(ok='ok')
        
def helpme():
    return auth.wiki()

@service.run
def upload():
    ret='OK'
    infile = request.vars.file_.decode('base64')
    import StringIO
    fh = StringIO.StringIO ( infile )
    if infile:
        fh.name=request.vars.filename_
        img = db.files.file_.store(fh, fh.name)
        id_ = db.files.insert(file_=img, title=fh.name, txt_content=request.vars.content.encode('utf-8'))
    else:
        ret='No File'
    return ret 

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


#@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
