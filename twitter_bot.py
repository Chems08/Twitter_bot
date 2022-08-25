import time
import requests
import json
import tweepy

list_des_valeurs_de_cours = []

def valeur_de_cours():
    symbol = 'AAPL' # Apple
    apikey = '...'
    interval = '60min'
    time_series = 'TIME_SERIES_INTRADAY'
    

    url = 'https://www.alphavantage.co/query?function=',time_series,'&symbol=',symbol,'&interval=',interval,'&apikey=',apikey
    url = "".join(url)

    r = requests.get(url)
    data = r.json()


#_________________________________________________________________

    #select la ligne du cours value in the json file

    COURS = 0

    time_interval = 'Time Series (60min)'       # 'Time Series (15min)' // 'Time Series (60min)' // 'Time Series (Daily)' 

    last_refresh = data["Meta Data"]["3. Last Refreshed"]

#_________________________________________________________________
    # last_refresh = list(last_refresh)


    # if last_refresh[9] != " ":
    #     last_refresh = last_refresh[:10]

    # elif last_refresh[9] == " ":
    #     last_refresh = last_refresh[:9]

#__________________________________________________________________

    
    last_refresh = "".join(last_refresh)

    print("\n\nDate : ",last_refresh,"\n")

    print("Le cours de l'action est de : $",data[time_interval][last_refresh]["1. open"])

    COURS = data[time_interval][last_refresh]["1. open"]

    list_des_valeurs_de_cours.append(COURS)

    
#_________________________________________________________________________

    #select line of MIN cours value in the json file : 

    CLOSE = 0
    
    print("Le minimum du cours de l'action est de : $",data[time_interval][last_refresh]["4. close"])

    CLOSE = data[time_interval][last_refresh]["4. close"]

    list_des_valeurs_de_cours.append(CLOSE)

    # 

#___________________________________________________________________________

    #select line of MAX cours value in the json file : (INUTILE SUITE AU CHANGEMENT DU CODE)

    # MAX = 0

    # print("Le maximum du cours de l'action est de : $",data[time_interval][last_refresh]["2. high"],"\n")

    # MAX = data[time_interval][last_refresh]["2. high"]

    # list_des_valeurs_de_cours.append(MAX)

    
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

    api = tweepy.API(auth, wait_on_rate_limit=True)

    if compteur_en_baisse == 1:
        heures = 'heure'
    else:
        heures = 'heures'

    status = "Le cours est en baisse depuis",compteur_en_baisse,heures,"! - Il est actuellement à",prix_en_baisse,"US Dollars."
    status = ' '.join(str(i) for i in status)
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

    api = tweepy.API(auth, wait_on_rate_limit=True)

    if compteur_en_hausse == 1:
        heures = 'heure'
    else:
        heures = 'heures'

    status = "Le cours est en baisse depuis",compteur_en_hausse,heures,"! - Il est actuellement à",prix_en_hausse,"US Dollars."
    status = ' '.join(str(i) for i in status)
    api.update_status(status=status)

    return 0

#____________________________________________________________________________

compteur_en_hausse = 0
compteur_en_baisse = 0

while True:

    valeur_de_cours()

    if list_des_valeurs_de_cours[0] > list_des_valeurs_de_cours[1]:     # open > close
        compteur_en_hausse += 1
        
        if compteur_en_hausse == 1:
            heures = 'heure'
        else:
            heures = 'heures'

        print("Analyse : \n")
        print("Le cours est en hausse depuis",compteur_en_hausse,heures,"! \n")

        tweet_avertir_max(compteur_en_hausse,list_des_valeurs_de_cours[1])

        compteur_en_baisse = 0
        list_des_valeurs_de_cours = []
    
    elif list_des_valeurs_de_cours[0] < list_des_valeurs_de_cours[1]:    # open > close
        compteur_en_baisse += 1

        if compteur_en_baisse == 1:
            heures = 'heure'
        else:
            heures = 'heures'

        print("Analyse : \n")
        print("Le cours est en baisse depuis",compteur_en_baisse,heures,"! \n")

        tweet_avertir_min(compteur_en_baisse,list_des_valeurs_de_cours[1])

        compteur_en_hausse = 0
        list_des_valeurs_de_cours = []

    else :
        print("Le cours est resté stable ! ")
    
    print("Mise à jour dans une heure...\n")
    
    time.sleep(3600) # = 15min (900) / 1h (3600) / 1 jour (86400)
