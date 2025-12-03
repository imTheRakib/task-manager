from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
import json

@action("ctp_setup/index")
@action.uses("ctp_setup/index.html",session,flash,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'

    return locals()

@action("ctp_setup/create", method=['GET', 'POST'])
@action.uses("ctp_setup/create.html", session,auth,T,db,flash)
def create(id=None): 
    pages=db(db.page_setup).select(db.page_setup.id,db.page_setup.page_name)
    request_id = request.query.get('id')
    
    if request_id:
        press_list=db(db.press_setup.id==request_id).select(db.press_setup.id,db.press_setup.press_name)
        record = db(db.ctp_setup.press_id == request_id).select().first()
        if record:
            redirect(URL('ctp_setup','edit',vars=dict(id=request_id)))
        else:
            return locals()
    else:
        return locals()

@action("ctp_setup/submit", method=['POST'])
@action.uses("ctp_setup/index.html", session,auth,T,db,flash)
def submit(id=None): 
    request_id = request.query.get('id')
    press=request.forms.get('press_name')
    page_names=request.forms.get('page_name')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if press=='' or press is None:
        errors.append('Enter Press name') 

    
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('ctp_setup','create',vars=dict(id=request_id))) 
    
    
    # split section
    press_id=0
    press_name=''
    if press:
        all_press=str(press).split('||')
        press_id=all_press[0]
        press_name=all_press[1]
        
    df_time=""
    for page in page_names:
        pages = page.split('||')
        df_time = request.forms.get('defalut_time_'+pages[0])
        ctp_dict = {
            'press_id': press_id,
            'press_name': press_name,
            "page_id": pages[0],
            "page_name": pages[1],
            "default_time": df_time,
            "status": status,
        }
        db.ctp_setup.update_or_insert(
            (db.ctp_setup.press_id == press_id) & (db.ctp_setup.page_id == pages[0]),
            **ctp_dict
        )
        
        
    flash.set('Record added successfully', 'success')
    redirect(URL('ctp_setup','index'))   

@action("ctp_setup/edit", method=['GET', 'POST'])
@action.uses("ctp_setup/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    pages = db(db.page_setup).select(db.page_setup.id, db.page_setup.page_name)
    request_id = request.query.get('id')
    if request_id:
        press_list = db(db.press_setup.id == request_id).select(db.press_setup.id, db.press_setup.press_name)
        record = db(db.ctp_setup.press_id == request_id).select()
        record_map = {int(rec.page_id): rec.default_time for rec in record}
       
        page_list = []
        for page in pages:
            page_list.append({
            'id': page.id,
            'page_name': page.page_name,
            'default_time': record_map.get(page.id, '')  # Get default_time or empty string if not found
            }) 
    return locals()

@action("ctp_setup/delete")
@action.uses("ctp_setup/index.html",session,flash,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.ctp_setup.press_id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('ctp_setup', 'index')))

    return locals()


@action("ctp_setup/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('name') != None and request.query.get('name') !='':
        conditions += " and cs.press_id = '"+str(request.query.get('name'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and cs.status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT cs.default_time as default_time,cs.page_name as page_name,cs.status as status,ps.press_name as press_name,ps.id as press_row_id FROM press_setup ps left join ctp_setup cs on cs.press_id=ps.id where 1 "+conditions, as_dict=True))

    
    page = int(int(request.query.get('start'))/int(request.query.get('length')) +1 or 1)
    rows_per_page = int(request.query.get('length') or 15)
    if rows_per_page == -1:
        rows_per_page = total_rows
    start = (page - 1) * rows_per_page         
    end = rows_per_page
    ##Paginate End##

    #Ordering Start##
    sort_column_index = int(request.query.get('order[0][column]') or 0)
    sort_column_name = request.query.get('columns[' + str(sort_column_index) + '][data]') or 'id'
    sort_direction = request.query.get('order[0][dir]') or 'desc'
    #Ordering End##

    ##Querry Start##
    sql = """
    SELECT cs.default_time as default_time,cs.page_name as page_name,cs.status as status,ps.press_name as press_name,ps.id as press_row_id FROM press_setup ps left join ctp_setup cs on cs.press_id=ps.id where 1 """+conditions+""" ORDER BY cs."""+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
