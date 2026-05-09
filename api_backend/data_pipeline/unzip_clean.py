import os
import zipfile
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "ml_model", "dataset")

os.makedirs(OUTPUT_DIR, exist_ok=True)

URL_FILE = os.path.join(OUTPUT_DIR, "clean_urls.txt")
EMAIL_FILE = os.path.join(OUTPUT_DIR, "clean_emails.txt")
CONTENT_FILE = os.path.join(OUTPUT_DIR, "clean_content.txt")


# REGEX
url_pattern = re.compile(r"https?://[^\s,]+")
email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def extract_zip():
    print("📦 Extracting ZIP files...")

    for file in os.listdir(BASE_DIR):
        if file.endswith(".zip"):
            zip_path = os.path.join(BASE_DIR, file)

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(BASE_DIR)
                print(f"✅ Extracted: {file}")
            except:
                print(f"❌ Failed: {file}")

    print("📦 Extraction complete\n")


def process_all_files():
    print("🔍 Processing files...")

    urls = set()
    emails = set()
    contents = set()

    for root, _, files in os.walk(BASE_DIR):
        for file in files:

            if file.endswith((".txt", ".csv", ".log")):

                filepath = os.path.join(root, file)

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:

                            line = line.strip()

                            # URL extract
                            for u in url_pattern.findall(line):
                                if len(u) > 10:
                                    urls.add(u.lower())

                            # Email extract
                            for e in email_pattern.findall(line):
                                emails.add(e.lower())

                            # Phishing content
                            if any(k in line.lower() for k in [
                                "verify", "login", "bank", "password",
                                "otp", "urgent", "account", "suspend"
                            ]):
                                contents.add(line)

                except:
                    continue

    return urls, emails, contents


def save_data(urls, emails, contents):
    print("💾 Saving cleaned data...")

    with open(URL_FILE, "w", encoding="utf-8") as f:
        for u in urls:
            f.write(u + "\n")

    with open(EMAIL_FILE, "w", encoding="utf-8") as f:
        for e in emails:
            f.write(e + "\n")

    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        for c in contents:
            f.write(c + "\n")

    print("✅ Saved all cleaned data\n")


def show_stats(urls, emails, contents):
    print("🎯 FINAL STATS:")
    print(f"URLs   : {len(urls)}")
    print(f"Emails : {len(emails)}")
    print(f"Content: {len(contents)}")


def main():
    extract_zip()

    urls, emails, contents = process_all_files()

    save_data(urls, emails, contents)

    show_stats(urls, emails, contents)

    print("\n🔥 DONE — अब तुम zip delete कर सकते हो safely")


if __name__ == "__main__":
    main()