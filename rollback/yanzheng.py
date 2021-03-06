import random,string
from PIL import Image,ImageDraw,ImageFont,ImageFilter
#生成随机字符串
def getRandomChar():
    	#string模块包含各种字符串，以下为小写字母加数字
	ran = string.ascii_lowercase+string.digits
	char = ''
	for i in range(4):
		char += random.choice(ran)
	return char

#返回一个随机的RGB颜色
def getRandomColor():
	return (random.randint(50,150),random.randint(50,150),random.randint(50,150))


def create_code():
	#创建图片，模式，大小，背景色
	img = Image.new('RGB', (120,46),(255,255,255))
	#创建画布
	draw = ImageDraw.Draw(img)
	#设置字体
	font = ImageFont.truetype('/www/weishikeji_object_rollback/ttf/Arial.ttf', 30)
	code = getRandomChar()
	#将生成的字符画在画布上
	for t in range(4):
		draw.text((30*t+5,0),code[t],getRandomColor(),font)
	#生成干扰点
	for _ in range(random.randint(0,50)):
	#位置，颜色
		draw.point((random.randint(0, 120), random.randint(0, 30)),fill=getRandomColor())
	#使用模糊滤镜使图片模糊
	img = img.filter(ImageFilter.BLUR)
	#保存
	#img.save(''.join(code)+'.jpg','jpeg')
	return img,code

if __name__ == '__main__':
	create_code()


import hashlib
def md5_encryption(pwd):
	m2=hashlib.md5()
	m2.update(pwd.encode("utf-8"))
	#转换成大写
	pas=m2.hexdigest()
	B_M=pas.upper()
	#return m2.hexdigest()
	return B_M
