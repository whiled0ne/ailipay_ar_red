# coding=utf-8
# whiledone@gmail.com
# 需要将图片截取出来处理
from PIL import Image,ImageFilter

imgfile="0.png"
image = Image.open(imgfile)
image2 = Image.open(imgfile)

# 获取getpixel的返回数

def getPixellen():
    return image.getpixel((1, 1))

# 判断黑线的像素点

def dotIsDark(x,y,p=0,maginrgb=300):
    pixel=image.getpixel((x, y))

    if len(pixel)==3:
        r,g,b=pixel
    else:
        r,g,b,z=pixel
    if p==1:
        print y,pixel,r+g+b
    if r<100  or  r<120 and g<80 and b<80 or r+g+b<maginrgb:
        return True
    else:
        return False

# 获取像素点r g b 之和
def getRGBNum(x,y):
    pixel=image.getpixel((x, y))

    if len(pixel)==3:
        r,g,b=pixel
    else:
        r,g,b,z=pixel
    #print y,pixel, r+g+b
    return r+g+b

def main():
    image_width = image.size[0]
    image_height = image.size[1]
    cutlist=[]
    lasthide=False
    rgbn=getPixellen()
    tt0=0
    # 计算像素的平均值，用于辅助判断黑线
    for i in range(image_height):
        tt0+=getRGBNum(10,i)
        tt0+=getRGBNum(image_width-10,i)
    maginrgb= tt0/(image_height*2)
    #return
    
    # 判断像素点是否属于黑线，每行采样三个点，都满足条件，作为判断依据
    for i in range(image_height):
        if dotIsDark(10,i,maginrgb=maginrgb) and dotIsDark(image_width/2,i,maginrgb=maginrgb) and dotIsDark(image_width-2,i,maginrgb=maginrgb):
            if lasthide==False:
                offset=1
            else:
                offset+=1
            lasthide=True
        elif lasthide==True:
            lasthide=False
            if offset>2:
                cut=(i,offset)
                cutlist.append(cut)
    # 采用差值发，对图像进行修改
    for i in range(len(cutlist)):
        start,offset=cutlist[i]
        start+=0
        offset+=1
        for j in range(0,image_width):
            if rgbn==3:
                r0,g0,b0=image.getpixel((j, max(start-offset-2,0)))
                r1,g1,b1=image.getpixel((j, min(start+2,image_width)))
            else:
                r0,g0,b0,z0=image.getpixel((j, max(start-offset-2,0)))
                r1,g1,b1,z1=image.getpixel((j, min(start+2,image_width)))
            for i in range(0,offset+1):
                r=(r1*(i+1)+r0*(offset-i-1))/offset
                g=(g1*(i+1)+g0*(offset-i-1))/offset
                b=(b1*(i+1)+b0*(offset-i-1))/offset
                image2.putpixel([min(j,image_width-1),max(start-offset+i,0)],(r,g,b))
    image2.show()

if __name__ == '__main__':
    main()
