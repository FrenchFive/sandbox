import hou

def crypto(kwargs):
    parent = hou.pwd().parent()
    matnet = hou.node(parent.path()+'/matnet')
    if matnet is None:
        matnet = parent.createNode('matnet','matnet')
    matbuilder = hou.node(matnet.path() + "/crypto")
    if matbuilder is None:
        matbuilder = matnet.createNode('arnold_materialbuilder','crypto')
        for i in range(len(matbuilder.children())):
            matbuilder.children()[i].destroy()
        crypto = matbuilder.createNode('cryptomatte')
        outnode = matbuilder.createNode('arnold_aov')
        outnode.setFirstInput(crypto, output_index=0)
        for i in range(len(matbuilder.children())):
            matbuilder.children()[i].moveToGoodPosition()
    hou.pwd().parm("ar_aov_shaders").set(str(matbuilder.path()))

def atmos(kwargs):
    parent = hou.pwd().parent()
    matnet = hou.node(parent.path()+'/matnet')
    if matnet is None:
        matnet = parent.createNode('matnet','matnet')
    matbuilder = hou.node(matnet.path() + "/atmos")
    if matbuilder is None:
        matbuilder = matnet.createNode('arnold_materialbuilder','atmos')
        for i in range(len(matbuilder.children())):
            matbuilder.children()[i].destroy()
        atmos = matbuilder.createNode('atmosphere_volume')
        atmos.parm("density").set(0.002)
        outnode = matbuilder.createNode('arnold_environment')
        outnode.setFirstInput(atmos, output_index=0)
        for i in range(len(matbuilder.children())):
            matbuilder.children()[i].moveToGoodPosition()
    hou.pwd().parm("ar_environment").set(str(matbuilder.path()))

def fog(kwargs):
    parent = hou.pwd().parent()
    matnet = hou.node(parent.path()+'/matnet')
    if matnet is None:
        matnet = parent.createNode('matnet','matnet')
    matbuilder = hou.node(matnet.path() + "/fog")
    if matbuilder is None:
        matbuilder = matnet.createNode('arnold_materialbuilder','fog')
        for i in range(len(matbuilder.children())):
            matbuilder.children()[i].destroy()
        fog = matbuilder.createNode('fog')
        outnode = matbuilder.createNode('arnold_environment')
        outnode.setFirstInput(fog, output_index=0)
        for i in range(len(matbuilder.children())):
            matbuilder.children()[i].moveToGoodPosition()
    hou.pwd().parm("ar_environment").set(str(matbuilder.path()))