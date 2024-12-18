from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


class DiverScraper:
    """
    DiverScraper is a Selenium-based web scraper designed to extract specific article data from a webpage.
    It filters orders based on pre-defined conditions and scrapes data such as description and quantity 
    for items of interest.

    Attributes:
        username (str): Username for login.
        password (str): Password for login.
        team (str): Team name to filter data.
        driver (webdriver): Selenium WebDriver instance for Chrome.
        specific_materials (set): A set of material names to identify relevant articles during scraping.
    """
    def __init__(self, username, password, team):
        """
        Initialize DiverScraper with user credentials and team filter.

        Args:
            username (str): The login username.
            password (str): The login password.
            team (str): The team name for filtering orders.
        """
        self.username = username
        self.password = password
        self.team = team
        self.service = Service(ChromeDriverManager().install())
        self.options = Options() 
        self.options.add_argument("--disable-notifications")  # Disable browser notifications
        self.options.add_argument("--headless")  # Run in headless mode (no GUI)
        self.driver = webdriver.Chrome(service=self.service)
        self.specific_materials = set(["Dibond", "Plexi", "PVC3MM", "entretoises"])

    def clean_search_filters(self):
        """
        Clears all search filters on the web page. This resets previous filter inputs 
        like order number, client name, and other fields.
        """
        # Clear each filter input field
        filter_ids = ['filter-ref', 'filter-ct-number', 'filter-societe',
                      'filter-site', 'filter-site-address', 'filter-site-contact', 'filter-date']

        for field_id in filter_ids:
            field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, field_id)))
            field.clear()

        # Submit the cleared filters
        field.send_keys(Keys.RETURN)

    def apply_search_filters(self):
        """
        Applies search filters to the page. Specifically:
        - Filters for orders with status 'BAT validé'.
        - Filters by team name provided during initialization.
        """
        try:
            # Open status filter and select 'BAT validé'
            statut_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-id='filter-status']"))
            )
            statut_button.click()
            option_bat_valide = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='BAT validé']"))
            )
            option_bat_valide.click()
            if self.team != "Tous":
                # Open team filter and select specified team
                groupe_button = WebDriverWait(self.driver, 10).until(
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
        """
        Closes any pop-up windows that may appear on the page.
        """
        try:
            popup_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'OK') or contains(text(),'Valider') or contains(text(),'Fermer')]"))
            )
            popup_button.click()
        except Exception as e:
            print(f"{e}")

    def scrape_data_from_order_page(self, commande_id):
        """
        Scrapes article data from an individual order page.

        Args:
            commande_id (str): The ID of the order being scraped.

        Returns:
            list[dict]: A list of dictionaries, each containing 'Description' and 'Quantité' of an article.
        """
        articles = []
        try:
            # Wait for the articles table to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'dataTable')]/tbody"))
            )
            lignes_articles = self.driver.find_elements(By.XPATH, "//tr[contains(@class, 'even') or contains(@class, 'odd')]")

            for ligne in lignes_articles:
                try:
                    description = ligne.find_element(By.XPATH, ".//td[1]").text
                    quantite = ligne.find_element(By.XPATH, ".//td[4]").text
                    quantite = int(quantite) if quantite else "Inconnue"

                    # Check if material is in specific materials
                    if any(material.lower() in description.lower() for material in self.specific_materials):
                        articles.append({"Description": description.strip(), "Quantité": quantite})

                    # Handle "divart" or "diver" collapsible articles
                    if "divart" in description.lower() or "diver" in description.lower():
                        collapse_button = ligne.find_element(By.XPATH, ".//td[1]//a[@data-toggle='collapse']")
                        collapse_button.click()
                        diver_specific = ligne.find_element(By.XPATH, ".//td[1]//div[contains(@class,'collapse') and contains(@class,'in')]").text
                        quantite = ligne.find_element(By.XPATH, ".//td[4]").text
                        quantite = int(quantite) if quantite else "Inconnue"
                        articles.append({"Description": diver_specific.strip(), "Quantité": quantite})
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'une ligne pour la commande {commande_id}: {e}")
        except Exception as e:
            print(f"Erreur lors de l'extraction des données pour la commande {commande_id} : {e}")
        return articles

    def run_scraper(self):
        """
        Loops through all order pages, scrapes relevant data, and navigates through pagination.

        Returns:
            list[dict]: A list of dictionaries containing order ID and its articles.
        """
        commandes = []
        current_page = 1
        try:
            # Navigate through pages
            while True:
                commande_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/commande/view/')]")
                print(len(commande_elements))
                for element in commande_elements:
                    commande_url = element.get_attribute("href")
                    commande_id = element.text

                    self.driver.execute_script("window.open(arguments[0], '_blank');", commande_url)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    time.sleep(2)

                    self.close_popups()
                    articles = self.scrape_data_from_order_page(commande_id)
                    commandes.append({"Référence": commande_id, "Articles Spécifiques": articles})

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                # Handle pagination
                try:
                    next_button = self.driver.find_element(By.XPATH, "//a[@title='Page Suivante']")
                    next_button.click()
                    time.sleep(3)
                    current_page += 1
                except:
                    print("Dernière page atteinte, arrêt de la boucle.")
                    break
        except Exception as e:
            print(f"Erreur lors de l'extraction des commandes : {e}")
        self.driver.quit()
        return commandes

    def run_script(self):
        """
        Main function that runs the scraper:
        - Logs in to the website.
        - Clears and applies search filters.
        - Scrapes data and returns the results.

        Returns:
            list[dict]: A list of orders with their associated articles.
        """
        self.driver.get("https://plans.desautel-sai.fr/plans/commande/list")
        time.sleep(2)

        # Login
        login_box = self.driver.find_element(By.ID, "username")
        password_box = self.driver.find_element(By.ID, "password")
        login_box.send_keys(self.username)
        password_box.send_keys(self.password)
        login_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # Filters and scraping
        self.clean_search_filters()
        time.sleep(2)
        self.apply_search_filters()
        data = self.run_scraper()
        return data
