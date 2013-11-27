import requests
import sys

base = sys.argv[1]

while True:
    path = raw_input("Path:> ")
    resp = requests.get(base + "/get_image", params={"path": path})
    if resp.status_code == 200:
        print resp.content
    else:
        print "No such file"