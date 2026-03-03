import os
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

async def backup_templates():
    print("Backing up current DB templates...")
    res = supabase.table("message_templates").select("*").order("accommodation_name, trigger_type").execute()
    
    templates = res.data
    
    with open("current_templates_backup.py", "w", encoding="utf-8") as f:
        f.write("# Auto-generated backup of current DB templates\n")
        f.write("import os\n")
        f.write("from supabase import create_client\n")
        f.write("from dotenv import load_dotenv\n\n")
        
        f.write("load_dotenv()\n")
        f.write("url = os.environ.get('SUPABASE_URL')\n")
        f.write("key = os.environ.get('SUPABASE_KEY')\n")
        f.write("supabase = create_client(url, key)\n\n")
        
        f.write("templates_data = [\n")
        for t in templates:
            f.write("    {\n")
            f.write(f"        'accommodation_name': {repr(t['accommodation_name'])},\n")
            f.write(f"        'trigger_type': {repr(t['trigger_type'])},\n")
            if t.get('send_time'):
                f.write(f"        'send_time': {repr(t['send_time'])},\n")
            if t.get('subject'):
                f.write(f"        'subject': {repr(t['subject'])},\n")
            f.write(f"        'content': {repr(t['content'])}\n")
            f.write("    },\n")
        f.write("]\n\n")
        
        f.write("def restore():\n")
        f.write("    print('Restoring templates from backup...')\n")
        f.write("    # Delete existing\n")
        f.write("    res = supabase.table('message_templates').select('id').execute()\n")
        f.write("    if res.data:\n")
        f.write("        ids = [r['id'] for r in res.data]\n")
        f.write("        supabase.table('message_templates').delete().in_('id', ids).execute()\n")
        f.write("    \n")
        f.write("    # Insert backups\n")
        f.write("    for t in templates_data:\n")
        f.write("        supabase.table('message_templates').insert(t).execute()\n")
        f.write("    print('Restore complete.')\n\n")
        
        f.write("if __name__ == '__main__':\n")
        f.write("    restore()\n")
        
    print("Backup complete. Wrote current_templates_backup.py")

if __name__ == "__main__":
    asyncio.run(backup_templates())
