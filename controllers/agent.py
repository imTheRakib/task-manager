from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("agent/index")
@action.uses("agent/index.html",session,flash,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    
    
    return locals()

@action("agent/create", method=['GET', 'POST'])
@action.uses("agent/create.html", session,auth,T,db,flash)
def create(id=None): 
    last_agent = db.agent.agent_id.max()
    last_agent = db().select(last_agent).first()[last_agent]
    if last_agent:
        agent_id = int(last_agent) + 1
    else:
        agent_id = 200001
    
    sub_routes=db(db.sub_route).select(db.sub_route.id,db.sub_route.sub_route_code,db.sub_route.sub_route_name)

    return locals()

@action("agent/submit", method=['POST'])
@action.uses("agent/index.html", session,auth,T,db,flash)
def submit(id=None): 
    agent_id=request.forms.get('agent_id')
    agent_name=request.forms.get('agent_name')
    agent_bangla=request.forms.get('agent_bangla')
    mobile=request.forms.get('mobile')
    sorting_order=request.forms.get('sorting_order')
    sub_route=request.forms.get('sub_route')
    billing_accpac_code=request.forms.get('billing_accpac_code')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if str(agent_name)=='' or agent_name is None:
        errors.append('Enter Agent name') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(sub_route)=="" or sub_route is None:
        errors.append('Enter Agent Area') 
    if str(billing_accpac_code)=="" or billing_accpac_code is None:
        errors.append('Enter Billing Agent') 
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('agent','create')) 
        
    sub_route_id=0
    sub_route_name=''
    if sub_route:
        sub_routes=str(sub_route).split('||')
        sub_route_id=sub_routes[0]
        sub_route_name=sub_routes[1]  
    
    
    # insert function
    db.agent.insert(
        agent_id=agent_id,
        agent_name=agent_name,
        agent_bangla=agent_bangla,
        mobile=mobile,
        sorting_order=sorting_order,
        sub_route_id=sub_route_id,
        sub_route_name=sub_route_name,
        billing_accpac_code=billing_accpac_code,
        status=status
    )
        
    flash.set('Record added successfully', 'success')
    redirect(URL('agent','index'))   

@action("agent/edit", method=['GET', 'POST'])
@action.uses("agent/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.agent.id == request_id).select().first()
    sub_routes=db(db.sub_route).select(db.sub_route.id,db.sub_route.sub_route_code,db.sub_route.sub_route_name)
    return locals()

@action("agent/update", method=['POST'])
@action.uses("agent/index.html", session,auth,T,db,flash)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.agent.id == request_id).select().first()
        
    agent_id=request.forms.get('agent_id')
    agent_name=request.forms.get('agent_name')
    agent_bangla=request.forms.get('agent_bangla')
    mobile=request.forms.get('mobile')
    sorting_order=request.forms.get('sorting_order')
    sub_route=request.forms.get('sub_route')
    billing_accpac_code=request.forms.get('billing_accpac_code')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if str(agent_name)=='' or agent_name is None:
        errors.append('Enter Agent name') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(sub_route)=="" or sub_route is None:
        errors.append('Enter Agent Area') 
    if str(billing_accpac_code)=="" or billing_accpac_code is None:
        errors.append('Enter Billing Agent') 
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('agent','edit',vars=dict(id=request_id))) 
    
    sub_route_id=0
    sub_route_name=''
    if sub_route:
        sub_routes=str(sub_route).split('||')
        sub_route_id=sub_routes[0]
        sub_route_name=sub_routes[1]  
        
    # insert function
    record.update_record(
        agent_id=agent_id,
        agent_name=agent_name,
        agent_bangla=agent_bangla,
        mobile=mobile,
        sorting_order=sorting_order,
        sub_route_id=sub_route_id,
        sub_route_name=sub_route_name,
        billing_accpac_code=billing_accpac_code,
        status=status
        )        
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('agent','index'))  


@action("agent/delete")
@action.uses("agent/index.html",session,flash,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.agent.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('agent', 'index')))

    return locals()


@action("agents/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('agent_name') != None and request.query.get('agent_name') !='':
        conditions += " and id = '"+str(request.query.get('agent_name'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM agent where 1 "+conditions, as_dict=True))

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
        SELECT * FROM agent where 1 """+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)



@action("agent/drop_point", method=['GET', 'POST'])
@action.uses("agent/drop_point.html", session,auth,T,db,flash)
def drop_point(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.agent.id == request_id).select().first()
        agent_id=record.id
    return locals()

@action("agent/sales_info", method=['GET', 'POST'])
@action.uses("agent/sales_info.html", session,auth,T,db,flash)
def sales_info(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.agent.id == request_id).select().first()
        papers= db(db.paper_list).select()
        agent_sales_infos= db(db.agent_sales_info.agent_id==record.id).select()
        record_map = {int(rec.paper_id): rec.quantity for rec in agent_sales_infos}
        paper_list = []
        for paper in papers:
            paper_list.append({
            'id': paper.id,
            'paper_name': paper.paper_name,
            'quantity': record_map.get(paper.id, '0')  # Get default_time or empty string if not found
            }) 
    return locals()

@action("agent/sales_info_save", method=['POST'])
@action.uses("agent/index.html", session,auth,T,db,flash)
def sales_info_save(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.agent.id == request_id).select().first()
        
    agent_code=request.forms.get('agent_id')
    agent_name=request.forms.get('agent_name')
    paper_lists=request.forms.get('paper_name')
    agent_id=record.id
    
    # paper_id=0
    # paper_name=''
    # if paper_lists:
    #     paper_list=str(paper_lists).split('||')
    #     paper_id=paper_list[0]
    #     paper_name=paper_list[1]
    
    quantity=""
    for paper in paper_lists:
        papers = paper.split('||')
        quantity = request.forms.get('quantity_'+papers[0])
        paper_dict = {
            'agent_id': agent_id,
            'agent_name': agent_name,
            "paper_id": papers[0],
            "paper_name": papers[1],
            "quantity": quantity
        }
        db.agent_sales_info.update_or_insert(
            (db.agent_sales_info.agent_id == agent_id) & (db.agent_sales_info.paper_id == papers[0]),
            **paper_dict
        )
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('agent','index')) 
