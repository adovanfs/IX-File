import urllib.request
import json
import re

# Daftar berbagai sumber RSS berita Indonesia via RSS2JSON API
SOURCES = [
    {"name": "ANTARA NEWS", "url": "https://api.rss2json.com/v1/api.json?rss_url=https://www.antaranews.com/rss/terkini.xml"},
    {"name": "CNN INDONESIA", "url": "https://api.rss2json.com/v1/api.json?rss_url=https://www.cnnindonesia.com/nasional/rss"},
    {"name": "CNBC INDONESIA", "url": "https://api.rss2json.com/v1/api.json?rss_url=https://www.cnbcindonesia.com/news/rss"},
    {"name": "REPUBLIKA", "url": "https://api.rss2json.com/v1/api.json?rss_url=https://www.republika.co.id/rss"}
]

def bersihkan_html(teks):
    if not teks:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', teks).strip()

def ambil_semua_berita():
    semua_berita = []

    for source in SOURCES:
        try:
            req = urllib.request.Request(
                source["url"], 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                items = data.get("items", [])
                
                for item in items[:5]:  # Ambil 5 berita teratas dari setiap sumber
                    desc_bersih = bersihkan_html(item.get("description", ""))
                    
                    semua_berita.append({
                        "source": source["name"],
                        "title": item.get("title"),
                        "description": desc_bersih,
                        "url": item.get("link"),
                        "image": item.get("enclosure", {}).get("link") or item.get("thumbnail"),
                        "pubDate": item.get("pubDate")
                    })
        except Exception as e:
            print(f"Gagal mengambil dari {source['name']}:", e)

    # Simpan hasil gabungan ke news.json
    try:
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump({"articles": semua_berita}, f, ensure_ascii=False, indent=4)
        print(f"Berhasil mengumpulkan {len(semua_berita)} berita dari berbagai sumber!")
    except Exception as e:
        print("Gagal menyimpan file news.json:", e)

if __name__ == "__main__":
    ambil_semua_berita()
