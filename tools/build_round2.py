"""Build data2.js (round-2 trip shapes x resorts) from research/round2_*.json.

Every matrix cell becomes a list of cost line items in the same schema as data.js,
so the page's cost engine, breakdown table and cost levers all use one source of truth.
"""
import json, os, urllib.request
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, 'research')
VOTE_API = 'https://script.google.com/macros/s/AKfycbx0xpQ9m3imgIU_5_4CmxtLu7ZN25M8bm75yihH3UCwl_4WYvLk50gJM9m-LfPcY2tR8w/exec'

SHAPES = [
    {'id': 'LS', 'nights': 6, 'dates': 'Sun 24 → Sat 30 Jan', 'al': '5', 'alDays': 'Mon–Fri', 'ski': '5 ski days, plus Saturday morning if flights allow', 'kannes': 'everyone flies out together on Sunday afternoon', 'kannesOk': True, 'note': 'Replaces round 1’s Sat → Sat: same leave, cheaper flats.', 'foodDays': 6, 'skiDays': 5, 'lessonDays': 5},
    {'id': 'M', 'nights': 5, 'dates': 'Tue 26 → Sun 31 Jan', 'al': '3–3.5', 'alDays': 'Tue afternoon–Fri', 'ski': 'About 4.5 ski days (Wed–Sat, Sunday morning)', 'kannes': 'everyone flies out together', 'kannesOk': True, 'note': 'Fly Tuesday afternoon or after work.', 'foodDays': 5, 'skiDays': 5, 'lessonDays': 4},
    {'id': 'S', 'nights': 4, 'dates': 'Wed 27 → Sun 31 Jan', 'al': '3', 'alDays': 'Wed–Fri', 'ski': 'About 3.5 ski days (Thu–Sat, Sunday morning)', 'kannes': 'everyone flies out together', 'kannesOk': True, 'note': 'Weekend skiing is cheaper for beginners at Les Arcs.', 'foodDays': 4, 'skiDays': 4, 'lessonDays': 3},
    {'id': 'XS', 'nights': 3, 'dates': 'Thu 28 → Sun 31 Jan', 'al': '2', 'alDays': 'Thu–Fri', 'ski': 'About 3 ski days (Thu afternoon–Sunday morning)', 'kannes': 'everyone flies out together', 'kannesOk': True, 'note': 'Early Thursday flight. Best where the transfer is short.', 'foodDays': 3, 'skiDays': 3, 'lessonDays': 3},
]

def load(name: str) -> dict:
    with open(os.path.join(R, name)) as f:
        return json.load(f)

FL = load('round2_flights.json')

def flight_item(airport: str, shape: str) -> dict:
    f = FL[airport][shape]
    pp = f['pp_gbp']; out = f['out']
    if airport == 'GVA' and shape == 'M':   # after-work Tuesday flight keeps leave to ~3 days
        pp = f['after_work']['pp_gbp']; out = f['after_work']['out']
    return {'label': f'Return flight London ⇄ {"Geneva" if airport == "GVA" else "Innsbruck" if airport == "INN" else "Salzburg"}',
            'note': f"Out: {out}. Back: {f.get('back', '').split(';')[0]}. Fare for 6 seats, cabin bag.",
            'adv': round(pp, 2), 'beg': round(pp, 2), 'cur': 'GBP', 'status': 'VERIFIED', 'src': f['url']}

SHORT_NAMES = [('Alpages du Chantel', 'Alpages du Chantel flat (ski-in/out, pool)'), ('Arcs 1800 60', 'Arc 1800 3-bed by the slopes'),
               ('La Nova', 'La Nova 3-bed, Villards'), ('Königin Serles', 'Königin Serles'), ('Kirchplatz', 'Kirchplatz Type C'),
               ('Ansitz Hofer', 'Ansitz Hofer'), ('Adler', 'Adler Boutique Hotel (B&B, pool)'), ('Bel Appartement', 'Bel Appartement 2-bed'),
               ('Chalet Éline', 'Chalet Éline, 4-star'), ('Duplex', 'Duplex Center 3-bed')]

def short_name(name: str) -> str:
    """Readable flat name for the matrix; the full listing name stays in the breakdown note."""
    for key, short in SHORT_NAMES:
        if key in name:
            return short
    return name

def stay(st: dict) -> dict:
    out = {k: st.get(k) for k in ('url', 'total', 'cur', 'beds', 'lift', 'rating', 'cancel', 'status')}
    out['name'] = short_name(st.get('name', ''))
    return out

def num(v: Any, default: float = 0.0) -> float:
    return float(v) if isinstance(v, (int, float)) else default

def build_cell(resort: dict, shape: dict, d: dict, tier: str, school_override: dict) -> list:
    sh = shape['id']
    st = d['stay_value'] if tier == 'budget' else d['stay_comfort']
    items = [flight_item(resort['airport'], sh),
             {'label': '23 kg hold bag, both ways', 'note': 'easyJet/BA estimate. On short trips two people can share one bag.', 'adv': 85, 'beg': 85, 'cur': 'GBP', 'status': 'ESTIMATE', 'kind': 'bag', 'days': 1},
             {'label': 'Airport transfer, return', 'note': d.get('transfer_note', ''), 'adv': num(d['transfer_pp']), 'beg': num(d['transfer_pp']), 'cur': 'EUR', 'status': 'ESTIMATE' if 'ESTIMATE' in d.get('transfer_note', '') else 'PUBLISHED'},
             {'label': f"{short_name(st['name'])}, {shape['nights']} nights", 'note': f"{st.get('beds', '')}. {st.get('lift', '')} to the lift. Rated {st.get('rating', 'n/a')}. {st.get('cancel', '')}", 'group': True, 'amount': num(st['total']), 'cur': st.get('cur', 'EUR'), 'status': 'VERIFIED' if 'VERIFIED' in str(st.get('status', '')) else 'ESTIMATE', 'src': st.get('url')}]
    if resort.get('touristTax'):
        tt = resort['touristTax'] * shape['nights']
        items.append({'label': 'Tourist tax', 'note': f"€{resort['touristTax']:.2f} per person per night, paid locally", 'adv': tt, 'beg': tt, 'cur': 'EUR', 'status': 'PUBLISHED'})
    items.append({'label': 'Lift pass', 'note': d.get('lift_note', ''), 'intAs': 'adv', 'adv': num(d['lift_adv']), 'beg': num(d['lift_beg']), 'cur': 'EUR', 'status': 'PUBLISHED', 'kind': 'lift', 'days': shape['skiDays']})
    if resort.get('carre'):
        c = 3.5 * shape['skiDays']
        items.append({'label': 'Carré Neige piste-rescue cover', 'intAs': 'adv', 'adv': c, 'beg': c, 'cur': 'EUR', 'status': 'PUBLISHED'})
    so = school_override[tier]
    items.append({'label': so['beg_label'], 'note': so.get('beg_note', d.get('school_note', '')), 'intAs': 0, 'adv': 0, 'beg': so['beg'], 'cur': 'EUR', 'status': so.get('status', 'PUBLISHED'), 'kind': 'school', 'days': shape['lessonDays']})
    if so.get('int'):
        items.append({'label': so['int_label'], 'note': so.get('int_note', ''), 'adv': 0, 'beg': 0, 'int': so['int'], 'cur': 'EUR', 'status': so.get('int_status', 'PUBLISHED'), 'kind': 'school', 'days': shape['lessonDays']})
    items.append({'intAs': 'beg', 'label': 'Rental for beginners and Natasha', 'note': d.get('rental_note', ''), 'adv': 0, 'beg': num(d['rental_beg']), 'cur': 'EUR', 'status': 'ESTIMATE' if 'ESTIMATE' in d.get('rental_note', '') else 'VERIFIED', 'kind': 'rental', 'days': shape['skiDays']})
    ins = 27 if shape['nights'] >= 6 else 22
    items.append({'label': 'Travel insurance with winter-sports cover', 'adv': ins, 'beg': ins, 'cur': 'GBP', 'status': 'ESTIMATE'})
    return items

# School choices per resort/shape/tier (beginners = Chloe, Kannes, Ina; int = Natasha), from research notes.
SCHOOL = {
  'arcs': {
    'LS': {'budget': {'beg': 236, 'beg_label': 'Beginners: ESF group course (join Monday)', 'int': 236, 'int_label': 'Natasha: ESF adult group at her level', 'int_status': 'ESTIMATE'},
           'comfort': {'beg': 417, 'beg_label': 'Beginners: private ESF instructor for 3, 5 mornings × 3h30', 'status': 'VERIFIED', 'int': 236, 'int_label': 'Natasha: ESF adult group at her level', 'int_status': 'ESTIMATE'}},
    'M': {'budget': {'beg': 220, 'beg_label': 'Beginners: Arc Aventures private for 3, 4 × 2h30', 'beg_note': 'No group course starts midweek, so a budget private is the cheapest option.', 'int': 260, 'int_label': 'Natasha: 2 private sessions × 2 h', 'int_status': 'ESTIMATE'},
          'comfort': {'beg': 333, 'beg_label': 'Beginners: private ESF instructor for 3, 4 × 3h30', 'status': 'VERIFIED', 'int': 390, 'int_label': 'Natasha: 3 private sessions × 2 h', 'int_status': 'ESTIMATE'}},
    'S': {'budget': {'beg': 165, 'beg_label': 'Beginners: Arc Aventures private for 3, 3 × 2h30', 'beg_note': 'No group course starts midweek.', 'int': 130, 'int_label': 'Natasha: 1 private session × 2 h', 'int_status': 'ESTIMATE'},
          'comfort': {'beg': 250, 'beg_label': 'Beginners: private ESF instructor for 3, 3 × 3h30', 'status': 'VERIFIED', 'int': 260, 'int_label': 'Natasha: 2 private sessions × 2 h', 'int_status': 'ESTIMATE'}},
    'XS': {'budget': {'beg': 153, 'beg_label': 'Beginners: Arc Aventures private for 3 (Thu pm, Fri, Sat)', 'int': 130, 'int_label': 'Natasha: 1 private session × 2 h', 'int_status': 'ESTIMATE'},
           'comfort': {'beg': 210, 'beg_label': 'Beginners: ESF private for 3 (Thu pm 2 h, Fri & Sat 3h30)', 'status': 'VERIFIED', 'int': 260, 'int_label': 'Natasha: 2 private sessions × 2 h', 'int_status': 'ESTIMATE'}},
  },
  'stubai': {
    'LS': {'budget': {'beg': 270, 'beg_label': 'Beginners: Skischule Stubai Tirol group, Mon–Thu 4 h', 'int': 205, 'int_label': 'Natasha: “slightly advanced” group, Mon–Thu 2 h'},
           'comfort': {'beg': 450, 'beg_label': 'Beginners: private instructor for 3, Mon–Fri mornings', 'int': 205, 'int_label': 'Natasha: “slightly advanced” group, Mon–Thu 2 h'}},
    'M': {'budget': {'beg': 180, 'beg_label': 'Beginners: group lessons Wed–Thu (4 h), then practise', 'beg_note': 'Fulpmes group courses don’t run Fri or Sat.', 'int': 140, 'int_label': 'Natasha: group Wed–Thu, 2 h'},
          'comfort': {'beg': 360, 'beg_label': 'Beginners: private instructor for 3, Wed–Sat mornings', 'int': 275, 'int_label': 'Natasha: Olympia glacier group, 4 days'}},
    'S': {'budget': {'beg': 210, 'beg_label': 'Beginners: Schischule Fulpmes private for 3, Thu–Sat mornings', 'beg_note': 'Only one group day (Thu) is possible, so private is the realistic option. Fulpmes school is about €70 pp a day.', 'status': 'ESTIMATE', 'int': 80, 'int_label': 'Natasha: group Thursday, 2 h'},
          'comfort': {'beg': 270, 'beg_label': 'Beginners: Skischule Stubai Tirol private for 3, Thu–Sat mornings', 'int': 240, 'int_label': 'Natasha: Olympia glacier group, 3 days'}},
    'XS': {'budget': {'beg': 210, 'beg_label': 'Beginners: Schischule Fulpmes private for 3 (Thu pm, Fri, Sat)', 'status': 'ESTIMATE', 'int': 180, 'int_label': 'Natasha: Olympia glacier group, Fri + Sat'},
           'comfort': {'beg': 263.33, 'beg_label': 'Beginners: Skischule Stubai Tirol private for 3 (Thu pm, Fri, Sat)', 'int': 180, 'int_label': 'Natasha: Olympia glacier group, Fri + Sat'}},
  },
}

RESORTS = [
    {'id': 'C', 'key': 'arcs', 'kanji': '三', 'short': 'Les Arcs 1800', 'sub': 'France · fly Geneva · ≈3 h transfer', 'airport': 'GVA', 'carre': True, 'food': 65},
    {'id': 'B', 'key': 'stubai', 'kanji': '二', 'short': 'Stubai (Fulpmes)', 'sub': 'Austria · fly Innsbruck · 25 min transfer', 'airport': 'INN', 'touristTax': 4.8, 'food': 60},
]

def main() -> None:
    cells, notes = {}, {}
    resorts = list(RESORTS)
    pivot_path = os.path.join(R, 'round2_pivot.json')
    if os.path.exists(pivot_path):
        P = load('round2_pivot.json')
        resorts.append(P['_resort'])
        SCHOOL['pivot'] = P['_school']
    for r in resorts:
        data = load(f"round2_{r['key']}.json")
        cells[r['id']] = {}
        for sh in SHAPES:
            d = data['shapes'].get(sh['id'])
            if not d or not d.get('feasible') or sh['id'] not in SCHOOL[r['key']]:
                cells[r['id']][sh['id']] = {'feasible': False, 'note': (d or {}).get('note', 'Not researched for this length')}
                continue
            cells[r['id']][sh['id']] = {
                'feasible': True, 'note': d.get('note', ''), 'food': r.get('food', 60),
                'budget': {'stay': stay(d['stay_value']), 'items': build_cell(r, sh, d, 'budget', SCHOOL[r['key']][sh['id']])},
                'comfort': {'stay': stay(d['stay_comfort']), 'items': build_cell(r, sh, d, 'comfort', SCHOOL[r['key']][sh['id']])},
            }
    # Freeze round-1 ballots (live snapshot at build time)
    with urllib.request.urlopen(VOTE_API) as resp:
        live = json.load(resp)
    r1 = [b for b in live['ballots'] if not b['answers'].get('round')]
    out = {'resorts': [{k: r[k] for k in ('id', 'kanji', 'short', 'sub')} for r in resorts], 'shapes': SHAPES, 'cells': cells,
           'round1': {'ballots': r1}}
    with open(os.path.join(ROOT, 'data2.generated.json'), 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('resorts', [r['short'] for r in resorts], 'round1 ballots', len(r1))

if __name__ == '__main__':
    main()
