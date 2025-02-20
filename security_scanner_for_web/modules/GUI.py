import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas


def start_scan():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Hata", "Lütfen bir URL girin!")
        return

    # Burada tarama işlemi yapılabilir, örnek sonuçlar ekliyoruz
    scan_results = {
        "SQL Injection": "Zayıf (Açık tespit edildi)",
        "XSS": "Güçlü (Açık tespit edilmedi)",
        "HTTP Güvenlik Başlıkları": "Eksik (Strict-Transport-Security eksik)"
    }

    # Sonuçları göster
    results_text.delete("1.0", tk.END)
    for issue, status in scan_results.items():
        results_text.insert(tk.END, f"{issue}: {status}\n")

    # Eğer kullanıcı PDF kaydetmeyi seçtiyse
    if pdf_var.get():
        save_results_to_pdf(scan_results)


def save_results_to_pdf(results, filename="scan_results.pdf"):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Web Güvenlik Tarama Sonuçları")

    y_position = 720
    for issue, status in results.items():
        c.drawString(100, y_position, f"{issue}: {status}")
        y_position -= 20

    c.save()
    messagebox.showinfo("Bilgi", f"Sonuçlar {filename} olarak kaydedildi.")


# Tkinter GUI
root = tk.Tk()
root.title("Web Güvenlik Tarayıcı")

tk.Label(root, text="Taranacak URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# PDF kaydetme seçeneği (Checkbox)
pdf_var = tk.BooleanVar()
pdf_checkbox = tk.Checkbutton(root, text="Sonuçları PDF olarak kaydet", variable=pdf_var)
pdf_checkbox.pack()

scan_button = tk.Button(root, text="Taramayı Başlat", command=start_scan)
scan_button.pack()

results_text = tk.Text(root, height=10, width=60)
results_text.pack()

root.mainloop()
