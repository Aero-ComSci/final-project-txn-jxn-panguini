import tkinter as tk
from tkinter import messagebox
import base64
import api
import random

root = tk.Tk()
root.geometry("550x650")
root.title("Weather App")
root.configure(bg="#e0f7fa")

weather_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.RIDGE)
weather_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

suggestions = ["Honolulu", "San Diego", "Lisbon", "Porto", "Cancun", "Puerto Vallarta", "Mexico City", "Dallas", "Miami", "Fort Lauderdale", "Tampa",
               "Bali", "Kuala Lumpur", "Manila", "Tokyo", "Paris", "Barcelona", "Machu Picchu", "Valencia", "Madrid", "Antigua", "Cairo", "Pheonix", "Dublin",
               "London", "Rome", "Milan", "Naples", "Venice", "Florence"]

placeholder = tk.PhotoImage(width=64, height=64)
for x in range(64):
    for y in range(64):
        placeholder.put("#cccccc", (x, y))

icon_label = tk.Label(weather_frame, image=placeholder, bg="#ffffff")
icon_label.image = placeholder
icon_label.pack(pady=10)

result_label = tk.Label(weather_frame, text="Weather info will appear here",
                        font=("Helvetica", 14, "bold"),
                        bg="#ffffff", fg="#333333", justify="left")
result_label.pack(pady=10)

recommendations_label = tk.Label(weather_frame, text="Some suggestions are: ",
                        font=("Helvetica", 14, "bold"),
                        bg="#ffffff", fg="#333333", justify="center", pady=10)
recommendations_label.pack(pady=100)

def updateRecommendationText():
    recommendationText = "Some suggestions are: "
    for i in range(1, 6):
        recommendationText += "\n" + random.choice(suggestions)

    recommendations_label.config(text=recommendationText)

updateRecommendationText()

input_frame = tk.Frame(root, bg="#e0f7fa")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter city name:", font=("Helvetica", 14, "bold"),
         bg="#e0f7fa").grid(row=0, column=0, padx=5, pady=5)

city_entry = tk.Entry(input_frame, font=("Helvetica", 12), bd=2, relief=tk.SOLID)
city_entry.grid(row=0, column=1, padx=5, pady=5, ipady=4)  # Increased padding inside entry box

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return
    
    try:
        weather, temp, name, country, weathericon, windspeed, region = api.get_weather_data(city)
        
        if weathericon.startswith("//"):
            weathericon = "http:" + weathericon

        icon_response = api.requests.get(weathericon)
        if icon_response.status_code == 200:
            b64_data = base64.b64encode(icon_response.content).decode('utf-8')
            photo = tk.PhotoImage(data=b64_data)
            icon_label.config(image=photo)
            icon_label.image = photo
        else:
            messagebox.showerror("Error", "Could not load weather icon image.")

        result_text = "Location: " + name + ", " + region + ", " + country + "\n"
        result_text += "Weather: " + weather + "\n"
        result_text += "Temperature: " + str(temp) + "°F\n"
        result_text += "Wind Speed: " + str(windspeed) + " mph"

        if not region:
            result_text = "Location: " + name + ", " + country + "\n"
            result_text += "Weather: " + weather + "\n"
            result_text += "Temperature: " + str(temp) + "°F\n"
            result_text += "Wind Speed: " + str(windspeed) + " mph"

        result_label.config(text=result_text)
        updateRecommendationText()

    except Exception as e:
        messagebox.showerror("Error", str(e))

get_weather_button = tk.Button(input_frame, text="Get Weather", command=get_weather,
                               font=("Helvetica", 12, "bold"), bg="#00796b",
                               fg="white", width=15, height=1)
get_weather_button.grid(row=0, column=2, padx=10, pady=5)

root.mainloop()
