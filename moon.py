# 
# moon.py
# 
# created at 21/05/2021 20:27:38
# written by llamaking136
# 

# MIT License
#     
# Copyright (c) 2021 llamaking136
#     
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#     
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#     
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import socket, os, sys, json

__copyright__ = "Copyright llamaking136 2021"
__version__ = "0.0.1"

HOME = os.environ["HOME"]

if not os.path.exists(HOME + "/.mooncfg.json"):
    f = open(HOME + "/.mooncfg.json", "w")
    f.write("{\"dns_server\": \"\"}")
    f.close()

f = open(HOME + "/.mooncfg.json", "r")
CONFIG = json.loads(f.read())
f.close()

if CONFIG["dns_server"] == "":
    CONFIG["dns_server"] = "telescope-dns.llamaking136.repl.co"
    f = open(HOME + "/.mooncfg.json", "w")
    f.write(json.dumps(CONFIG))
    f.close()

argv = sys.argv[1:]

if len(argv) == 0:
    print("usage: moon <url> [args]", file = sys.stderr)
    exit(1)

args = {}

# simple argparser
for i in range(len(argv)):
    if argv[i].startswith("-"):
        args[argv[i]] = i

if "--configure-dns" in args.keys():
    new_dns = args["--configure-dns"] + 1
    CONFIG["dns_server"] = new_dns
    f = open(HOME + "/.mooncfg.json", "w")
    f.write(json.dumps(CONFIG))
    f.close()
    exit(0)

# TODO: figure out DNS stuff later

def getUrlFile(url):
    split = url.split("/")[1:]
    if len(split) == 0:
        return "/index.star"
    if not "." in split[-1]:
        split[-1] += "/index.star"
    result = "/".join(split)
    if result[0] != "/":
        return "/" + result
    else:
        return result

url = argv[0]
server = argv[0].split("/")[0]
url_file = getUrlFile(url)

codes = {
    "00": "success",
    "60": "not found",
    "61": "bad request"
}

addr = (server, 5742)
conn = socket.socket()

conn.connect(addr)

print("Requesting file " + url_file + " from server " + server + "...")
conn.send(url_file.encode("utf-8") + b" 0")

data = ""
while True:
    temp = conn.recv(1024)
    data += temp.decode("utf-8")
    if not temp:
        break

header = data.split("\n")[0]
if header in codes.keys():
    print("Error: Got status code '" + codes[header] + "' from server")
    exit(1)

print(data)
