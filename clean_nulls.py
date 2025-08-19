import os

def remove_null_bytes_from_file(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    if b"\x00" in content:
        print(f"🧹 Cleaning null bytes in: {file_path}")
        cleaned = content.replace(b"\x00", b"")
        with open(file_path, "wb") as f:
            f.write(cleaned)

def scan_and_clean(root="."):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".py"):
                remove_null_bytes_from_file(os.path.join(dirpath, filename))

if __name__ == "__main__":
    print("🔎 Scanning for null bytes in Python files...")
    scan_and_clean(".")
    print("✅ Done! All .py files cleaned.")
