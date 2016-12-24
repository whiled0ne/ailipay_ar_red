# coding=utf-8
from PIL import Image,ImageFilter

imgfile="9.png"
image = Image.open(imgfile)
image2 = Image.open(imgfile)

image_width = image.size[0]
image_height = image.size[1]

cutlist=[]
lasthide=False

for i in range(image_height):
    r,g,b,z= image.getpixel((10, i))
    if r<100  or  r<125 and g<70 and b<70:
        if lasthide==False:
            offset=1
        else:
            offset+=1
        lasthide=True
    elif lasthide==True:
        lasthide=False
        cut=(i,offset)
        cutlist.append(cut)

for i in range(len(cutlist)):
    start,offset=cutlist[i]
    offset+=1

    for j in range(0,image_width):
        r0,g0,b0,z0=image.getpixel((j, start-offset-2))
        r1,g1,b1,z1=image.getpixel((j, start+2))
        for i in range(0,offset+2):
            r=(r0*(i+1)+r1*(offset-i-1))/offset
            g=(g0*(i+1)+g1*(offset-i-1))/offset
            b=(b0*(i+1)+b1*(offset-i-1))/offset
            #print r,g,b
            image2.putpixel([j,start-offset+i],(r,g,b))
            #image2.paste(img1, (20, start-offset+i-1))

image2.show()
#img=image2.filter(ImageFilter.SMOOTH_MORE)
#img.show()

