# Imports
import maya.cmds as cmds
import random

# Normal Square block
def SquareBlock():
    
    # Fetching slider data
    blockDepth = cmds.intSliderGrp('SquareBlockDepth', query=True, value=True)
    blockWidth = cmds.intSliderGrp('SquareBlockWidth', query=True, value=True)
    rgb = cmds.colorSliderGrp('SquareBlockColour', query=True, rgbValue=True) 
    rnd= random.randrange(0,1000)
    namespace_tmp = "Block_" + str(rnd)
    
    cmds.select(clear=True) 
    cmds.namespace(add=namespace_tmp) 
    cmds.namespace(set=namespace_tmp) 
    
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

    RoblockDepth = cmds.intSliderGrp('RoblockDepth', query=True, value=True)
    rgb = cmds.colorSliderGrp('RoblockColour', query=True, rgbValue=True) 
    rnd= random.randrange(0,1000)
    namespace_tmp = "RoBlock_" + str(rnd)
    
    cmds.select(clear=True) 
    cmds.namespace(add=namespace_tmp) 
    cmds.namespace(set=namespace_tmp) 
    
    RoblockWidth = 1
    rectSizeX = RoblockWidth
    rectSizeY = 0.05
    rectSizeZ = RoblockDepth
    
    cmds.polyCube(h=rectSizeY, w=rectSizeX, d=rectSizeZ/2.0)
    cmds.move(((RoblockDepth) - (rectSizeZ/0.78)), moveZ=True, a=True)
    cmds.move((rectSizeY + 0.54), moveY=True, a=True)
    cmds.polyCube(h=rectSizeY, w=rectSizeX, d=rectSizeZ/2.0)
    cmds.move(((RoblockDepth) - (rectSizeZ/0.78)), moveZ=True, a=True)
    cmds.move((rectSizeY), moveY=True, a=True)
     
    for i in range(RoblockWidth): 
        for j in range(RoblockDepth):
            
            cmds.polyPipe(r=0.3, h=RoblockWidth*2, t=0.05, ax=(1,0,0)) 
            cmds.move(((j*0.55) - (rectSizeZ/2.0)), moveZ=True, a=True)
            cmds.move((rectSizeY + 0.27), moveY=True, a=True)
    
    myShader = cmds.shadingNode('lambert', asShader=True, name="blockMaterial") 
    cmds.setAttr(namespace_tmp+":blockMaterial.color", rgb[0], rgb[1], rgb[2], type='double3') 
    cmds.polyUnite((namespace_tmp+":*"), n=namespace_tmp, ch=False) 
    cmds.delete(ch=True) 
    cmds.hyperShade(assign=(namespace_tmp+":blockMaterial")) 
    cmds.namespace(set=":") 
    

	
window = cmds.window(title="Lego Blocks", menuBar=True, widthHeight=(483, 620)) 

cmds.menu(label="Options") 
cmds.menuItem(label="New Scene", command=('cmds.file(new=True,force=True)')) 
cmds.menuItem(label="Delete Selected", command=('cmds.delete()')) 

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

# Build the window
cmds.showWindow( window )	
	