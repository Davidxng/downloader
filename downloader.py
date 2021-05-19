import requests
import os

#指定并创建下载目录
SaveTo = './tmp'
if not os.path.exists(SaveTo):
	os.makedirs(SaveTo)

#文件下载函数
def download(URL, SaveAs):
	SavePath = os.path.join(SaveTo,SaveAs)
	res = requests.get(URL,stream=True)
	res.raise_for_status()
	try:
		size = int(res.headers['content-length'])
	except KeyError:
		with open(SavePath, 'wb') as fso:
			fso.write(res.content) #r.content：以二进制方式读取文件
			print(f"\r{SaveAs}--------下载完成",end='')
	else:
		with open(SavePath, 'wb') as fso:
			num =0 #下载块计数器
			for chunk in res.iter_content(1024):
				fso.write(chunk)
				num += 1
				rate = int((num * 1024 / size)*100)
				print(f"\r{SaveAs}--------下载进度:{rate:}%",end='')

#从txt文件获取批量下载链接
with open('links.txt') as file:
	print('')
	for line in file.readlines():
		content = line.replace('\n','').split(',')
		myURL = content[0]
		mySaveAs =content[1]
		download(myURL, mySaveAs)
		print('')
