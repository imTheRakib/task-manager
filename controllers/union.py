from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("union/index")
@action.uses("union/index.html",flash,session,auth,T,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'

    
    return locals()

@action("union/create", method=['GET', 'POST'])
@action.uses("union/create.html",flash,session,auth,T,db)
def create(id=None): 
    divisions=db(db.division).select(db.division.id,db.division.division)
    districts=db(db.district).select(db.district.id,db.district.district)
    police_stations=db(db.police_station).select(db.police_station.id,db.police_station.police_station)
    post_offices=db(db.post_office).select(db.post_office.id,db.post_office.post_code,db.post_office.post_office)
    return locals()

@action("union/submit", method=['POST'])
@action.uses("union/index.html",flash,session,auth,T,db)
def submit(id=None): 
    union=request.forms.get('union')
    post_office=request.forms.get('post_office')
    police_station=request.forms.get('police_station')
    division=request.forms.get('division')
    district=request.forms.get('district')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if union=='' or union is None:
        errors.append('Enter Union')     
    if post_office=='' or post_office is None:
        errors.append('Enter Post Office') 
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
        redirect(URL('union','create')) 
        
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
        
    pols_id=0
    pols_name=''
    if police_station:
        police_stations=str(police_station).split('||')
        pols_id=police_stations[0]
        pols_name=police_stations[1]
        
    post_id=0
    post_name=''
    if post_office:
        post_offices=str(post_office).split('||')
        post_id=str(post_offices[0]).strip()
        post_name=str(post_offices[1]).strip()
    
    
    # insert function
    db.unions.insert(
        union_name=union,
        post_id=post_id,
        post_office=post_name,
        pols_id=pols_id,
        police_station=pols_name,
        dist_id=dist_id,
        district=district_name,
        div_id=div_id,
        division=division_name,
        status=status
        )        
        
    flash.set('Record added successfully', 'success')
    redirect(URL('union','index'))   

@action("union/edit", method=['GET', 'POST'])
@action.uses("union/edit.html",flash,session,auth,T,db)
def edit(id=None): 
    request_id = request.query.get('id')
    divisions=db(db.division).select(db.division.id,db.division.division)
    districts=db(db.district).select(db.district.id,db.district.district)
    police_stations=db(db.police_station).select(db.police_station.id,db.police_station.police_station)
    post_offices=db(db.post_office).select(db.post_office.id,db.post_office.post_code,db.post_office.post_office)

    if request_id:
        record = db(db.unions.id == request_id).select().first()
        
    return locals()

@action("union/update", method=['POST'])
@action.uses("union/index.html",flash,session,auth,T,db)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.unions.id == request_id).select().first()
        
    union=request.forms.get('union')
    post_office=request.forms.get('post_office')
    police_station=request.forms.get('police_station')
    division=request.forms.get('division')
    district=request.forms.get('district')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if union=='' or union is None:
        errors.append('Enter Union')     
    if post_office=='' or post_office is None:
        errors.append('Enter Post Office') 
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
        redirect(URL('union','edit',vars=dict(id=request_id))) 
    
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
        
    pols_id=0
    pols_name=''
    if police_station:
        police_stations=str(police_station).split('||')
        pols_id=police_stations[0]
        pols_name=police_stations[1]
    
    post_id=0
    post_name=''
    if post_office:
        post_offices=str(post_office).split('||')
        post_id=str(post_offices[0]).strip()
        post_name=str(post_offices[1]).strip()
    
    # update function
    record.update_record(
        union_name=union,
        post_id=post_id,
        post_office=post_name,
        pols_id=pols_id,
        police_station=pols_name,
        dist_id=dist_id,
        district=district_name,
        div_id=div_id,
        division=division_name,
        status=status
        )  
    
    flash.set('Record updated successfully', 'success')
    redirect(URL('union','index'))  


@action("union/delete")
@action.uses("union/index.html",flash,session,auth,T,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.unions.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('union', 'index')))

    return locals()


@action("union/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    
    #Search Start##
    conditions = ""
    
    if  request.query.get('union') != None and request.query.get('union') !='':
        conditions += " and id = '"+str(request.query.get('union'))+"'"
        
    if  request.query.get('post_office') != None and request.query.get('post_office') !='':
        conditions += " and post_id = '"+str(request.query.get('post_office'))+"'"
        
    if  request.query.get('police_station') != None and request.query.get('police_station') !='':
        conditions += " and pols_id = '"+str(request.query.get('police_station'))+"'"
        
    if  request.query.get('district') != None and request.query.get('district') !='':
        conditions += " and dist_id = '"+str(request.query.get('district'))+"'"
        
    if  request.query.get('division') != None and request.query.get('division') !='':
        conditions += " and div_id = '"+str(request.query.get('division'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM unions where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `unions` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
