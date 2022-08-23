import time
import requests
import json
import tweepy

list_des_valeurs_de_cours = []

def valeur_de_cours():
    symbol = 'AAPL'
    apikey = '...'
    

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=',symbol,'&apikey=',apikey
    url = "".join(url)

    r = requests.get(url)
    data = r.json()


#_________________________________________________________________

    #select la ligne du cours value in the json file

    COURS = 0

    last_refresh = data["Meta Data"]["3. Last Refreshed"]

    last_refresh = list(last_refresh)


    if last_refresh[9] != " ":
        last_refresh = last_refresh[:10]

    elif last_refresh[9] == " ":
        last_refresh = last_refresh[:9]

    
    last_refresh = "".join(last_refresh)

    print("\n\nDate : ",last_refresh,"\n")

    print("Le cours de l'action est de : $",data["Time Series (Daily)"][last_refresh]["1. open"])

    COURS = data["Time Series (Daily)"][last_refresh]["1. open"]

    list_des_valeurs_de_cours.append(COURS)

    
#_________________________________________________________________________

    #select line of MIN cours value in the json file : 

    MIN = 0
    
    print("Le minimum du cours de l'action est de : $",data["Time Series (Daily)"][last_refresh]["3. low"])

    MIN = data["Time Series (Daily)"][last_refresh]["3. low"]

    list_des_valeurs_de_cours.append(MIN)

    # 

#___________________________________________________________________________

    #select line of MAX cours value in the json file : 

    MAX = 0

    print("Le maximum du cours de l'action est de : $",data["Time Series (Daily)"][last_refresh]["2. high"],"\n")

    MAX = data["Time Series (Daily)"][last_refresh]["2. high"]

    list_des_valeurs_de_cours.append(MAX)

    
    return 0


#____________________________________________________________________________


def tweet_avertir_min(compteur_en_baisse,prix_en_baisse):


    api_key = "..."
    api_secrets = "..."
    access_token = "..."
    access_secret = "..."

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key,api_secrets)
    auth.set_access_token(access_token,access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    status = "Le cours est en baisse depuis",compteur_en_baisse,"jours ! Il est actuellement à",prix_en_baisse,"dollars."
    api.update_status(status=status)

    return 0

def tweet_avertir_max(compteur_en_hausse,prix_en_hausse):

    api_key = "..."
    api_secrets = "..."
    access_token = "..."
    access_secret = "..."

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key,api_secrets)
    auth.set_access_token(access_token,access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    status = "Le cours est en baisse depuis",compteur_en_hausse,"jours ! Il est actuellement à",prix_en_hausse,"dollars."
    api.update_status(status=status)

    return 0

#____________________________________________________________________________

compteur_en_hausse = 0
compteur_en_baisse = 0

while True:

    valeur_de_cours()

    if list_des_valeurs_de_cours[0] < list_des_valeurs_de_cours[2]:
        compteur_en_hausse += 1
        print("Analyse : \n")
        print("Le cours est en hausse depuis",compteur_en_hausse,"jours ! \n")

        tweet_avertir_max(compteur_en_hausse,list_des_valeurs_de_cours[2])

        compteur_en_baisse = 0
        list_des_valeurs_de_cours = []
    
    elif list_des_valeurs_de_cours[0] > list_des_valeurs_de_cours[1]:
        compteur_en_baisse += 1
        print("Analyse : \n")
        print("Le cours est en baisse depuis",compteur_en_baisse,"jours ! \n")

        tweet_avertir_min(compteur_en_baisse,list_des_valeurs_de_cours[1])

        compteur_en_hausse = 0
        list_des_valeurs_de_cours = []

    else :
        print("Le cours est resté stable ! ")
    
    print("Mise à jour demain...\n")
    
    time.sleep(86400) # = 1 jour