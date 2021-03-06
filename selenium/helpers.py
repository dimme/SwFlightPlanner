import re
import time
from settings import create_sel

def login(sel):
    """
    Go to splash-screen, and then login as 'selenium'.
    """
    sel.open("/")
    sel.type("username", "selenium")
    sel.type("password", "selenium")
    sel.click("login")
    sel.wait_for_page_to_load("30000")
    bt=sel.get_body_text()    
    assert re.search(ur".*Search Destination.*", bt)
    
def open_trip(sel,tripname):
    sel.click("//button[@onclick='more_trip_functions();return false;']")
    sel.click("//button[@onclick='open_trip();return false;']")
    sel.select("choose_trip",tripname)
    sel.click("//button[@onclick='on_open_trip();return false;']")
    sel.wait_for_page_to_load("30000")


def list_other_trips(sel):
    sel.click("//button[@onclick='more_trip_functions();return false;']")
    sel.click("//button[@onclick='open_trip();return false;']")
    if not sel.is_element_present("choose_trip"):
        return []
    return list(sel.get_select_options("choose_trip"))
def get_cur_trip(sel):
    return sel.get_value("entertripname")

def add_trip(sel,tripname):    
    """
    Add a new trip.
    Precondition: Browser must be pointing at mapview screen.
    """
    sel.click("//button[@onclick='more_trip_functions();return false;']")
    sel.click("//button[@onclick='open_trip();return false;']")
    sel.click("//button[@onclick='add_new_trip();return false;']")
    sel.type("addtripname", tripname)
    sel.click("//button[@onclick='on_add_trip();return false;']")
    sel.wait_for_page_to_load("30000")
def delete_cur_trip(sel):
    """
    Precondition: Trip which is to be deleted must be active.
                  Current screen must be mapview.
    """
    sel.click("//button[@onclick='more_trip_functions();return false;']")
    sel.click("//button[@onclick='open_trip();return false;']")
    sel.click("//button[@onclick='more_trip_functions();return false;']")
    sel.click("//button[@onclick='on_delete_trip();return false;']")
    sel.wait_for_page_to_load("30000")

def add_named_wp(sel,name):
    """
    Precondition: Must be at mapview-screen.
    """
    sel.type("searchfield", name[:-1])
    sel.type_keys("searchfield", name[-1])
    for i in range(60):
        try:
            if sel.is_visible("searchpopup"): break
        except Exception: pass
        time.sleep(0.1)
    else: raise Exception("time out")
    for i in range(60):
        try:
            if not sel.is_visible("searchprogtext"): break
        except Exception: pass
        time.sleep(0.1)
    else: raise Exception("time out")
    sel.click("//p[@onclick='search_select(0)']")


def wait_not_visible(sel,what):
    for i in range(60):
        try:
            if not sel.is_visible(what): break
        except Exception: pass
        time.sleep(0.1)
    else: self.fail("time out")
def wait_visible(sel,what):
    for i in range(60):
        try:
            if sel.is_visible(what): break
        except Exception: pass
        time.sleep(0.1)
    else: self.fail("time out")

class selconn:
    def __enter__(self):
        self.sel = create_sel()
        self.sel.start()
        self.sel.window_maximize()
        self.sel.open("/")        
        return self.sel
    def __exit__(self, type, value, traceback):
        if type:
            print type,value,traceback
            print "Press enter to clean up"
            raw_input()
        self.sel.stop()
        
class temporary_trip:
    def __init__(self,temptrip):
        self.temptrip=temptrip
        
    def __enter__(self):
        self.sel = create_sel()
        self.sel.start()
        self.sel.window_maximize()
    
        login(self.sel)
        
        self.sel.open("/mapview/index")
        self.sel.wait_for_page_to_load("10000")
        
        if self.temptrip in list_other_trips(self.sel):
            open_trip(self.sel,self.temptrip)
            delete_cur_trip(self.sel)
        prevtrip=get_cur_trip(self.sel)    
        if prevtrip==self.temptrip:
            delete_cur_trip(self.sel)
        print "prev trip:",prevtrip
        add_trip(self.sel,self.temptrip)
        actcurtrip=get_cur_trip(self.sel)
        print "Actual curtrip:",actcurtrip
        assert actcurtrip==self.temptrip
        return self.sel
    def __exit__(self, type, value, traceback):
        if not traceback:
            self.sel.stop()
            