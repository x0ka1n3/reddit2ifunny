import requests, json, os, sys, time
from math import ceil

ifunnyHeader = {"User-Agent":"iFunny/5.31.1(17657) Android/9 (Samsung; Galaxy S7; Samsung)"}
chromeHeader = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
appAuth = ("64363564633131332D323032382D343066662D616531612D656130363664353034313131_MsOIJ39Q28", "72b04a0adff6c2be7be5b8dcf73a34ec9e8327c1")
imgArr = ["png", "jpg", "jpeg"]
gifArr = ["gif"]
videosArr = ["mp4", "tmp", "avi", "wmv", "mov"]

def progressBar(done, length, barLen = 20, title = ""):
	barFillNum = int(round(barLen*done/float(length)))
	barFill = barFillNum*"*"
	barRemain = (barLen - barFillNum)*"-"

	if len(title):
		title = "| " + title

	bar = barFill+barRemain
	barPerc = round((done/length)*100)
	sys.stdout.write("\r[%s] %d%s | %d/%d %s" % (bar, barPerc, "%", done, length, title))
	sys.stdout.flush()
	if done == length:
		print("\n")

def downloader(filename, url):
	with open(filename, "wb+") as media:
				media.write(requests.get(url, headers = chromeHeader).content)

def downloadOrganizer(Type, url):
	path = "{0}/{1}".format(os.path.abspath(""),Type)
	if not os.path.exists(path):
		os.makedirs(path)
	filename = url.split("/")[-1]
	filePath = "{0}/{1}".format(path,filename)
	if not os.path.exists(filePath) or int(os.path.getsize(filePath)) == 0:
		downloader("{0}/{1}".format(path,filename), url)
		queue = json.load(open("uploadQueue.json", "r+"))
		if Type in queue and filename not in queue[Type]:
			queue[Type].append(filename)
			json.dump(queue, open("uploadQueue.json", "w+"), indent = 10)

def uploadOrganizer(file, Type, tokenAuthHeader):
	fp = "{0}/{1}/{2}".format(os.path.abspath(""),Type,file)
	if os.path.exists(fp):
		# if Type == "pics":
		# 	resp = requests.post("https://api.ifunny.mobi/v4/content", headers = tokenAuthHeader, files = {"image":open(fp, "rb+")}, data = {"type":"pic", "visibility":"public"}).json()
		# elif Type == "gifs":
		# 	resp = requests.post("https://api.ifunny.mobi/v4/content", headers = tokenAuthHeader, files = {"image":open(fp, "rb+")}, data = {"type":"gif", "visibility":"public"}).json()
		# elif Type == "videos":
		# 	resp = requests.post("https://api.ifunny.mobi/v4/content", headers = tokenAuthHeader, files = {"video":open(fp, "rb+")}, data = {"type":"video_clip", "visibility":"public"}).json()
		# if "error" in resp:
		# 	print("\nError: {0}".format(resp["error_description"]))
		# 	return 1
		queue = json.load(open("uploadQueue.json", "r+"))
		print(queue, "\n", file, "\n\n")
		queue[Type].remove(file)
		json.dump(queue, open("uploadQueue.json", "w+"), indent = 10)
		os.remove(fp)
		return 0
	else:
		queue = json.load(open("uploadQueue.json", "r+"))
		if file in queue[Type]:
			queue[Type].remove(file)
		return 1

def getNew(subreddit = sys.argv[1], sort = "top", count = int(sys.argv[2]), time = "day"):
	pages = int(ceil(count/100))
	sub = ""
	for char in subreddit:
		if char not in ["", " ", "\n"]:
			sub += char

	subreddit = sub

	if "," in subreddit:
		subredditArr = subreddit.split(",")
	else:
		subredditArr = [subreddit]

	for subreddit in subredditArr:
		after = 0
		postCount = 0
		for page in range(1, pages+1):
			thread = requests.get("https://www.reddit.com/r/{0}/{1}.json?limit={2}&t={3}&after={4}".format(subreddit, sort, count, time, after), headers = chromeHeader).json()["data"]
			after = thread["after"]
			complete = 1

			for child in thread["children"]:
				url = child["data"]["url"]
				if child["data"]["url"].split(".")[-1] in imgArr:
					downloadOrganizer("pics", url)
				elif child["data"]["url"].split(".")[-1] in gifArr:
					downloadOrganizer("gifs", url)
				elif child["data"]["url"].split(".")[-1] in videosArr:
					downloadOrganizer("videos", url)
				postCount += 1
				progressBar(complete, len(thread["children"]), title = "Parsing \"{0}\". Page {1}".format(subreddit, page))
				complete += 1
			if len(thread["children"]) < 100:
				break

def uploader(file, tokenAuthHeader):
	if file.split(".")[-1] in imgArr:
		uploadOrganizer(file, "pics", tokenAuthHeader)
	elif file.split(".")[-1] in gifArr:
		uploadOrganizer(file, "gifs", tokenAuthHeader)
	elif file.split(".")[-1] in videosArr:
		uploadOrganizer(file, "videos", tokenAuthHeader)

def authIfunny(login, password):
	auth = requests.post("https://api.ifunny.mobi/v4/oauth2/token", auth = appAuth, data = {"grant_type":"password", "username":login, "password":password}).json()
	if "error" in auth and "error_description" in auth:
		print(auth["error_description"])
		return 0
	else:
		return auth["access_token"]