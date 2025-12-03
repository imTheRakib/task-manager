from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("sales_area/index")
@action.uses("sales_area/index.html", flash,session,auth,T,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    
    
    return locals()

@action("sales_area/create", method=['GET', 'POST'])
@action.uses("sales_area/create.html", flash,session,auth,T,db)
def create(id=None): 

    
    rm_employees=db((db.employee.emp_type=="Regional Manager") & (db.employee.status=="1")).select(db.employee.emp_id,db.employee.emp_name)
    agents=db(db.agent.status=='1').select(db.agent.id,db.agent.agent_id,db.agent.agent_name)
    stations=db((db.station.status=="1")).select(db.station.id,db.station.station_code,db.station.station)

    return locals()

@action("sales_area/submit", method=['POST'])
@action.uses("sales_area/index.html", flash,session,auth,T,db)
def submit(id=None): 
    regional_manager=request.forms.get('regional_manager')
    agent=request.forms.get('agent')
    station=request.forms.get('station')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if str(regional_manager)=='' or regional_manager is None:
        errors.append('Enter regional manager') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(agent)=="" or agent is None:
        errors.append('Enter agent') 
    if str(station)=="" or station is None:
        errors.append('Enter station') 
        
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('sales_area','create')) 
        
    rm_id=0
    rm_name=''
    if regional_manager:
        rm=str(regional_manager).split('||')
        rm_id=rm[0]
        rm_name=rm[1] 
        
    agent_id=0
    agent_name=''
    if agent:
        ag=str(agent).split('||')
        agent_id=ag[0]
        agent_name=ag[1]  
        
    station_id=0
    station_name=''
    if station:
        st=str(station).split('||')
        station_id=st[0]
        station_name=st[1]  
    
    
    # insert function
    db.employee_agent.insert(
        rm_id=rm_id,
        rm_name=rm_name,
        agent_id=agent_id,
        agent_name=agent_name,
        station_id=station_id,
        station_name=station_name,
        status=status
    )
        
    flash.set('Record added successfully', 'success')
    redirect(URL('sales_area','index'))   

@action("sales_area/edit", method=['GET', 'POST'])
@action.uses("sales_area/edit.html", flash,session,auth,T,db)
def edit(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.employee_agent.id == request_id).select().first()
    rm_employees=db((db.employee.emp_type=="Regional Manager") & (db.employee.status=="1")).select(db.employee.emp_id,db.employee.emp_name)
    agents=db(db.agent.status=='1').select(db.agent.id,db.agent.agent_id,db.agent.agent_name)
    stations=db((db.station.status=="1")).select(db.station.id,db.station.station_code,db.station.station)
    return locals()

@action("sales_area/update", method=['POST'])
@action.uses("sales_area/index.html",  flash,session,auth,T,db)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.employee_agent.id == request_id).select().first()
        
    regional_manager=request.forms.get('regional_manager')
    agent=request.forms.get('agent')
    station=request.forms.get('station')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if str(regional_manager)=='' or regional_manager is None:
        errors.append('Enter regional manager') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(agent)=="" or agent is None:
        errors.append('Enter agent') 
    if str(station)=="" or station is None:
        errors.append('Enter station') 
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('sales_area','edit',vars=dict(id=request_id))) 
    
    rm_id=0
    rm_name=''
    if regional_manager:
        rm=str(regional_manager).split('||')
        rm_id=rm[0]
        rm_name=rm[1] 
        
    agent_id=0
    agent_name=''
    if agent:
        ag=str(agent).split('||')
        agent_id=ag[0]
        agent_name=ag[1]  
        
    station_id=0
    station_name=''
    if station:
        st=str(station).split('||')
        station_id=st[0]
        station_name=st[1]  
        
    # insert function
    record.update_record(
        rm_id=rm_id,
        rm_name=rm_name,
        agent_id=agent_id,
        agent_name=agent_name,
        station_id=station_id,
        station_name=station_name,
        status=status
        )        
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('sales_area','index'))  


@action("sales_area/delete")
@action.uses("sales_area/index.html", flash,session,auth,T,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.employee_agent.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('sales_area', 'index')))

    return locals()


@action("sales_area/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('regional_manager') != None and request.query.get('regional_manager') !='':
        conditions += " and e.rm_id = '"+str(request.query.get('regional_manager'))+"'"
        
    if  request.query.get('agent_name') != None and request.query.get('agent_name') !='':
        conditions += " and e.agent_id = '"+str(request.query.get('agent_name'))+"'"
        
    if  request.query.get('station') != None and request.query.get('station') !='':
        conditions += " and e.station_id = '"+str(request.query.get('station'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and e.status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT e.* FROM employee_agent e where 1 "+conditions, as_dict=True))

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
        SELECT e.*,s.def_copy,s.station_code,a.agent_id as agent_code FROM employee_agent e, station s,agent a where e.station_id=s.id and e.agent_id=a.id """+conditions+""" ORDER BY e."""+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)

