# Fayllarni to'g'rilash

Terminalda quyidagi buyruqlarni bajaring:

```bash
cd /Users/xoji/Documents/comment

# bg.png ni ko'chirish
cp assets/images/cubes/bg.pngsrgb assets/images/cubes/bg.png

# advect.png ni ko'chirish
cp assets/images/cubes/advect.pngcolordata-repeat assets/images/cubes/advect.png

# cubes_env.exr ni ko'chirish
cp assets/cubes_env.exr assets/images/cubes_env.exr

# Tekshirish
ls -lh assets/images/cubes/bg.png assets/images/cubes/advect.png assets/images/cubes_env.exr
```

Yoki Python skriptini ishga tushiring:

```bash
cd /Users/xoji/Documents/comment
python3 copy_correct_names.py
```

Keyin brauzerda qayta yuklang (Cmd+R yoki F5).

