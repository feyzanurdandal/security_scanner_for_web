from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def save_results_to_pdf(results, filename="scan_results.pdf"):
    """
    Güvenlik tarama sonuçlarını PDF olarak kaydeder.
    :param results: Tarama sonucu sözlüğü (Örn: {"SQL Injection": "Zayıf", "XSS": "Güçlü"})
    :param filename: Kaydedilecek PDF dosya adı
    """
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, "Web Güvenlik Tarama Sonuçları")
    c.line(100, 745, 400, 745)  # Başlık altına çizgi ekle

    y_position = 720
    for issue, status in results.items():
        c.drawString(100, y_position, f"{issue}: {status}")
        y_position -= 20  # Her satır için aşağı kaydır

    c.save()
    print(f"Sonuçlar {filename} olarak kaydedildi.")


# Örnek kullanım:
scan_results = {
    "SQL Injection": "Zayıf (Açık tespit edildi)",
    "XSS": "Güçlü (Açık tespit edilmedi)",
    "HTTP Güvenlik Başlıkları": "Eksik (Strict-Transport-Security eksik)"
}

save_results_to_pdf(scan_results)
