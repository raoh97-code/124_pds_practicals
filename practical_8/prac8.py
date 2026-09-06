import requests
from bs4 import BeautifulSoup

# Website URL
url = "https://ldce.ac.in/"

# Send request to website
response = requests.get(url, timeout=10)

# Check response
print("Status Code:", response.status_code)
print("Content Length:", len(response.text))

if response.status_code == 200:
    
    print("\nWebsite successfully retrieved.")
    # Create BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract webpage title
    print("\nWEBPAGE TITLE:")
    if soup.title:
        print("Page Title:", soup.title.get_text(strip=True))
    else:
        print("Page Title: Not found")

    # Extract headings
    print("\nHEADINGS:")
    headings = soup.find_all(["h1", "h2", "h3"])

    for heading in headings:
        text = heading.get_text(" ", strip=True)

        if text:
            print(text)

    # Extract text
    print("\nWEBPAGE TEXT:")
    text = soup.get_text(" ", strip=True)

    # Display first 2000 characters
    print(text[:2000])

    # Extract hyperlinks
    print("\nHYPERLINKS:")
    links = soup.find_all("a")

    for link in links[:20]:

        link_text = link.get_text(" ", strip=True)
        href = link.get("href")

        if href:
            print("Text:", link_text)
            print("URL:", href)
            print()

    # Extract images
    print("\nIMAGES:")
    images = soup.find_all("img")

    print("Number of images:", len(images))
    for image in images[:10]:

        image_source = image.get("src")
        image_alt = image.get("alt")

        print("Image Source:", image_source)
        print("Alternative Text:", image_alt)
        print()

else:
    print("Failed to retrieve the webpage.")
    print("Status Code:", response.status_code)