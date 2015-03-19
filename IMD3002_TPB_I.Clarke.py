# Imports
import maya.cmds as cmds
import random
import math as math
 
 
#                                       #
#    PRIMARY HANDLER FUNCTIONS          #
#                                       #
 
# Normal Square block
def doCloud():
     
    components = []
     
    # Fetching slider data
    cloudDensity = cmds.intSliderGrp('cloudDensity', query=True, value=True)
    cloudLayers = cmds.intSliderGrp('cloudLayers', query=True, value=True)
    particleSize = cmds.intSliderGrp('particleSize', query=True, value=True)
    rgb = cmds.colorSliderGrp('SquareBlockColour', query=True, rgbValue=True) 
     
    cmds.select(clear=True) 
    rnd = random.randrange(0, 5)
      
    currentLayer = cloudLayers
     
    # Constructing spheres
    for i in range(cloudLayers): 
        currentLayer -= 1
        for j in range(0, currentLayer):
            rnd = random.randrange(1, 4) * ( 1/currentLayer )
            rnd2 = random.randrange(1, 5) * 0.3
            rndX = random.randrange(1, 10) * (rnd2 * 1.5)
            rndZ = random.randrange(1, 10) * (rnd2 * 1.5)
            particles = cmds.polySphere(r=0.15 * rnd * particleSize, ch=False) 
            components.append(particles[0])
            cmds.move((i * 1), moveY=True, a=True)
            cmds.move(rndX * ( 4 / cloudDensity), moveX=True, a=True)
            cmds.move(rndZ * ( 4 / cloudDensity), moveZ=True, a=True)
            print currentLayer
             
     
    finalShape =  cmds.polyUnite( components, ch=False)
     
     
    # Adding on the colour
    #shadedShape = addShader(finalShape, rgb)


     
#                                       #
#    SECONDARY RE-USEABLE FUNCTIONS     #
#                                       #
 
# Adds the shader color to object
def addShader(finalShape, rgb):
    myShader = cmds.shadingNode('lambert', asShader=True, name="blockMaterial") 
    cmds.setAttr(myShader + ".color", rgb[0], rgb[1], rgb[2], type='double3')
    cmds.select(finalShape, r=True)
    cmds.hyperShade(assign=myShader)
    cmds.namespace(set=":") 
     


#                    #
#    UI STUFF        #
#                    #

if cmds.window(window, exists=True):
    cmds.deleteUI(window, window=True) 
     
window = cmds.window(title="ACME CloudMaker 5000", menuBar=True, widthHeight=(483, 800)) 
 
# Normal Square block
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Cloud Maker!") 
cmds.columnLayout()
cmds.intSliderGrp('cloudDensity',label="Cloud Density", field=True, min=4, max=30, value=4)
cmds.intSliderGrp('cloudLayers',label="Cloud Layers", field=True, min=2, max=30, value=2)
cmds.intSliderGrp('particleSize',label="Particle Size", field=True, min=2, max=30, value=2)
cmds.colorSliderGrp('SquareBlockColour',label="Colour", hsv=(400, 0, 0.5)) 
cmds.columnLayout()
cmds.button(label="Let's make some fluffies!", command=('doCloud()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

 
# Build the window
cmds.showWindow( window )   