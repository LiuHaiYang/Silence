# from PIL import Image,ImageFont,ImageDraw
# im=Image.open('car.jpg')
# im=im.rotate(20)
# im1=Image.open('steve.jpg')
# im1.thumbnail((700,400))
# im.paste(im1,(550,70))
# im.show()


# from PIL import Image
# im1 = Image.open("car.jpg")
# box = [100,100,200,200]
# im_crop = im1.crop(box)
# r,g,b = im_crop.split()
# im1.paste(im_crop,(200,100,300,200),b)



# from PIL import Image
# im1 = Image.open("car.jpg")
# box = [100,100,200,200]
# im_crop = im1.crop(box)
# im1.paste(im_crop,(300,300,400,400))



from PIL import Image
im1 = Image.open("car.jpg")
box = [100,100,300,400]
im_crop = im1.crop(box)
im1.paste(im_crop,(100,100,300,400))  #等价于im1.paste(im_crop,(200,200))
im1.show()

# import Image
# n12090 = Image.new('RGB',(120,90),'black')
# n12060 = Image.new('RGB',(120,70),'white')
# n12090.paste(n12060,(0,10))
# n12090.show()