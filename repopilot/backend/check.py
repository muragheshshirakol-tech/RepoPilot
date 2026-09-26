from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("postgresql://postgres:kGVl0Qgh2ZMoX3LN@db.yhdysllimwcrdgfbvpxc.supabase.co:5432/postgres")

print("Python is reading this exact URL:")
print(url)
print(f"Length of URL: {len(url)} characters")