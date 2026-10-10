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
  {'k': 'Linen', 'd': 'Bed linen and towels for the girls’ flat (not provided there): hire or bring', 'girl': 20, 'boy': 0, 'was': None, 'tag': 'estimate'},
  {'k': 'Insurance', 'd': 'Winter-sports cover', 'girl': 22 + gbp(14), 'boy': 22 + gbp(14), 'was': None, 'tag': 'estimate'},
]
girl = sum(l['girl'] for l in lines); boy = sum(l['boy'] for l in lines)
budget_girl = girl - 1168 / 6 + 592 / 6; budget_boy = boy - 1168 / 6 + 592 / 6
C = json.load(open(os.path.join(R, 'round3_chalet.json')))
nid, val = C['current']['nid_alpin'], C['current']['value_flat']
opt = {o['name'].split(',')[0]: o for o in C['single_options']}
golf = next(o for o in C['single_options'] if 'Refuge du Golf' in o['name'])
ald = next(o for o in C['single_options'] if 'Aldébaran' in o['name'])
GOLF_CLEAN_GBP = 98  # end-of-stay cleaning, maeva estimate €80–150
flats = [
  {'tier': 'pick', 'name': 'Two flats in Flaine Forêt', 'total': 1168, 'nights_note': 'Wed 27 → Sun 31, exact dates',
   'beds': 'Girls: bunk room (2), a double (1), sofa bed (1), so everyone has her own bed. Boys: their own renovated flat (double + bunk cabin).',
   'where': 'About 200 m apart (3–5 min). Lifts 3–8 min via the free inclined lifts to the Forum.',
   'reviews': 'Boys’ flat 5.0 from 7 (new, very clean). Girls’ flat 4.0 from 1 (good location, no linen).',
   'pros': ['Cheapest way to give the boys their own space', 'Exact dates, nothing wasted', 'Both free to cancel until 28 Dec'],
   'cons': ['Two kitchens, so dinners are cosier in a restaurant', 'Girls’ flat: kitchenette, no wifi, no linen, 1 bathroom', 'Girls’ checkout 09:00 vs a 14:45 minibus'],
   'links': [{'label': 'Girls’ flat ↗', 'url': val['url']}, {'label': 'Boys’ flat ↗', 'url': nid['url']}]},
  {'tier': 'one roof', 'name': 'Refuge du Golf, 3 bedrooms (maeva)', 'total': golf['total_gbp'] + GOLF_CLEAN_GBP, 'nights_note': 'Sun 24 → Sun 31: 7 nights minimum, so 3 unused',
   'beds': 'Boys: double with its own bathroom. Girls: a twin room and a double. 66 m², table for 8, 2 bathrooms.',
   'where': 'Hameau, about 2 km above the centre: free shuttle every 15 min, so beginners carry kit on the bus.',
   'reviews': '4.5 from 2 (2021–22); manager maeva 4.0 from 1,692. Clean, quiet, great view.',
   'pros': ['Everyone together, with a big table and a pool', 'Proper rooms for everyone'],
   'cons': ['About £118 more each, partly for 3 nights we don’t use', 'Shuttle-dependent; few reviews; €700 deposit; cleaning extra'],
   'links': [{'label': 'Listing ↗', 'url': golf['url']}]},
  {'tier': 'best location', 'name': 'Aldébaran, Flaine Forum (ski-in/out)', 'total': ald['total_gbp'], 'nights_note': 'Sun 24 → Sun 31: 7 nights minimum, so 3 unused',
   'beds': 'Boys: own room, but it shares a wall with a girls’ room. Girls: a twin room, plus 2 singles in the living room.',
   'where': 'On the snow at the Forum, with the ski school downstairs and the supermarket 100 m away.',
   'reviews': '4.76 from 33: warm, good showers, well-stocked kitchen; cleanliness 4.3.',
   'pros': ['Best spot for beginners', 'Linen included, 2 bathrooms + WC'],
   'cons': ['Doesn’t fully separate the boys', 'Two girls sleep in the living room', 'About £75 more each, partly for unused nights'],
   'links': [{'label': 'Listing ↗', 'url': ald['url']}]},
]
for f in flats:
    f['pp'] = round(f['total'] / 6)
before_booking = ['Ask the girls’ host whether linen can be hired; otherwise bring a sheet set and towel each.',
                  'Agree a late checkout or a place to leave bags on Sunday (checkout 09:00, minibus 14:45); the boys’ flat checks out at 11:00.',
                  'Confirm the boys’ flat has a table for six for a night in.']
DATA = {
  'voteApi': VOTE_API,
  'checked': '10 Oct 2026',
  'pricePerson': {'girl': round(girl), 'boy': round(boy), 'budgetGirl': round(budget_girl), 'budgetBoy': round(budget_boy), 'foodPerDayEur': 60},
  'lines': [dict(l, girl=round(l['girl'], 2), boy=round(l['boy'], 2), was=(round(l['was'], 2) if l['was'] else None)) for l in lines],
  'flats': flats,
  'beforeBooking': before_booking,
  'oneRoofDelta': round((golf['total_gbp'] + GOLF_CLEAN_GBP - 1168) / 6),
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
