from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("vehicle_route/index")
@action.uses("vehicle_route/index.html",flash,session,auth,T,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    
    
    
    return locals()

@action("vehicle_route/create", method=['GET', 'POST'])
@action.uses("vehicle_route/create.html", flash,session,auth,T,db)
def create(id=None): 

    vehicles=db(db.vehicle).select(db.vehicle.id,db.vehicle.vehicle_code,db.vehicle.vehicle_name)
    routes=db(db.route_setup).select(db.route_setup.id,db.route_setup.route_code,db.route_setup.route_name)
    sub_routes=db(db.sub_route).select(db.sub_route.id,db.sub_route.sub_route_code,db.sub_route.sub_route_name)


    return locals()

@action("vehicle_route/submit", method=['POST'])
@action.uses("vehicle_route/index.html", flash,session,auth,T,db)
def submit(id=None): 
    vehicle=request.forms.get('vehicle_name')
    driver_name=request.forms.get('driver_name')
    license_no=request.forms.get('license_no')
    route_names=request.forms.get('route_name')
    sub_route=request.forms.get('sub_route')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if str(vehicle)=='' or vehicle is None:
        errors.append('Enter vehicle') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(driver_name)=="" or driver_name is None:
        errors.append('Enter driver name') 
    if str(license_no)=="" or license_no is None:
        errors.append('Enter license no.') 
    if str(route_names)=="" or route_names is None:
        errors.append('Enter route') 
    if str(sub_route)=="" or sub_route is None:
        errors.append('Enter sub route')
        
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('vehicle_route','create')) 
        
        
    vehicle_id=0
    vehicle_name=''
    if vehicle:
        vehicles=str(vehicle).split('||')
        vehicle_id=vehicles[0]
        vehicle_name=vehicles[1] 
        
    route_id=0
    route_name=''
    if route_names:
        routes=str(route_names).split('||')
        route_id=routes[0]
        route_name=routes[1] 
        
    sub_route_id=0
    sub_route_name=''
    if sub_route:
        sub_routes=str(sub_route).split('||')
        sub_route_id=sub_routes[0]
        sub_route_name=sub_routes[1] 
    
    # insert function
    db.vehicle_route.insert(
        vehicle_id=vehicle_id,
        vehicle_name=vehicle_name,
        driver_name=driver_name,
        license_no=license_no,
        route_id=route_id,
        route_name=route_name,
        sub_route_id=sub_route_id,
        sub_route_name=sub_route_name,
        status=status
    )
        
    flash.set('Record added successfully', 'success')
    redirect(URL('vehicle_route','index'))   

@action("vehicle_route/edit", method=['GET', 'POST'])
@action.uses("vehicle_route/edit.html",flash,session,auth,T,db)
def edit(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.vehicle_route.id == request_id).select().first()
    
    vehicles=db(db.vehicle).select(db.vehicle.id,db.vehicle.vehicle_code,db.vehicle.vehicle_name)
    routes=db(db.route_setup).select(db.route_setup.id,db.route_setup.route_code,db.route_setup.route_name)
    sub_routes=db(db.sub_route).select(db.sub_route.id,db.sub_route.sub_route_code,db.sub_route.sub_route_name)
    
    return locals()

@action("vehicle_route/update", method=['POST'])
@action.uses("vehicle_route/index.html", flash,session,auth,T,db)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.vehicle_route.id == request_id).select().first()
        
    vehicle=request.forms.get('vehicle_name')
    driver_name=request.forms.get('driver_name')
    license_no=request.forms.get('license_no')
    route_names=request.forms.get('route_name')
    sub_route=request.forms.get('sub_route')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if str(vehicle)=='' or vehicle is None:
        errors.append('Enter vehicle') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(driver_name)=="" or driver_name is None:
        errors.append('Enter driver name') 
    if str(license_no)=="" or license_no is None:
        errors.append('Enter license no.') 
    if str(route_names)=="" or route_names is None:
        errors.append('Enter route') 
    if str(sub_route)=="" or sub_route is None:
        errors.append('Enter sub route')
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('vehicle_route','edit',vars=dict(id=request_id))) 
    
    
    vehicle_id=0
    vehicle_name=''
    if vehicle:
        vehicles=str(vehicle).split('||')
        vehicle_id=vehicles[0]
        vehicle_name=vehicles[1] 
        
    route_id=0
    route_name=''
    if route_names:
        routes=str(route_names).split('||')
        route_id=routes[0]
        route_name=routes[1] 
        
    sub_route_id=0
    sub_route_name=''
    if sub_route:
        sub_routes=str(sub_route).split('||')
        sub_route_id=sub_routes[0]
        sub_route_name=sub_routes[1] 
        
        
    # insert function
    record.update_record(
        vehicle_id=vehicle_id,
        vehicle_name=vehicle_name,
        driver_name=driver_name,
        license_no=license_no,
        route_id=route_id,
        route_name=route_name,
        sub_route_id=sub_route_id,
        sub_route_name=sub_route_name,
        status=status
        )        
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('vehicle_route','index'))  


@action("vehicle_route/delete")
@action.uses("vehicle_route/index.html",flash,session,auth,T,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.vehicle_route.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('vehicle_route', 'index')))

    return locals()


@action("vehicle_route/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('vehicle_name') != None and request.query.get('vehicle_name') !='':
        conditions += " and vr.vehicle_id = '"+str(request.query.get('vehicle_name'))+"'"
        
    if  request.query.get('driver_name') != None and request.query.get('driver_name') !='':
        conditions += " and driver_name like '%"+str(request.query.get('driver_name'))+"%'"
        
    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT vr.* FROM vehicle_route vr where 1 "+conditions, as_dict=True))

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
       SELECT
            vr.*,
            v.vehicle_code,
            rs.route_code,
            sr.sub_route_code
        FROM
            vehicle_route vr
        LEFT JOIN vehicle v ON
            vr.vehicle_id = v.id
        LEFT JOIN route_setup rs ON
            vr.route_id=rs.id
        LEFT JOIN sub_route sr ON
            vr.sub_route_id=sr.id
            where 1 """+conditions+""" ORDER BY vr."""+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    print(sql)
    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)

