"""Build update.html: round-2 result + refreshed prices + next steps (warm, photo-led).

Inputs: research/round3_flaine.json, research/round3_arcs_flights.json, research/images*.json.
Every price shown is computed here from line items so the page and STATUS.html agree.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, 'research')
FX = 1.1764  # GBP→EUR, XE 4 Oct 2026; EUR items are converted at this rate
F = json.load(open(os.path.join(R, 'round3_flaine.json')))
A = json.load(open(os.path.join(R, 'round3_arcs_flights.json')))
U = json.load(open(os.path.join(R, 'images_unsplash.json')))
VOTE_API = 'https://script.google.com/macros/s/AKfycbx0xpQ9m3imgIU_5_4CmxtLu7ZN25M8bm75yihH3UCwl_4WYvLk50gJM9m-LfPcY2tR8w/exec'

def gbp(eur: float) -> float:
    return eur / FX

def photo(subject_key: str) -> dict:
    for p in F['photos']:
        if subject_key.lower() in p['subject'].lower():
            return {**p, 'src': 'Wikimedia Commons'}
    raise KeyError(subject_key)

def un(key: str, i: int) -> dict:
    return {**U[key][i], 'src': 'Unsplash'}

# --- package (per person, GBP) --------------------------------------------
out = A['flights']['out_wed27'][0]; back = next(f for f in A['flights']['back_sun31'] if 'PICK' in f['label'])
lines = [
  {'k': 'Flights', 'd': f"easyJet {out['from']} {out['dep']} → Geneva, back {back['dep']} → Gatwick", 'girl': out['pp_gbp'] + back['pp_gbp'], 'boy': out['pp_gbp'] + back['pp_gbp'], 'was': 94.17, 'tag': 'live'},
  {'k': 'Hold bag', 'd': '23 kg, both ways (or share one between two)', 'girl': 85, 'boy': 85, 'was': 85, 'tag': 'estimate'},
  {'k': 'Minibus', 'd': 'Private for 6, Geneva ⇄ Flaine, about 1h15', 'girl': F['transfer']['pp_gbp'], 'boy': F['transfer']['pp_gbp'], 'was': 411.43 / 6, 'tag': 'live'},
  {'k': 'Flats', 'd': 'Two flats in Flaine Forêt, split six ways', 'girl': 1168 / 6, 'boy': 1168 / 6, 'was': None, 'tag': 'live'},
  {'k': 'Lift pass', 'd': 'Beginner pass for the girls · Grand Massif for the boys', 'girl': gbp(F['lift']['beg_eur']), 'boy': gbp(F['lift']['adv_eur']), 'was': None, 'tag': 'published'},
  {'k': 'Lessons', 'd': 'Private ESF instructor for the four girls, Thu–Sat mornings', 'girl': gbp(480 / 4), 'boy': 0, 'was': gbp(144 * 3 / 4), 'tag': 'published'},
  {'k': 'Rental', 'd': 'Skis, boots, poles, helmet, booked online (−30%)', 'girl': gbp(F['rental']['beg_eur']), 'boy': 0, 'was': None, 'tag': 'live'},
  {'k': 'Insurance', 'd': 'Winter-sports cover', 'girl': 22 + gbp(14), 'boy': 22 + gbp(14), 'was': None, 'tag': 'estimate'},
]
girl = sum(l['girl'] for l in lines); boy = sum(l['boy'] for l in lines)
budget_girl = girl - 1168 / 6 + 592 / 6; budget_boy = boy - 1168 / 6 + 592 / 6
flats = [dict(x, total_gbp=x['total']) for x in F['flats']]
for x in flats:  # neutral wording on a public page
    x['name'] = x['name'].replace('(couple)', '(the boys)').replace('couple', 'boys')
    x['beds'] = x['beds'].replace('Couple:', 'The boys:').replace('(couple)', '(boys)').replace('couple', 'boys')
    x['note'] = (x.get('note') or '').replace('Couple fully separate (snoring solved)', 'The boys get their own flat').replace('couple', 'boys')

DATA = {
  'voteApi': VOTE_API,
  'checked': '10 Oct 2026',
  'pricePerson': {'girl': round(girl), 'boy': round(boy), 'budgetGirl': round(budget_girl), 'budgetBoy': round(budget_boy), 'foodPerDayEur': 60},
  'lines': [dict(l, girl=round(l['girl'], 2), boy=round(l['boy'], 2), was=(round(l['was'], 2) if l['was'] else None)) for l in lines],
  'flats': flats,
  'flights': {'out': A['flights']['out_wed27'][:2], 'back': [back] + [f for f in A['flights']['back_sun31'] if 'PICK' not in f['label']][:1]},
  'lessons': F['lessons'][:2],
  'experiences': F['experiences'],
  'arcs': {'girl': 796, 'boy': 719},
  'photos': {
    'hero': photo('Mont Blanc from'), 'platieres': photo('Grandes Platières (30'), 'forum': photo('Forum'), 'village': photo('overview'),
    'cascade': photo('Cascade'), 'fondue': un('mood_fondue', 0), 'apres': un('mood_apres', 0), 'lesson': un('mood_lesson', 0),
    'chalet': un('mood_chalet_interior', 1), 'night': un('mood_chalet_dusk', 3),
  },
}
tpl = open(os.path.join(ROOT, 'tools', 'update_template.html')).read()
html = tpl.replace('/*__DATA__*/', 'window.UPD = ' + json.dumps(DATA, ensure_ascii=False) + ';')
open(os.path.join(ROOT, 'update.html'), 'w').write(html)
print('update.html', len(html), '| girl', round(girl), 'boy', round(boy), '| budget', round(budget_girl), round(budget_boy))
