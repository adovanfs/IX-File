import urllib.request
import json

# Menggunakan API RSS to JSON Converter yang stabil dari Antara News
API_URL = "https://api.rss2json.com/v1/api.json?rss_url=https://www.antaranews.com/rss/terkini.xml"

def ambil_berita():
    try:
        req = urllib.request.Request(
            API_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get("items", [])
            
            berita_terbaru = {"articles": []}
            for item in items:
                berita_terbaru["articles"].append({
                    "title": item.get("title"),
                    "description": item.get("description", "").replace("<p>", "").replace("</p>", ""),
                    "url": item.get("link"),
                    "image": item.get("enclosure", {}).get("link") or item.get("thumbnail"),
                    "pubDate": item.get("pubDate")
                })
            
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(berita_terbaru, f, ensure_ascii=False, indent=4)
                
            print(f"Berhasil mengambil {len(berita_terbaru['articles'])} berita!")
            
    except Exception as e:
        print("Gagal mengambil berita:", e)

if __name__ == "__main__":
    ambil_berita()
