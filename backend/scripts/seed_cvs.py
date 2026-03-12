import os
import httpx
import glob
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
UPLOAD_ENDPOINT = f"{BACKEND_URL}/api/cv/upload"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/pdf")

def seed():
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {DATA_DIR}")
        return

    print(f"Found {len(pdf_files)} PDF files. Seeding...")
    
    with httpx.Client() as client:
        for pdf_path in pdf_files:
            filename = os.path.basename(pdf_path)
            try:
                with open(pdf_path, "rb") as f:
                    files = {"file": (filename, f, "application/pdf")}
                    response = client.post(UPLOAD_ENDPOINT, files=files, timeout=30.0)
                    
                if response.status_code == 200:
                    print(f"Successfully uploaded {filename}")
                else:
                    print(f"Failed to upload {filename}: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")

if __name__ == "__main__":
    seed()
