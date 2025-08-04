import undetected_chromedriver as uc
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.webdriver.common.action_chains import ActionChains


def CommericalEstateScrape(city:str,page:int):
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    # base_url = f"https://www.crexi.com/properties?pageSize=60&showMap=false&page={page}"
    base_url=f'https://www.crexi.com/properties?pageSize=60&showMap=false&placeIds%5B%5D=ChIJgRo4_MQfVIgRZNFDv-ZQRog&page={page}'
    driver.get(base_url)

    time.sleep(5)  # Let JS-heavy page load
    # Locate the search input box and enter the city dynamically
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='search_term_string']"))
    )

    # Execute JS directly to set the value and fire events like we did in console
    city_script = f"""
    let input = document.querySelector('input[name="search_term_string"]');
    input.focus();
    input.value = '{city}';
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    setTimeout(() => {{
        input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', bubbles: true }}));
        input.dispatchEvent(new KeyboardEvent('keyup', {{ key: 'Enter', bubbles: true }}));
    }}, 200);
    """
    driver.execute_script(city_script)
    time.sleep(5)



    # Scroll for lazy-loading
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Wait until listings load
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "crx-property-tile-aggregate[data-cy='propertyTile']")
        )
    )

    cards = driver.find_elements(By.CSS_SELECTOR, "crx-property-tile-aggregate[data-cy='propertyTile']")
    properties = []

    for card in cards:
        try:
            price = card.find_element(By.CSS_SELECTOR, "[data-cy='propertyPrice']").text.strip()
        except:
            price = None

        try:
            name = card.find_element(By.CSS_SELECTOR, "[data-cy='propertyName']").text.strip()
        except:
            name = None

        try:
            address = card.find_element(By.CSS_SELECTOR, "[data-cy='propertyAddress']").text.strip()
        except:
            address = None

        try:
            description = card.find_element(By.CSS_SELECTOR, "[data-cy='propertyDescription']").text.strip()
        except:
            description = None
        try:
            link = card.find_element(By.CSS_SELECTOR, "a.cui-card-cover-link").get_attribute("href")
            if link.startswith("http"):
                full_link = link
            else:
                full_link = "https://www.crexi.com" + link
        except:
            full_link = None

        # try:
        #     link = card.find_element(By.CSS_SELECTOR, "a.cui-card-cover-link").get_attribute("href")
        #     full_link = "https://www.crexi.com" + link
        # except:
        #     link = None
        properties.append({
            "city": city,
            "price": price,
            "name": name,
            "address": address,
            "description": description,
            "link": full_link,
        })

    driver.quit()
    return properties


#Now scrape additional information For each Property
import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_updated_info(driver, label_text):
    try:
        labels = driver.find_elements(By.CSS_SELECTOR, "div.pdp_updated-date-label")
        for label in labels:
            if label.text.strip() == label_text:
                value = label.find_element(By.XPATH, "../div[@data-cy='value']/span").text.strip()
                return value
        return None
    except NoSuchElementException:
        return None


def get_all_details(driver):
    try:
        detail_items = driver.find_elements(By.CSS_SELECTOR, "[data-cy='details']")
        details_dict = {}
        for item in detail_items:
            try:
                label = item.find_element(By.CLASS_NAME, "detail-name").text.strip().lower()
                label = label.replace(" ", "_").replace("/", "_").replace("-", "_").replace("(", "").replace(")", "")
                value = item.find_element(By.CSS_SELECTOR, "[data-cy='detailsValue']").text.strip()
                details_dict[label] = value
            except NoSuchElementException:
                continue
        return details_dict
    except NoSuchElementException:
        return {}


def scrape_property_details(driver, url):
    driver.get(url)
    time.sleep(5)

    data = {}
    try:
        data['asking_price'] = driver.find_element(By.CSS_SELECTOR, "span.term-value.asking-price").text.strip()
    except:
        data['asking_price'] = None

    data['date_added'] = get_updated_info(driver, "Date Added")
    data['days_on_market'] = get_updated_info(driver, "Days on Market")

    details = get_all_details(driver)
    data.update(details)

    return data


def AdditionalInformation(city:str,page:int):
    df = pd.read_csv(f"data/{city}_Property_Data{page}.csv")

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    for idx, row in df.iterrows():
        url = row['link']
        print(f"Scraping {idx + 1}/{len(df)}: {url}")
        try:
            detail_data = scrape_property_details(driver, url)

            for key in detail_data.keys():
                if key not in df.columns:
                    df[key] = None

            for key, value in detail_data.items():
                df.at[idx, key] = value
        except Exception as e:
            print(f"Failed on {url}: {e}")
            continue

    driver.quit()
    df.to_csv(f"data/{city}_PropertyDataComplete{page}.csv", index=False)
    print("Scraping complete. CSV saved.")



def RunPipeline(city:str,page:int):

    """"""

    OuterData = CommericalEstateScrape(city,page)
    print(type(OuterData))
    print(OuterData)
    # data = json.loads(OuterData)
    daf = pd.DataFrame(OuterData)
    daf.to_csv(f"data/{city}_Property_Data{page}.csv", index=False)
    AdditionalInformation(city,page)


#

