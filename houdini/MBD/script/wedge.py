import hou
import os

def path(kwargs):
    if hou.pwd().parm("pathtype").eval()==0:
        hou.pwd().parm("path").set('$HIP/WEDGE/`padzero(2,chs("version"))`') 
    elif hou.pwd().parm("pathtype").eval()==1:
        hou.pwd().parm("path").set('D:/WEDGE/`padzero(2,chs("version"))`')
    elif hou.pwd().parm("pathtype").eval()==2:
        hou.pwd().parm("path").set('I:/MOBYDICK/tools/publish/v000/PDG_WORK/$HIPNAME/WEDGE/`padzero(2,chs("version"))`')