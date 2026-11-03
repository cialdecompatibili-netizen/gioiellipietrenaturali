"""Genera le copertine (header.teaser) mancanti degli articoli con Gemini (img.py) e le collega.

Uso:  python automation/foto_mancanti.py [--max N] [--no-push] [--dry]
- cerca gli articoli IT (_posts) senza header.teaser; EN (en/_posts) con lo stesso `ref` riusa la stessa foto
- genera assets/images/posts/<ref>.webp (profilo blog 16:9, senza testo: sito multilingua)
- scrive header.teaser nel front matter IT+EN, poi commit e push (salvo --no-push)
Prodotti/categorie mancanti: python automation/gen_foto_gioielli.py
"""
import argparse, glob, os, re, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = r"C:\Users\mirco\Desktop\gemini_auto\img.py"
OUT = os.path.join(R, "assets", "images", "posts")
EXTRA = ("ABSOLUTELY NO TEXT of any kind: no letters, no numbers, no words, no logos, no watermark. "
         "Language-neutral editorial photo of natural stone jewelry, soft natural light, elegant, no people.")


def leggi(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def fm(t):
    m = re.match(r"---\r?\n(.*?)\r?\n---", t, re.S)
    return m.group(1) if m else ""


def campo(f, k):
    m = re.search(r"^%s:\s*\"?(.*?)\"?\s*$" % k, f, re.M)
    return m.group(1) if m else ""


def collega(p, url):
    t = leggi(p)
    nl = "\r\n" if "\r\n" in t else "\n"
    m = re.match(r"(---\r?\n.*?)(\r?\n---)", t, re.S)
    nuovo = m.group(1) + nl + "header:" + nl + '  teaser: "%s"' % url + m.group(2) + t[m.end():]
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(nuovo)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=0)
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    todo = []
    for p in sorted(glob.glob(os.path.join(R, "_posts", "*.md"))):
        f = fm(leggi(p))
        if "teaser:" in f:
            continue
        ref = campo(f, "ref") or os.path.splitext(os.path.basename(p))[0][11:]
        todo.append((ref, p, campo(f, "title"), campo(f, "excerpt")))
    if a.max:
        todo = todo[:a.max]
    print("Articoli senza copertina:", len(todo))
    if a.dry or not todo:
        for t in todo:
            print(" -", t[0])
        return
    os.makedirs(OUT, exist_ok=True)
    fatti = []
    for ref, p, titolo, exc in todo:
        dest = os.path.join(OUT, ref + ".webp")
        if not os.path.exists(dest):
            soggetto = "Blog cover about: %s. %s" % (titolo, exc)
            subprocess.run([sys.executable, IMG, soggetto, "--profilo", "blog", "--nome", ref,
                            "--out", OUT, "--extra", EXTRA], cwd=R)
        if not os.path.exists(dest):
            print("MANCA", dest, "(da rifare)")
            continue
        url = "/assets/images/posts/%s.webp" % ref
        collega(p, url)
        for pe in glob.glob(os.path.join(R, "en", "_posts", "*.md")):
            fe = fm(leggi(pe))
            if campo(fe, "ref") == ref and "teaser:" not in fe:
                collega(pe, url)
        fatti.append(ref)
        print("OK", ref, "- guarda la foto:", dest)
    if fatti and not a.no_push:
        subprocess.run(["git", "add", "-A"], cwd=R)
        subprocess.run(["git", "commit", "-m", "Copertine articoli: " + ", ".join(fatti)], cwd=R)
        subprocess.run(["git", "push"], cwd=R)
    print("FINITO")


if __name__ == "__main__":
    main()
