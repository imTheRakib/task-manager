# check compatibility
import py4web

assert py4web.check_compatible("0.1.20190709.1")

# by importing db you expose it to the _dashboard/dbadmin
from .models import db

# by importing controllers you expose the actions defined in it
from .controllers import login,default,dashboard,category,page_setup,press_setup,ctp_setup,paper_list,unsold_reason,division,district,police_station,post_office,union,station,route,sub_route,population,designation,employees,agent,sales_area,vehicle,vehicle_route,transport_maintenance,order_entry

# optional parameters
__version__ = "0.0.0"
__author__ = "you <you@example.com>"
__license__ = "anything you want"

# from threading import Timer

# def keep_db_alive():
#     try:
#         db.executesql("SELECT 1")
#     except:
#         db._adapter.close()  # close dead connection
#     Timer(300, keep_db_alive).start()  # ping every 5 minutes

# keep_db_alive()
