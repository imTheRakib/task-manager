from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("route/index")
@action.uses("route/index.html", flash,session,auth,T,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'

    
    return locals()

@action("route/create", method=['GET', 'POST'])
@action.uses("route/create.html",  flash,session,auth,T,db)
def create(id=None): 
    stations=db(db.station).select(db.station.id,db.station.station,db.station.station_code)
    return locals()

@action("route/submit", method=['POST'])
@action.uses("route/index.html", session,auth,T)
def submit(id=None): 
    route_code=request.forms.get('route_code')
    route_name=request.forms.get('route_name')
    route_bangla=request.forms.get('route_bangla')
    start_point=request.forms.get('start_point')
    end_point=request.forms.get('end_point')
    departure_time=request.forms.get('departure_time')
    arrive_time=request.forms.get('arrive_time')
    distance_km=request.forms.get('distance_km')
    sorting_order=request.forms.get('sorting_order')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if route_code=='' or route_code is None:
        errors.append('Enter Route Code')      
    else:
        rows_check=db((db.route_setup.route_code==route_code) ).select(db.route_setup.route_code,limitby=(0,1))
        if rows_check:
            errors.append('Route Code already exist')   
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
        redirect(URL('route','create')) 
        
    # split section
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
    db.route_setup.insert(
        route_code=route_code,
        route_name=route_name,
        route_bangla=route_bangla,
        sp_id=sp_id,
        start_point=sp_name,
        ep_id=ep_id,
        end_point=ep_name,
        sorting_order=sorting_order,
        distance_km=distance_km,
        departure_time=departure_time,
        arrive_time=arrive_time,
        status=status
        )        
        
    flash.set('Record added successfully', 'success')
    redirect(URL('route','index'))   

@action("route/edit", method=['GET', 'POST'])
@action.uses("route/edit.html",  flash,session,auth,T,db)
def edit(id=None): 
    request_id = request.query.get('id')
    stations=db(db.station).select(db.station.id,db.station.station,db.station.station_code)

    if request_id:
        record = db(db.route_setup.id == request_id).select().first()
        
    return locals()

@action("route/update", method=['POST'])
@action.uses("route/index.html", flash,session,auth,T,db)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.route_setup.id == request_id).select().first()
        
    route_code=request.forms.get('route_code')
    route_name=request.forms.get('route_name')
    route_bangla=request.forms.get('route_bangla')
    start_point=request.forms.get('start_point')
    end_point=request.forms.get('end_point')
    departure_time=request.forms.get('departure_time')
    arrive_time=request.forms.get('arrive_time')
    distance_km=request.forms.get('distance_km')
    sorting_order=request.forms.get('sorting_order')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if route_code=='' or route_code is None:
        errors.append('Enter Route Code')      
    else:
        rows_check=db((db.route_setup.route_code==route_code) & (db.route_setup.id!=request_id) ).select(db.route_setup.route_code,limitby=(0,1))
        if rows_check:
            errors.append('Route Code already exist')   
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
        redirect(URL('route','edit',vars=dict(id=request_id))) 
    
    # split section
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
        route_code=route_code,
        route_name=route_name,
        route_bangla=route_bangla,
        sp_id=sp_id,
        start_point=sp_name,
        ep_id=ep_id,
        end_point=ep_name,
        sorting_order=sorting_order,
        distance_km=distance_km,
        departure_time=departure_time,
        arrive_time=arrive_time,
        status=status
        )  
    
    flash.set('Record updated successfully', 'success')
    redirect(URL('route','index'))  


@action("route/delete")
@action.uses("route/index.html", flash,session,auth,T,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.route_setup.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('route', 'index')))

    return locals()


@action("route/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    
    #Search Start##
    conditions = ""
    
    if  request.query.get('route_name') != None and request.query.get('route_name') !='':
        conditions += " and id = '"+str(request.query.get('route_name'))+"'"
        
    if  request.query.get('sp_name') != None and request.query.get('sp_name') !='':
        conditions += " and sp_id = '"+str(request.query.get('sp_name'))+"'"
        
    if  request.query.get('ep_name') != None and request.query.get('ep_name') !='':
        conditions += " and ep_id = '"+str(request.query.get('ep_name'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM route_setup where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `route_setup` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
