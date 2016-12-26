# coding=utf-8
# whiledone@gmail.com
# wechat:while0811
from PIL import Image,ImageFilter

# 获取getpixel的返回数

class MyImage:
    def __init__(self,imgfile):

        image = Image.open(imgfile)
        print image.size
        # IPhone 6
        if image.size==(750,1334):
            self.image_width = 340
            self.image_height = 340
            image_x=205
            image_y=638
        # Iphone 7
        elif image.size==(640,1136):
            self.image_width = 340
            self.image_height = 340
            image_x=151
            image_y=441
        else:
            self.image_width = 340
            self.image_height = 340
            image_x=151
            image_y=441
        image2=image.crop(
            (
            image_x,image_y,image_x+self.image_width,image_y+self.image_height)
        )

        self.image=image2

    def getPixellen(self):
        return len(self.image.getpixel((1, 1)))

    # 判断黑线的像素点

    def dotIsDark(self,x,y,p=0,maginrgb=300):
        pixel=self.image.getpixel((x, y))

        if len(pixel)==3:
            r,g,b=pixel
        else:
            r,g,b,z=pixel
        if p==1:
            print y,pixel,r+g+b
        if r<100  or  r<120 and g<80 and b<80 or r+g+b<maginrgb :
            return True
        else:
            return False

    # 获取像素点r g b 之和
    def getRGBNum(self,x,y):
        pixel=self.image.getpixel((x, y))

        if len(pixel)==3:
            r,g,b=pixel
        else:
            r,g,b,z=pixel

        return r+g+b

    def getDistance(self,x,y):
        if y>1:
            return self.getRGBNum(x,y)-self.getRGBNum(x,y-1)
        else:
            return 0

    def getPixel(self,x,y):
        return self.image.getpixel((x,y))

    def setPixel(self,x,y,r,g,b):
        self.image.putpixel([x,y],(r,g,b))


def main():
    myimage=MyImage("3.jpg")
    image_width = myimage.image_width
    image_height = myimage.image_height
    cutlist=[]
    lasthide=False
    rgbn=myimage.getPixellen()
    tt0=0
    thistt=0
    for i in range(image_height):
        thistt=myimage.getRGBNum(10,i)+myimage.getRGBNum(image_width-10,i)
        tt0+=thistt
    for i in range(image_height-2):
        print myimage.image.getpixel((10, i)),"%d\t%d\t%d"%(i,myimage.getRGBNum(10,i),myimage.getDistance(10,i)),myimage.dotIsDark(10,i,maginrgb=300)
    print rgbn
    #return
    maginrgb= tt0/(image_height*2)
    #return

    for i in range(image_height):
        if myimage.dotIsDark(10,i,maginrgb=maginrgb) and myimage.dotIsDark(262,i,maginrgb=maginrgb) and myimage.dotIsDark(image_width-2,i,maginrgb=maginrgb) or myimage.getDistance(10,i)<-100:
            if lasthide==False:
                offset=1
            else:
                offset+=1
            lasthide=True
        elif lasthide==True and myimage.getDistance(10,i)<0:
            offset+=1
        elif lasthide==True:
            lasthide=False
            if offset>2:
                cut=(i,offset)
                cutlist.append(cut)

    for i in range(len(cutlist)):
        start,offset=cutlist[i]
        start+=0
        offset+=1
        for j in range(0,image_width):
            if rgbn==3:
                r0,g0,b0=myimage.getPixel(j, max(start-offset-2,0))
                r1,g1,b1=myimage.getPixel(j, min(start+2,image_width))
            else:
                r0,g0,b0,z0=myimage.getPixel(j, max(start-offset-2,0))
                r1,g1,b1,z1=myimage.getPixel(j, min(start+2,image_width))
            for i in range(0,offset+1):
                r=int((r1*(i+1)+r0*(offset-i-1))/offset)
                g=int((g1*(i+1)+g0*(offset-i-1))/offset)
                b=int((b1*(i+1)+b0*(offset-i-1))/offset)
                myimage.setPixel(min(j,image_width-1),max(start-offset+i,0),r,g,b)
    myimage.image.show()

if __name__ == '__main__':
    main()
