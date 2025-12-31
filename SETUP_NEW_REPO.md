# 🚀 Yangi GitHub Repository'ga Deploy Qilish

## 📋 Qadamlar:

### 1. GitHub'da yangi repository yaratish

1. https://github.com/new ga kiring (`brorasulov` username bilan)
2. **Repository name**: `comment` (yoki istalgan nom)
3. **Public** qiling
4. **README qo'shmang**
5. **Create repository** bosing

### 2. Terminalda ulash

```bash
cd /Users/xoji/Documents/comment

# Remote qo'shish (REPO_NAME o'rniga repository nomingizni qo'ying)
git remote add origin https://github.com/brorasulov/REPO_NAME.git

# Barcha fayllarni qo'shish
git add .

# Commit qilish
git commit -m "Deploy igloo.inc website"

# Branch nomini o'zgartirish
git branch -M main

# GitHub'ga yuborish
git push -u origin main
```

### 3. GitHub Pages'ni yoqish

1. https://github.com/brorasulov/REPO_NAME ga kiring
2. **Settings** > **Pages**
3. **Source**: Deploy from a branch
4. **Branch**: main
5. **Folder**: / (root)
6. **Save**

### 4. Sayt manzili

```
https://brorasulov.github.io/REPO_NAME/
```

Masalan, agar repository nomi `comment` bo'lsa:
```
https://brorasulov.github.io/comment/
```

## ✅ Tayyor!

Sayt 1-2 daqiqadan keyin ishga tushadi!

