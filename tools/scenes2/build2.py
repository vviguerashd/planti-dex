# Genera los fondos v2 (sin plantas ni Gala) y sus variantes de temporada, más src/lib/scenes.json.
# Uso: TV_IMG=/ruta/gala_con_dios.png python3 tools/scenes2/build2.py   (la imagen de la tele no va al repo)
import json, os, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / 'tools' / 'scenes'))
import estudio2, escaleras2, sala2, bufetera2, jardin2
SEASONS = ['halloween']
OUT = ROOT / 'public' / 'scenes'; OUT.mkdir(parents=True, exist_ok=True)

def render(season):
    for m in (estudio2, escaleras2, sala2, bufetera2, jardin2): m.SEASON = season
    res = {}
    res['estudio'] = (estudio2.background(1), {'P13': (146, 38), 'P09': (206, 97)}, 206, (130, 159))
    im, hooks = escaleras2.background(1); (h1x, h1y), (h2x, h2y) = hooks
    res['escaleras'] = (im, {'P05': (123, 46), 'P01': (h1x - 40, h1y), 'P02': (h2x - 40, h2y)}, 207, (196, 162))
    res['sala'] = (sala2.background(1), sala2.POS, 216, (300, 168))
    res['bufetera'] = (bufetera2.background(1), bufetera2.POS, 207, (120, 160))
    res['cochera'] = (jardin2.cochera_bg(1), jardin2.CO_POS, 214, (240, 170))
    res['pasillo'] = (jardin2.pasillo_bg(1), jardin2.PA_POS, 214, (280, 170))
    return res

if not os.environ.get('TV_IMG') or not os.path.exists(os.environ['TV_IMG']):
    raise SystemExit('Falta TV_IMG: la imagen de Gala con Dios para la tele (no se guarda en el repo).')
base = render(None)
labels = {'escaleras': 'Escaleras', 'estudio': 'Estudio', 'sala': 'Sala', 'bufetera': 'Bufetera', 'cochera': 'Cochera', 'pasillo': 'Pasillo'}
out = []
for sid in ('escaleras', 'estudio', 'sala', 'bufetera', 'cochera', 'pasillo'):
    im, pos, floor, sleep = base[sid]; im.convert('RGB').save(OUT / f'{sid}.png', optimize=True)
    out.append({'id': sid, 'label': labels[sid], 'w': im.width, 'h': im.height, 'floor': floor, 'sleep': list(sleep),
                'plants': {k: list(v) for k, v in pos.items()}, 'seasons': SEASONS})
for season in SEASONS:
    for sid, (im, *_rest) in render(season).items(): im.convert('RGB').save(OUT / f'{sid}_{season}.png', optimize=True)
json.dump(out, open(ROOT / 'src' / 'lib' / 'scenes.json', 'w'), ensure_ascii=False, indent=1)
print([(o['id'], o['w'], o['h']) for o in out])
