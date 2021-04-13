import time
import httplib
from string import find
import re

# Settings
BRIDGE_LOCAL_IP = "192.168.100.5:8080"
MACHINE_NAME = "MDE01"
MACHINE_SERIAL_NUMBER = "130276"
MACHINE_IP = "192.168.100.210"
FNAME = r"/home/tpsys/log/mhproc/log"

# Init Start Values
CAN_PROCESS = 0
f = open(FNAME, 'r')

def add2str(pr, ne):
    """Helper to concat"""
    return pr + ne

def broadcast_action(action, slot, type, serial, feeder, x, y , yvalid, angle):
    """Make post request to local brigde"""
    conn = httplib.HTTPConnection(BRIDGE_LOCAL_IP)
    params = ''
    params = add2str(params, '?mc_ip='+ MACHINE_IP)
    params = add2str(params, '&mc_name='+ MACHINE_NAME)
    params = add2str(params, '&mc_serial='+ MACHINE_SERIAL_NUMBER)
    params = add2str(params, '&action='+ action)
    params = add2str(params, '&mg_serial='+serial)
    params = add2str(params, '&slot='+ slot)
    params = add2str(params, '&type='+ type)
    params = add2str(params, '&feeder='+ feeder)
    params = add2str(params, '&cl_x='+ x)
    params = add2str(params, '&cl_y='+ y)
    params = add2str(params, '&cl_angle='+ angle)
    print("POSTING:", BRIDGE_LOCAL_IP + "/machine/action" + params)
    conn.request("POST", "/machine/action" + params)


def process_action(line):
    """Process new line (new action)"""
    sline = line.split()
    action = None
    slot = 'NA'
    type = 'NA'
    serial = 'NA'
    feeder = 'NA'
    x = 'NA'
    y = 'NA'
    yvalid = 'NA'
    angle = 'NA'
    if not line:
         return
    if 'TEX' in sline:
         print("tex")
         return
    if find(sline[1], 'MIMHButtonPressed') >= 0:
        action = 'BTN' # Button Pressed
        slot = re.findall(r'\d+', sline[2])[0]
    if find(sline[1], 'MIMHMagRemoved') >= 0:
        action = 'MR' # Magazine Removed
        slot = re.findall(r'\d+', sline[2])[0]
    if find(sline[1], 'insertMag') >=0 :
        action = 'MI' # Magazine Inserted
        info = re.findall(r'\d+', sline[1])
        slot = info[4]
        type = info[3]
        serial = info[2]
    if action:
        broadcast_action(action, slot, type, serial, feeder, x, y , yvalid, angle)



CAN_PROCESS = 0
while 1:
    line = f.readline()
    if not line:
        # Reread all old lines, set flag CAN_PROCESS
        # sleep 1 sec
        CAN_PROCESS = 1
        time.sleep(1)
    else:
        if CAN_PROCESS:
           print("Debug", line.split())
           process_action(line)