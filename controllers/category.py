from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("category/index")
@action.uses("category/index.html",session,flash,db)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'

    
    return locals()

@action("category/create", method=['GET', 'POST'])
@action.uses("category/create.html", session,auth,T,db,flash)
def create(id=None): 
    return locals()

@action("category/submit", method=['POST'])
@action.uses("category/index.html", session,auth,T,db,flash)
def submit(id=None): 
    category_name=request.forms.get('category_name')
    sat_no_page=request.forms.get('sat_no_page')
    sat_price=request.forms.get('sat_price')
    sun_no_page=request.forms.get('sun_no_page')
    sun_price=request.forms.get('sun_price')
    mon_no_page=request.forms.get('mon_no_page')
    mon_price=request.forms.get('mon_price')
    tue_no_page=request.forms.get('tue_no_page')
    tue_price=request.forms.get('tue_price')
    wed_no_page=request.forms.get('wed_no_page')
    wed_price=request.forms.get('wed_price')
    thu_no_page=request.forms.get('thu_no_page')
    thu_price=request.forms.get('thu_price')
    fri_no_page=request.forms.get('fri_no_page')
    fri_price=request.forms.get('fri_price')
    
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if category_name=='' and category_name is None:
        errors.append('Enter category name') 
    else:
        rows_check=db((db.category.category_name==category_name)).select(db.category.category_name,limitby=(0,1))
        if rows_check:
            errors.append('category name already exist')
    if sat_no_page == '' or sat_no_page is None:
        errors.append('Enter Saturday No Page')
    if sat_price == '' or sat_price is None:
        errors.append('Enter Saturday Price')
    if sun_no_page == '' or sun_no_page is None:
        errors.append('Enter Sunday No Page')
    if sun_price == '' or sun_price is None:
        errors.append('Enter Sunday Price')
    if mon_no_page == '' or mon_no_page is None:
        errors.append('Enter Monday No Page')
    if mon_price == '' or mon_price is None:
        errors.append('Enter Monday Price')
    if tue_no_page == '' or tue_no_page is None:
        errors.append('Enter Tuesday No Page')
    if tue_price == '' or tue_price is None:
        errors.append('Enter Tuesday Price')
    if wed_no_page == '' or wed_no_page is None:
        errors.append('Enter Wednesday No Page')
    if wed_price == '' or wed_price is None:
        errors.append('Enter Wednesday Price')
    if thu_no_page == '' or thu_no_page is None:
        errors.append('Enter Thursday No Page')
    if thu_price == '' or thu_price is None:
        errors.append('Enter Thursday Price')
    if fri_no_page == '' or fri_no_page is None:
        errors.append('Enter Friday No Page')
    if fri_price == '' or fri_price is None:
        errors.append('Enter Friday Price')
        
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('category','create')) 
    # insert function
    db.category.insert(
        category_name=category_name,
        sat_no_page=sat_no_page,
        sat_price=sat_price,
        sun_no_page=sun_no_page,
        sun_price=sun_price,
        mon_no_page=mon_no_page,
        mon_price=mon_price,
        tue_no_page=tue_no_page,
        tue_price=tue_price,
        wed_no_page=wed_no_page,
        wed_price=wed_price,
        thu_no_page=thu_no_page,
        thu_price=thu_price,
        fri_no_page=fri_no_page,
        fri_price=fri_price,
        status=status
    )
        
    flash.set('Record added successfully', 'success')
    redirect(URL('category','index'))   

@action("category/edit", method=['GET', 'POST'])
@action.uses("category/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.category.id == request_id).select().first()
    
    return locals()

@action("category/update", method=['POST'])
@action.uses("category/index.html", session,auth,T,db,flash)
def update(id=None): 
    request_id = request.query.get('id')
    if request_id:
        record = db(db.category.id == request_id).select().first()
        
    category_name=request.forms.get('category_name')
    sat_no_page=request.forms.get('sat_no_page')
    sat_price=request.forms.get('sat_price')
    sun_no_page=request.forms.get('sun_no_page')
    sun_price=request.forms.get('sun_price')
    mon_no_page=request.forms.get('mon_no_page')
    mon_price=request.forms.get('mon_price')
    tue_no_page=request.forms.get('tue_no_page')
    tue_price=request.forms.get('tue_price')
    wed_no_page=request.forms.get('wed_no_page')
    wed_price=request.forms.get('wed_price')
    thu_no_page=request.forms.get('thu_no_page')
    thu_price=request.forms.get('thu_price')
    fri_no_page=request.forms.get('fri_no_page')
    fri_price=request.forms.get('fri_price')
    status=request.forms.get('status')
    
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if category_name=='':
        errors.append('Enter category name') 
    else:
        rows_check=db((db.category.category_name==category_name) & (db.category.id!=request_id)).select(db.category.category_name,limitby=(0,1))
        if rows_check:
            errors.append('Category name already exist')
    if sat_no_page == '' or sat_no_page is None:
        errors.append('Enter Saturday No Page')
    if sat_price == '' or sat_price is None:
        errors.append('Enter Saturday Price')
    if sun_no_page == '' or sun_no_page is None:
        errors.append('Enter Sunday No Page')
    if sun_price == '' or sun_price is None:
        errors.append('Enter Sunday Price')
    if mon_no_page == '' or mon_no_page is None:
        errors.append('Enter Monday No Page')
    if mon_price == '' or mon_price is None:
        errors.append('Enter Monday Price')
    if tue_no_page == '' or tue_no_page is None:
        errors.append('Enter Tuesday No Page')
    if tue_price == '' or tue_price is None:
        errors.append('Enter Tuesday Price')
    if wed_no_page == '' or wed_no_page is None:
        errors.append('Enter Wednesday No Page')
    if wed_price == '' or wed_price is None:
        errors.append('Enter Wednesday Price')
    if thu_no_page == '' or thu_no_page is None:
        errors.append('Enter Thursday No Page')
    if thu_price == '' or thu_price is None:
        errors.append('Enter Thursday Price')
    if fri_no_page == '' or fri_no_page is None:
        errors.append('Enter Friday No Page')
    if fri_price == '' or fri_price is None:
        errors.append('Enter Friday Price')
        
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('category','edit',vars=dict(id=request_id))) 
    
    
    # category log
    old_category = {
        'category_name': record.category_name,
        'sat_no_page': record.sat_no_page,
        'sat_price': record.sat_price,
        'sun_no_page': record.sun_no_page,
        'sun_price': record.sun_price,
        'mon_no_page': record.mon_no_page,
        'mon_price': record.mon_price,
        'tue_no_page': record.tue_no_page,
        'tue_price': record.tue_price,
        'wed_no_page': record.wed_no_page,
        'wed_price': record.wed_price,
        'thu_no_page': record.thu_no_page,
        'thu_price': record.thu_price,
        'fri_no_page': record.fri_no_page,
        'fri_price': record.fri_price,
        'status': record.status
    }
    
    new_category = {
        'category_name': category_name,
        'sat_no_page': sat_no_page,
        'sat_price': sat_price,
        'sun_no_page': sun_no_page,
        'sun_price': sun_price,
        'mon_no_page': mon_no_page,
        'mon_price': mon_price,
        'tue_no_page': tue_no_page,
        'tue_price': tue_price,
        'wed_no_page': wed_no_page,
        'wed_price': wed_price,
        'thu_no_page': thu_no_page,
        'thu_price': thu_price,
        'fri_no_page': fri_no_page,
        'fri_price': fri_price,
        'status': status
    }
    
    # category log
    

    # insert function
    record.update_record(
        category_name=category_name,
        sat_no_page=sat_no_page,
        sat_price=sat_price,
        sun_no_page=sun_no_page,
        sun_price=sun_price,
        mon_no_page=mon_no_page,
        mon_price=mon_price,
        tue_no_page=tue_no_page,
        tue_price=tue_price,
        wed_no_page=wed_no_page,
        wed_price=wed_price,
        thu_no_page=thu_no_page,
        thu_price=thu_price,
        fri_no_page=fri_no_page,
        fri_price=fri_price,
        status=status,
        note=old_category
        ) 
    db.category_log.insert(
        category_name=category_name,
        old_category=old_category,
        new_category=new_category,
    )
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('category','index'))  


@action("category/delete")
@action.uses("category/index.html",session,flash,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    if request_id:
        db(db.category.id == request_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('category', 'index')))

    return locals()


@action("category/get_data", method=['GET', 'POST'])
@action.uses(db)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('name') != None and request.query.get('name') !='':
        conditions += " and id = '"+str(request.query.get('name'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM category where 1 "+conditions, as_dict=True))

    page = int(int(request.query.get('start'))/int(request.query.get('length')) +1 or 1)
    rows_per_page = int(request.query.get('length') or 16)
    if rows_per_page == -1:
        rows_per_page = total_rows
    start = (page - 1) * rows_per_page         
    end = rows_per_page
    #Paginate End##


    #Ordering Start##
    sort_column_index = int(request.query.get('order[0][column]') or 0)
    sort_column_name = request.query.get('columns[' + str(sort_column_index) + '][data]') or 'id'
    sort_direction = request.query.get('order[0][dir]') or 'desc'
    #Ordering End##

    ##Query Start##
    sql = """
    SELECT * FROM category WHERE 1 """ + conditions + """ ORDER BY """ + sort_column_name + """ """ + sort_direction + """ LIMIT """ + str(start) + """, """ + str(end) + """;
    """

    data = db.executesql(sql, as_dict=True)
    
    # Transform data
    transformed_data = []
    for item in data:
        transformed_data.append({
            "category_name": item["category_name"],
            "type_name": "No Pages",
            "sat_value": item["sat_no_page"],
            "sun_value": item["sun_no_page"],
            "mon_value": item["mon_no_page"],
            "tue_value": item["tue_no_page"],
            "wed_value": item["wed_no_page"],
            "thu_value": item["thu_no_page"],
            "fri_value": item["fri_no_page"],
            "status": item["status"],
            "id": item["id"]
        })
        

        transformed_data.append({
            "category_name": item["category_name"],
            "type_name": "Rate (TK)",
            "sat_value": item["sat_price"],
            "sun_value": item["sun_price"],
            "mon_value": item["mon_price"],
            "tue_value": item["tue_price"],
            "wed_value": item["wed_price"],
            "thu_value": item["thu_price"],
            "fri_value": item["fri_price"],
            "status": item["status"],
            "id": item["id"]
        })

    return dict(data=transformed_data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
