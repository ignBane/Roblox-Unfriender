import requests, json, colorama

from colorama import Fore, init
init(autoreset=True)

username = str(input("Username: "))
cookie = str(input("Cookie: "))
ignore_friends = ["Person 1", "Person 2"]
session = requests.session()


def csrf(x): # Based On https://github.com/suufi/noblox.js/blob/master/lib/util/getGeneralToken.js
  try: 
    re = requests.post("https://auth.roblox.com/v2/logout", headers={"Cookie":".ROBLOSECURITY=" + x})
    token = re.headers['x-csrf-token'] 
    if token:
      return token
    else:
      print("Did not recevie X-CSRF-TOKEN") 
  except Exception as e:
    print(f"Seems there was an error authentication with roblox api:(")  

def count_friends(x):
    user_id = session.get(f"https://api.roblox.com/users/get-by-username?username={username}").json()['Id']

    friends = session.get(f"https://friends.roblox.com/v1/users/{user_id}/friends", headers={"Cookie":f".ROBLOSECURITY={x}"}).json()['data']

    for friend in friends:
        if friend['displayName'] in ignore_friends:
            pass
        else:
            re = session.post(f"https://friends.roblox.com/v1/users/{friend['id']}/unfriend", headers={"X-CSRF-TOKEN": csrf(x), "Cookie":f".ROBLOSECURITY={x}"})
            print(f"Unfriended {Fore.GREEN}{friend['displayName']}")

count_friends(cookie)
