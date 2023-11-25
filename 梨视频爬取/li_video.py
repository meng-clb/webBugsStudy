import requests

url = 'https://www.pearvideo.com/video_1100951'
videoId = url.split('_')[1]
# print(videoId)
# 通过抓包获取到的视频访问地址
videoStatus = f'https://www.pearvideo.com/videoStatus.jsp?contId={videoId}&mrd=0.7002658548017244'
# 通过抓包的地址进行处理，得到原视频地址

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
	              'like Gecko) '
	              'Chrome/119.0.0.0 Safari/537.36',
	# 防盗链, 系统会自动往回上一级寻找, 找到当前访问的上一级是哪, 如果不符合来源, 就无法访问
	'Referer': url
}

resp = requests.get(videoStatus, headers=headers)
# 通过抓到的地址获取视频信息
videoInfo = resp.json()
systemTime = videoInfo['systemTime']
# 解析出来的视频链接,对链接进行处理,即可得到视频链接
srcUrl = videoInfo['videoInfo']['videos']['srcUrl']
""""
https://video.pearvideo.com/mp4/short/20170628/{cont-1100951}-10579851-hd.mp4   原视频地址
https://video.pearvideo.com/mp4/short/20170628/{1698937448999}-10579851-hd.mp4  通过抓包抓到的地址
对比两个链接,只有这两个地方不一样, 将抓包的地址,进行处理, 得到原视频链接
"""
video_src = srcUrl.replace(systemTime,f'cont-{videoId}')

# 通过链接下载视频
with open(f'./videos/{videoId}.mp4', 'wb') as f:
	f.write(requests.get(video_src).content)
	print('over!!!')
print('over_all!!')


