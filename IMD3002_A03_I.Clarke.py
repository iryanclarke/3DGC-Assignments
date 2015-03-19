# Imports
import maya.cmds as cmds
import random
import math as math
 
 
#                                       #
#    PRIMARY HANDLER FUNCTIONS          #
#                                       #
 
# Normal Square block
def SquareBlock():
     
    components = []
     
    # Fetching slider data
    blockDepth = cmds.intSliderGrp('SquareBlockDepth', query=True, value=True)
    blockWidth = cmds.intSliderGrp('SquareBlockWidth', query=True, value=True)
    rgb = cmds.colorSliderGrp('SquareBlockColour', query=True, rgbValue=True) 
     
    cmds.select(clear=True) 
     
    # Set to the lego size presets
    cubeDimX = blockWidth * 0.8
    blockHeight = 1
    cubeDimY = blockHeight * 0.32
    cubeDimZ = blockDepth * 0.8
     
    cube = cmds.polyCube(h=cubeDimY, w=cubeDimX, d=cubeDimZ, ch=False) 
    cmds.move((cubeDimY/2.0), moveY=True) 
     
    # Constructing the bumps
    for i in range(blockWidth): 
        for j in range(blockDepth):
            topBump = cmds.polyCylinder(r=0.25, h=0.20, ch=False) 
            components.append(topBump[0])
            cmds.move((cubeDimY + 0.10), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeDimX/2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (cubeDimZ/2.0) + 0.4), moveZ=True, a=True)
             
     
    finalShape =  cmds.polyUnite( cube[0], components, ch=False)
     
     
    # Adding on the colour
    shadedShape = addShader(finalShape, rgb)
     
# Square block with holes
def HoleBlock():
     
    # Initialize the building blocks and the subtraction blocks
    components = []
    subtracts = []
     
    # Fetching slider data
    blockDepth = cmds.intSliderGrp('HoleblockDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('HoleblockColour', query=True, rgbValue=True) 
     
    cmds.select(clear=True) 
       
    blockWidth = 1
    cubeDimX = blockWidth * 0.8
    blockHeight = 1
    cubeDimY = blockHeight * 0.96
    cubeDimZ = blockDepth * 0.8
 
    cube = cmds.polyCube(h=cubeDimY, w=cubeDimX, d=cubeDimZ, sz=blockDepth, ch=False) 
    cmds.move((cubeDimY/2.0), moveY=True) 
   
     
    # Pipes on top of block
    for i in range(blockDepth):
        components.append(cmds.polyPipe(r=0.24, h=0.36, thickness=0.09, ch=False)[0]) 
        cmds.move((cubeDimY + 0.10), moveY=True, a=True)
        cmds.move(((i * 0.8) - (cubeDimZ/2.0) + 0.4), moveZ=True, a=True)
     
    # Holes within block
    for k in range(blockDepth - 1):   
        holes = cmds.polyCylinder( h=1, r=0.24, ax=(1,0,0), ch=False)
        subtracts.append(holes[0]);
        cmds.move( 0, cubeDimY - 0.38, ((k*0.8) - (cubeDimZ/2.0) + 0.8), holes[0], a=True)         
   
    # Unite the cube and the top
    addShape = cmds.polyUnite(cube, components, ch=False)
     
    currentHole = subtracts[0]
    
    # Unite all of the holes for a boolean subtraction 
    for hole in range(len(subtracts)- 1):
        uniteHole = cmds.polyUnite(currentHole, subtracts[hole+1], ch=False)
        currentHole = uniteHole
         
    finalShape = cmds.polyCBoolOp(addShape, currentHole, op=2, ch=False)[0]
     
    # Adding on the colour
    shadedShape = addShader(finalShape, rgb) 
 
# Rounded/Bent blocks
def RoundBlock():
     
    # Fetching slider data
    blockDepth = cmds.intSliderGrp('RoblockDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('RoblockColour', query=True, rgbValue=True) 
     
    cmds.select(clear=True) 
    
    # Use re-useable function to make curved beam 
    finalShape = makeRoundHoleBlock(blockDepth)
     
    # Adding on the colour
    shadedShape = addShader(finalShape, rgb)
     
# Angled blocks
def AngledBlock():
    components = []
     
    # Fetching slider data
    firstBlockDepth = cmds.intSliderGrp('firstDepth', query=True, value=True)
    secondBlockDepth = cmds.intSliderGrp('secondDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('angledBlockColour', query=True, rgbValue=True) 
     
    cmds.select(clear=True) 
     
    cubeDimZ = (firstBlockDepth * 0.8) - (firstBlockDepth*0.8/firstBlockDepth)
    cubeDimZ2 = (secondBlockDepth * 0.8) - (secondBlockDepth*0.8/secondBlockDepth)
     
    height = (cubeDimZ2/2.0) * (math.sin(0.7853))
     
    # Use re-useable function to make curved beam  
    firstBlock = makeRoundHoleBlock(firstBlockDepth)
    components.append(firstBlock[0])
    secondBlock = makeRoundHoleBlock(secondBlockDepth)
    components.append(secondBlock[0])
    translation = 0
    if(cubeDimZ > cubeDimZ2):
        translation = (cubeDimZ/2.0) - (cubeDimZ2/2.0)
        cmds.move(translation, moveZ=True, a=True)
        cmds.rotate(135, 0, 0, secondBlock[0], pivot=(0, 0.78/2, cubeDimZ2/2.0 + translation) )
    if(cubeDimZ < cubeDimZ2):
        translation = (cubeDimZ/2.0) - (cubeDimZ2/2.0)
        cmds.move(translation, moveZ=True, a=True)
        cmds.rotate(135, 0, 0, secondBlock[0], pivot=(0, 0.78/2, cubeDimZ2/2.0 + translation) ) 
    if(cubeDimZ == cubeDimZ2):    
        cmds.rotate(135, 0, 0, secondBlock[0], pivot=(0, 0.78/2, cubeDimZ2/2.0) )
     
    finalShape = cmds.polyUnite(components, ch=False)
     
    # Adding on the colour
    shadedShape = addShader(finalShape, rgb)
     
# Right Angle blocks
def RightBlock():
    components = []
     
    # Fetching slider data
    firstBlockDepth = cmds.intSliderGrp('firstAngleDepth', query=True, value=True)
    secondBlockDepth = cmds.intSliderGrp('secondAngleDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('angled90BlockColour', query=True, rgbValue=True) 
     
    cmds.select(clear=True) 
     
    cubeDimY = 1 * 0.96
    cubeDimZ = (firstBlockDepth * 0.8) - (firstBlockDepth*0.8/firstBlockDepth)
    cubeDimZ2 = (secondBlockDepth * 0.8) - (secondBlockDepth*0.8/secondBlockDepth)
    
    # Use re-useable function to make curved beam   
    firstBlock = makeRoundHoleBlock(firstBlockDepth)
    components.append(firstBlock[0])
    secondBlock = makeRoundHoleBlock(secondBlockDepth)
    components.append(secondBlock[0])
    
    # Move the length of the first one divided by two, and translate up the length of the second divided by two
    cmds.move((cubeDimZ/2.0), moveZ=True, a=True) 
    cmds.move((cubeDimZ2/2.0), moveY=True, a=True) 
    cmds.rotate(90, 0, 0, secondBlock[0])
    
    finalShape = cmds.polyUnite(components, ch=False)
     
    # Adding on the colour
    shadedShape = addShader(finalShape, rgb)       
 
# Pneumatics
def pneumatic():
    components = []
     
    # Fetching slider data
    rgb = cmds.colorSliderGrp('pneuColour', query=True, rgbValue=True) 
      
    cmds.select(clear=True) 
      
    cube = cmds.polyCube(h=0.3, w=0.3, d=0.2, ch=False) 
    cyl1 = cmds.polyCylinder(r=0.15, h=1.0, ax=(0,0,1), ch=False)
    cmds.move(0,0,0.6)
    components.append(cyl1[0])
    cyl2 = cmds.polyCylinder(r=0.05, h=0.8, ax=(0,0,1), ch=False)
    cmds.move(0,0,1.5)
    components.append(cyl2[0])
    pipe = cmds.polyPipe(r=0.08, t=0.02, h=0.3, ax=(1,0,0), ch=False)
    cmds.move(0,0,1.96)
    components.append(pipe[0])
     
    finalShape =  cmds.polyUnite( cube[0], components, ch=False)
     
    # Adding on the color
    shadedShape = addShader(finalShape, rgb) 
 
# Axels
def Axel():
     
    # Fetching slider data 
    AxelDepth = cmds.intSliderGrp('AxelDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('AxelColour', query=True, rgbValue=True) 
      
    cmds.select(clear=True) 
         
    cube1 = cmds.polyCube(d=AxelDepth, w=0.2, h=0.1, ch=False)
    cube2 = cmds.polyCube(d=AxelDepth, w=0.1, h=0.2, ch=False)
     
    finalShape =  cmds.polyUnite( cube1[0], cube2[0], ch=False)
      
    # Adding on the color
    shadedShape = addShader(finalShape, rgb)
 
# Wheels
def Wheel():
     
    # Fetching slider data 
    rgb = cmds.colorSliderGrp('WheelColour', query=True, rgbValue=True)  
     
    cmds.select(clear=True) 
      
    wheelHeight = 2
    wheelRadius = 1.5
    wheelThickness = 0.9
    finalShape = cmds.polyPipe(h=wheelHeight, r=wheelRadius, t=wheelThickness, ax=(0,0,1)) 
    cmds.polyExtrudeFacet('.f[40:59]', kft=False, ltz=0.2, ls=(1, 1, 1), ch=False)
    cmds.polyExtrudeFacet('.f[20:39]', kft=False, ltz=0.2, ls=(1, 1, 1), ch=False)
    cmds.polyExtrudeFacet('.f[60:79]', kft=False, ltz=0.2, ls=(1, 1, 1), ch=False)
    cmds.polyExtrudeFacet('.f[0:19]', kft=False, ltz=0.3, ls=(1, 1, 1), ch=False)
     
      
    # Adding on the color
    shadedShape = addShader(finalShape, rgb)
     
# Hole Connector
def HoleConnector():
     
    components = []
    
    # Fetching slider data 
    rgb = cmds.colorSliderGrp('HoleColour', query=True, rgbValue=True) 
      
    cmds.select(clear=True) 
     
    cubeDimX = 0.74
    cubeDimY = 0.78
     
    # Inner tube    
    innerCyl = cmds.polyPipe( r=cubeDimY * 0.40, h=cubeDimX*3.85, t=0.1, ax=(1,0,0), ch=False )
     
    # End Ring
    endCyl1 = cmds.polyPipe( r=cubeDimY * 0.45, h=cubeDimX*0.1, t=0.05, ax=(1,0,0), ch=False )
    cmds.move(cubeDimX*1 - (cubeDimX*0.05),0,0)
     
    midShape =  cmds.polyCBoolOp( innerCyl[0], endCyl1[0] , op=1, ch=False)
     
    # Subtraction cube
    endCube1 = cmds.polyCube(width=0.5, height=0.09, depth=1, ch=False)
    cmds.move(cubeDimX*1 - (cubeDimX*0.15),0,0)
     
    midShape = cmds.polyCBoolOp( midShape[0], endCube1[0], op=2, ch=False )
     
    # End Ring 2
    endCyl2 = cmds.polyPipe( r=cubeDimY * 0.45, h=cubeDimX*0.1, t=0.05, ax=(1,0,0), ch=False )
    cmds.move((cubeDimX*0.05) - cubeDimX*1,0,0)
     
    midShape =  cmds.polyCBoolOp( midShape[0], endCyl2[0] , op=1, ch=False)
     
    # Subtraction cube 2
    endCube2 = cmds.polyCube(width=0.5, height=0.09, depth=1, ch=False)
    cmds.move((cubeDimX*0.15) - cubeDimX*1,0,0)
     
    midShape = cmds.polyCBoolOp( midShape[0], endCube2[0], op=2, ch=False )
     
    outerCyl1 = cmds.polyPipe( r=cubeDimY * 0.45, h=cubeDimX*0.2, t=0.05, ax=(1,0,0),ch=False )
     
     
    finalShape =  cmds.polyCBoolOp( midShape[0], outerCyl1[0], op=1, ch=False )
     
    # Adding on the color
    shadedShape = addShader(finalShape, rgb)    
     
     
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
     
# Punches holes into the technic block        
def makeBeamHole( block, z, cubeDimX, cubeDimY, cubeDimZ ):
    hole = cmds.polyCylinder( r=cubeDimY * 0.45, h=cubeDimX, ax=(1,0,0), ch=False )
    cmds.move( (z * 0.8) - (cubeDimZ/2.0), moveZ= True, a=True)  
    cmds.move( (cubeDimY * 0.5), moveY= True, a=True) 
    block =  cmds.polyCBoolOp( block[0], hole[0], op=2, ch=False )
    return block

# Adds in pipes from beam block to create more complexity 
def makeBeamPipe( block, x, cubeDimX, cubeDimY, cubeDimZ ):
    innerPipe = cmds.polyPipe( r=cubeDimY * 0.5, h=cubeDimX*2, t=0.05, ax=(1,0,0) )
    innerAdd = cmds.polyPipe( r=cubeDimY * 0.45, h=cubeDimX*1.64, t=0.1, ax=(1,0,0) )
    inner = cmds.polyCBoolOp( innerPipe[0], innerAdd[0], op=1, ch=False )
    cmds.move( (x*0.8) - (cubeDimZ/2.0), moveZ= True, a=True)  
    cmds.move( (cubeDimY * 0.5), moveY= True, a=True) 
    block =  cmds.polyCBoolOp( block[0], inner[0], op=1, ch=False )
    return block    

# Makes a standard rounded block with holes 
def makeRoundHoleBlock(blockDepth):
       
    cubeDimX = 0.74
    cubeDimY = 0.78
    cubeDimZ = (blockDepth * 0.8) - (blockDepth*0.8/blockDepth)
     
    # Make Block
    block = cmds.polyCube(width=cubeDimX, height=cubeDimY, depth=cubeDimZ, ch=False)
    cmds.move((cubeDimY/2.0), moveY=True) 
     
    # Make left endcap
    endCap = cmds.polyCylinder(r=cubeDimY * 0.5, h=cubeDimX, ax=(1,0,0), ch=False )
    cmds.move( (cubeDimZ * 0.5), moveZ=True, a=True)
    cmds.move( (cubeDimY * 0.5), moveY=True, a=True)
    block = cmds.polyCBoolOp( block[0], endCap[0], op=1, ch=False )
     
    # Make right endcap
    endCap = cmds.polyCylinder(r=cubeDimY * 0.5, h=cubeDimX, ax=(1,0,0), ch=False )
    cmds.move( (cubeDimZ * -0.5), moveZ=True, a=True)
    cmds.move( (cubeDimY * 0.5), moveY=True, a=True)
    block = cmds.polyCBoolOp( block[0], endCap[0], op=1, ch=False )
 
    cmds.xform(centerPivots = True )
     
    for z in range(blockDepth):
        block = makeBeamHole( block, z , cubeDimX, cubeDimY, cubeDimZ )
        block = makeBeamPipe( block, z , cubeDimX, cubeDimY, cubeDimZ )
     
    return block
 

#                         #
#    GUI CREATION         #
#                         #
     
window = cmds.window(title="Lego Blocks", menuBar=True, widthHeight=(483, 800)) 
 
# Normal Square block
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Square Block") 
cmds.columnLayout()
cmds.intSliderGrp('SquareBlockDepth',label="Depth", field=True, min=4, max=30, value=4)
cmds.intSliderGrp('SquareBlockWidth',label="Width", field=True, min=2, max=30, value=2)
cmds.colorSliderGrp('SquareBlockColour',label="Colour", hsv=(400, 0, 0.5)) 
cmds.columnLayout()
cmds.button(label="Create Square Block", command=('SquareBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Square block with holes
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Square Block With Holes", collapse=True) 
cmds.columnLayout()
cmds.intSliderGrp('HoleblockDepth',label="Bumps", field=True, min=2, max=10, value=4)
cmds.colorSliderGrp('HoleblockColour',label="Colour", hsv=(350, 1, 1)) 
cmds.columnLayout()
cmds.button(label="Create Square Block", command=('HoleBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Rounded/Bent blocks
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Rounded Blocks", collapse=True) 
cmds.columnLayout()
cmds.intSliderGrp('RoblockDepth',label="Length", field=True, min=4, max=30, value=5)
cmds.colorSliderGrp('RoblockColour',label="Colour", hsv=(56, 1, 1)) 
cmds.columnLayout()
cmds.button(label="Create Rounded Block", command=('RoundBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Angled Blocks
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Angled block", collapse=True) 
cmds.columnLayout()
cmds.intSliderGrp('firstDepth',label="First Block Length", field=True, min=4, max=20, value=5)
cmds.intSliderGrp('secondDepth',label="Second Block Length", field=True, min=4, max=20, value=5)
cmds.colorSliderGrp('angledBlockColour',label="Colour", hsv=(56, 1, 1)) 
cmds.columnLayout()
cmds.button(label="Create angled block", command=('AngledBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Right Angled Blocks
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="90 degree block", collapse=True) 
cmds.columnLayout()
cmds.intSliderGrp('firstAngleDepth',label="First Block Length", field=True, min=4, max=20, value=5)
cmds.intSliderGrp('secondAngleDepth',label="Second Block Length", field=True, min=4, max=20, value=5)
cmds.colorSliderGrp('angled90BlockColour',label="Colour", hsv=(56, 1, 1)) 
cmds.columnLayout()
cmds.button(label="Create angled block", command=('RightBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Pneumatics
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Pneumatics", collapse=True) 
cmds.columnLayout()
cmds.colorSliderGrp('pneuColour',label="Colour", hsv=(0, 0, 0.1)) 
cmds.columnLayout()
cmds.button(label="Create Pneumatic", command=('pneumatic()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Wheel
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Wheels", collapse=True) 
cmds.columnLayout()
cmds.colorSliderGrp('WheelColour',label="Colour", hsv=(0, 0, 0.1)) 
cmds.columnLayout()
cmds.button(label="Create Wheel", command=('Wheel()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Axels
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Axels", collapse=True) 
cmds.columnLayout()
cmds.intSliderGrp('AxelDepth',label="Axel Length", field=True, min=2, max=10, value=5)
cmds.colorSliderGrp('AxelColour',label="Colour", hsv=(0, 0, 0.1)) 
cmds.columnLayout()
cmds.button(label="Create Axel", command=('Axel()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Hole connector
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Hole Connector", collapse=True) 
cmds.columnLayout()
cmds.colorSliderGrp('HoleColour',label="Colour", hsv=(0, 0, 0.1)) 
cmds.columnLayout()
cmds.button(label="Create Hole Connector", command=('HoleConnector()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )
 
# Build the window
cmds.showWindow( window )   