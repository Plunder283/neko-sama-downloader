import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os
import re
import time
import random
import urllib
import configparser
import traceback
import sys
import ctypes
import msvcrt
import requests
import subprocess

# options pour lancer le navigateur en mode headless
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")
options.add_argument("--window-size=500,500")
options.add_argument("--disable-extensions")  # désactiver toutes les extensions
options.add_argument("--disable-dev-shm-usage")  # éviter les problèmes de mémoire partagée
options.add_argument("--disable-blink-features=AutomationControlled") # éviter la détection du navigateur

##################################################################################################################################################
def print_logo():
    x = """

          .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'   -Sk_   `98v8P' DOWNLOAD `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
                               `             '
                         
██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ 
██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗
██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║
██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║
██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝
╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                    
       Coded By: -Sk_ https://github.com/Soma-Yukihira     
       Beta Testers: Plunder 
    """
    for line in x.split("\n"):
        print(line)
        time.sleep(0.01)

##################################################################################################################################################
def launch_fullscreen():
    # Obtenir le handle de la fenêtre de la console
    console_handle = ctypes.windll.kernel32.GetConsoleWindow()

    # Attendre 3 secondes pour que l'utilisateur puisse appuyer sur une touche
    print("Lancement en plein écran dans 3 secondes. Appuyez sur Entrée pour annuler...")
    for i in range(3, 0, -1):
        if msvcrt.kbhit():  # si l'utilisateur tape une touche
            print("\nLancement annulé.")
            return
        print(i, end=" ", flush=True)
        time.sleep(1)

    # Maximiser la fenêtre
    ctypes.windll.user32.ShowWindow(console_handle, 3)
##################################################################################################################################################

def test_connexion():
    # Vérifier la connexion internet
    connected = False
    while not connected:
        try:
            response = requests.get("http://www.google.com")
            print("connexion à google.com en cours...")
            if response.status_code == 200:
                connected = True
                print('connexion réussi.')
            response = requests.get("http://httpbin.org/ip")
            public_ip = response.json()["origin"]
            print(f"        Adresse IP avant proxy : {public_ip}\n")
        except requests.exceptions.ConnectionError:
            pass

        if not connected:
            print("Connexion internet absente. Nouvelle tentative dans 5 secondes...")
            time.sleep(5)

##################################################################################################################################################
def read_txt_proxy_section(section_name):
    try:
        # Lire les informations de proxy à partir du fichier de configuration
        config = configparser.ConfigParser()
        config.read('proxy.txt')
        ip_port = config.get(section_name, 'ip')
        ip, port = ip_port.split(':')
        options.add_argument(f"--proxy-server={ip}:{port}")
        print(f"L'adresse IP du proxy est : {ip}")
        print(f"Le port du proxy est : {port}\n")
        return ip, port
    except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError):
        print("Le fichier de configuration du proxy n'existe pas ou est mal formaté. Le script sera exécuté sans proxy.\n")
        return None

###################################
def read_txt_proxy_default():
    return read_txt_proxy_section('proxy')

###################################
def read_txt_proxy_perso():
    # Demander l'adresse IP et le port du proxy à l'utilisateur
    print("Format de l'adresse IP du proxy : adresse_IP:port")
    enter_proxy = input("Entrez l'adresse IP du proxy : ")
    # Vérifier si l'entrée du proxy est bien formatée
    if ":" not in enter_proxy:
        print("     Le format du proxy est incorrect.")
        enter_proxy = input("Entrez l'adresse IP du proxy : ")
    ip, port = enter_proxy.split(':')
    options.add_argument(f"--proxy-server={ip}:{port}")
    print(f"L'adresse IP du proxy est : {ip}")
    print(f"Le port du proxy est : {port}\n")
    return ip, port


##################################################################################################################################################

 # Définir une fonction pour tester le proxy
def test_proxy_script(driver, url):
    try:
        # Charger la page à tester avec le proxy
        driver.get(url)

        # Exécuter un script JavaScript qui effectue une requête à la page et vérifie la réponse
        script = """
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '{0}', false);
            xhr.send();
            return xhr.status === 200;
        """.format(url)
        result = driver.execute_script(script)

        return result
    except Exception as e:
        print(f"Erreur de connexion via proxy : {e}")
        return False
##################################################################################################################################################

def ip_publique():
    # Récupérer l'adresse IP publique à partir de http://httpbin.org/ip
    driver.get("http://httpbin.org/ip")
    driver.execute_script("window.open('http://httpbin.org/ip');")
    public_ip = driver.find_element(By.CSS_SELECTOR, "pre").text

    print(f"L'adresse IP publique est : {public_ip}")
##################################################################################################################################################
def options_nav_no_proxy():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=500,500")
    options.add_argument("--disable-extensions")  # désactiver toutes les extensions
    options.add_argument("--disable-dev-shm-usage")  # éviter les problèmes de mémoire partagée
    options.add_argument("--disable-blink-features=AutomationControlled") # éviter la détection du navigateur
    driver = uc.Chrome(options=options)
    driver.set_window_size(500, 500)
    return driver
##################################################################################################################################################
def test_and_config_proxy(driver, ip, port):
    if test_proxy_script(driver, "http://httpbin.org/ip"):
        elapsed_time = time.time() - start_time
        print("Le proxy fonctionne correctement.")
        print(f"Fin du test du proxy. Temps écoulé : {elapsed_time:.2f} secondes.\n")
        print("Test du proxy sur neko-sama")
        if test_proxy_script(driver, "https://www.neko-sama.fr/"):
            elapsed_time = time.time() - start_time
            print("Le proxy sur neko-sama fonctionne correctement.")
            print(f"Fin du test du proxy. Temps écoulé : {elapsed_time:.2f} secondes.\n")
        else:
            elapsed_time = time.time() - start_time
            print(f"Le proxy sur neko-sama ne fonctionne pas. Temps écoulé : {elapsed_time:.2f} sec. Le script sera exécuté sans proxy.")
            driver.quit()
            driver = options_nav_no_proxy()
            print("Fin du test du proxy.\n")
    else:
        elapsed_time = time.time() - start_time
        print(f"Le proxy ne fonctionne pas. Temps écoulé : {elapsed_time:.2f} sec. Le script sera exécuté sans proxy.")
        driver.quit()
        driver = options_nav_no_proxy()
        print("Fin du test du proxy.\n")
    return driver
##################################################################################################################################################

try:
    launch_fullscreen()
    print_logo()
    test_connexion()

    # Demander à l'utilisateur de choisir une fonction de lecture de proxy
    print("    [default = 1]    [proxy perso = 2]    [no-proxy = 0]")
    function_name = input("Veuillez choisir un proxy : [1/2/0] ")

    # Exécuter la fonction choisie par l'utilisateur
    while function_name not in ["1", "2", "0"]:
        print("     Choix proxy invalide.")
        function_name = input("Veuillez choisir un proxy : [1/2/3/0] ")


    # Exécuter la fonction choisie par l'utilisateur
    if function_name == "1":
        ip, port = read_txt_proxy_default()
    elif function_name == "2":
        ip, port = read_txt_proxy_perso()
    elif function_name == "0":
        print("     Le script est lancé sans proxy\n")
        ip = None
        port = None


    #ip, port = read_txt_proxy()

    # Démarrer le navigateur
    driver = uc.Chrome(options=options)
    driver.set_window_size(500, 500)

    #Tester le proxy s'il est utilisé
    if ip and port:
        start_time = time.time()
        driver = test_and_config_proxy(driver, ip, port)
    else:
        driver.quit()
        driver = options_nav_no_proxy()

    ip_publique()
    print("Exemple URL: https://www.neko-sama.fr/anime/episode/3458-hagane-no-renkinjutsushi-fullmetal-alchemist-01_vostfr\n")

##################################################################################################################################################
    # Définir une fonction pour récupérer les URLs des épisodes
    def get_episode_urls(driver, url):
        # Naviguer vers la première page
        driver.get(url)

        # Initialiser un compteur pour les épisodes
        #episode = 1

        # Trouver le numéro de l'épisode à la fin de l'URL
        episode_number = re.search(r'\d{1,3}(?=_vostfr)', url)
        
        # Si l'episode est un film il n'a pas de numero d'episode donc on remplace le NoneType par 0 pour eviter une erreur (Plunder)
        episode_number = 0 if episode_number == None else episode_number.group()

        # Convertir le numéro de l'épisode en entier
        episode = int(episode_number)

        # Afficher le numéro de l'épisode
        print(f"Le numéro de l'épisode est : {episode}\n")

        print("Le téléchargement des url commence dans 10 secondes...")

        for i in range(10, 0, -1):
            print(i, end=' ', flush=True)
            time.sleep(1)
            print('\r', end='', flush=True)    

        #time.sleep(10)
        # Extraire le titre de la série
        title = driver.find_element(By.CSS_SELECTOR, "div.row.no-gutters h1").text

        # Supprimer les mots contenant des nombres suivis de "VOSTFR" du titre
        title = re.sub(r'\b(\d{2,4} )?VOSTFR\b', '', title)


        # Remplacer les espaces et les caractères spéciaux par des traits d'union
        filename = re.sub(r'[^\w\s-]', '', title.strip().replace(' ', '-'))

        print(f"Le fichier {filename}.txt a bien été créé.\n")

        # Stocker la dernière URL trouvée
        last_url = driver.current_url

        # Boucle pour répéter le processus de récupération de l'URL et de navigation
        while True:
            # Récupérer l'URL de l'iframe
            iframe = driver.find_element(By.ID, "un_episode")
            iframe_url = iframe.get_attribute("src")

            # Créer le dossier "url" s'il n'existe pas
            if not os.path.exists("url"):
                os.makedirs("url")

            # Enregistrer l'URL dans un fichier .txt
            with open(f"url/{filename}.txt", "a") as file:
                file.write(f"Episode {episode}: {iframe_url}\n\n")
                print(f"Episode {episode}: {iframe_url}")

                # Faire un saut de 5 lignes tous les 30 épisodes
                if episode % 30 == 0:
                    file.write('\n' * 5)

            # Incrémenter le compteur d'épisodes
            episode += 1

            # Cliquer sur le bouton "Episode suivant" après que la page soit chargée
            try:
                next_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui.button.small.with-svg-right"))
                )
                # Attendre entre 1 et 2 secondes aléatoirement
                #time.sleep(random.uniform(1, 2))
                
                next_button.click()

                # Stocker la dernière URL trouvée
                last_url = driver.current_url
                
            except:
                #pour plus tard
                #verifier les animes en cours par l'url si page 404 rencontré faire l'except
                # Trouver le numéro de l'épisode à la fin de l'URL
                try:

                    # Chercher le nombre dans l'URL à l'aide d'une expression régulière
                    number = int(re.search(r'(\d+)(?=_vostfr)', last_url).group(1))

                    # Incrémenter le nombre de 1
                    new_number = number + 1

                    # Ajouter un 0 devant le nombre si le nombre est inférieur à 10
                    if new_number < 10:
                        new_number_str = '0' + str(new_number)
                    else:
                        new_number_str = str(new_number)

                    # Remplacer le nombre dans l'URL par le nouveau nombre incrémenté
                    new_url = re.sub(r'(\d+)(?=_vostfr)', new_number_str, last_url)

                    driver.get(new_url)

                    #print(f'L\'URL actuelle est : {last_url}')
                    #print(f'L\'URL incrémentée est : {new_url}\n')

                    response = requests.get(new_url)

                    if response.status_code == 404:
                        #print(f"La page {new_url} n'a pas été trouvée.")
                        raise ValueError('La page n\'a pas été trouvée')

                     # Stocker la dernière URL trouvée
                    last_url = new_url


###########################################################################################################################################
                except:
                    if "/anime/episode" in url:
                        url = url.replace("/anime/episode/", "/anime/info/")
                        
                    if url.endswith("-01_vostfr"):
                        url = url.replace("-01_vostfr", "_vostfr")
                    elif re.search(r'-\d{2,5}_vostfr$', url):
                        url = re.sub(r'-\d{2,5}_vostfr$', '_vostfr', url) 

                    if url.endswith("-01_vf"):
                        url = url.replace("-01_vf", "_vf")
                    elif re.search(r'-\d{2,5}_vf$', url):
                        url = re.sub(r'-\d{2,5}_vf$', '_vf', url) 
                        
                    # Naviguer vers l'URL modifiée
                    driver.execute_script(f"window.location.href = '{url}';")
                    
                    # Récupérer le texte dans la balise HTML <div class="synopsis">
                    synopsis_text = driver.find_element(By.CSS_SELECTOR, "div.synopsis p").text

                    # Enregistrer le synopsis au début du fichier .txt
                    with open(f"url/{filename}.txt", "r+") as file:
                        content = file.read()
                        file.seek(0, 0)
                        file.write(f"Synopsis:\n\n{synopsis_text}\n\n{content}")
                        print(f"Le synopsis à été écrit au début du fichier\n")
                        
                    print(f"Tous les épisodes ont été téléchargés")
                    break

        # Demander une nouvelle URL
        url = input("Entrez une nouvelle URL : ")
        
        # Vérifier si l'URL est valide
        while not url.startswith("https://www.neko-sama.fr/anime/episode/"):
            print("     URL invalide. Veuillez saisir une URL valide.")
            print("Exemple URL valide : https://www.neko-sama.fr/anime/episode/7735-nanatsu-no-taizai-01_vostfr\n")
            url = input("Entrez l'URL : ")
        if url:
            get_episode_urls(driver, url)
            print("Attendre que la page soit complétement chargée...")

    # Demander la première URL
    url = input("Entrez l'URL : ")
    print("Attendre que la page soit complétement chargée...")

    # Vérifier si l'URL est valide
    while not url.startswith("https://www.neko-sama.fr/anime/episode/"):
        print("     URL invalide. Veuillez saisir une URL valide.")
        print("Exemple URL valide : https://www.neko-sama.fr/anime/episode/7735-nanatsu-no-taizai-01_vostfr\n")
        url = input("Entrez l'URL : ")
        
    get_episode_urls(driver, url)

    # Fermer le navigateur
    driver.quit()
except Exception as e:
    print(f"\nErreur : {e}")
    traceback.print_exc()
    print("\nL'invite de commande va se fermer automatiquement dans une minute.")
    time.sleep(60)
