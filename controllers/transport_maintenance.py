from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_cid import date_time_list
import random

@action("transport_maintenance/index")
@action.uses("transport_maintenance/index.html",flash,session,auth,T,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    
    
    
    return locals()

@action("transport_maintenance/create", method=['GET', 'POST'])
@action.uses("transport_maintenance/create.html", flash,session,auth,T,db)
def create(id=None): 
    
    random_number = random.randint(10, 99)
    trans_id=str(date_time_list['currentdate'])+str(random_number)

    stations=db(db.station).select(db.station.id,db.station.station,db.station.station_code)
    paper_list=db(db.paper_list).select(db.paper_list.id,db.paper_list.paper_name)
    reason_list=db(db.unsold_reason.reason_type=='Vehicle').select(db.unsold_reason.id,db.unsold_reason.reason_name)
    return locals()

@action("transport_maintenance/submit", method=['POST'])
@action.uses("transport_maintenance/index.html", session,auth,T)
def submit(id=None): 
    trans_id=request.forms.get('trans_id')
    transaction_date=request.forms.get('transaction_date')
    station=request.forms.get('station')
    paper_list=request.forms.get('paper_list')
    
    
    errors=[]
    if str(trans_id)=='' or trans_id is None:
        errors.append('Enter trans id') 
    else:
        rows_check=db((db.transport_maintenance_head.trans_id==trans_id)).select(db.transport_maintenance_head.trans_id,limitby=(0,1))
        if rows_check:
            errors.append('Transaction id already exist! please refresh the page.')
            
    if str(transaction_date)=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(station)=="" or station is None:
        errors.append('Enter station') 
        
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('transport_maintenance','create')) 
    
    station_id=0
    station_name=''
    if station:
        stations=str(station).split('||')
        station_id=stations[0]
        station_name=stations[1] 
    
    # insert function
    head_id=db.transport_maintenance_head.insert(
        trans_id=trans_id,
        trans_date=transaction_date,
        station_id=station_id,
        station_name=station_name,
        status=1
    )
    
    details_list=[]
    for papers in paper_list:
        paper_id=str(papers).split('||')[0]
        paper_name=str(papers).split('||')[1]
        departure_time=request.forms.get('departure_time_'+str(paper_id))
        arrive_time=request.forms.get('arrive_time_'+str(paper_id))
        reason_of_delay=request.forms.get('reason_of_delay_'+str(paper_id))
        details_list.append({
            'head_id':head_id,
            'trans_id':trans_id,
            'paper_id':paper_id,
            'paper_name':paper_name,
            'departure_time':departure_time,
            'arrive_time':arrive_time,
            'reason_of_delay':reason_of_delay
            })
    db.transport_maintenance_details.bulk_insert(details_list)
        
    flash.set('Record added successfully', 'success')
    redirect(URL('transport_maintenance','index'))   

@action("transport_maintenance/edit", method=['GET', 'POST'])
@action.uses("transport_maintenance/edit.html", flash,session,auth,T,db)
def edit(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.transport_maintenance_head.id == request_id).select().first()
        details_record = db(db.transport_maintenance_details.head_id == request_id).select()
    
    trans_id=record.trans_id
    stations=db(db.station).select(db.station.id,db.station.station,db.station.station_code)
    reason_list=db(db.unsold_reason.reason_type=='Vehicle').select(db.unsold_reason.id,db.unsold_reason.reason_name)
    paper_record=db(db.paper_list).select(db.paper_list.id,db.paper_list.paper_name)
    record_map = {
        int(rec.paper_id): {
            'departure_time': rec.departure_time,
            'arrive_time': rec.arrive_time,
            'reason_of_delay': rec.reason_of_delay
        } for rec in details_record
    }
    
    paper_list = []
    for paper in paper_record:
        paper_list.append({
            'id': paper.id,
            'paper_name': paper.paper_name,
            'departure_time': str(record_map.get(paper.id, {}).get('departure_time', '')),
            'arrive_time': str(record_map.get(paper.id, {}).get('arrive_time', '')),
            'reason_of_delay': str(record_map.get(paper.id, {}).get('reason_of_delay', ''))
        })
        
    return locals()

@action("transport_maintenance/update", method=['POST'])
@action.uses("transport_maintenance/index.html", flash,session,auth,T,db)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.transport_maintenance_head.id == request_id).select().first()
        details_record = db(db.transport_maintenance_details.head_id == request_id).select()
        head_id=record.id
        trans_id=record.trans_id
        
    transaction_date=request.forms.get('transaction_date')
    station=request.forms.get('station')
    paper_list=request.forms.get('paper_list')
    
    
    errors=[]
    if str(transaction_date)=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    # else:
    #     rows_check=db((db.designation.desg_name==desg_name)).select(db.designation.desg_name,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Designation name already exist')
    if str(station)=="" or station is None:
        errors.append('Enter station') 
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('transport_maintenance','edit',vars=dict(id=request_id))) 
    
    station_id=0
    station_name=''
    if station:
        stations=str(station).split('||')
        station_id=stations[0]
        station_name=stations[1]
        
    # insert function
    record.update_record(
        trans_date=transaction_date,
        station_id=station_id,
        station_name=station_name,
        status=1
        )   
    
    details_list=[]
    for papers in paper_list:
        paper_id=str(papers).split('||')[0]
        paper_name=str(papers).split('||')[1]
        departure_time=request.forms.get('departure_time_'+str(paper_id))
        arrive_time=request.forms.get('arrive_time_'+str(paper_id))
        reason_of_delay=request.forms.get('reason_of_delay_'+str(paper_id))
        details_list.append({
            'head_id':head_id,
            'trans_id':trans_id,
            'paper_id':paper_id,
            'paper_name':paper_name,
            'departure_time':departure_time,
            'arrive_time':arrive_time,
            'reason_of_delay':reason_of_delay
            })
    
    db(db.transport_maintenance_details.head_id == head_id).delete()
    
    db.transport_maintenance_details.bulk_insert(details_list)     
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('transport_maintenance','index'))  


@action("transport_maintenance/delete")
@action.uses("transport_maintenance/index.html",flash,session,auth,T,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.transport_maintenance_head.id == request_id).delete()
        db(db.transport_maintenance_details.head_id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('transport_maintenance', 'index')))

    return locals()


@action("transport_maintenance/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('station') != None and request.query.get('station') !='':
        conditions += " and th.station_id = '"+str(request.query.get('station'))+"'"
        
    if  request.query.get('transaction_date') != None and request.query.get('transaction_date') !='':
        conditions += " and th.trans_date = '"+str(request.query.get('transaction_date'))+"'"
        
        
    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and th.status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT th.* FROM transport_maintenance_head th where 1 "+conditions, as_dict=True))

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
        SELECT th.*,s.station_code FROM transport_maintenance_head th left join station s on th.station_id=s.id where 1 """+conditions+""" ORDER BY th."""+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)

