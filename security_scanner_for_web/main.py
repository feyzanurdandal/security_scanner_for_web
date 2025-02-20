from modules.website_analysis_and_data_extraction import *
from modules.port_scanner import *
from modules.HTTP_headers_check import *
from modules.sql_injection import *
def main():
    while True:
        print("\n--- Güvenlik Aracı Menüsü ---")
        print("1.Web Sitesi Analizi ve Veri Çekme")
        print("2. Port Tarayıcı")
        print("3. HTTP Başlık Analiz Aracı")
        print("4. SQL Injection Testi")
        print("5. XSS Tespiti")
        print("6. Çıkış")
        choice = input("Seçiminiz (1-6): ")

        if choice == "1":
            # web analizi bölümü çalışacak
            target_url = input("Hedef URL (http:// veya https:// ile girin): ")
            analyze_website(target_url)
        elif choice == "2":
            # port tarayıcı çalışacak
            target = input("Hedef IP veya Domain: ")
            # Tarama aralığını isteğe göre değiştirebilirsin
            ports = range(20, 1025)  # 20-1024 arası portları tarar
            port_scanner(target, ports)
        elif choice == "3":
            # HTTP başlık analiz modülünü çalıştır
            target_url = input("Hedef URL (http:// veya https:// ile girin): ")
            check_headers(target_url)
        elif choice == "4":
            # SQL Injection modülü çalıştır
            target_url = input("Hedef URL (http:// veya https:// ile girin): ")
            perform_sql_injection_test(target_url)
        elif choice == "5":
            #XSS tespiti modülünü koysam mı emin değilim ?
            pass
        elif choice == "6":
            print("Program kapanıyor.")
            break
        else:
            print("Geçerli bir seçim yapınız.")

if __name__ == "__main__":
    main()
