from flask import Flask, render_template, request, redirect, url_for
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import time
import os
import json
import sys
import subprocess
import build_urls_file

app = Flask(__name__)

# Ensure the screenshots directory exists
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Load URLs from a text file
def load_urls():
    urls_by_date = {}
    with open('output_links.txt', 'r') as file:
        for line in file:
            date, url = line.strip().split(',', 1)
            if date not in urls_by_date:
                urls_by_date[date] = []
            urls_by_date[date].append(url)
    return urls_by_date

# Check if a URL is a scam using the API
def is_scam(url):
    api_url = "https://url-scan-api-11d8349414c2.herokuapp.com/automatic_ai_scan"
    headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.870emAVSISgWX3ofXN7ChZBchtPE0YmfPLyCizI89qs",
            "Content-Type": "application/json"
    }
    data = json.dumps({'url': url})
    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        print("Request done")
        predictions = response.json()
        return any(pred == 1 for pred in predictions.values())
    else:
        print(response.text)
    return False

# Take a screenshot of the website using Selenium
def take_screenshot(url, filename):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Run in headless mode

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    driver.save_screenshot(filename)
    driver.quit()

# Route to display the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to start the scam checking process
@app.route('/check', methods=['POST'])
def check_urls():
    scam_urls_by_date = {}

    result = subprocess.run(["scp",  "-i", "~/.ssh/mailtrap_key.pem", "-o", "stricthostkeychecking=no", "azureuser@9.169.186.209:/var/mail/azureuser", "./mails"])

    build_urls_file.main()
    urls_by_date = load_urls()

    for date, urls in urls_by_date.items():
        scam_urls_by_date[date] = []
        for url in urls:
            if is_scam(url):
                scam_urls_by_date[date].append(url)
                screenshot_filename = f"screenshots/{url.replace('://', '_').replace('/', '_')}.png"
                take_screenshot(url, screenshot_filename)

    return render_template('index.html', scam_urls_by_date=scam_urls_by_date)

if __name__ == '__main__':
    app.run(debug=True)
