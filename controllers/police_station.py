from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("police_station/index")
@action.uses("police_station/index.html",session,flash,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'

    
    return locals()

@action("police_station/create", method=['GET', 'POST'])
@action.uses("police_station/create.html", session,auth,T,db,flash)
def create(id=None): 
    divisions=db(db.division).select(db.division.id,db.division.division)
    districts=db(db.district).select(db.district.id,db.district.district)
    return locals()

@action("police_station/submit", method=['POST'])
@action.uses("police_station/index.html", session,auth,T,db,flash)
def submit(id=None): 
    police_station=request.forms.get('police_station')
    status=request.forms.get('status')
    division=request.forms.get('division')
    district=request.forms.get('district')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if police_station=='' or police_station is None:
        errors.append('Enter Police Station') 
    if district=='' or district is None:
        errors.append('Enter District Name') 
    if division=='' or division is None:
        errors.append('Enter Division Name') 
    # else:
    #     rows_check=db((db.police_station.police_station==police_station) ).select(db.police_station.police_station,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Police Station name already exist')
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('police_station','create')) 
        
    # split section
    div_id=0
    division_name=''
    if division:
        divisions=str(division).split('||')
        div_id=divisions[0]
        division_name=divisions[1]
        
    dist_id=0
    district_name=''
    if district:
        districts=str(district).split('||')
        dist_id=districts[0]
        district_name=districts[1]
    
    
    # insert function
    db.police_station.insert(
        police_station=police_station,
        dist_id=dist_id,
        district=district_name,
        div_id=div_id,
        division=division_name,
        status=status
        )        
        
    flash.set('Record added successfully', 'success')
    redirect(URL('police_station','index'))   

@action("police_station/edit", method=['GET', 'POST'])
@action.uses("police_station/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    request_id = request.query.get('id')
    divisions=db(db.division).select(db.division.id,db.division.division)
    districts=db(db.district).select(db.district.id,db.district.district)
    
    if request_id:
        record = db(db.police_station.id == request_id).select().first()
        
    return locals()

@action("police_station/update", method=['POST'])
@action.uses("police_station/index.html", session,auth,T,db,flash)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.police_station.id == request_id).select().first()
        
    police_station=request.forms.get('police_station')
    status=request.forms.get('status')
    division=request.forms.get('division')
    district=request.forms.get('district')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if police_station=='' or police_station is None:
        errors.append('Enter Police Station') 
    if district=='' or district is None:
        errors.append('Enter District Name') 
    if division=='' or division is None:
        errors.append('Enter Division Name') 
    # else:
    #     rows_check=db((db.district.district==district) & (db.district.id!=request_id)).select(db.district.district,limitby=(0,1))
    #     if rows_check:
    #         errors.append('District name already exist')
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('police_station','edit',vars=dict(id=request_id))) 
    
    # split section
    div_id=0
    division_name=''
    if division:
        divisions=str(division).split('||')
        div_id=divisions[0]
        division_name=divisions[1]
    
    dist_id=0
    district_name=''
    if district:
        districts=str(district).split('||')
        dist_id=districts[0]
        district_name=districts[1]
    
    # insert function
    record.update_record(
        police_station=police_station,
        dist_id=dist_id,
        district=district_name,
        div_id=div_id,
        division=division_name,
        status=status
        )        
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('police_station','index'))  


@action("police_station/delete")
@action.uses("police_station/index.html",session,flash,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.police_station.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('police_station', 'index')))

    return locals()


@action("police_station/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    
    #Search Start##
    conditions = ""
    
    if  request.query.get('police_station') != None and request.query.get('police_station') !='':
        conditions += " and id = '"+str(request.query.get('police_station'))+"'"
        
    if  request.query.get('district') != None and request.query.get('district') !='':
        conditions += " and dist_id = '"+str(request.query.get('district'))+"'"
        
    if  request.query.get('division') != None and request.query.get('division') !='':
        conditions += " and div_id = '"+str(request.query.get('division'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM police_station where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `police_station` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
