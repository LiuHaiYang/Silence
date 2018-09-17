#conding:utf-8
import math

x1,y1,x2,y2,x3,y3=2,0,1,2,2,2
#计算三条边长
a=math.sqrt((x2-x3)*(x2-x3)+(y2-y3)*(y2-y3))
b=math.sqrt((x1-x3)*(x1-x3)+(y1-y3)*(y1-y3))
c=math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
#利用余弦定理计算三个角的角度
A=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
C=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
#输出三个角的角度
print("There three angles are",round(A,2),round(B,2),round(C,2))
