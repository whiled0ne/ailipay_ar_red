# coding=utf-8
# whiledone@gmail.com

from PIL import Image

imgfile="0.jpg"
image = Image.open(imgfile)
image2 = Image.open(imgfile)

#红包线索的尺寸
image_width = 340
image_height = 340

#红包线索在劫图中的坐标
image_x=205
image_y=638

cutlist=[]
lasthide=False

# 搜索并计算黑线的位置
for i in range(image_height):
    r,g,b= image.getpixel((image_x+1, image_y+i))
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

# 填充图像
for i in range(len(cutlist)):
    start,offset=cutlist[i]
    img1 = image.crop(
        (image_x, image_y+start+2, image_x+image_width, image_y+start+3))
    #print cut
    #print 0, start, image_width, start+offset
    for i in range(0,offset+1):
        image2.paste(img1, (image_x, image_y+start-offset+i))

image2.show()

