import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    """
    Belirtilen URL'den HTML içeriğini alır.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        return response.text
    except requests.RequestException as e:
        print(f"Hata: {e}")
        return None


def parse_forms(html):
    """
    HTML içeriğindeki formları bulur ve detaylarını yazdırır.
    """
    soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")
    print(f"\nBulunan form sayısı: {len(forms)}")

    for idx, form in enumerate(forms, start=1):
        print(f"\nForm {idx}:")
        action = form.get("action")
        method = form.get("method", "get").lower()
        print(f"  Action: {action}")
        print(f"  Method: {method}")

        inputs = form.find_all("input")
        for input_field in inputs:
            input_name = input_field.get("name")
            input_type = input_field.get("type", "text")
            print(f"    Input: {input_name} (type: {input_type})")


def parse_links(html):
    """
    HTML içeriğindeki tüm linkleri (a etiketleri) bulur ve yazdırır.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")
    print(f"\nBulunan link sayısı: {len(links)}")

    for idx, link in enumerate(links, start=1):
        href = link.get("href")
        text = link.get_text(strip=True)
        print(f"Link {idx}: {text} -> {href}")


def analyze_website(url):
    """
    Belirtilen URL'yi analiz ederek formlar ve linkleri tespit eder.
    """
    html = fetch_page(url)
    if html:
        print(f"\n{url} sayfasının analizi:")
        parse_forms(html)
        parse_links(html)
    else:
        print("HTML içeriği alınamadı.")


if __name__ == "__main__":
    target_url = input("Hedef URL (http:// veya https:// ile girin): ")
    analyze_website(target_url)
