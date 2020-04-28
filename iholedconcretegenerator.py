from abaqus import *
from abaqusConstants import *
import regionToolset
import math
import numpy as np

tf=10 #flange thickness
tw=8 #web thickness
h=160 #section depth
b=160 #section width
d=350 #section diameter
L=2000 #extrude length
fcm=100 #concrete compressive strength
ec1=0.001*min(0.7*fcm**0.31,2.8)
ecu1=0.001*min(3.5,2.8+27*((98-fcm)/float(100))**4)

Ecm=1000*(22*(fcm/10)**0.3)

if fcm<58:
    fctm=0.3*(fcm-8)**(2/3)
else:
    fctm=2.12*math.log(1+fcm/10)
    
ec=np.linspace(0,ecu1,num=20)


sigc=[]
k=1.05*Ecm*ec1/fcm
eta=ec/ec1
sigc=fcm*(k*eta-np.power(eta,2))/(1+(k-2)*eta)
sigc=np.append(sigc,fcm/10)
ec=np.append(ec,ecu1+0.0005)
sigc.tolist

#cctable=[[0 for x in range(2)] for y in range(len(ec))]
cctable=np.zeros((len(ec),2))

#print(cctable)

for i in range(len(ec)):
    cctable[i][0]=sigc[i]
    cctable[i][1]=ec[i]-cctable[i][0]/Ecm


i=0
while i in range(len(cctable[:,1])):
    if cctable[i][0]>=0.4*fcm and cctable[i][1]>=0:
        break
    else:
        i=i+1
    
cuttab=cctable[i:]

cctab=tuple(map(tuple, cctable[i:]))
    
#print(cctab)


session.viewports['Viewport: 1'].setValues(displayedObject=None)

#mdb.models.changeKey(fromName='Model-1',toName='Cantilever Beam')
column_model = mdb.models['Model-1']

import sketch
import part

concrete_sketch=column_model.ConstrainedSketch(name='beam',sheetSize=160)

concrete_sketch.Line(point1=(b/2,h/2),point2=(b/2,h/2-tf))
concrete_sketch.Line(point1=(b/2,h/2-tf),point2=(tw/2,h/2-tf))
concrete_sketch.Line(point1=(tw/2,h/2-tf),point2=(tw/2,-(h/2-tf)))
concrete_sketch.Line(point1=(tw/2,-(h/2-tf)),point2=(b/2,-(h/2-tf)))
concrete_sketch.Line(point1=(b/2,-(h/2-tf)),point2=(b/2,-h/2))
concrete_sketch.Line(point1=(b/2,-h/2),point2=(-b/2,-h/2))
concrete_sketch.Line(point1=(-b/2,-h/2),point2=(-b/2,-(h/2-tf)))
concrete_sketch.Line(point1=(-b/2,-(h/2-tf)),point2=(-tw/2,-(h/2-tf)))
concrete_sketch.Line(point1=(-tw/2,-(h/2-tf)),point2=(-tw/2,(h/2-tf)))
concrete_sketch.Line(point1=(-tw/2,(h/2-tf)),point2=(-b/2,(h/2-tf)))
concrete_sketch.Line(point1=(-b/2,(h/2-tf)),point2=(-b/2,h/2))
concrete_sketch.Line(point1=(-b/2,h/2),point2=(b/2,h/2))
concrete_sketch.CircleByCenterPerimeter((0,0),(0,d/2))

concrete_part=column_model.Part(name='concrete',dimensionality=THREE_D,type=DEFORMABLE_BODY)
concrete_part.BaseSolidExtrude(sketch=concrete_sketch,depth=L)
concrete_part.PartitionCellByPlaneThreePoints(cells=concrete_part.cells,point1=(b/2,h/2,6),point2=(b/2,-h/2,5),point3=(b/2,-h/2,4))
concrete_part.PartitionCellByPlaneThreePoints(cells=concrete_part.cells,point1=(-b/2,h/2,6),point2=(-b/2,-h/2,5),point3=(-b/2,-h/2,4))
concrete_part.PartitionCellByPlaneThreePoints(cells=concrete_part.cells,point1=(-b/2,h/2,6),point2=(b/2,h/2,5),point3=(-b/2,h/2,4))
concrete_part.PartitionCellByPlaneThreePoints(cells=concrete_part.cells,point1=(-b/2,-h/2,6),point2=(b/2,-h/2,5),point3=(-b/2,-h/2,4))
concrete_part.PartitionCellByPlaneThreePoints(cells=concrete_part.cells,point1=(-b/2,-(h/2-tf),6),point2=(b/2,-(h/2-tf),5),point3=(-b/2,-(h/2-tf),4))
concrete_part.PartitionCellByPlaneThreePoints(cells=concrete_part.cells,point1=(-b/2,(h/2-tf),6),point2=(b/2,(h/2-tf),5),point3=(-b/2,(h/2-tf),4))
concrete_part.PartitionCellByPlaneThreePoints(cells=concrete_part.cells,point1=(0,(h/2-tf),6),point2=(0,-(h/2-tf),5),point3=(0,(h/2-tf),4))

import material

concmaterial=column_model.Material(name='concretemat')
concmaterial.ConcreteDamagedPlasticity(table=((35,0.1,1.16,0.67,0),))
concmaterial.concreteDamagedPlasticity.ConcreteCompressionHardening(table=cctab)
