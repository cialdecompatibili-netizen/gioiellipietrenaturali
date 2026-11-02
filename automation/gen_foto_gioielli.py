import csv, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from dati_shop_gioielli import CAT, P
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = r"C:\Users\mirco\Desktop\gemini_auto\img.py"
EXTRA = "No text, no logos, no brand names, no watermark."
def run(righe, profilo, out):
    lst = os.path.join(R, "automation", "_lista_%s.csv" % profilo)
    with open(lst, "w", encoding="utf-8", newline="") as f:
        for i, s in righe: f.write("%s;%s;%s\n" % (i, s, profilo))
    subprocess.run([sys.executable, IMG, "--lista", lst, "--out", os.path.join(R, out), "--extra", EXTRA], cwd=R)
    os.remove(lst)
def manca(i, d): return not os.path.exists(os.path.join(R, d, i + ".webp"))
prod = [(p[0], p[8]) for p in P if p[8] and manca(p[0], r"assets\images\prodotti")]
cat = [(k, v[0]) for k, v in CAT.items() if manca(k, r"assets\images\categorie")]
if prod: run(prod, "prodotto", r"assets\images\prodotti")
if cat: run(cat, "categoria", r"assets\images\categorie")
print("FINITO")
