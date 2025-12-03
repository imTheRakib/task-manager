from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("sub_route/index")
@action.uses("sub_route/index.html", flash,session,auth,T,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    location_rows = db(db.combo_settings.key_name == 'location_list').select()
    location_list = str(location_rows[0]['value']).split(',') if location_rows else []
    
    return locals()

@action("sub_route/create", method=['GET', 'POST'])
@action.uses("sub_route/create.html",  flash,session,auth,T,db)
def create(id=None): 
    stations=db(db.station).select(db.station.id,db.station.station,db.station.station_code)
    route_setup=db(db.route_setup).select(db.route_setup.id,db.route_setup.route_name,db.route_setup.route_code)
    press_list=db(db.press_setup).select(db.press_setup.id,db.press_setup.press_name)
    
    
    location_rows = db(db.combo_settings.key_name == 'location_list').select()
    location_list = str(location_rows[0]['value']).split(',') if location_rows else []
    
    
    return locals()

@action("sub_route/submit", method=['POST'])
@action.uses("sub_route/index.html",  flash,session,auth,T,db)
def submit(id=None): 
    sub_route_code=request.forms.get('sub_route_code')
    sub_route_name=request.forms.get('sub_route_name')
    sub_route_bangla=request.forms.get('sub_route_bangla')
    route_name=request.forms.get('route_name')
    start_point=request.forms.get('start_point')
    end_point=request.forms.get('end_point')
    departure_time=request.forms.get('departure_time')
    arrive_time=request.forms.get('arrive_time')
    sorting_order=request.forms.get('sorting_order')
    press=request.forms.get('press')
    location=request.forms.get('location')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if sub_route_code=='' or sub_route_code is None:
        errors.append('Enter Sub-Route Code')      
    else:
        rows_check=db((db.sub_route.sub_route_code==sub_route_code) ).select(db.sub_route.sub_route_code,limitby=(0,1))
        if rows_check:
            errors.append('Sub-Route Code already exist')   
    if route_name=='' or route_name is None:
        errors.append('Enter Route')     
    if start_point=='' or start_point is None:
        errors.append('Enter Start Point') 
    if end_point=='' or end_point is None:
        errors.append('Enter End Point') 
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('sub_route','create')) 
        
    # split section
    route_id=0
    rt_name=''
    if route_name:
        route_names=str(route_name).split('||')
        route_id=str(route_names[0]).strip()
        rt_name=str(route_names[1]).strip()
        
    sp_id=0
    sp_name=''
    if start_point:
        start_points=str(start_point).split('||')
        sp_id=str(start_points[0]).strip()
        sp_name=str(start_points[1]).strip()
        
    ep_id=0
    ep_name=''
    if end_point:
        end_points=str(end_point).split('||')
        ep_id=str(end_points[0]).strip()
        ep_name=str(end_points[1]).strip()
    
    # last_station = db.station.station_code.max()
    # last_station = db().select(last_station).first()[last_station]
    # if last_station:
    #     station_code = int(last_station) + 1
    # else:
    #     station_code = 100001
    
    # insert function
    db.sub_route.insert(
        sub_route_code=sub_route_code,
        sub_route_name=sub_route_name,
        sub_route_bangla=sub_route_bangla,
        route_id=route_id,
        route_name=rt_name,
        sp_id=sp_id,
        start_point=sp_name,
        ep_id=ep_id,
        end_point=ep_name,
        sorting_order=sorting_order,
        departure_time=departure_time,
        arrive_time=arrive_time,
        press=press,
        location=location,
        status=status
        )        
        
    flash.set('Record added successfully', 'success')
    redirect(URL('sub_route','index'))   

@action("sub_route/edit", method=['GET', 'POST'])
@action.uses("sub_route/edit.html",  flash,session,auth,T,db)
def edit(id=None): 
    request_id = request.query.get('id')
    stations=db(db.station).select(db.station.id,db.station.station,db.station.station_code)
    route_setup=db(db.route_setup).select(db.route_setup.id,db.route_setup.route_name,db.route_setup.route_code)
    press_list=db(db.press_setup).select(db.press_setup.id,db.press_setup.press_name)
    
    location_rows = db(db.combo_settings.key_name == 'location_list').select()
    location_list = str(location_rows[0]['value']).split(',') if location_rows else []

    if request_id:
        record = db(db.sub_route.id == request_id).select().first()
        
    return locals()

@action("sub_route/update", method=['POST'])
@action.uses("sub_route/index.html",  flash,session,auth,T,db)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.sub_route.id == request_id).select().first()
        
    sub_route_code=request.forms.get('sub_route_code')
    sub_route_name=request.forms.get('sub_route_name')
    sub_route_bangla=request.forms.get('sub_route_bangla')
    route_name=request.forms.get('route_name')
    start_point=request.forms.get('start_point')
    end_point=request.forms.get('end_point')
    departure_time=request.forms.get('departure_time')
    arrive_time=request.forms.get('arrive_time')
    sorting_order=request.forms.get('sorting_order')
    press=request.forms.get('press')
    location=request.forms.get('location')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if sub_route_code=='' or sub_route_code is None:
        errors.append('Enter Sub-Route Code')      
    else:
        rows_check=db((db.sub_route.sub_route_code==sub_route_code)  & (db.sub_route.id!=request_id) ).select(db.sub_route.sub_route_code,limitby=(0,1))
        if rows_check:
            errors.append('Sub-Route Code already exist')   
    if route_name=='' or route_name is None:
        errors.append('Enter Route')     
    if start_point=='' or start_point is None:
        errors.append('Enter Start Point') 
    if end_point=='' or end_point is None:
        errors.append('Enter End Point')
    
    
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('sub_route','edit',vars=dict(id=request_id))) 
    
    # split section
    route_id=0
    rt_name=''
    if route_name:
        route_names=str(route_name).split('||')
        route_id=str(route_names[0]).strip()
        rt_name=str(route_names[1]).strip()
        
    sp_id=0
    sp_name=''
    if start_point:
        start_points=str(start_point).split('||')
        sp_id=str(start_points[0]).strip()
        sp_name=str(start_points[1]).strip()
        
    ep_id=0
    ep_name=''
    if end_point:
        end_points=str(end_point).split('||')
        ep_id=str(end_points[0]).strip()
        ep_name=str(end_points[1]).strip()
    
    # update function
    record.update_record(
        sub_route_code=sub_route_code,
        sub_route_name=sub_route_name,
        sub_route_bangla=sub_route_bangla,
        route_id=route_id,
        route_name=rt_name,
        sp_id=sp_id,
        start_point=sp_name,
        ep_id=ep_id,
        end_point=ep_name,
        sorting_order=sorting_order,
        departure_time=departure_time,
        arrive_time=arrive_time,
        press=press,
        location=location,
        status=status
        )  
    
    flash.set('Record updated successfully', 'success')
    redirect(URL('sub_route','index'))  


@action("sub_route/delete")
@action.uses("sub_route/index.html", flash,session,auth,T,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.sub_route.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('sub_route', 'index')))

    return locals()


@action("sub_route/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    
    #Search Start##
    conditions = ""
    
    if  request.query.get('sub_route') != None and request.query.get('sub_route') !='':
        conditions += " and id = '"+str(request.query.get('sub_route'))+"'"

    if  request.query.get('route_name') != None and request.query.get('route_name') !='':
        conditions += " and route_id = '"+str(request.query.get('route_name'))+"'"
        
    if  request.query.get('sp_name') != None and request.query.get('sp_name') !='':
        conditions += " and sp_id = '"+str(request.query.get('sp_name'))+"'"
        
    if  request.query.get('ep_name') != None and request.query.get('ep_name') !='':
        conditions += " and ep_id = '"+str(request.query.get('ep_name'))+"'"
        
    if  request.query.get('press_name') != None and request.query.get('press_name') !='':
        conditions += " and press = '"+str(request.query.get('press_name'))+"'"
        
    if  request.query.get('location') != None and request.query.get('location') !='':
        conditions += " and location = '"+str(request.query.get('location'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM sub_route where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `sub_route` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
