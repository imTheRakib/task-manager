from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("vehicle/index")
@action.uses("vehicle/index.html",flash,session,auth,T,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    
    
    
    return locals()

@action("vehicle/create", method=['GET', 'POST'])
@action.uses("vehicle/create.html", flash,session,auth,T,db)
def create(id=None): 

    last_vehicle = db.vehicle.vehicle_code.max()
    last_vehicle = db().select(last_vehicle).first()[last_vehicle]
    if last_vehicle:
        vehicle_code = int(last_vehicle) + 1
    else:
        vehicle_code = 1001

    return locals()

@action("vehicle/submit", method=['POST'])
@action.uses("vehicle/index.html", flash,session,auth,T,db)
def submit(id=None): 
    vehicle_code=request.forms.get('vehicle_code')
    vehicle_name=request.forms.get('vehicle_name')
    vehicle_bangla=request.forms.get('vehicle_bangla')
    vehicle_reg_no=request.forms.get('vehicle_reg_no')
    capacity=request.forms.get('capacity')
    rate_per_trip=request.forms.get('rate_per_trip')
    owner_name=request.forms.get('owner_name')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if str(vehicle_code)=='' or vehicle_code is None:
        errors.append('Enter vehicle code') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(vehicle_name)=="" or vehicle_name is None:
        errors.append('Enter vehicle name') 
    if str(vehicle_reg_no)=="" or vehicle_reg_no is None:
        errors.append('Enter Registration No.') 
    if str(capacity)=="" or capacity is None:
        errors.append('Enter capacity') 
    if str(rate_per_trip)=="" or rate_per_trip is None:
        errors.append('Enter rate per trip') 
    if str(owner_name)=="" or owner_name is None:
        errors.append('Enter owner name') 
        
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('vehicle','create')) 
    
    # insert function
    db.vehicle.insert(
        vehicle_code=vehicle_code,
        vehicle_name=vehicle_name,
        vehicle_bangla=vehicle_bangla,
        vehicle_reg_no=vehicle_reg_no,
        capacity=capacity,
        rate_per_trip=rate_per_trip,
        owner_name=owner_name,
        status=status
    )
        
    flash.set('Record added successfully', 'success')
    redirect(URL('vehicle','index'))   

@action("vehicle/edit", method=['GET', 'POST'])
@action.uses("vehicle/edit.html", flash,session,auth,T,db)
def edit(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.vehicle.id == request_id).select().first()
    return locals()

@action("vehicle/update", method=['POST'])
@action.uses("vehicle/index.html", flash,session,auth,T,db)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.vehicle.id == request_id).select().first()
        
    vehicle_code=request.forms.get('vehicle_code')
    vehicle_name=request.forms.get('vehicle_name')
    vehicle_bangla=request.forms.get('vehicle_bangla')
    vehicle_reg_no=request.forms.get('vehicle_reg_no')
    capacity=request.forms.get('capacity')
    rate_per_trip=request.forms.get('rate_per_trip')
    owner_name=request.forms.get('owner_name')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if str(vehicle_code)=='' or vehicle_code is None:
        errors.append('Enter vehicle code') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(vehicle_name)=="" or vehicle_name is None:
        errors.append('Enter vehicle name') 
    if str(vehicle_reg_no)=="" or vehicle_reg_no is None:
        errors.append('Enter Registration No.') 
    if str(capacity)=="" or capacity is None:
        errors.append('Enter capacity') 
    if str(rate_per_trip)=="" or rate_per_trip is None:
        errors.append('Enter rate per trip') 
    if str(owner_name)=="" or owner_name is None:
        errors.append('Enter owner name')  
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('vehicle','edit',vars=dict(id=request_id))) 
    
        
    # insert function
    record.update_record(
        vehicle_code=vehicle_code,
        vehicle_name=vehicle_name,
        vehicle_bangla=vehicle_bangla,
        vehicle_reg_no=vehicle_reg_no,
        capacity=capacity,
        rate_per_trip=rate_per_trip,
        owner_name=owner_name,
        status=status
        )        
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('vehicle','index'))  


@action("vehicle/delete")
@action.uses("vehicle/index.html",flash,session,auth,T,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.vehicle.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('vehicle', 'index')))

    return locals()


@action("vehicle/get_data", method=['GET', 'POST'])
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
        conditions += " and id = '"+str(request.query.get('vehicle_name'))+"'"
        
    if  request.query.get('owner_name') != None and request.query.get('owner_name') !='':
        conditions += " and owner_name like '%"+str(request.query.get('owner_name'))+"%'"
        
    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM vehicle where 1 "+conditions, as_dict=True))

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
        SELECT * FROM vehicle where 1 """+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    print(sql)
    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)

