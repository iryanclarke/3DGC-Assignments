# Imports
import maya.cmds as cmds
import random


#                                       #
#    PRIMARY HANDLER FUNCTIONS          #
#                                       #

# Normal Square block
def SquareBlock():
    
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
    
    cmds.polyCube(h=cubeDimY, w=cubeDimX, d=cubeDimZ) 
    cmds.move((cubeDimY/2.0), moveY=True) 
    
    # Constructing the bumps
    for i in range(blockWidth): 
        for j in range(blockDepth):
            cmds.polyCylinder(r=0.25, h=0.20) 
            cmds.move((cubeDimY + 0.10), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeDimX/2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (cubeDimZ/2.0) + 0.4), moveZ=True, a=True)
    
    # Adding in shader
    myShader = cmds.shadingNode('lambert', asShader=True, name="blockMaterial") 
    cmds.setAttr(namespace_tmp+":blockMaterial.color", rgb[0], rgb[1], rgb[2], type='double3') 
    cmds.polyUnite((namespace_tmp+":*"), n=namespace_tmp, ch=False) 
    cmds.delete(ch=True) 
    cmds.hyperShade(assign=(namespace_tmp+":blockMaterial")) 
    cmds.namespace(set=":") 
    
# Square block with holes
def HoleBlock():
    
    # Initialize the building blocks and the subtraction blocks
    components = []
    subtracts = []
    
    blockDepth = cmds.intSliderGrp('HoleblockDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('HoleblockColour', query=True, rgbValue=True) 
    
    cmds.select(clear=True) 
      
    blockWidth = 1
    cubeDimX = blockWidth * 0.8
    blockHeight = 1
    cubeDimY = blockHeight * 0.96
    cubeDimZ = blockDepth * 0.8

    cube = cmds.polyCube(h=cubeDimY, w=cubeDimX, d=cubeDimZ, sz=blockDepth) 
    cmds.move((cubeDimY/2.0), moveY=True) 
  
    
    # Pipes on top of block
    for i in range(blockDepth):
        components.append(cmds.polyPipe(r=0.24, h=0.36, thickness=0.09)[0]) 
        cmds.move((cubeDimY + 0.10), moveY=True, a=True)
        cmds.move(((i * 0.8) - (cubeDimZ/2.0) + 0.4), moveZ=True, a=True)
    
    # Holes within block
    for k in range(blockDepth - 1):   
        holes = cmds.polyCylinder( h=1, r=0.24, ax=(1,0,0))
        subtracts.append(holes[0]);
        cmds.move( 0, cubeDimY - 0.38, ((k*0.8) - (cubeDimZ/2.0) + 0.8), holes[0], a=True)         
  
    # Unite the cube and the top
    addShape = cmds.polyUnite(cube, components, ch=False)
    
    currentHole = subtracts[0]
    
    for hole in range(len(subtracts)- 1):
        uniteHole = cmds.polyUnite(currentHole, subtracts[hole+1], ch=False)
        currentHole = uniteHole
        
    finalShape = cmds.polyCBoolOp(addShape, uniteHole, op=2, ch=False)[0]
    
    # Adding on the colour
    myShader = cmds.shadingNode('lambert', asShader=True, name="blockMaterial") 
    cmds.setAttr(myShader + ".color", rgb[0], rgb[1], rgb[2], type='double3')
    cmds.select(finalShape, r=True)
    cmds.hyperShade(assign=myShader)
    cmds.namespace(set=":") 

# Rounded/Bent blocks
def RoundBlock():

    blockDepth = cmds.intSliderGrp('RoblockDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('RoblockColour', query=True, rgbValue=True) 
    
    cmds.select(clear=True) 
    
    finalShape = makeRoundHoleBlock(blockDepth)
    
    # Adding on the colour
    myShader = cmds.shadingNode('lambert', asShader=True, name="blockMaterial") 
    cmds.setAttr(myShader + ".color", rgb[0], rgb[1], rgb[2], type='double3')
    cmds.select(finalShape, r=True)
    cmds.hyperShade(assign=myShader)
    cmds.namespace(set=":") 
    
# Angled blocks
def AngledBlock():

    firstBlockDepth = cmds.intSliderGrp('firstDepth', query=True, value=True)
    secondBlockDepth = cmds.intSliderGrp('secondDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('angledBlockColour', query=True, rgbValue=True) 
    
    cmds.select(clear=True) 
    
    cubeDimY = 1 * 0.96
    cubeDimZ = firstBlockDepth * 0.8
    
    firstBlock = makeRoundHoleBlock(firstBlockDepth)
    secondBlock = makeRoundHoleBlock(secondBlockDepth)
    cmds.move((cubeDimZ)-(firstBlockDepth*0.08), moveZ=True) 
    #cmds.move((cubeDimZ/2.0), moveY=True) 
    cmds.rotate('143.5deg', 0, 0, secondBlock[0])
    finalShape = cmds.polyCBoolOp(firstBlock[0], secondBlock[0], op=1)
    
    # Adding on the colour
    myShader = cmds.shadingNode('lambert', asShader=True, name="blockMaterial") 
    cmds.setAttr(myShader + ".color", rgb[0], rgb[1], rgb[2], type='double3')
    cmds.select(finalShape, r=True)
    cmds.hyperShade(assign=myShader)
    cmds.namespace(set=":")  
    
# Right Angle blocks
def RightBlock():

    firstBlockDepth = cmds.intSliderGrp('firstAngleDepth', query=True, value=True)
    secondBlockDepth = cmds.intSliderGrp('secondAngleDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('angled90BlockColour', query=True, rgbValue=True) 
    
    cmds.select(clear=True) 
    
    cubeDimY = 1 * 0.96
    cubeDimZ = (firstBlockDepth * 1.0) - (firstBlockDepth*1.0/firstBlockDepth)
    cubeDimZ2 = (secondBlockDepth * 1.0) - (secondBlockDepth*1.0/secondBlockDepth)
    
    firstBlock = makeRoundHoleBlock(firstBlockDepth)
    secondBlock = makeRoundHoleBlock(secondBlockDepth)
    cmds.move((cubeDimZ/2.0), moveZ=True) 
    cmds.move((cubeDimZ2/2.0), moveY=True) 
    cmds.rotate('90deg', 0, 0, secondBlock[0])
    finalShape = cmds.polyCBoolOp(firstBlock[0], secondBlock[0], op=1)
    
    # Adding on the colour
    myShader = cmds.shadingNode('lambert', asShader=True, name="blockMaterial") 
    cmds.setAttr(myShader + ".color", rgb[0], rgb[1], rgb[2], type='double3')
    cmds.select(finalShape, r=True)
    cmds.hyperShade(assign=myShader)
    cmds.namespace(set=":")         

#                                       #
#    SECONDARY RE-USEABLE FUNCTIONS     #
#                                       #
    
def makeBeamHole( block, z, cubeDimX, cubeDimY, cubeDimZ ):
    hole = cmds.polyCylinder( r=cubeDimY * 0.45, h=cubeDimX, ax=(1,0,0) )
    cmds.move( (z * 1.0) - (cubeDimZ/2.0), moveZ= True, a=True)  
    cmds.move( (cubeDimY * 0.5), moveY= True, a=True) 
    block =  cmds.polyCBoolOp( block[0], hole[0], op=2 )
    return block

def makeBeamPipe( block, x, cubeDimX, cubeDimY, cubeDimZ ):
    hole = cmds.polyCylinder( r=cubeDimY * 0.45, h=cubeDimX, ax=(1,0,0) )
    cmds.move( (x*0.6) - (cubeDimZ/2.0), moveZ= True, a=True)  
    cmds.move( (cubeDimY * 0.5), moveY= True, a=True) 
    block =  cmds.polyCBoolOp( block[0], hole[0], op=2 )
    return block    

def makeRoundHoleBlock(blockDepth):
      
    cubeDimX = 1 * 0.8
    cubeDimY = 1 * 0.96
    cubeDimZ = (blockDepth * 1.0) - (blockDepth*1.0/blockDepth)
    
    # Make Block
    block = cmds.polyCube(width=cubeDimX, height=cubeDimY, depth=cubeDimZ)
    cmds.move((cubeDimY/2.0), moveY=True) 
    
    # Make left endcap
    endCap = cmds.polyCylinder(r=cubeDimY * 0.5, h=cubeDimX, ax=(1,0,0) )
    cmds.move( (cubeDimZ * 0.5), moveZ=True, a=True)
    cmds.move( (cubeDimY * 0.5), moveY=True, a=True)
    block = cmds.polyCBoolOp( block[0], endCap[0], op=1 )
    
    # Make right endcap
    endCap = cmds.polyCylinder(r=cubeDimY * 0.5, h=cubeDimX, ax=(1,0,0) )
    cmds.move( (cubeDimZ * -0.5), moveZ=True, a=True)
    cmds.move( (cubeDimY * 0.5), moveY=True, a=True)
    block = cmds.polyCBoolOp( block[0], endCap[0], op=1 )
    
    cmds.xform(centerPivots = True )
    
    for z in range(blockDepth):
        block = makeBeamHole( block, z , cubeDimX, cubeDimY, cubeDimZ )
    
    return block

	
window = cmds.window(title="Lego Blocks", menuBar=True, widthHeight=(483, 620)) 

# Normal Square block
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Square Block", width=475, height=110) 
cmds.columnLayout()
cmds.intSliderGrp('SquareBlockDepth',label="Depth", field=True, min=4, max=8, value=4)
cmds.intSliderGrp('SquareBlockWidth',label="Width", field=True, min=2, max=8, value=2)
cmds.colorSliderGrp('SquareBlockColour',label="Colour", hsv=(400, 0, 0.5)) 
cmds.columnLayout()
cmds.button(label="Create Square Block", command=('SquareBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

# Square block with holes
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Square Block With Holes", width=475, height=110) 
cmds.columnLayout()
cmds.intSliderGrp('HoleblockDepth',label="Bumps", field=True, min=3, max=10, value=4)
cmds.colorSliderGrp('HoleblockColour',label="Colour", hsv=(350, 1, 1)) 
cmds.columnLayout()
cmds.button(label="Create Square Block", command=('HoleBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

# Rounded/Bent blocks
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Rounded Blocks", width=475, height=110) 
cmds.columnLayout()
cmds.intSliderGrp('RoblockDepth',label="Length", field=True, min=4, max=8, value=5)
cmds.colorSliderGrp('RoblockColour',label="Colour", hsv=(56, 1, 1)) 
cmds.columnLayout()
cmds.button(label="Create Rounded Block", command=('RoundBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

# Angled Blocks
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="Angled block", width=475, height=110) 
cmds.columnLayout()
cmds.intSliderGrp('firstDepth',label="First Block Length", field=True, min=4, max=8, value=5)
cmds.intSliderGrp('secondDepth',label="Second Block Length", field=True, min=4, max=8, value=5)
cmds.colorSliderGrp('angledBlockColour',label="Colour", hsv=(56, 1, 1)) 
cmds.columnLayout()
cmds.button(label="Create angled block", command=('AngledBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

# Right Angled Blocks
cmds.columnLayout()
cmds.frameLayout(collapsable=True, label="90 degree block", width=475, height=110) 
cmds.columnLayout()
cmds.intSliderGrp('firstAngleDepth',label="First Block Length", field=True, min=4, max=8, value=5)
cmds.intSliderGrp('secondAngleDepth',label="Second Block Length", field=True, min=4, max=8, value=5)
cmds.colorSliderGrp('angled90BlockColour',label="Colour", hsv=(56, 1, 1)) 
cmds.columnLayout()
cmds.button(label="Create angled block", command=('RightBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

# Build the window
cmds.showWindow( window )	
''' OLD ONE
# Rounded/Bent blocks
def RoundBlock():

    blockDepth = cmds.intSliderGrp('RoblockDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('RoblockColour', query=True, rgbValue=True) 
    
    cmds.select(clear=True) 
    
    # Initialize the building blocks and the subtraction blocks
    components = []
    subtracts = []
    
    cubeDimX = 1 * 0.8
    cubeDimY = 1 * 0.96
    cubeDimZ = blockDepth * 0.8
    
    for x in range(0, blockDepth + 1):
      holes = cmds.polyCylinder( h=1, r=0.24, ax=(1,0,0))
      subtracts.append(holes[0]);
      cmds.move( 0, cubeDimY/2, ((x*0.8) - (cubeDimZ/2.0)), holes[0], a=True)    

    cube = cmds.polyCube(sx=2,sy=2,sz=blockDepth+1, width=cubeDimX, height=cubeDimY, depth=cubeDimZ)
    #cmds.delete(cube[0] + ".f[40:47]")
    cmds.move((cubeDimY/2.0), moveY=True) 

    #caps
    capOne = cmds.polyCylinder(sc=1, sy=2, radius=0.48, height=cubeDimX, ax=(1,0,0))
    cmds.rotate('90deg',0,0,capOne[0])
    cmds.move(0,cubeDimY/2,cubeDimZ/2,capOne[0])
    cmds.delete(capOne[0] + ".f[0:3]", capOne[0] + ".f[14:23]", capOne[0] + ".f[34:43]", capOne[0] + ".f[54:63]", capOne[0] + ".f[74:79]")
    components.append(capOne[0])

    #caps
    capTwo = cmds.polyCylinder(sc=1, sy=2, radius=0.48, height=cubeDimX, ax=(1,0,0))
    cmds.rotate('90deg','180deg',0,capTwo[0])
    cmds.move(0,cubeDimY/2,cubeDimZ/2 - cubeDimZ,capTwo[0])
    cmds.delete(capTwo[0] + ".f[0:3]", capTwo[0] + ".f[14:23]", capTwo[0] + ".f[34:43]", capTwo[0] + ".f[54:63]", capTwo[0] + ".f[74:79]")
    components.append(capTwo[0])
    
    # Unite the cube and the caps
    addShape = cmds.polyUnite(cube, components, ch=False)
    #cmds.polyMergeVertex( addShape, d=0.15 )    
    
    currentHole = subtracts[0]
    
    for hole in range(len(subtracts)- 1):
        uniteHole = cmds.polyUnite(currentHole, subtracts[hole+1], ch=False)
        currentHole = uniteHole
        
    finalShape = cmds.polyCBoolOp(addShape, uniteHole, op=2, ch=False)[0]
 
    
    # Adding on the colour
    #myShader = cmds.shadingNode('lambert', asShader=True, name="blockMaterial") 
    #cmds.setAttr(myShader + ".color", rgb[0], rgb[1], rgb[2], type='double3')
    #cmds.select(finalShape, r=True)
    #cmds.hyperShade(assign=myShader)
    cmds.namespace(set=":") '''	