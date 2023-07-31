import subprocess
subprocess.check_call(['pip', 'install', 'requests'])
import os
import importlib
import requests
import tkinter as tk
from tkinter import simpledialog, filedialog
import configparser


# Function to download an image from the given URL
def download_image(url, folder_path, image_name):
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(folder_path, image_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {image_name}")
        return True
    else:
        print(f"Failed to download: {image_name}")
        return False

# Function to download images with the specified tag
def download_images_with_tag(tag, num_images, api_key, download_location="."):
    num_images_per_request = 30  # Limit per API request
    num_requests = (num_images - 1) // num_images_per_request + 1  # Calculate number of requests needed

    folder_name = os.path.join(download_location, f"unsplash_reg_images_{tag}")
    os.makedirs(folder_name, exist_ok=True)
    downloaded_count = 0

    for request_num in range(num_requests):
        page_num = request_num + 1
        url = f'https://api.unsplash.com/photos/random/?client_id={api_key}&count={num_images_per_request}&query={tag}&page={page_num}'

        response = requests.get(url)
        if response.status_code == 200:
            images_data = response.json()

            for idx, image_data in enumerate(images_data):
                image_url = image_data['urls']['raw']
                image_name = f"{tag}_{downloaded_count}.jpg"  # Use the total count as the index
                if download_image(image_url, folder_name, image_name):
                    downloaded_count += 1
                    if downloaded_count == num_images:  # Stop if desired number of images is reached
                        break

    open_folder(folder_name)
    print(f"All {downloaded_count} images downloaded.")
    root.destroy()  # Close the GUI window after download


    open_folder(folder_name)
    print(f"All {downloaded_count} images downloaded.")
    root.destroy()  # Close the GUI window after download
# Function to open the folder where images are stored
def open_folder(folder_path):
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(folder_path)
        elif os.name == 'posix':  # For Linux or macOS
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, folder_path])
    except Exception as e:
        print(f"Failed to open folder: {e}")

# Function to handle GUI button click event
def on_download_button_click():
    search_tag = entry_tag.get()
    num_images = int(entry_num_images.get())
    api_key = get_unsplash_api_key()
    download_images_with_tag(search_tag, num_images, api_key, download_location.get())  # Pass the chosen download location

# Function to handle GUI button click event for "Choose Download Location"
def on_choose_location_click():
    chosen_location = filedialog.askdirectory()
    if chosen_location:
        download_location.set(chosen_location)
        
# Function to get the Unsplash API key from the configuration file
def get_unsplash_api_key():
    config = configparser.ConfigParser()
    if os.path.exists("config.ini"):
        config.read("config.ini")
        return config.get("Settings", "api_key", fallback="")
    return ""

# Function to handle "Edit Unsplash API Key" button click event
def on_edit_api_key_click():
    previous_api_key = get_unsplash_api_key()
    new_api_key = simpledialog.askstring("Edit API Key", "Enter your Unsplash API Key:", initialvalue=previous_api_key)

    if new_api_key:
        # Save the API key to the configuration file for subsequent runs
        config = configparser.ConfigParser()
        config["Settings"] = {"api_key": new_api_key}
        with open("config.ini", "w") as config_file:
            config.write(config_file)

# Create GUI window
root = tk.Tk()
root.title("Unsplash Image Downloader")

# Set the size of the GUI window
window_width = 800  # Increase the width
window_height = 300  # Increase the height
root.geometry(f"{window_width}x{window_height}")

# Create input fields and labels with increased font size
label_tag = tk.Label(root, text="Enter the search tag for Unsplash images:", font=("Arial", 16))
label_tag.pack()
entry_tag = tk.Entry(root, font=("Arial", 16))
entry_tag.pack()

label_num_images = tk.Label(root, text="Enter the number of images you want to download:", font=("Arial", 16))
label_num_images.pack()
entry_num_images = tk.Entry(root, font=("Arial", 16))
entry_num_images.pack()

# Create download button with increased font size
download_button = tk.Button(root, text="Download Images", font=("Arial", 16), command=on_download_button_click)
download_button.pack()

# Create "Edit Unsplash API Key" button with increased font size
edit_api_key_button = tk.Button(root, text="Edit Unsplash API Key", font=("Arial", 16), command=on_edit_api_key_click)
edit_api_key_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create "Choose Download Location" button with increased font size
choose_location_button = tk.Button(root, text="Choose Download Location", font=("Arial", 16), command=on_choose_location_click)
choose_location_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a Tkinter StringVar to store the download location
download_location = tk.StringVar()

root.mainloop()
