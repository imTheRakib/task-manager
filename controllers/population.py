from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("population/index")
@action.uses("population/index.html",session,flash,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'

    
    return locals()

@action("population/create", method=['GET', 'POST'])
@action.uses("population/create.html", flash,session,auth,T,db)
def create(id=None): 
    stations=db(db.station).select(db.station.id,db.station.station,db.station.station_code)
    return locals()

@action("population/submit", method=['POST'])
@action.uses("population/index.html",  flash,session,auth,T,db)
def submit(id=None): 
    station=request.forms.get('station')
    population=request.forms.get('population')
    literacy=request.forms.get('literacy')
    total_subscriber=request.forms.get('total_subscriber')
    reguler_subscriber=request.forms.get('reguler_subscriber')
    floating_subscriber=request.forms.get('floating_subscriber')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if station=='' or station is None:
        errors.append('Enter Station Code')      
    else:
        st_id=0
        st_name=''
        if station:
            stations=str(station).split('||')
            st_id=str(stations[0]).strip()
            st_name=str(stations[1]).strip()
        rows_check=db((db.population.station_id==st_id) ).select(db.population.station_id,limitby=(0,1))
        if rows_check:
            errors.append('Station Population already exist')   
    if population=='' or population is None:
        errors.append('Enter Population')     
    if literacy=='' or literacy is None:
        errors.append('Enter Literacy') 
    if total_subscriber=='' or total_subscriber is None:
        errors.append('Enter Total Subscriber') 
    if reguler_subscriber=='' or reguler_subscriber is None:
        errors.append('Enter Reguler Subscriber') 
    if floating_subscriber=='' or floating_subscriber is None:
        errors.append('Enter Floating Subscriber') 
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('population','create')) 
        
    
    # insert function
    db.population.insert(
        station_id=st_id,
        station_name=st_name,
        population=population,
        literacy=literacy,
        total_subscriber=total_subscriber,
        reguler_subscriber=reguler_subscriber,
        floating_subscriber=floating_subscriber,
        status=status
    )
        
    flash.set('Record added successfully', 'success')
    redirect(URL('population','index'))   

@action("population/edit", method=['GET', 'POST'])
@action.uses("population/edit.html",  flash,session,auth,T,db)
def edit(id=None): 
    request_id = request.query.get('id')
    stations=db(db.station).select(db.station.id,db.station.station,db.station.station_code)

    if request_id:
        record = db(db.population.id == request_id).select().first()
        
    return locals()

@action("population/update", method=['POST'])
@action.uses("population/index.html",  flash,session,auth,T,db)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.population.id == request_id).select().first()
        
    # station=request.forms.get('station')
    population=request.forms.get('population')
    literacy=request.forms.get('literacy')
    total_subscriber=request.forms.get('total_subscriber')
    reguler_subscriber=request.forms.get('reguler_subscriber')
    floating_subscriber=request.forms.get('floating_subscriber')
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    # if station=='' or station is None:
    #     errors.append('Enter Station Code')      
    # else:
    #     st_id=0
    #     st_name=''
    #     if station:
    #         stations=str(station).split('||')
    #         st_id=str(stations[0]).strip()
    #         st_name=str(stations[1]).strip()
    #     rows_check=db((db.population.station_id==st_id) & (db.population.id!=request_id)).select(db.population.station_id,limitby=(0,1))
    #     if rows_check:
    #         errors.append('Station Population already exist')   
    if population=='' or population is None:
        errors.append('Enter Population')     
    if literacy=='' or literacy is None:
        errors.append('Enter Literacy') 
    if total_subscriber=='' or total_subscriber is None:
        errors.append('Enter Total Subscriber') 
    if reguler_subscriber=='' or reguler_subscriber is None:
        errors.append('Enter Reguler Subscriber') 
    if floating_subscriber=='' or floating_subscriber is None:
        errors.append('Enter Floating Subscriber') 
    
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('population','edit',vars=dict(id=request_id))) 
    
    
    # update function
    record.update_record(
        # station_id=st_id,
        # station_name=st_name,
        population=population,
        literacy=literacy,
        total_subscriber=total_subscriber,
        reguler_subscriber=reguler_subscriber,
        floating_subscriber=floating_subscriber,
        status=status
        )  
    
    flash.set('Record updated successfully', 'success')
    redirect(URL('population','index'))  


@action("population/delete")
@action.uses("population/index.html", flash,session,auth,T,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.population.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('population', 'index')))

    return locals()


@action("population/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    
    #Search Start##
    conditions = ""
    
    if  request.query.get('station_name') != None and request.query.get('station_name') !='':
        conditions += " and station_id = '"+str(request.query.get('station_name'))+"'"
        
    

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM population where 1 "+conditions, as_dict=True))

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
    SELECT p.*,s.station_code FROM `population` p,station s where p.station_id=s.id """+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
