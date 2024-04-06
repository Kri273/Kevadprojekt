from tkinter import *
import sqlite3

root = Tk()
root.title("Food Calories Search")
root.iconbitmap('food.ico')
root.geometry("500x500")


# Lisa andmete näitamine
label_displayed = False
my_label = None
def display_result():
    selected_item = my_list.get(ANCHOR)
    global label_displayed
    global my_label
    
    if selected_item:
        food_name, calories = selected_item.split(": ")
        calorie_value = int(calories.strip().split()[0])
        if not label_displayed:
            my_label = Label(root, text=f"Food: {food_name}\nCalories: {calories}\nServing: 100g", font=("Arial", 18))
            my_label.pack(pady=20)
            label_displayed = True
        else:
            my_label.config(text=f"Food: {food_name}\nCalories: {calories}\nServing: 100g")

        # Värvi määramine kalorite väärtusel
        if calorie_value < 50:
            my_label.config(fg="green")
        elif calorie_value > 120:
            my_label.config(fg="red")
        else:
            my_label.config(fg="black")



# Uuendab listi kasti
def update(data):
    my_list.delete(0, END)
    data.sort()

    # Lisab näited kasti
    for item in data:
        my_list.insert(END,  item)
# Uuenda sisestuskasti kui listis vajutatakse    
def fillout(e):
    my_entry.delete(0, END)
    my_entry.insert(0, my_list.get(ANCHOR))

def check(e):
    typed = my_entry.get().lower()

    if typed == '':
        data = names
    else:
        data = []
        for item in names:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)
# Enteri vajutamine
def enter_pressed(e):
    display_result()
    
    

# Teeb sildi
my_label = Label(root, text="Search for your food...", font=("Arial", 18), fg="grey")
my_label.pack(pady=5)

# Sisestuskast
my_entry = Entry(root, font=("Arial", 20))
my_entry.pack(pady=5)

# Teeb nupu
button = Button(root, text="Search", font=("Arial", 12), fg="blue", bg="lightblue", command=display_result)
button.pack(pady=5, padx=5)

# Listi kast
my_list = Listbox(root, width=50)
my_list.pack(pady=20)

# Andmebaasist andmete võtmine
conn = sqlite3.connect('calories.db')
cursor = conn.cursor()

cursor.execute('SELECT DISTINCT name, calories FROM FoodProducts')
data = cursor.fetchall()
names = [f"{name}: {calories}" for name, calories in data]
update(names)


# Listile vajutamiseks
my_list.bind("<<ListboxSelect>>", fillout)
my_entry.bind("<KeyRelease>", check)
my_list.bind('<Return>', enter_pressed)


conn.close()
root.mainloop()