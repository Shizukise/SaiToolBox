import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


class DiverScraper():

    def __init__(self,username,password,team):
        self.username = username
        self.password = password
        self.team = team
        self.service = Service(ChromeDriverManager().install())
        self.options = Options()
        self.options.add_argument("--start-maximized")  
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(service=self.service)
        self.specific_materials = set(["Dibond", "Dibond", "Dibond", "Plexi", "PVC3MM","entretoises"])

    def apply_search_filters(self):
        try:
            statut_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-id='filter-status']")) #Opens status collapse
            )
            statut_button.click()
            option_bat_valide = WebDriverWait(self.driver, 10).until(               #Waits for collapse button to be opened and selects
                EC.element_to_be_clickable((By.XPATH, "//span[text()='BAT validé']"))   #BAT validé from the list
            )
            option_bat_valide.click()  
            groupe_button = WebDriverWait(self.driver, 10).until(                                       #Same process for team filter option
                EC.element_to_be_clickable((By.XPATH, "//button[@data-id='filter-designer-group']"))
            )
            groupe_button.click()
            team_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{self.team}']"))
            )
            team_select.click()
        except Exception as e:
            print(f"Erreur lors de l'application des filtres : {e}")

    def close_popups(self):
        try:
            popup_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'OK') or contains(text(),'Valider') or contains(text(),'Fermer')]"))
            )
            popup_button.click()
            print("Pop-up fermé avec succès.")
        except:
            print("Aucun pop-up à fermer.")

    def scrape_data_from_order_page(self,commande_id):
        articles = []
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'dataTable')]/tbody"))
            )
            # Waits for ordered items table to be shown. then grabs all tr with class 'even' or 'odd'.[This are the classes defined for tr in this table]
            lignes_articles = self.driver.find_elements(By.XPATH, "//tr[contains(@class, 'even') or contains(@class, 'odd')]")
            for ligne in lignes_articles:
                try:
                    description = ligne.find_element(By.XPATH, ".//td[1]").text #This is one of the data wanted. First index at the row contains
                                                                                #The name of the item. 
                    quantite_index = ligne.find_elements(By.XPATH, ".//td[4]")[0].text #Next data wanted is quantity. This is at index 4 for this tr.
                    quantite = int(quantite_index) if quantite_index else "Inconnue"   #Hold it as an integer
                    if any(material.lower().strip().lower() in description.lower() for material in self.specific_materials):
                        #After grabbing name and quantity, we store it if it is one of the materials in self.specific_materials
                        #This is what is being scraped
                        articles.append({ 
                            "Description": description.strip(),
                            "Quantité": quantite
                        })
                    if "divart" in description.lower() or "diver" in description.lower():
                        #This is the most important piece of data being scraped. When the name of the item is not shown directly in the tr
                        #It has a name of divart (stands for diverse articles) and needs to be collapsed to see collapse in element
                        #This collapsed id element will contain the name of the specific article wich is user created
                        try:
                            # variables that end with W are here to force a wait, hence make sure element is visible before trying to continue with the script
                            collapse_buttonW = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, ".//td[1]//a[@data-toggle='collapse']")))
                            collapse_button = ligne.find_element(By.XPATH, ".//td[1]//a[@data-toggle='collapse']")
                            collapse_button.click()
                            diver_specificW = WebDriverWait(self.driver, 10).until(
                                EC.visibility_of_element_located(
                                    (By.XPATH, ".//td[1]//div[contains(@class,'collapse') and contains(@class,'in')]")
                                )
                            )
                            diver_specific = ligne.find_element(By.XPATH, ".//td[1]//div[contains(@class,'collapse') and contains(@class,'in')]").text
                            quantite_elementDiv = ligne.find_elements(By.XPATH, ".//td[4]")[0].text
                            quantiteDiv = int(quantite_elementDiv) if quantite_elementDiv else "Inconnue"
                            articles.append({
                                "Description": diver_specific.strip(),
                                "Quantité": quantiteDiv
                            })
                        except Exception as e:
                            print(f"Error while handling collapse for the current row: {e}")
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'une ligne pour la commande {commande_id}: {e}")
        except Exception as e:
            print(f"Erreur lors de l'extraction des données pour la commande {commande_id} : {e}")

        return articles

    def run_scraper(self):
        #This is the function that will run trough all pages opening orders, and inside each order page will run the scraper
        #While storing wanted data and returning it after its done
        commandes = []
        try:
            try:
                page_input = self.driver.find_element(By.CLASS_NAME, "pagination-pf-page")
                page_input.clear() 
                page_input.send_keys("1")  
                page_input.send_keys(Keys.ENTER) 
                time.sleep(3) 
            except Exception as e:
                print(f"Erreur lors de la mise à jour de la page : {e}")
            current_page = 1 
            while True:
                # commande_elements will store all <a>tags with a link to an individual order page
                commande_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/commande/view/')]")
                for element in commande_elements:
                    commande_url = element.get_attribute("href")
                    commande_id = element.text #We store the commande id, so we can pass it to the individual scraper [That will serve only to link]
                    self.driver.execute_script("window.open(arguments[0], '_blank');", commande_url)                        #[order id to its data]
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    time.sleep(2)
                    try:
                        self.close_popups() #Some orders will trigger a pop up directly after opening
                        articles = self.scrape_data_from_order_page(commande_id)  #Then we simply scrape the data we want
                        commandes.append({
                            "Référence": commande_id,                   #and store it to later be returned
                            "Articles Spécifiques": articles
                        })
                    except Exception as e:
                        print(f"Erreur lors de l'extraction des détails pour la commande {commande_url} : {e}")
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0]) #closes current window and changes to the one window left that being handled
                try:
                    #After all orders from this page are scraped, we will check if there are any page left and continue
                    pagination = self.driver.find_element(By.XPATH, "//ul[contains(@class, 'pagination-pf-forward')]")
                    next_page_button = pagination.find_elements(By.TAG_NAME, "li")
                    if len(next_page_button) > 1 and 'disabled' in next_page_button[1].get_attribute('class').split():
                        print("Dernière page atteinte, arrêt de la boucle.")
                        break
                    next_button = self.driver.find_element(By.XPATH, "//a[@title='Page Suivante']")
                    next_button.click()
                    time.sleep(3)
                    current_page += 1
                except Exception as e:
                    print(f"Erreur lors de la recherche du bouton 'Page Suivante' ou dernière page atteinte : {e}")
                    break  
        except Exception as e:
                print(f"Erreur lors de l'extraction des commandes : {e}")
        self.driver.quit()
        return commandes

    def run_script(self):
        self.driver.get("https://plans.desautel-sai.fr/plans/commande/list")
        time.sleep(2)
        # Connexion
        login_box = self.driver.find_element(By.ID, "username")
        password_box = self.driver.find_element(By.ID, "password")
        login_box.send_keys(self.username)
        password_box.send_keys(self.password)
        login_box.send_keys(Keys.RETURN)
        time.sleep(3)
        self.apply_search_filters()
        data = self.run_scraper()
        return data

    


