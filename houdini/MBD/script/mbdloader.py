import json
import hou
import os

def load(kwargs):
    cleanimport(kwargs)
    cleanlayer(kwargs)
    #RELOADING OLTS
    reload_olts(kwargs)
    #CREATING THE BASICS
    skl = hou.node(hou.pwd().path()+'/GLOBAL_SCALE')
    if skl is None:
        skl = hou.pwd().createNode("null","GLOBAL_SCALE")
    skl.parm('scale').set(1)
    #LOADING STUFF
    seq = hou.pwd().parm('sequence').eval()
    shot = hou.pwd().parm('plan').eval()
    task = hou.pwd().parm('task').eval()
    liseq = ['01','02','03','04','05','06','07']
    lishot = ['010','015','020','025','030','032','035','040','050','060','070','075','080','090','100','110','120','130']
    litask = ['animation','layout','finallayout']
    elements = ["cam","harald","pickup","interior","grenade","flare","mecharm","kiki"]
    if hou.pwd().parm('env').eval() == 1:
        elements.append("enviro")
    #DATA JSON 
    with open("I:/MOBYDICK/tools/publish/v000/script/time.json", "r") as f:
        data = json.load(f)
    search = f"s{liseq[seq]}_p{lishot[shot]}"

    for i in data:
        if i[0] == search:
            hou.pwd().parm("animator").set(f"ANIMATOR : {i[2]} // Frames : {i[1]}")
            fend = int(i[1]) + 1000
            hou.hscript(f"tset `(1001-1)/$FPS` `{fend}/$FPS`")
            hou.setFrame(1001)
            break

    #TEST Mulitple Kiki
    import os
    kikiname = 'kiki_0'
    filenamemult = "mobydick_"+ 's'+liseq[seq] +"_"+ 'p'+lishot[shot] +"_"+ litask[task] +"_main_publish_v000_"+ kikiname +".abc"
    filepathmult = "I:/mobydick/shots/"+ 's'+liseq[seq] +"/"+ 'p'+lishot[shot] +"/"+ litask[task] +"_main/publish/v000/abc/"+ kikiname +"/"+filenamemult
    if os.path.isfile(filepathmult):
        elements.remove("kiki")
        for t in range(8):
            elements.append('kiki_' + str(t))
    columnname = "column_0"
    filenamemult = "mobydick_"+ 's'+liseq[seq] +"_"+ 'p'+lishot[shot] +"_"+ litask[task] +"_main_publish_v000_"+ columnname +".abc"
    filepathmult = "I:/mobydick/shots/"+ 's'+liseq[seq] +"/"+ 'p'+lishot[shot] +"/"+ litask[task] +"_main/publish/v000/abc/"+ columnname +"/"+filenamemult
    if os.path.isfile(filepathmult):
        for t in range(5):
            elements.append('column_' + str(t))


    #LOOP CREATION
    for i in elements:
        if i.startswith("kiki"):
            bname = "kiki"
        elif i == "mecharm":
            bname = "harald"
        elif i.startswith("column"):
            bname = "column"
        else:
            bname = i
        abcimporter(i, bname, 's'+liseq[seq], 'p'+lishot[shot], litask[task], kwargs)
    #LAYER ALL
    rop = hou.node('/out').createNode("arnold",'LAYER_ALL')
    hou.hscript('oppresetload '+rop.path()+' MBD_GEO')
    for child in hou.pwd().children():
        if child.name().startswith("IMPORT") and child.name() != "IMPORT_CAM":
            ropobjects = rop.parm("forceobject").eval()
            ropobjects += child.path() + '/geo '
            rop.parm('forceobject').set(ropobjects)
    rop.parm("camera").set(hou.pwd().path()+"/IMPORT_CAM/RENDER_CAM")
    rop.parm("vobject").set("")
    rop.moveToGoodPosition()
    if rop.parm('forceobject').eval() == '':
        rop.destroy()
    #MOVE TO GOOD POSITION
    for child in hou.pwd().children():
        child.moveToGoodPosition()
    
def abcimporter(object, bname, seq, shot, task, kwargs):
    import os
    name = "IMPORT_" + object.upper()
    filename = "mobydick_"+ seq +"_"+ shot +"_"+ task +"_main_publish_v000_"+ object +".abc"
    filepath = "I:/mobydick/shots/"+ seq +"/"+ shot +"/"+ task +"_main/publish/v000/abc/"+object+"/"+filename
    skl = hou.node(hou.pwd().path()+"/GLOBAL_SCALE")
    if os.path.isfile(filepath) and object != "cam":
        geo = hou.pwd().createNode("geo",name)
        abc = geo.createNode("alembic","ABC_"+object.upper())
        abc.parm("fileName").set(filepath)
        abc.parm("reload").pressButton()
        geo.setFirstInput(skl, output_index=0)
        geo.moveToGoodPosition()

        #TRANSFORM TO SCALE
        xform = geo.createNode('xform','Skale')
        xform.parm('scale').set(0.01)
        toimpletment = 'ch("../../global_scale")'
        xform.setFirstInput(abc , output_index = 0)

        #ADD ARNOLD PROPERTIES
        from htoa.properties import addArnoldProperties
        addArnoldProperties(hou.node(geo.path()))
        #MAT
        if hou.pwd().parm('force_grey').eval() == 0:
            try:
                mathda = geo.createNode("MBD_"+bname.upper()+"_MTL")
            except:
                mathda = geo.createNode("MBD_GREYSHADER_MTL")
        else:
            mathda = geo.createNode("MBD_GREYSHADER_MTL")
        mathda.setFirstInput(xform , output_index = 0)
        #OUTPUT
        output = geo.createNode("null","OUT_"+object.upper())
        output.setFirstInput(mathda , output_index = 0)
        output.setRenderFlag(True)
        output.setDisplayFlag(True)
        #MOVING TO GOOD POSITION
        for child in geo.children():
            child.moveToGoodPosition()
        #ROP
        if hou.pwd().parm('separate_layer').eval() == 1:
            rop = hou.node('/out').createNode('arnold','LAYER_'+object.upper())
            rop.moveToGoodPosition()
            hou.hscript('oppresetload '+rop.path()+' MBD_GEO')
            rop.parm("camera").set(hou.pwd().path()+"/IMPORT_CAM/RENDER_CAM")
            rop.parm("vobject").set("")
            rop.parm("forceobject").set(geo.path())
        
        #SPECIAL
        if object in ["harald","pickup","interior","grenade","flare","mecharm","kiki"]:
            geo.parm('ar_subdiv_type').set("catclark")
            geo.parm('ar_subdiv_iterations').set(2)
            
        if object == "pickup":
            pickuplights(kwargs, False)
        if object == "interior":
            blastInterior = geo.createNode('blast')
            blastSeat = geo.createNode('blast')
            blastSeat.parm('group').set('@path=/coussin/coussinShape,/joystick/pCube1/pCube1Shape,/joystick/pCube2/pCube2Shape,/joystick/pCylinder4/pCylinder4Shape,/joystick/pCylinder13/pCylinder13Shape,/joystick/pCylinder19/pCylinder19Shape,/joystick/polySurface2/polySurface2Shape,/joystick/polySurface6/polySurface6Shape,/joystick/polySurface7/polySurface7Shape,/joystick/triggergeo/triggergeoShape,/pCube55/pCube55Shape,/pCylinder5/pCylinder5Shape,/pCylinder14/pCylinder14Shape,/polySurface639/polySurface639Shape')
            blastInterior.parm('group').set('@path=/coussin/coussinShape,/joystick/pCube1/pCube1Shape,/joystick/pCube2/pCube2Shape,/joystick/pCylinder4/pCylinder4Shape,/joystick/pCylinder13/pCylinder13Shape,/joystick/pCylinder19/pCylinder19Shape,/joystick/polySurface2/polySurface2Shape,/joystick/polySurface6/polySurface6Shape,/joystick/polySurface7/polySurface7Shape,/joystick/triggergeo/triggergeoShape,/pCube55/pCube55Shape,/pCylinder5/pCylinder5Shape,/pCylinder14/pCylinder14Shape,/polySurface639/polySurface639Shape')
            blastInterior.setFirstInput(output, output_index=0)
            blastSeat.setFirstInput(output, output_index=0)
            nullInterior = geo.createNode('null','OUT_INTERIOR')
            nullSeat = geo.createNode('null','OUT_SEAT')
            nullInterior.setFirstInput(blastInterior, output_index=0)
            nullSeat.setFirstInput(blastSeat, output_index=0)
            #SET RENDER FLAG
            nullInterior.setRenderFlag(True)
            nullInterior.setDisplayFlag(True)
        if object == "grenade":
            geo.parm('ar_disp_height').set(0)
        if object == "kiki":
            geo.parm('ar_subdiv_iterations').set(4)
            #RENDER SETTINGS
            geo.parm('ar_disp_height').set(0.01)
        if object == "harald":
            #RENDER SETTINGS
            geo.parm('ar_disp_height').set(0.01)

            output.setName('OUT_HARALD_BASE')
            #SEPERATING HEADS
            heads = geo.createNode('HARALD_HEADS','HARALD_HEADS')
            heads.setFirstInput(output, output_index=0)
            nullhead = geo.createNode('null','HEAD_SIM')
            nullbody = geo.createNode('null', 'BODY_SIM')
            nullhead.setFirstInput(heads, output_index=1)
            nullbody.setFirstInput(heads, output_index=2)
            #SEPERATING EYES AND BODY
            split = geo.createNode('split',"SPLIT")
            split.parm('group').set('@path=*/eyes_GEO/*, ^@path=*/eyes_extra_GEO/*')
            split.parm('negate').set(1)
            split.setFirstInput(heads, output_index=0)
            nullweyes = geo.createNode('null','OUT_HARALD')
            nulleyes = geo.createNode('null','OUT_EYES')
            nullweyes.setInput(0, split, output_index=0)
            nulleyes.setInput(0, split, output_index=1)
            nullweyes.setRenderFlag(True)
            nullweyes.setDisplayFlag(True)
            #REPLACING THINGS
            for child in geo.children():
                child.moveToGoodPosition()
            #HAIR AND EYES
            haraldhair(kwargs, False)
            haraldeyes(kwargs, False)
            #TEST TIME
            rigpath = "I:/MOBYDICK/assets/character/harald/rigging_main/publish/v000/ma/main/mobydick_character_harald_rigging_main_publish_v000_main.ma"
            tmharald = int(os.path.getmtime(filepath))
            tmharaldrig = int(os.path.getmtime(rigpath))  - 7200
            diff = tmharald - tmharaldrig
            print(tmharald)
            print(tmharaldrig)
            print(diff)
            if diff > 0:
                hou.pwd().parm('warningrig').set('')
                hou.pwd().parm('warningheader').set('')
            else:
                hou.pwd().parm('warningheader').set('!!! WARNING !!!')
                hou.pwd().parm('warningrig').set('THE ANIMATION IS OUTDATED')
                
        if object == "flare":
            flarelight(kwargs, False)

    elif os.path.isfile(filepath) and object == "cam":
        #SCALE TRANSFORM
        sklcam = hou.pwd().createNode("null","CAM_SCALE")
        sklcam.parm('scale').set(0.01)
        sklcam.setFirstInput(skl, output_index=0)
        sklcam.setDisplayFlag(False)

        abc = hou.pwd().createNode("alembicarchive",name) 
        abc.parm("fileName").set(filepath)
        abc.parm("buildSubnet").set(0)
        abc.parm("buildSingleGeoNode").set(1)
        abc.parm("buildHierarchy").pressButton()
        skl = hou.node(hou.pwd().path()+"/GLOBAL_SCALE")
        abc.setFirstInput(sklcam, output_index=0)
        abc.moveToGoodPosition()

        for child in abc.children():
            if child.type().name() == "cam":
                child.setName("RENDER_CAM")
        scene_viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        viewport = scene_viewer.curViewport()
        camera_node = hou.node(abc.path() + '/RENDER_CAM')
        viewport.setCamera(camera_node)
    else:
        print("NO FILE FOUND FOR : " + object.upper())

def pickuplights(kwargs, new):
    if new:
        test = False
        for child in hou.pwd().children():
            if child.name().startswith("PICKUP_LIGHTS"):
                test = True
        if test == False:
            hou.pwd().createNode("PICKUP_LIGHTS","PICKUP_LIGHTS")
    else:
        hou.pwd().createNode("PICKUP_LIGHTS","PICKUP_LIGHTS")

def flarelight(kwargs, new):
    if new:
        test = False
        for child in hou.pwd().children():
            if child.name().startswith("FLARE_LIGHT"):
                test = True
    if new == False or test == False:
        hou.pwd().createNode("FLARE_LIGHT","FLARE_LIGHT")

def haraldeyes(kwargs, new):
    if new:
        test = False
        for child in hou.pwd().children():
            if child.name().startswith("HARALD_EYES"):
                test = True
    if new == False or test == False:
        hou.pwd().createNode("HARALD_EYES", "HARALD_EYES")

def haraldhair(kwargs, new):
    if new:
        test = False
        for child in hou.pwd().children():
            if child.name().startswith("HARALD_HAIR"):
                test = True
    if new == False or test == False:
        hou.pwd().createNode("HARALD_HAIR","HARALD_HAIR")

def cleanall(kwargs):
    cleanimport(kwargs)
    cleanlayer(kwargs)
    for child in hou.pwd().children():
        child.moveToGoodPosition()

def cleanimport(kwargs):
    for child in hou.pwd().children():
        print(child.name())
        if child.name() != "GLOBAL_SCALE":
            child.destroy()

def cleanlayer(kwargs):
    for child in hou.node("/out").children():
        if child.name().startswith("LAYER"):
            child.destroy()

def reload_olts(kwargs):
    hda_folder = "I:/MOBYDICK/tools/publish/v000/hda"

    try:
        # Iterate through all files in the folder
        for filename in os.listdir(hda_folder):
            if filename.lower().endswith(".hdanc"):
                hdanc_path = os.path.join(hda_folder, filename)
                hou.hda.installFile(hdanc_path)
                print(f"Reloaded and installed: {hdanc_path}")
    except Exception as e:
        print(f"Error reloading and installing HDANC files: {str(e)}")

