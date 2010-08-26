from tilegen_planner import TilePlanner
import tilegen_worker
import sys
import os
from fplan.config.environment import load_environment
from paste.deploy import appconfig

def run_unithread(target_path,tma,zoomlevel=13):
    p=TilePlanner()
    #cachedir tma
    p.init(target_path,tma,zoomlevel)
    tilegen_worker.run(p)

def update_unithread(zoomlevel):
    if os.path.exists("/home/anders/saker/avl_fplan_world/intermediate/"):
        if os.system("rm -rfv /home/anders/saker/avl_fplan_world/intermediate/level*"):
            raise Exception("Couldn't clear dir")
    else:
        if os.system("mkdir -pv /home/anders/saker/avl_fplan_world/intermediate"):
            raise Exception("Couldn't create dir")
    run_unithread("/home/anders/saker/avl_fplan_world/intermediate","1",zoomlevel)
    if os.system("mv -v /home/anders/saker/avl_fplan_world/intermediate/level* /home/anders/saker/avl_fplan_world/tiles/airspace"):
        raise Exception("Couldn't move updated airspace blobs to active dir")

if __name__=='__main__':
    conf = appconfig('config:%s'%(os.path.join(os.getcwd(),"development.ini"),))    
    load_environment(conf.global_conf, conf.local_conf)

    update_unithread(int(sys.argv[1]))

