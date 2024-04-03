from bs4 import BeautifulSoup
import requests
import sqlite3
import re


def scrape_calories_info(url):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    rows = soup.find_all('tr')
    
    vastus = []
    for row in rows:
        food_tag = row.find('p', class_='MuiTypography-root MuiTypography-body2 css-1tg7buc')
        calories_tag = row.find('td', class_='MuiTableCell-root MuiTableCell-body MuiTableCell-alignRight MuiTableCell-sizeMedium css-yu17rd')
        
        if food_tag is not None:
            if food_tag.text == '' or food_tag.text == "1000 Island Dressing":
                continue
            else:
                food = food_tag.text
                print(food)
        else:
            continue
            
        if calories_tag is not None:
            calories = calories_tag.text
        else:
            continue
        
        print("Food:", food)
        print("Calories:", calories)

        vastus.append((food, calories))
        
    return vastus

def create_database(vastused):
    conn = sqlite3.connect('calories123.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS FoodProducts
                 (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Serving_Size TEXT, Calories TEXT)''')
    
    # Insert data into the table only if it doesn't already exist and meets certain conditions
    for item in vastused:
        print(item)
        food, calories = item
        
        # Check if the food name meets certain conditions before inserting
        if item not in vastused:
            print("yes")  # Skip specific food item
            c.execute("INSERT INTO FoodProducts (Name, Serving_Size, Calories) VALUES (?, '100g', ?)", (food, calories))
     
    conn.commit()
    conn.close()

if __name__ == "__main__":
    urllist = ['https://www.calories.info/food/mushrooms', 'https://www.calories.info/food/fish-seafood', 'https://www.calories.info/food/nuts-seeds', 'https://www.calories.info/food/tofu-vegan-products', 'https://www.calories.info/food/supplements-protein-powder', 'https://www.calories.info/food/sauces-gravy-dressing-spreads']

    for url in urllist:
        vastused = scrape_calories_info(url)
        #print(vastused)
        create_database(vastused)