import os
from bs4 import BeautifulSoup
import pandas as pd

# Function to read HTML file and parse it with BeautifulSoup
def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

# Function to extract data
def extract_data(soup):
    data = []
    divs = soup.find_all('div', class_='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20')
    for div in divs:
        try:
            img = div.find('img', class_='s-image')
            img_src = img['src']
        except:
            img_src = ""
        
        try:
            whole_price = div.find('span', class_='a-price-whole').text
        except:
            whole_price = "0"
        
        try:
            fraction_price = div.find('span', class_='a-price-fraction').text
        except:
            fraction_price = "0"
        
        try:
            price = f"{whole_price}.{fraction_price}"
        except:
            price = "0.00"
        
        try:
            name = div.find('span', class_='a-size-base-plus a-color-base a-text-normal').text
            name = " ".join(name.split())
        except:
            name = ""
        
        data.append({ 'Name': name, 'Price': price, 'Image Source': img_src})
    
    return data

# Function to write data to Excel file
def write_to_excel(data):
    try:
        monitors = pd.read_excel('monitor_price_in_amazon.xlsx')
        new_df = pd.DataFrame(data)
        append_df = pd.concat([monitors, new_df], ignore_index=True)
        append_df.to_excel('monitor_price_in_amazon.xlsx', index=False)
    except:
        df = pd.DataFrame(data)
        df.to_excel('monitor_price_in_amazon.xlsx', index=False)

# Main function
def main():
    html_files_dir = './html_files'
    html_file_path = os.path.join(html_files_dir, 'Amazon.com_ Computer Monitors - Computers & Accessories_ Electronics.html')
    
    # Parse HTML file
    soup = parse_html_file(html_file_path)
    
    # Extract data
    data = extract_data(soup)
    
    # Write data to Excel file
    write_to_excel(data)

if __name__ == "__main__":
    main()
