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
    conn = sqlite3.connect('calories.db')
    c = conn.cursor()
    
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS FoodProducts
                 (Id INTEGER, Name TEXT, Serving_Size TEXT, Calories TEXT, PRIMARY KEY("Id" AUTOINCREMENT))''')
    
    # Insert data into the table
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
    urllist = ['https://www.calories.info/food/potato-products', 'https://www.calories.info/food/vegetables-legumes', 'https://www.calories.info/food/mushrooms', 'https://www.calories.info/food/salad', 'https://www.calories.info/food/fruit', 'https://www.calories.info/food/milk-dairy-products', 'https://www.calories.info/food/yogurt', 'https://www.calories.info/food/cheese', 'https://www.calories.info/food/cream-cheese', 'https://www.calories.info/food/meat', 'https://www.calories.info/food/beef-veal', 'https://www.calories.info/food/pork', 'https://www.calories.info/food/poultry-chicken-turkey', 'https://www.calories.info/food/ham-sausage', 'https://www.calories.info/food/rice-products', 'https://www.calories.info/food/bread-rolls-pastries', 'https://www.calories.info/food/pasta-noodles', 'https://www.calories.info/food/flour-grains-baking-ingredients', 'https://www.calories.info/food/cereal', 'https://www.calories.info/food/fish-seafood', 'https://www.calories.info/food/nuts-seeds', 'https://www.calories.info/food/oils-fats', 'https://www.calories.info/food/tofu-vegan-products', 'https://www.calories.info/food/supplements-protein-powder', 'https://www.calories.info/food/sauces-gravy-dressing-spreads', 'https://www.calories.info/food/chips-popcorn-snacks', 'https://www.calories.info/food/herbs-spices-tea', 'https://www.calories.info/food/desserts-pudding', 'https://www.calories.info/food/cakes-pies', 'https://www.calories.info/food/ice-cream', 'https://www.calories.info/food/sweets-chocolate-cookies-candy', 'https://www.calories.info/food/meals-dishes', 'https://www.calories.info/food/fast-food-burgers', 'https://www.calories.info/food/pizza', 'https://www.calories.info/food/sushi']

    for url in urllist:
        vastused = scrape_calories_info(url)
        #print(vastused)
        create_database(vastused)
    