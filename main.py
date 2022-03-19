from funcs import *

# if os.path.exists(os.path.abspath(os.path.dirname(sys.argv[0]))+"/auth.json"):
# 	global access_token

# 	ifunny 		= json.load(open("auth.json", "r+"))
# 	login 		= ifunny["login"]
# 	password	= ifunny["password"]
	
# 	if "token" in ifunny and len(ifunny["token"]) and not ifunny["token"] == "0":
# 		access_token = ifunny["token"]
# 	else:
# 		access_token = str(authIfunny(login, password))
# 		authJson = json.load(open("auth.json", "r+"))
# 		authJson["token"] = access_token
# 		json.dump(authJson, open("auth.json", "r+"), indent = 10)

# print("Got access_token.\n")

# tokenAuthHeader = {"User-Agent":"iFunny/5.31.1(17657) Android/9 (Samsung; Galaxy S7; Samsung)","Authorization": "Bearer {0}".format(access_token)}

getNew()

# queue = json.load(open("uploadQueue.json", "r+"))

# count = 0
# for key in queue:
# 	for val in queue[key]:
# 		count += 1

# i = 0
# for key in queue:
# 	for val in queue[key]:
# 		if uploader(val, 1) == 2:
# 			time.sleep(300)
# 		i += 1
# 		progressBar(i,count, title = "Uploading...")
# 		time.sleep(0.1)