import re
import email
from email import policy
from email.parser import BytesParser
from datetime import datetime

def extract_links(text):
    """Extract all URLs from the given text using a regular expression."""
    url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
    return url_pattern.findall(text)

def parse_mail_file(mail_file_path):
    """Parse the mail file and extract links with their received datetime."""
    links_with_dates = []

    with open(mail_file_path, 'rb') as mail_file:
        msg = BytesParser(policy=policy.default).parse(mail_file)

        # Extract the received date from the email headers
        received_date = msg['Date']
        if received_date:
            received_date = datetime.strptime(received_date, '%a, %d %b %Y %H:%M:%S %z')

        # Extract the email body
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    links = extract_links(body)
                    if links:
                        links_with_dates.extend([(link, received_date) for link in links])
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            links = extract_links(body)
            if links:
                links_with_dates.extend([(link, received_date) for link in links])

    return links_with_dates

def save_links_to_file(links_with_dates, output_file_path):
    """Save the extracted links and their received dates to a text file."""
    with open(output_file_path, 'w') as output_file:
        for link, date in links_with_dates:
            output_file.write(f"{date},{link}\n")


def main():
    mail_file_path = 'mails'
    output_file_path = 'output_links.txt'
    links_with_dates = parse_mail_file(mail_file_path)
    save_links_to_file(links_with_dates, output_file_path)
    print(f"Extracted {len(links_with_dates)} links. Saved to {output_file_path}.")
