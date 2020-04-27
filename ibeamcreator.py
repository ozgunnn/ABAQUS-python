from abaqus import *
from abaqusConstants import *
import regionToolset

tf=10 #flange thickness
tw=8 #web thickness
h=160 #section depth
b=160 #section width
L=2000 #extrude length

session.viewports['Viewport: 1'].setValues(displayedObject=None)

#mdb.models.changeKey(fromName='Model-1',toName='Cantilever Beam')
beam_model = mdb.models['Model-1']

import sketch
import part

beam_sketch=beam_model.ConstrainedSketch(name='beam',sheetSize=160)

beam_sketch.Line(point1=(-h/2,(h-tf)/2),point2=(0,(h-tf)/2))
beam_sketch.Line(point1=(0,(h-tf)/2),point2=(h/2,(h-tf)/2))
beam_sketch.Line(point1=(-h/2,-(h-tf)/2),point2=(0,-(h-tf)/2))
beam_sketch.Line(point1=(0,-(h-tf)/2),point2=(h/2,-(h-tf)/2))
beam_sketch.Line(point1=(0,-1*(h-tf)/2),point2=(0,(h-tf)/2))

beam_part=beam_model.Part(name='Beam',dimensionality=THREE_D,type=DEFORMABLE_BODY)
beam_part.BaseShellExtrude(sketch=beam_sketch,depth=L)