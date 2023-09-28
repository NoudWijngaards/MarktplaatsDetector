import time
import random
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pygame.mixer
from functions import return_item_info_from_scraped

pygame.mixer.init()
sound = pygame.mixer.Sound('ding.wav')

waiting_time_list = [i for i in range(200, 300)]

search_link = input("Welke link wilt u gebruiken om resultaten voor te zoeken?: ")

if search_link[:2] == "www":
    search_link = "http://" + search_link

links_history = []
result_history = []

while True:
    scraped_items = []
    page_content = BeautifulSoup(requests.get(search_link).content, 'html.parser')

    # Extract all messages from the page. The approach is dependent on whether the user has provided the full
    # class or only a part of the class.
    items = page_content.find_all(class_=lambda x: x == "hz-Listing hz-Listing--list-item hz-Listing--list-item-BNL16952")

    # Add the messages to the list of all messages and increase the page and iteration.
    scraped_items.extend(items)

    new_items = []

    for item in scraped_items:
        item_info = return_item_info_from_scraped(
            item=item,
            name_class="hz-Listing-title",
            link_class="hz-Link hz-Link--block hz-Listing-coverLink",
            description_class="hz-Listing-description hz-text-paragraph",
            price_class="hz-Listing-price hz-Listing-price--mobile hz-text-price-label",
            seller_class="hz-Listing-seller-name"
        )

        # Check if it contains a link.
        if len(item_info["link"]) > 0:
            # Links are always unique, and can thus be used as an identifier.
            if item_info["link"][0] not in links_history:
                links_history.append(item_info["link"][0])
                new_items.append(item_info)
                result_history.append(item)
                sound.play()

        else:
            # If there is no link, use the full item as an identifier.
            if item not in result_history:
                result_history.append(item)
                new_items.append(item_info)
                sound.play()

    amount_of_new_items = len(new_items)
    print("Aantal nieuwe items gevonden: " + str(amount_of_new_items) + "\n")

    if len(new_items) > 0:
        sound.play()

    # For item in new_items, display them properly to the user.
    for item in new_items:
        print("Nieuw item gevonden: " + item["name"])
        print("Beschrijving: " + item["description"])
        print("Prijs: " + item["price"])
        print("Verkoper: " + item["seller"])
        if len(item["link"]) > 0:
            print("Link: " + item["link"][0])
        else:
            print("Link: Geen link gevonden")
        print()

    # Geeft aan hoe lang wordt gewacht tot de volgende dataverzameling

    now = datetime.now()

    waiting_time_seconds = random.choice(waiting_time_list)
    waiting_full_time = now + timedelta(seconds=waiting_time_seconds)
    print("Volgende dataverzameling: " + waiting_full_time.strftime('%H:%M:%S') + "\n")
    time.sleep(waiting_time_seconds)
