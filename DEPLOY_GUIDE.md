# 🚀 GitHub Pages'ga Deploy Qilish

## 📋 Qadamlar:

### 1. GitHub'da repository yaratish

1. https://github.com/new ga kiring
2. Repository nomini kiriting (masalan: `igloo-site`)
3. **Public** qiling (bepul uchun)
4. **README qo'shmang** (bizda allaqachon bor)
5. **Create repository** bosing

### 2. Terminalda deploy qilish

```bash
cd /Users/xoji/Documents/comment

# Git'ni initialize qilish (agar qilinmagan bo'lsa)
git init

# GitHub repository'ni qo'shish
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Barcha fayllarni qo'shish
git add .

# Commit qilish
git commit -m "Deploy igloo.inc website"

# GitHub'ga yuborish
git branch -M main
git push -u origin main
```

### 3. GitHub Pages'ni yoqish

1. GitHub repository'ga kiring
2. **Settings** ga kiring
3. Chap menudan **Pages** ni tanlang
4. **Source** ostida:
   - **Deploy from a branch** ni tanlang
   - **Branch**: `main`
   - **Folder**: `/ (root)`
5. **Save** bosing

### 4. Saytni ochish

1-2 daqiqadan keyin saytingiz tayyor bo'ladi:

```
https://YOUR_USERNAME.github.io/REPO_NAME/
```

Masalan:
- Username: `xoji`
- Repo: `igloo-site`
- URL: `https://xoji.github.io/igloo-site/`

## ⚡ Tez yo'l (skript bilan):

```bash
cd /Users/xoji/Documents/comment
./deploy_to_github.sh
```

Keyin GitHub repository URL'ni kiriting.

## ✅ Xususiyatlar:

- ✅ **Bepul** - hech qanday to'lov yo'q
- ✅ **Haqiqiy domain** - `github.io` domain
- ✅ **HTTPS** - xavfsiz
- ✅ **1 oy+ ishlaydi** - GitHub Pages bepul
- ✅ **Butun dunyoda** - hamma ko'ra oladi
- ✅ **Avtomatik deploy** - har safar `git push` qilsangiz yangilanadi

## 🔄 Yangilash:

Saytni yangilash uchun:

```bash
cd /Users/xoji/Documents/comment
git add .
git commit -m "Update website"
git push
```

1-2 daqiqadan keyin yangilanishlar ko'rinadi!

## 📝 Eslatmalar:

- Repository **Public** bo'lishi kerak (bepul uchun)
- Fayllar 1GB dan oshmasligi kerak
- Har bir repository uchun 1 ta GitHub Pages sayti

