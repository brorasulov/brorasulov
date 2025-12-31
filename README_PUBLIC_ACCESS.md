# 🌐 Public Access Setup

Saytni internet orqali hamma ko'ra olishi uchun quyidagilarni bajaring:

## 📋 Qadamlar:

### 1. Local server'ni ishga tushiring

Bir terminal ochib:

```bash
cd /Users/xoji/Documents/comment
python3 -m http.server 8000 --bind 0.0.0.0
```

### 2. Public tunnel'ni ishga tushiring

**Ikkinchi terminal** ochib:

```bash
cd /Users/xoji/Documents/comment
./start_public_tunnel.sh
```

## 🔧 Tunnel vositalari:

### Variant 1: ngrok (Tavsiya etiladi)

**O'rnatish:**
```bash
brew install ngrok/ngrok/ngrok
```

**Ishga tushirish:**
```bash
ngrok http 8000
```

Sizga public URL beriladi, masalan: `https://abc123.ngrok-free.app`

### Variant 2: localtunnel

**O'rnatish:**
```bash
npm install -g localtunnel
```

**Ishga tushirish:**
```bash
lt --port 8000
```

### Variant 3: Cloudflare Tunnel

**O'rnatish:**
```bash
brew install cloudflared
```

**Ishga tushirish:**
```bash
cloudflared tunnel --url http://localhost:8000
```

## ⚠️ Eslatmalar:

1. **Ikki terminal kerak:**
   - Birinchisi: Local server (python3 -m http.server)
   - Ikkinchisi: Tunnel (ngrok yoki boshqa)

2. **Tunnel URL'ni boshqalarga yuboring:**
   - Masalan: `https://abc123.ngrok-free.app`
   - Bu URL butun dunyoda ishlaydi!

3. **Server'ni to'xtatish:**
   - Har ikkala terminalda `Ctrl+C` bosing

## 🎯 Eng oson yo'l:

```bash
# Terminal 1
cd /Users/xoji/Documents/comment
python3 -m http.server 8000 --bind 0.0.0.0

# Terminal 2 (yangi terminal)
cd /Users/xoji/Documents/comment
ngrok http 8000
```

Keyin ngrok bergan URL'ni boshqalarga yuboring!

