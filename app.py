from flask import Flask, render_template, request, redirect, url_for
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

app = Flask(__name__)

# Ensure the screenshots directory exists
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Load URLs from a text file
def load_urls():
    with open('urls.txt', 'r') as file:
        urls = file.read().splitlines()
    return urls

# Check if a URL is a scam using the API
def is_scam(url):
    api_url = "https://url-scan-api-11d8349414c2.herokuapp.com/automatic_ai_scan"
    response = requests.post(api_url, data={'url': url})
    if response.status_code == 200:
        predictions = response.json()
        return any(pred == 1 for pred in predictions.values())
    return False

# Take a screenshot of the website using Selenium
def take_screenshot(url, filename):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(), options=options)
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
    scam_urls = []
    urls = load_urls()

    for url in urls:
        if is_scam(url):
            scam_urls.append(url)
            screenshot_filename = f"screenshots/{url.replace('://', '_').replace('/', '_')}.png"
            take_screenshot(url, screenshot_filename)

    return render_template('index.html', scam_urls=scam_urls)

if __name__ == '__main__':
    app.run(debug=True)
