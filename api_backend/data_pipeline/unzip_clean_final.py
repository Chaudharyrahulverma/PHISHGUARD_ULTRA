import os
import zipfile
import re
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PIPELINE_DIR = os.path.join(BASE_DIR, "data_pipeline")
DATASET_DIR = os.path.join(BASE_DIR, "ml_model", "dataset")

os.makedirs(DATASET_DIR, exist_ok=True)

url_pattern = re.compile(r'https?://[^\s,"]+')
email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')

clean_urls = set()
clean_emails = set()
clean_content = set()

# -------------------------
# STEP 1: EXTRACT ZIP
# -------------------------
print("📦 Extracting ZIP files...")

for file in os.listdir(DATA_PIPELINE_DIR):
    if file.endswith(".zip"):
        zip_path = os.path.join(DATA_PIPELINE_DIR, file)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(DATA_PIPELINE_DIR)
            print(f"✅ Extracted: {file}")
        except:
            print(f"❌ Error extracting: {file}")

print("📦 Extraction complete\n")

# -------------------------
# STEP 2: PROCESS FILES
# -------------------------
print("🔍 Processing files...")

for root, dirs, files in os.walk(DATA_PIPELINE_DIR):
    for file in files:
        if file.endswith((".txt", ".csv")):
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", errors="ignore") as f:
                    for line in f:
                        line = line.strip()

                        # URLs
                        urls = url_pattern.findall(line)
                        for u in urls:
                            clean_urls.add(u.lower())

                        # Emails
                        emails = email_pattern.findall(line)
                        for e in emails:
                            clean_emails.add(e.lower())

                        # Content (text lines)
                        if len(line) > 20:
                            clean_content.add(line)

            except:
                continue

# -------------------------
# STEP 3: SAVE CLEAN DATA
# -------------------------
print("💾 Saving cleaned data...")

def save_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(item + "\n")

save_file(os.path.join(DATASET_DIR, "clean_urls.txt"), clean_urls)
save_file(os.path.join(DATASET_DIR, "clean_emails.txt"), clean_emails)
save_file(os.path.join(DATASET_DIR, "clean_content.txt"), clean_content)

print("✅ Saved clean dataset\n")

# -------------------------
# STEP 4: CLEAN RAW FILES
# -------------------------
print("🧹 Cleaning raw files...")

for root, dirs, files in os.walk(DATA_PIPELINE_DIR):
    for file in files:
        if file.endswith((".zip", ".csv", ".txt")):
            try:
                os.remove(os.path.join(root, file))
            except:
                pass

# remove empty folders
for root, dirs, files in os.walk(DATA_PIPELINE_DIR, topdown=False):
    for d in dirs:
        try:
            shutil.rmtree(os.path.join(root, d))
        except:
            pass

print("🧹 Cleanup complete\n")

# -------------------------
# FINAL STATS
# -------------------------
print("🎯 FINAL STATS:")
print(f"URLs   : {len(clean_urls)}")
print(f"Emails : {len(clean_emails)}")
print(f"Content: {len(clean_content)}")

print("\n🔥 SYSTEM READY — अब सिर्फ clean dataset बचा है")