import urllib.request
import json

# Mengambil berita dari API CNN Indonesia
API_URL = "https://api-berita-indonesia.vercel.app/cnn/terbaru/"

def ambil_berita():
    try:
        req = urllib.request.Request(
            API_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            posts = data.get("data", {}).get("posts", [])
            
            berita_terbaru = {"articles": []}
            for item in posts:
                berita_terbaru["articles"].append({
                    "title": item.get("title"),
                    "description": item.get("snippet"),
                    "url": item.get("link"),
                    "image": item.get("image", {}).get("large") or item.get("image", {}).get("small"),
                    "pubDate": item.get("pubDate")
                })
            
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(berita_terbaru, f, ensure_ascii=False, indent=4)
                
            print(f"Berhasil memperbarui {len(berita_terbaru['articles'])} berita!")
            
    except Exception as e:
        print("Gagal mengambil berita:", e)

if __name__ == "__main__":
    ambil_berita()
