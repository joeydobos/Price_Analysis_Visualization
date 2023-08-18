import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def retrieve_product_and_price(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    item = soup.find('title').text
    price = soup.find('span', class_="price").text
    return item, price

def remove_pound_and_comma(price):
    return float(price.replace('£', '').replace(',', ''))

def combined_price(items):
    total = 0
    for _, price in items:
        cleaned_price = remove_pound_and_comma(price)
        total += cleaned_price
    return total

def update_total_price_database(total_combined_price):
    conn = sqlite3.connect('total_prices.db')
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO total_prices (date, total_price) VALUES (?, ?)', (today, total_combined_price))
    conn.commit()
    conn.close()

def send_email(subject, body, sender, recipients, password):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Email sent!")

def send_email_with_attachment(subject, body, sender, recipients, password, attachment_filename):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment_filename}')
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

def main():
    subject = "Todays Camera Prices"
    sender = "josephdobos@gmail.com"
    recipients = ["josephdobos@gmail.com"]
    password = "tqquceiegiemdpxl"

    camera = 'https://www.wexphotovideo.com/sony-a7-iv-digital-camera-body-3020039/'
    lens1 = 'https://www.wexphotovideo.com/sony-fe-35mm-f1-4-g-master-lens-1764151/'
    lens2 = 'https://www.wexphotovideo.com/sony-fe-24mm-f1-4-g-master-lens-1676437/'
    tripod = 'https://www.wexphotovideo.com/smallrig-freeblazer-heavy-duty-carbon-fibre-tripod-4167-3099748/'

    items = [
        retrieve_product_and_price(camera),
        retrieve_product_and_price(lens1),
        retrieve_product_and_price(lens2),
        retrieve_product_and_price(tripod)
    ]

    total_combined_price = combined_price(items)

    # Update the new database with today's total price
    update_total_price_database(total_combined_price)

    # Retrieve data for total prices from the 'total_prices' table
    conn = sqlite3.connect('total_prices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM total_prices ORDER BY date')
    total_prices_data = cursor.fetchall()
    conn.close()

    # Extract dates and total prices for the graph
    dates = [row[0] for row in total_prices_data]
    total_prices = [row[1] for row in total_prices_data]

    # Create a graph of combined price over time
    plt.figure(figsize=(10, 6))
    plt.plot(dates, total_prices, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Total Price (£)')
    plt.title('Past Prices')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Save the figure as an image
    plt.savefig('past_prices.png')

    # Prepare the email body
    body = "Todays Individual Prices \n "
    for item, price in items:
        body += f"{item}: {price}\n"

    body += f"\nTodays Combined Price: £{total_combined_price:.2f}"

    # Send the email
    send_email_with_attachment(subject, body, sender, recipients, password, 'past_prices.png')

if __name__ == "__main__":
    main()