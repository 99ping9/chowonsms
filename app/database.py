import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url:
    # Vercel 환경에서는 .env 파일이 없을 수 있으므로 os.environ에서 직접 읽어올 수도 있음 (이미 위에서 처리함)
    print("Warning: SUPABASE_URL not set.")

supabase: Client = create_client(url, key) if url and key else None

def get_supabase() -> Client:
    return supabase
