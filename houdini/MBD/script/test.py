import json
import hou

def load(kwargs):
    #CREATING THE BASICS
    skl = hou.node(hou.pwd().path()+'/GLOBAL_SCALE')
    if skl is None:
        skl = hou.pwd().createNode("null","GLOBAL_SCALE")
        skl.parm('scale').set(0.01)
    ropnet = hou.node(hou.pwd().path()+'/SCENE_ROP')
    if ropnet is None:
        ropnet = hou.pwd().createNode("ropnet","SCENE_ROP")
        ropnet.moveToGoodPosition()
    #LOADING STUFF
    seq = hou.pwd().parm('sequence').eval()
    shot = hou.pwd().parm('plan').eval()
    task = hou.pwd().parm('task').eval()
    liseq = ['01','02','03','04','05','06']
    lishot = ['010','015','020','025','030','035','040','050','060','070','075','080','090','100','110','120','130']
    litask = ['animation','layout','finallayout']
    elements = ["cam","harald","pickup","interior","grenade","flare","kiki","enviro"]
    #DATA JSON 
    with open("I:/MOBYDICK/tools/publish/v000/script/time.json", "r") as f:
        data = json.load(f)
    search = f"s{liseq[seq]}_p{lishot[shot]}"
    for i in data:
        if i[0] == search:
            hou.pwd().parm("animator").set(f"ANIMATOR : {i[2]}")
            fend = int(i[1]) + 1001
            hou.hscript(f"tset `(1001-1)/$FPS` `{fend}/$FPS`")
            hou.setFrame(1001)
            print(f"The value for {search} is {i[1]} and {i[2]}")
            break
    #LOOP CREATION
    for i in elements:
        abcimporter(i, 's'+liseq[seq], 'p'+lishot[shot], litask[task])
    
def abcimporter(object, seq, shot, task):
    import os
    name = "IMPORT_" + object.upper()
    filename = "mobydick_"+ seq +"_"+ shot +"_"+ task +"_main_publish_v000_"+ object +".abc"
    filepath = "I:/mobydick/shots/"+ seq +"/"+ shot +"/"+ task +"_main/publish/v000/abc/"+object+"/"+filename
    if os.path.isfile(filepath): 
        abc = hou.pwd().createNode("alembicarchive",name) 
        abc.parm("fileName").set(filepath)
        abc.parm("buildSubnet").set(0)
        abc.parm("buildSingleGeoNode").set(1)
        abc.parm("buildHierarchy").pressButton()
        skl = hou.node(hou.pwd().path()+"/GLOBAL_SCALE")
        abc.setFirstInput(skl, output_index=0)
        abc.moveToGoodPosition()
        if (object == "cam"):
            for child in abc.children():
                if child.type().name() == "cam":
                    child.setName("RENDER_CAM")
        else:
            #OUTPUT
            albcnode = hou.node(abc.path() +"/geo/alembic")
            output = hou.node(abc.path() +"/geo").createNode("null","OUT_"+object.upper())
            output.setFirstInput(albcnode , output_index = 0)
            output.moveToGoodPosition()
            output.setRenderFlag(True)
            output.setDisplayFlag(True)
            #ROP
            rop = hou.node(hou.pwd().path() + '/SCENE_ROP').createNode('arnold','LAYER_'+object.upper())
            rop.moveToGoodPosition()
            hou.hscript('oppresetload '+rop.path()+' MBD_GEO')
            rop.parm("camera").set("/obj/MBD_SCENE/IMPORT_CAMV2/RENDER_CAM")
            rop.parm("vobject").set("")
            rop.parm("forceobject").set(abc.path()+'/geo')
    else:
        print("NO FILE FOUND FOR : " + object.upper())