import requests
import time

# Replace with your ESP32's IP address
esp32_ip = "http://192.168.43.233"

def send_command(command):
    try:
        response = requests.get(f"{esp32_ip}/{command}")
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error communicating with ESP32:", e)



def startShooting():
    
    send_command("SERVO1-")
    time.sleep(0)
    send_command("SERVO1-")
    time.sleep(0)
    send_command("SERVO1-")
    time.sleep(0)
    send_command("TRIGGER") 
    time.sleep(0)
    send_command("SERVO1+")
    time.sleep(1)
    send_command("SERVO1+")
    time.sleep(1)
    send_command("SERVO1+")
    
 
startShooting()    
# while True:
#     print("\nSelect an option:")
#     print("1. Move Servo 1: 30 degrees left")
#     print("2. Move Servo 1: 30 degrees right")
#     print("3. Trigger Servo 2 (Gun)")
#     print("4. Exit")

#     choice = input("Enter your choice: ")

#     if choice == "1":
#         send_command("SERVO1-")  # Decrement Servo 1 angle
#     elif choice == "2":
#         send_command("SERVO1+")  # Increment Servo 1 angle
#     elif choice == "3":
#         send_command("TRIGGER")  # Trigger the gun
#     elif choice == "4":
#         print("Exiting...")
#         break
#     else:
#         print("Invalid choice. Please try again.")