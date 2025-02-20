import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-XSS-Protection",
    "X-Content-Type-Options",
    "Referrer-Policy"
]
def check_headers(url):
    """Web sitesinin güvenlik başlıklarını analiz eder."""
    try:
        response = requests.get(url, verify=False, timeout=5)
        print(f"\n[+] {url} sitesine bağlanıldı.")

        headers = response.headers
        for header in SECURITY_HEADERS:
            if header in headers:
                print(f"[✔] {header}: {headers[header]}")
            else:
                print(f"[❌] Eksik: {header}")

    except requests.RequestException as e:
        print(f"Hata: {e}")