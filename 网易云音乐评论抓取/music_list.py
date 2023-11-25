import requests
from lxml import etree


def id_list():
	"""
	:return: 返回抓取到的音乐id和名字列表
	"""
	# 抓取哪个榜单,把榜单的id写入这里
	page_id = 3778678
	url = input('请输入浏览器中榜单链接(默认抓取热歌榜,输入q开始抓取热歌榜):')
	if url == 'q':
		pass
	else:
		page_id = url.split('=')[1]
	Id_url = f'https://music.163.com/discover/toplist?id={page_id}'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
		              'like Gecko) Chrome/119.0.0.0 Safari/537.36',
	}

	resp = requests.get(Id_url, headers=headers)
	html = etree.HTML(resp.text)
	music_name_list = html.xpath('//ul[@class="f-hide"]//li/a/text()')
	music_id_list = html.xpath('//ul[@class="f-hide"]//li/a/@href')
	return music_id_list, music_name_list


# for item in music_id_list:
# 	item = item.split('=')[1]
# 	return Id_list

# for item1,item2 in zip(music_name_list,music_id_list):
# 	item2 = item2.split('=')[1]
# 	print(item1,item2)
if __name__ == '__main__':
	list = id_list()
	for item1, item2 in zip(list[0], list[1]):
		item1 = item1.split('=')[1]
		print(item2, item1)
