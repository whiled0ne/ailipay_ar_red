# coding=utf-8
# whiledone@gmail.com
# wechat:while0811

from PIL import Image,ImageFilter
import math
import random,sys,os

# 获取getpixel的返回数

class MyImage:
    def __init__(self,imgfile):
        image = Image.open(imgfile)

        if image.size==(480,854):
            self.image_width = 210
            self.image_height = 210
            image_x=136
            image_y=431
        # IPhone 6
        elif image.size==(750,1334):
            self.image_width = 340
            self.image_height = 340
            image_x=205
            image_y=638
        # Iphone 7
        elif image.size==(640,1136):
            self.image_width = 340
            self.image_height = 340
            image_x=150
            image_y=441
        # mi 5 plus
        elif image.size==(720,1280) or image.size==(719,1280):
            self.image_width = 256
            self.image_height = 256
            image_x=232
            image_y=760
        elif image.size==(899,1600):
            self.image_width = 404
            self.image_height = 404
            image_x=247
            image_y=766
        # samsung s6 edge by gMan1990
        elif image.size==(1440,2560):
            self.image_width = 560
            self.image_height = 560
            image_x=440
            image_y=1444
        # samsung s6 edge by zhangbo
        elif image.size==(1242,2208):
            self.image_width = 511
            self.image_height = 511
            image_x=365
            image_y=1164
        elif image.size==(1080,1920):
            self.image_width = 420
            self.image_height = 420
            image_x=330
            image_y=962
        else:
            self.image_width = image.size[0]
            self.image_height =image.size[1]
            image_x=0
            image_y=0

        image2=image.crop(
            (
            image_x,image_y,image_x+self.image_width,image_y+self.image_height)
        )

        self.image=image2
        bgcolor = (255,255,255)
        self.newimage = Image.new('RGB',((self.image_width+30)*3 ,(self.image_height+30)*2 ),bgcolor)

    def getPixellen(self):
        return len(self.image.getpixel((1, 1)))

    def getPixel(self,x,y):
        pixel=self.image.getpixel((x, y))

        if len(pixel)==3:
            r,g,b=pixel
        else:
            r,g,b,z=pixel
        return (r,g,b)

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
        if x>=self.image_width:
            x=self.image_width-1
        if y>=self.image_height:
            y=self.image_height-1
        #print x,y
        return self.image.getpixel((x,y))

    def setPixel(self,x,y,r,g,b):
        x=min(self.newimage.size[0]-1,x)
        y=min(self.newimage.size[1]-1,y)
        self.newimage.putpixel([x,y],(r,g,b))


def main():
    if len(sys.argv)<2:
        print "\n  Run as the following command:"
        print "\t%s  path_of_image\n"%os.path.basename(sys.argv[0])
        print u"截图时，请对着白色的墙壁或者白纸截图，提高成功率"
        return
    if len(sys.argv)==3:
        offset=sys.argv[2]
    myimage=MyImage(sys.argv[1])
    if myimage==None:
        print "You must modify image size and offset in code"
        return

    image_width = myimage.image_width
    image_height = myimage.image_height
    cutlist=[[],[],[]]

    ttlist=[]
    ratlist=[]
    tt0=0

    for y in range(image_height):
        linedots=[]
        for x in range(0,image_width,3):
            linedots.append(myimage.getRGBNum(x,y))
        linedots.sort()
        ttlist.append(linedots[-5])
        rat=math.log(max(linedots)/min(linedots))
        ratlist.append(rat)
        #print y,rat,max(linedots)-min(linedots)#,linedots

    #return

    steps=[]

    for i in range(0,image_height,12):
        seglist=ttlist[i+3:i+12+3]
        steps.append(min(seglist)-max(seglist))
    max_line_with=9*myimage.image_height/340
    for m in (0,1,2):
        matt_delta=m*0.3
        lasthide=False
        line_with=0
        stack=0
        stack_nums_pos=0
        stack_nums_neg=0
        max_tt=0
        magin_rat=10


        for i in range(1,len(ttlist)):
            distance= ttlist[i]-ttlist[i-1]
            calc_step=max(-100,steps[i/12]/10)
            stack_num=(stack_nums_neg,stack_nums_pos)

            if line_with<max_line_with and \
            (distance<calc_step or (stack <-1) or ttlist[i]<max_tt) \
            and (ratlist[i]<=magin_rat+matt_delta or line_with<max_line_with/2)\
            and (len(cutlist[m])==0 or i-cutlist[m][-1][0]>2 ): # gap of two line at least 3
                line_is= "\t\t[+++++]"
                if magin_rat<ratlist[i] or magin_rat==10:
                    magin_rat=ratlist[i]
                if distance>0:
                    stack_nums_pos+=distance
                    stack+=1
                else:
                    stack_nums_neg+=distance
                    if max_tt<ttlist[i]:
                        max_tt=ttlist[i]
                    stack-=1
                if lasthide==False:
                    stack_nums_pos=0
                    stack_nums_neg=0
                    line_with=1
                else:
                    line_with+=1
                lasthide=True
            elif lasthide==True:
                line_is= "\t\t[----]"
                magin_rat=10
                lasthide=False
                if line_with>2:
                    cut=(i,line_with)
                    cutlist[m].append(cut)
                    line_with=0
                    stack=0
                    max_tt=0
            else:
                stack=0
                max_tt=0
                line_is= ""
            print i,ttlist[i],line_with,stack,distance,ratlist[i],calc_step,max_tt,stack_num,line_is
    for i in cutlist:
        print i
    #return

    img1=myimage.image.crop((0,0,image_width,image_height))

    last_y=0
    for w in range(0,2):
        for k in range(0,len(cutlist)):
            myimage.newimage.paste(img1,((image_width+30)*k,(image_height+30)*w))
            for i in range(len(cutlist[k])):
                start,line_with=cutlist[k][i]
                for j in range(0,image_width):
                    p0=myimage.getPixel(j, min(max(start-line_with-w-1,0),image_width))
                    p1=myimage.getPixel(j, min(start+w+1,image_width))

                    r0,g0,b0=p0[0:3]
                    r1,g1,b1=p1[0:3]

                    for i in range(0,line_with+1):
                        r=int((r1*(i+1)+r0*(line_with-i-1))/line_with)
                        g=int((g1*(i+1)+g0*(line_with-i-1))/line_with)
                        b=int((b1*(i+1)+b0*(line_with-i-1))/line_with)
                        x=min(j,image_width-1)
                        y=max(start-line_with+i,0)
                        myimage.setPixel(x+(image_width+30)*k,y+(image_height+30)*w,r,g,b)
    myimage.newimage.show()

if __name__ == '__main__':
    main()
