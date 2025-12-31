# 🔑 GitHub Personal Access Token Yaratish

## Qadamlar:

1. **GitHub'ga kiring:**
   - https://github.com/settings/tokens ga kiring
   - `brorasulov` username bilan login qiling

2. **Token yaratish:**
   - "Generate new token" > "Generate new token (classic)" ni bosing
   - **Note**: "igloo-site-deploy" (yoki istalgan nom)
   - **Expiration**: 90 days (yoki istalgan muddat)
   - **Select scopes**: 
     - ✅ **repo** (barcha repository'lar uchun)
   - "Generate token" ni bosing

3. **Token'ni nusxalab oling:**
   - ⚠️ Token faqat bir marta ko'rsatiladi!
   - Token'ni nusxalab, xavfsiz joyga saqlang

4. **Token'ni ishlatish:**
   - `git push` paytida password o'rniga token kiriting
   - Username: `brorasulov`
   - Password: Token'ni yozing

## Yoki credential helper ishlatish:

```bash
# Token'ni credential helper'ga saqlash
git config --global credential.helper osxkeychain

# Keyin push qilish
git push -u origin main
# Username: brorasulov
# Password: TOKEN_BU_YERDA
```

