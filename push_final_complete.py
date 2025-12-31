#!/usr/bin/env python3
import subprocess
import os
import sys

print("📦 Final push - ALL files to GitHub...")
print("")

os.chdir("/Users/xoji/Documents/comment")

# 1. Barcha fayllarni qo'shish
print("📝 Adding ALL files...")
subprocess.run(["git", "add", "-f", "."], check=False)
subprocess.run(["git", "add", "-f", "assets/"], check=False)
subprocess.run(["git", "add", "-A"], check=False)

# 2. Status
print("\n📊 Files to commit:")
result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
files = result.stdout.strip().split('\n')
print(f"   {len([f for f in files if f])} files to commit")

# 3. Commit
print("\n💾 Committing...")
result = subprocess.run(["git", "commit", "-m", "Complete deployment - all assets (no tokens in scripts)"], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print("✅ Committed successfully")
else:
    print("ℹ️  No changes to commit or already committed")

# 4. Push (token bilan - environment variable'dan)
print("\n⬆️  Pushing to GitHub...")
token = os.environ.get("GITHUB_TOKEN", "")

if not token:
    print("❌ GITHUB_TOKEN environment variable not set")
    print("   Run: export GITHUB_TOKEN='your_token'")
    print("   Then run this script again")
    sys.exit(1)

# Remote URL'ni o'rnatish
subprocess.run(["git", "remote", "set-url", "origin", 
               f"https://brorasulov:{token}@github.com/brorasulov/brorasulov.git"], check=False)

# Push
result = subprocess.run(["git", "push", "origin", "main", "--force"], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print("✅ Push successful!")
else:
    print("❌ Push failed:")
    print(result.stderr)
    print(result.stdout)

# Remote URL'ni tozalash
subprocess.run(["git", "remote", "set-url", "origin", 
               "https://github.com/brorasulov/brorasulov.git"], check=False)

print("\n✅ Done!")
print("\n⏱️  Wait 2-3 minutes for GitHub Pages to update")
print("🌐 Then check: https://brorasulov.github.io/brorasulov/")

