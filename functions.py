from urllib.parse import urljoin


def extract_text_by_class(soup, class_: str):
    """
    Extracts the text from a BeautifulSoup object based on a class.
    :param soup: The BeautifulSoup object.
    :param class_: The class of the HTML element that contains the text.
    :return: The text.
    """
    elements = soup.find_all(class_=class_)
    texts = []
    for element in elements:
        text = element.text.strip()
        if text:
            texts.append(text)
    return ' '.join(texts)


def extract_href_by_class(soup, class_: str, base_url=""):
    elements = soup.find_all("a", class_=class_)
    hrefs = []

    for element in elements:
        # Check if the element has the data-tracking attribute (indicating an official seller)
        # or doesn't have it (indicating an unofficial seller).
        # Extract href for both cases.
        href = element.get("href")
        if href:
            # Join the href with the base URL (if provided) to get an absolute URL
            absolute_url = urljoin(base_url, href)
            hrefs.append(absolute_url)
    return hrefs


def create_discussion_url(base_url: str, relative_url: str) -> str:
    """
    Creates a full discussion URL based on the base URL and a relative URL.

    :param base_url: The base URL of the forum.
    :param relative_url: The relative URL of the discussion.
    :return: The full URL of the discussion.
    """
    return urljoin(base_url, relative_url)


def return_item_info_from_scraped(item, name_class: str, link_class: str, description_class: str, seller_class: str,
                                  price_class: str):
    item_name = extract_text_by_class(item, name_class)
    item_link = extract_href_by_class(item, link_class, "https://www.marktplaats.nl/")
    #item_link = "http://marktplaats.nl/v" + item_link[0][2:]
    item_description = extract_text_by_class(item, description_class)
    item_seller = extract_text_by_class(item, seller_class)
    item_price = extract_text_by_class(item, price_class)


    return {
        "name": item_name,
        "link": item_link,
        "description": item_description,
        "seller": item_seller,
        "price": item_price
    }
