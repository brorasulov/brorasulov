# 🔧 GitHub Pages URL'ni To'g'rilash

## Muammo:
Custom domain maydoniga `brorasulov.github.io/brorasulov/` kiritilgan, bu noto'g'ri.

## Yechimlar:

### Variant 1: Repository nomini o'zgartirish (URL: https://brorasulov.github.io/)

Agar URL `https://brorasulov.github.io/` bo'lishini xohlasangiz:

1. **Yangi repository yarating:**
   - Repository nomi: `brorasulov.github.io` (maxsus nom)
   - https://github.com/new ga kiring
   - Repository name: `brorasulov.github.io`
   - Public qiling

2. **Fayllarni yangi repository'ga push qiling:**
   ```bash
   cd /Users/xoji/Documents/comment
   git remote set-url origin https://github.com/brorasulov/brorasulov.github.io.git
   git push -u origin main
   ```

3. **GitHub Pages'ni yoqing:**
   - Settings > Pages
   - Source: Deploy from a branch
   - Branch: main
   - Folder: / (root)

4. **Sayt manzili:**
   ```
   https://brorasulov.github.io/
   ```

### Variant 2: Hozirgi repository bilan ishlash (URL: https://brorasulov.github.io/brorasulov/)

Agar hozirgi repository bilan ishlashni xohlasangiz:

1. **GitHub Pages'da:**
   - Settings > Pages
   - **Custom domain** maydonini bo'sh qoldiring
   - Faqat Source sozlamalarini qiling:
     - Source: Deploy from a branch
     - Branch: main
     - Folder: / (root)

2. **Sayt manzili:**
   ```
   https://brorasulov.github.io/brorasulov/
   ```

### Variant 3: Haqiqiy custom domain qo'shish

Agar haqiqiy domain'ingiz bo'lsa (masalan: `example.com`):

1. **CNAME faylini yarating:**
   ```bash
   echo "example.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **GitHub Pages'da:**
   - Settings > Pages
   - Custom domain: `example.com`
   - Save

3. **DNS sozlamalari:**
   - Domain provayderingizda CNAME yoki A record qo'shing

## Tavsiya:

Agar URL `https://brorasulov.github.io/` bo'lishini xohlasangiz, **Variant 1** ni tanlang.

Agar hozirgi URL bilan tushunsangiz, **Variant 2** ni tanlang.

