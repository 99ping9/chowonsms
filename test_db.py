import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

print("--------------------------------------------------")
print("Supabase Connection Test")
print("--------------------------------------------------")
print(f"URL: {url}")
print(f"KEY: {key[:10]}..." if key else "KEY: None")

if not url or not key:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY is missing in .env")
    sys.exit(1)

try:
    print("Connecting to Supabase...")
    supabase: Client = create_client(url, key)
    
    # Simple query to check connection (fetch accommodations)
    # This table should exist if schema.sql was run.
    print("Executing query (SELECT count(*) FROM accommodations)...")
    response = supabase.table("accommodations").select("*", count="exact").limit(1).execute()
    
    print("✅ Connection Successful!")
    print(f"Found {response.count} accommodations in DB.")
    
    if response.data:
        print("Sample Data:", [a['name'] for a in response.data])
    else:
        print("Table is empty (but connected).")

except Exception as e:
    print("❌ Connection Failed!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Details: {e}")
    if hasattr(e, 'code'):
        print(f"Code: {e.code}")
    if hasattr(e, 'details'):
        print(f"Error Details: {e.details}")
    if hasattr(e, 'message'):
        print(f"Message: {e.message}")
    sys.exit(1)
