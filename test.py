import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Prompt the user to enter the city name
city = input("Enter the city name: ")

# Initialize Selenium WebDriver (Chrome)
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver (Chrome)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to search for top restaurants in the given city
def search_restaurants(city):
    search_url = "https://www.google.com"
    driver.get(search_url)
    
    # Find the search box and enter the search query
    search_box = driver.find_element(By.NAME, "q")
    search_query = f"THE 10 BEST Restaurants in {city}"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    
    # Wait for the results to load
    time.sleep(3)  # Increased wait time
    
    # Print the page source for debugging
    print(driver.page_source)
    
    # Click on the link for "THE 10 BEST Restaurants in [City]"
    try:
        best_restaurants_link = driver.find_element(By.PARTIAL_LINK_TEXT, "THE 10 BEST Restaurants in")
        best_restaurants_link.click()
    except Exception as e:
        print(f"Could not find the link for the best restaurants: {e}")
        driver.quit()
        return []

    # Wait for the results to load
    time.sleep(3)  # Increased wait time
    
    # Scrape restaurant names, ratings, and reviews
    restaurants = []
    
    try:
        # Locate restaurant elements (modify XPath depending on Google's structure)
        cards = driver.find_elements(By.XPATH, '//div[@data-automation="searchResults"]')[:10]  # Limit to top 10 results
        
        for card in cards:
            try:
                # Get the restaurant name
                name = card.find_element(By.XPATH, '(//div[contains(@class,"VDEXx u")])').text
            except Exception as e:
                name = "No name available"
                print(f"Error retrieving name: {e}")

            try:
                # Extract rating (use a valid XPath to target the rating section)
                rating = card.find_element(By.XPATH, '(//span[@class="YECgr Tsrjt"]//a)').text
            except Exception as e:
                rating = "No rating available"
                print(f"Error retrieving rating: {e}")

            try:
                # Extract review count or snippet
                review = card.find_element(By.XPATH, '(//div[contains(@class,"TQNqt y")])').text
            except Exception as e:
                review = "No review data"
                print(f"Error retrieving review: {e}")

            # Append restaurant details to the list
            restaurants.append({
                'name': name,
                'rating': rating,
                'review': review
            })
    
    except Exception as e:
        print(f"An error occurred while scraping: {e}")
    
    return restaurants

# Search for the restaurants and collect data
restaurant_data = search_restaurants(city)

# Store the restaurant data in a JSON file
if restaurant_data:
    with open(f'{city}_top_restaurants.json', 'w') as json_file:
        json.dump(restaurant_data, json_file, indent=4)

    print(f"Data for top 10 restaurants in {city} has been saved to '{city}_top_restaurants.json'.")
else:
    print("No restaurant data found.")

# Close the browser session
#driver.quit()
