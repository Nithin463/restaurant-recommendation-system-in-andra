import pandas as pd       
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time



localities = [
"https://www.zomato.com/vijayawada/labbipet-restaurants",
"https://www.zomato.com/vijayawada/auto-nagar-restaurants",
"https://www.zomato.com/vijayawada/gurunanak-colony-restaurants",
"https://www.zomato.com/vijayawada/governorpet-restaurants",
"https://www.zomato.com/vijayawada/poranki-restaurants",
"https://www.zomato.com/vijayawada/islampet-restaurants",
"https://www.zomato.com/vijayawada/gollapudi-restaurants",
"https://www.zomato.com/vijayawada/mangalagiri-restaurants",
"https://www.zomato.com/vijayawada/gandhi-nagar-restaurants",
"https://www.zomato.com/vijayawada/tadepalli-restaurants",
"https://www.zomato.com/vijayawada/christurajupuram-restaurants",
"https://www.zomato.com/vijayawada/gunadala-restaurants",
"https://www.zomato.com/vijayawada/gannavaram-restaurants",
"https://www.zomato.com/vijayawada/krishna-lanka-restaurants",
"https://www.zomato.com/vijayawada/ramavarappadu-restaurants",
"https://www.zomato.com/vijayawada/machavaram-restaurants",
"https://www.zomato.com/vijayawada/pnt-colony-restaurants",
"https://www.zomato.com/vijayawada/enikepadu-restaurants",
"https://www.zomato.com/vijayawada/shri-ramachandra-nagar-restaurants",
"https://www.zomato.com/vijayawada/payakapuram-restaurants",
"https://www.zomato.com/vijayawada/madhura-nagar-restaurants"

]

all_urls = []
all_rest_name = []
all_ratings = []
all_price = []
all_cuisine = []
all_opening_hours = []
all_locations = []
all_signature_dishes = []  
all_special_features = []  
all_safety_measures = []  
all_address = []
more_information = []

driver = webdriver.Chrome()

for link in localities: 
    
    driver.get(link)
    time.sleep(2)

    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.findAll('div', class_='jumbo-tracker')

    for parent in divs:
        
        name_tag = parent.find("h4")
        if name_tag is not None:
            rest_name = name_tag.text.strip()
            link_tag = parent.find("a")
            restaurant_link = urljoin("https://www.zomato.com", link_tag.get('href')) if link_tag else None

            try:
                driver.get(restaurant_link)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                time.sleep(2) 

                inner_soup = BeautifulSoup(driver.page_source, 'html.parser')

                rating_tag = parent.div.a.next_sibling.div.div.div.div.div.div.div
                rating_value = rating_tag.text.strip() if rating_tag else 'Not available'


                price_tag = parent.div.a.next_sibling.p.next_sibling
                price_value = price_tag.text.strip() if price_tag else 'Not available'

                cuisine_tag = parent.div.a.next_sibling.p
                cuisine_value = cuisine_tag.text.strip() if cuisine_tag else 'Not available'

                open_timing_tag = inner_soup.find('span', class_='sc-kasBVs dfwCXs')
                open_timing_value = open_timing_tag.text.strip() if open_timing_tag else 'Not available'

                location_tag = inner_soup.find('a', class_='sc-clNaTc vNCcy')
                location_value = location_tag.text.strip() if location_tag else 'Not available'

                popular_dishes_tag = inner_soup.find('h3', text='Popular Dishes')
                signature_dishes_text_value = popular_dishes_tag.find_next('p').text.strip() if popular_dishes_tag else 'Not available'

                people_say_tag = inner_soup.find('h3', text='People Say This Place Is Known For')
                special_features_text_value = people_say_tag.find_next('p').text.strip() if people_say_tag else 'Not available'

                safety_measures_section_1 = inner_soup.find('section', class_='sc-bgxRrC fHqOaY')
                safety_measures_value_list_items_1 = safety_measures_section_1.find_all('p') if safety_measures_section_1 else []

                safety_measures_section_2_items = inner_soup.find_all('p', class_='sc-1hez2tp-0 fvARMW')  
                
                all_safety_measures_items = [item.text.strip() for item in safety_measures_value_list_items_1]
                all_safety_measures_items += [item.text.strip() for item in safety_measures_section_2_items]

                safety_measures_value_final = ", ".join(all_safety_measures_items) if all_safety_measures_items else 'Not available'

                address_section = inner_soup.find('p', class_ ="sc-bFADNz fMQfFo")
                address_value = address_section.text.strip() if address_section else 'Not available'

                more_info_section = inner_soup.find('h3', text='More Info')

                if more_info_section:
                    more_info_container = more_info_section.find_next('div', class_='sc-bke1zw-0')
                    more_info_features = []

                    if more_info_container:
                        p_tags = more_info_container.find_all('p', class_='sc-1hez2tp-0')
                        for p_tag in p_tags:
                            more_info_features.append(p_tag.text.strip())

                    more_info_value = ", ".join(more_info_features) if more_info_features else 'Not available'
                else:
                    more_info_value = 'Not available'

                all_urls.append(restaurant_link)
                all_rest_name.append(rest_name)
                all_ratings.append(rating_value)
                all_price.append(price_value)
                all_cuisine.append(cuisine_value)
                all_opening_hours.append(open_timing_value)
                all_locations.append(location_value)
                all_signature_dishes.append(signature_dishes_text_value)
                all_special_features.append(special_features_text_value)
                all_safety_measures.append(safety_measures_value_final)
                all_address.append(address_value)
                more_information.append(more_info_value)

            except Exception as e:
                print(f"Error processing {restaurant_link}: {e}")
                continue  
            

    

df = pd.DataFrame({
    'links': all_urls,
    'names': all_rest_name,
    'ratings': all_ratings,
    'price for two': all_price,
    'cuisine': all_cuisine,
    'opening & closing time': all_opening_hours,
    'location': all_locations,
    'signature dishes': all_signature_dishes,  
    'special features': all_special_features,  
    'safety measures': all_safety_measures,     
    'address': all_address,
    'more_info': more_information

})

df.to_csv('andra_restaurants_data.csv', index=False)
print("Data collected and stored in andra_restaurants_data.csv")
driver.close()


