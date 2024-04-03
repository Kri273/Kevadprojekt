from tkinter import *
import sqlite3

root = Tk()
root.title("Food Calories Search")
root.iconbitmap('food.ico')
root.geometry("500x500")


result_window = None
# Uue akna tegemine
def display_result():
    selected_item = my_list.get(ANCHOR)
    global result_window
    if result_window:
        result_window.destroy()

    if selected_item:
        food_name, calories = selected_item.split(": ")
        result_window = Toplevel(root)
        result_window.title("Food Result")
        result_window.iconbitmap('food.ico')
        result_window.geometry("300x100")
        # Paneb "Food results" alla paremasse äärde
        result_window.geometry(f"+{root.winfo_x() + root.winfo_width() - 300}+{root.winfo_y() + root.winfo_height() - 100}")



        result_label = Label(result_window, text=f"Food: {food_name}\nCalories: {calories}\nServing: 100g")
        calorie_value = int(calories.strip().split()[0])



        # Set color based on calorie value
        if calorie_value < 50:
            result_label.config(fg="green")
        elif calorie_value > 120:
            result_label.config(fg="red")

        result_label.pack(pady=20)

# Uuendab listi kasti
def update(data):
    # Tühjendab
    my_list.delete(0, END)
    # Sorteerib tähestikulises järjekorras
    data.sort()

    # Lisab näited kasti
    for item in data:
        my_list.insert(END,  item)
# Uuenda sisestuskasti kui listis vajutatakse    
def fillout(e):
    # Kustutab tekstikasti kirjutatud asjad
    my_entry.delete(0, END)
    
    # Lisab tekstikasti valitud eseme
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
# Enter vajutamisel avab uue akna
def enter_pressed(e):

    display_result()
    
    

# Teeb sildi
my_label = Label(root, text="Search for your food...", font=("Arial", 18), fg="grey")
my_label.pack(pady=20)

# Sisestuskast
my_entry = Entry(root, font=("Arial", 20))
my_entry.pack(pady=10)


# Listi kast
my_list = Listbox(root, width=50)
my_list.pack(pady=40)


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

