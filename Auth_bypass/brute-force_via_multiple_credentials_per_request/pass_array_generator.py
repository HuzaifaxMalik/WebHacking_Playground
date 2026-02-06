import json

passwords=[]

with open('passwords.txt', 'r') as infile:
    for line in infile:
        passwd = line.strip()
        passwords.append(passwd)

with open('pass_array.txt', 'w') as outfile:
    json.dump(passwords, outfile)

print(f"Saved {len(passwords)} passwords in pass_array.txt")