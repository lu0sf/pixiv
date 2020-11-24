import datetime
def time_now():
	now = datetime.datetime.now().strftime("%Y%m%d")
	return now
# 考虑跨年的情形
def time_before_three_month():
	now = datetime.datetime.now()
	if now.month > 3:
		before = datetime.datetime(now.year, now.month - 3, now.day).strftime("%Y%m%d")
	else:
		before = datetime.datetime(now.year - 1, now.month + 9, now.day).strftime(
			"%Y%m%d")
	return before

mode = 'monthly' #daily，weekly，monthly，rookie，weekly_r18，daily_r18，male_r18
content = 'illust' #只能插画
ldata = str(time_before_three_month()) + '-' + str(time_now())
out = 'G:/pixiv/'
cookie = 'xxx'
view_count = 50000 #爬取观看人数大于多少的图片，粗略过滤