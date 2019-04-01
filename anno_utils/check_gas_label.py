# gas_label文件的逆操作，检查标注的x1,y1,x2,y2到x,y,w,h的转换是否正确

def reconvert(size,anno):
    x,y,w,h=anno
    dw = size[0]
    dh = size[1]
    x2 = ((x)*2+w)/2
    x1 = x2-w
    y2 = ((y)*2+h)/2
    y1 = y2-h
    x1 = x1*dw+1
    x2 = x2*dw+1
    y1 = y1*dh+1
    y2 = y2*dh+1
    return x1,y1,x2,y2


size1=(1069,500)
size2=(618,618)

anno = (0.6010289990645463 ,0.665 ,0.16744621141253507 ,0.34600000000000003)

print(reconvert(size1,anno))
