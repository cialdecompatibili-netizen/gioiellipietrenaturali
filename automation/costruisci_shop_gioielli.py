# Scrive catalogo.json (categorie con descrizione/immagine, 1 prodotto reale per categoria) e le pagine prodotto IT+EN.
# JSON con ensure_ascii=False (docs/ERRORI_NOTI.md punto 23). Prezzi = segnaposto da confermare.
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from dati_shop_gioielli import CAT, P
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(R, "_data", "catalogo.json")
def foto(rel):  # campo immagine solo se il file esiste (il layout ricade sull'icona se vuoto)
    return rel if os.path.exists(os.path.join(R, rel)) else ""
d = json.load(open(path, encoding="utf-8"))
for c in d["categorie"]:
    s = CAT[c["id"]]
    c["descrizione"] = s[1]
    c["immagine"] = foto("assets/images/categorie/%s.webp" % c["id"])
    c.setdefault("tr", {}).setdefault("en", {})["descrizione"] = s[2]
prod = []
for (pid, cat, nit, nen, prezzo, dit, den, slug, _s) in P:
    prod.append({
        "tipo": "fisico", "id": pid, "nome": nit, "categoria": cat, "prezzo_centesimi": prezzo,
        "descrizione": dit,
        "descrizione_completa": dit + "\nPietre naturali, ogni pezzo puo' avere piccole differenze di colore e venatura.\nFatto a mano.",
        "immagine": foto("assets/images/prodotti/%s.webp" % pid), "icona": "\U0001F48E", "visibile": True,
        "tr": {"en": {"nome": nen, "descrizione": den,
                      "descrizione_completa": den + "\nNatural stones: each piece may show slight differences in colour and veining.\nHandmade."}}})
d["prodotti"] = prod
json.dump(d, open(path, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
json.load(open(path, encoding="utf-8"))
def w(rel, txt):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(txt)
for (pid, cat, nit, nen, prezzo, dit, den, slug, _s) in P:
    w("_negozio/%s.md" % pid, '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /negozio/%s/\ndescription: "%s"\nref: shop-prod-%s\n---\n' % (nit, pid, pid, dit.replace('"', "'"), pid))
    w("en/negozio/%s.md" % pid, '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /en/shop/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-prod-%s\n---\n' % (nen, pid, slug, den.replace('"', "'"), pid))
print("OK", len(prod))
