"""Build book.html (booking night) from research/bn_*.json + round3 photos. All money is computed here."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, 'research')
FX = 1.1764  # GBP→EUR, XE 4 Oct 2026
VOTE_API = 'https://script.google.com/macros/s/AKfycbx0xpQ9m3imgIU_5_4CmxtLu7ZN25M8bm75yihH3UCwl_4WYvLk50gJM9m-LfPcY2tR8w/exec'
load = lambda n: json.load(open(os.path.join(R, n)))
S, F, X, P3 = load('bn_stay.json'), load('bn_flights.json'), load('bn_extras.json'), load('round3_flaine.json')
gbp = lambda eur: eur / FX
photo = lambda key: next({**p, 'src': 'Wikimedia Commons'} for p in P3['photos'] if key.lower() in p['subject'].lower())
opt = {o['id']: o for o in S['options']}

# --- per-person money (recommended plan) ---------------------------------
out, back = F['recommended']['out'], F['recommended']['back']
BAG_EST = 80          # 23 kg both ways, easyJet dynamic pricing (agent range £30–55 each way)
INSURANCE_EST = 30    # winter-sports single trip, agent range £20–45
LINEN_EST = 20        # girls' flat has no linen
flat_pp = opt['two_flats']['total_gbp'] / 6
lessons_eur = X['lessons'][0]['pp_eur']
common = [('Flights (out + back)', out['pp_1'] + back['pp_1'], 'You book: easyJet app or Google Flights'),
          ('Hold bag, both ways', BAG_EST, 'You add it to your flight (or share one between two)'),
          ('Flat share', flat_pp, 'Send to Joaquin, who books both flats'),
          ('Minibus share', X['transfer']['pp_gbp'], 'Send to whoever books the minibus'),
          ('Insurance', INSURANCE_EST, 'You buy: winter-sports cover'),
          ('Carré Neige rescue cover', gbp(14), 'Added to your lift pass in Flaine')]
girls = common + [('Lift pass (beginner)', gbp(X['passes']['beg_eur']), 'Buy day by day in Flaine'),
                  ('Lessons', gbp(lessons_eur), 'Send to whoever books the instructor'),
                  ('Rental with helmet', gbp(X['rental']['beg_eur']), 'Booked online by one person for all'),
                  ('Linen', LINEN_EST, 'Hire from the host or bring your own')]
boys = common + [('Lift pass (Grand Massif)', gbp(X['passes']['adv_eur']), 'Buy online the week before')]
total = lambda rows: sum(v for _, v, _ in rows)

def stay_card(o, tier, rec=False, extra_cons=None, label_urls=None):
    urls = o.get('urls') if isinstance(o.get('urls'), list) else [o.get('urls') or o.get('url')]
    labels = label_urls or (['Open listing ↗'] * len(urls))
    return {'tier': tier, 'rec': rec, 'name': o['name'].replace("'Apartment for 4 to 6 people' ", '').replace('value flat ', 'girls’ flat '),
            'total': o['total_gbp'], 'pp': round(o['total_gbp'] / 6), 'dates': o['dates'], 'beds': o['beds'], 'walk': o['walk'],
            'reviews': f"{o['rating']}. {o.get('reviews_themes', '')}", 'cancel': o['cancel'], 'pros': o['pros'][:4], 'cons': (o['cons'] + (extra_cons or []))[:4],
            'how': o.get('how_to_book', '') if rec else '', 'urls': [{'url': u, 'label': l} for u, l in zip(urls, labels)]}

stay_opts = [
  stay_card(opt['two_flats'], 'Our pick · exact dates', True, label_urls=['Book the boys’ flat ↗', 'Book the girls’ flat ↗']),
  stay_card(opt['two_flats_studio_cabin'], 'Same plan, better-reviewed girls’ flat', label_urls=['Boys’ flat ↗', 'Girls’ studio cabin ↗']),
  stay_card(opt['refuge_du_golf'], 'One roof · needs Sun → Sun'),
  stay_card(opt['grand_massif_4star_women'], 'Comfort upgrade for the girls', label_urls=['Boys’ flat ↗', 'Girls’ 4★ flat ↗']),
]
NAMES = ['Two flats in Flaine Forêt', 'Two flats, with the studio cabin for the girls', 'Refuge du Golf, 3 bedrooms (maeva)', 'Two flats, with a 4★ flat for the girls']
HOW = {0: 'Book the boys’ flat first (2 guests, £573), then the girls’ flat (4 guests, £590). Joaquin pays both, everyone sends £194. Set a reminder for 26 Dec, the last free-cancellation day. If the girls’ flat goes, use the studio cabin instead.'}
for i, c in enumerate(stay_opts):
    c['name'] = NAMES[i]
    c['how'] = HOW.get(i, '')
    c['dates'] = c['dates'].replace('->', '→').replace(' (27-31 not available)', ', our dates not offered')
    c['cancel'] = c['cancel'].replace('free before 28 Dec 2026', 'free until 27 Dec').replace('Free before 28 Dec 2026', 'Free until 27 Dec')
for c in stay_opts:  # neutral wording on a public page
    for k in ('name', 'beds', 'how'):
        c[k] = c[k].replace('the men', 'the boys').replace('the women', 'the girls').replace('Men:', 'Boys:').replace('Women:', 'Girls:')
    c['pros'] = [p.replace('the men', 'the boys').replace('woman', 'girl').replace('women', 'girls') for p in c['pros']]
    c['cons'] = [p.replace('the men', 'the boys').replace('Women', 'Girls').replace('women', 'girls').replace('woman', 'girl') for p in c['cons']]

host_message = """Hi! We've just booked your flat for Wed 27 → Sun 31 January, really looking forward to it.
A few quick questions:
1. Is linen and towels hire possible, and the price? (Girls' flat)
2. Could we drop bags or check out late on Sunday 31st? Our minibus leaves at 14:45.
3. Any chance of an earlier check-in on Wednesday? We land in Geneva at 13:15 and should arrive around 15:30.
4. (Boys' flat) Is there a table and chairs for 6 for one dinner together?
Thank you so much!"""

alts = [dict(dir='Out', dep=a['dep'], **{'from': a['from']}, to='GVA', airline=f"{a['airline']} {a['flight']}", pp=a['pp_1'], note='misses the minibus' if a['dep'] > '11:00' else 'catches the minibus') for a in F['alternatives_out']]
alts += [dict(dir='Back', dep=a['dep'], **{'from': 'GVA'}, to=a['arr'].split()[-1], airline=f"{a['airline']} {a['flight']}", pp=a['pp_1'], note='£17 cheaper, longer wait' if a['dep'] == '19:55' else '') for a in F['alternatives_back']]
bags = F['bags']
bags_html = (f"<p>23 kg hold bag: about {bags['hold_23kg_oneway'].replace('ESTIMATE ~GBP ', '£').split(' online')[0]} each way online (£60 at the airport). "
             f"Large cabin bag: {bags['large_cabin_oneway'].replace('ESTIMATE ~GBP ', '£').split(' online')[0]}. Seat to sit together: {bags['seat_from'].replace('ESTIMATE ~GBP ', '£').split(' standard')[0]}.</p>"
             "<p>A small under-seat bag is free. Ski bags are £45 per flight; rent skis in Flaine instead.</p>")
tips = ['Search the flight number in the easyJet app: U2 5741 out (Southend), U2 8490 back (Gatwick).',
        'Book tonight, in the same sitting: today the price is the same for 1 or 6 seats, and the cheapest seats go first.',
        'Name exactly as in your passport. Each of us adds our own bag and seat.',
        'To sit together, pick seats next to the ones already taken.',
        'HKSAR, BN(O) and British passports need no visa for a short Schengen trip. Allow time for the new EU biometric check at Geneva.',
        'Coming from the west? SWISS LX 359 from Heathrow at 07:00 (£67) also makes the minibus.']

les = X['lessons']
les_opts = [{'tier': 'Recommended', 'rec': True, 'name': 'ESF Flaine, private', 'pp': les[0]['pp_eur'], 'total': les[0]['price_total_eur'], 'format': '3 × 2 h, Thu–Sat mornings', 'note': 'The resort’s main school, meeting at Forêt or the Forum. The online calendar isn’t loading, so email or call tonight (04 50 90 81 00). Afternoons are €408 in total and warmer.', 'cancel': 'Ask: usually only with a medical note or Carré Neige', 'url': les[0]['url']},
            {'tier': 'Best rated', 'rec': False, 'name': 'Maison Sport, Flaine instructors', 'pp': les[1]['pp_eur'], 'total': les[1]['price_total_eur'], 'format': 'Pick a named instructor', 'note': 'Corentin R. is rated 4.98 from 163 reviews and speaks English. Prices from €60 an hour and may rise for 4.', 'cancel': les[1]['cancel'], 'url': les[1]['url']},
            {'tier': 'Independent', 'rec': False, 'name': 'Les Moniteurs Indépendants', 'pp': les[2]['pp_eur'], 'total': les[2]['price_total_eur'], 'format': '3 × 2 h mornings', 'note': 'English confirmed. Booking by form or phone: +33 6 07 19 56 09.', 'cancel': 'Ask', 'url': les[2]['url']}]
lesson_en = X['lesson_request_en'].replace('One of them is nervous after a fall and feels the cold, so we', 'We')
lesson_fr = X['lesson_request_fr'].replace("L'une d'elles appréhende depuis une chute et est frileuse : nous", 'Nous')

ins = X['insurance']
extras = [
  {'who': 'One volunteer · tonight or this week', 'title': 'Minibus to Flaine', 'price': f"£{X['transfer']['pp_gbp']:.0f} each", 'what': f"Private minibus for 6, Geneva 13:15 → Flaine, and back Sun 14:45 for the 18:25 flight. £{X['transfer']['price_total_gbp']:.0f} in total.", 'note': 'Free cancellation up to 24 hours before. On the site choose Private, Return, Geneva Airport → Flaine, 6 people, 6 bags.', 'links': [{'url': X['transfer']['url'], 'label': 'Alps2Alps ↗'}]},
  {'who': 'Everyone · this week', 'title': 'Travel insurance', 'price': '£20–45 each', 'what': 'Winter-sports cover with mountain rescue. A packaged bank account may already include it.', 'note': 'The free GHIC card covers state healthcare in France, not rescue.', 'links': [{'url': i['url'], 'label': i['name'].split(' +')[0].split(' (')[0] + ' ↗'} for i in ins] + [{'url': X['ghic_url'], 'label': 'GHIC (NHS) ↗'}]},
  {'who': 'One person · November', 'title': 'Skis, boots, helmets', 'price': f"€{X['rental']['beg_eur']:.0f} per girl", 'what': f"Book all six online with sizes; 30% off the shop price. Boys’ performance skis €{X['rental']['perf_eur']:.0f} if you don’t bring your own.", 'note': 'Pick a shop in Flaine Forêt, next to the flats.', 'links': [{'url': X['rental']['url'], 'label': 'Skiset Flaine ↗'}]},
  {'who': 'Later', 'title': 'Lift passes', 'price': f"€{X['passes']['beg_eur']:.0f} / €{X['passes']['adv_eur']:.0f}", 'what': 'Girls buy the beginner pass day by day in Flaine: same price, nothing wasted. Boys buy the Grand Massif pass online the week before.', 'note': 'Add Carré Neige rescue cover (€3.50 a day) at the till.', 'links': [{'url': X['passes']['url'], 'label': 'Grand Massif passes ↗'}]},
]
kit = [{'item': k['item'], 'buy_or_rent': k['buy_or_rent'].capitalize(), 'price': (f"£{k['price_gbp']:.2f}" if isinstance(k['price_gbp'], (int, float)) else f"£{k['price_gbp']}"), 'url': k.get('url', ''), 'note': k.get('note', '').replace('For the one who feels the cold', 'If you feel the cold').replace('for the one who feels the cold', 'if you feel the cold')} for k in X['kit']]
for k in kit:
    k['item'] = k['item'].replace('(for the one who feels the cold)', '(extra warm)')

tasks = [
  {'id': 'stay', 'anchor': 'stay', 'who': 'Joaquin books · everyone sends £194', 'title': 'Hold the two flats', 'what': 'Boys’ flat first, then the girls’ flat. Free to cancel until 27 December.', 'when': 'At the table, before the main course'},
  {'id': 'flight', 'anchor': 'flight', 'who': 'Everyone · on your phone', 'title': 'Book your flights', 'what': 'easyJet U2 5741 Southend 10:40 out; U2 8490 Gatwick 18:25 back (or 19:55, £17 cheaper).', 'when': 'Tonight, while seats are £28'},
  {'id': 'lessons', 'anchor': 'lessons', 'who': 'One of the girls', 'title': 'Send the lesson request', 'what': 'Copy the message below to ESF and Maison Sport, then pick the first good reply.', 'when': 'Tonight; reply within days'},
  {'id': 'minibus', 'anchor': 'extras', 'who': 'One volunteer', 'title': 'Book the minibus', 'what': f"Alps2Alps, £{X['transfer']['price_total_gbp']:.0f} for six, free to cancel until 24 h before.", 'when': 'This week'},
  {'id': 'insurance', 'anchor': 'extras', 'who': 'Everyone', 'title': 'Insurance + GHIC', 'what': 'Winter-sports cover with mountain rescue; free GHIC card from the NHS site.', 'when': 'This week'},
  {'id': 'gear', 'anchor': 'kit', 'who': 'Girls · one person books rental', 'title': 'Layers and rental', 'what': 'Buy warm layers before the trip; one person books skis for all six in November.', 'when': 'November'},
]
track = [{'id': 'flat', 'label': 'Flats booked', 'task': 'stay'}, {'id': 'fout', 'label': 'Flight out booked', 'task': 'flight'}, {'id': 'fback', 'label': 'Flight back booked', 'task': 'flight'},
         {'id': 'paid', 'label': 'Flat share sent', 'task': 'stay'}, {'id': 'lessons', 'label': 'Lesson request sent', 'task': 'lessons'}, {'id': 'minibus', 'label': 'Minibus booked', 'task': 'minibus'}, {'id': 'ins', 'label': 'Insurance bought', 'task': 'insurance'}]

girl_total, boy_total = total(girls), total(boys)
DATA = {
  'voteApi': VOTE_API, 'today': 'Saturday 17 October', 'checked': '17 Oct 2026 (flats, flights, minibus live; lessons, passes published; rental 10 Oct)',
  'crew': ['Joaquin', 'Juan', 'Chloe', 'Kannes', 'Ina', 'Natasha'],
  'price': {'girl': round(girl_total), 'boy': round(boy_total)},
  'glanceLead': f"Everything below was checked today. All-in it comes to about £{girl_total:.0f} per girl and £{boy_total:.0f} per boy, excluding food (around £200 for four days of meals and après).",
  'glance': [{'k': 'Where', 'v': 'Flaine, 1,600 m', 's': 'Grand Massif · 265 km of pistes'}, {'k': 'When', 'v': 'Wed 27 → Sun 31 Jan', 's': '4 nights · lessons Thu–Sat'},
             {'k': 'Getting there', 'v': 'Geneva + minibus', 's': 'Land 13:15 · in Flaine by about 15:30'}, {'k': 'Per person', 'v': f"£{girl_total:.0f} · £{boy_total:.0f}", 's': 'girls · boys, all-in except food'}],
  'tasks': tasks, 'trackTasks': track,
  'stay': {'headline': f"Two flats in Flaine Forêt, £{flat_pp:.0f} each", 'lead': 'Re-checked tonight. For our exact dates it’s still the only way to give the boys their own space and every girl her own bed. Nothing under one roof takes a Wednesday-to-Sunday booking. Both flats are free to cancel until 27 December, so booking tonight keeps every option open.',
           'options': stay_opts, 'hostMessage': host_message},
  'flights': {'lead': f"Everyone books their own ticket on the same flights, so we travel together and nobody fronts the money. Today: £{out['pp_1']} out and £{back['pp_1']} back, or £{F['alternatives_back'][0]['pp_1']} on the later return.",
              'out': {**out, 'to': 'GVA', 'pp': out['pp_1'], 'book_url': out['gf_url'], 'airline': 'easyJet'}, 'back': {**back, 'to': 'LGW', 'pp': back['pp_1'], 'book_url': back['gf_url'], 'airline': 'easyJet'},
              'alts': alts, 'bags': bags_html, 'tips': tips},
  'lessons': {'lead': 'One instructor for all four girls, three mornings, at their pace. Send the request below tonight and book whichever school replies first with a good instructor.', 'options': les_opts, 'en': lesson_en, 'fr': lesson_fr},
  'extras': extras,
  'money': {'lead': 'Each of us books our own flight, bag, insurance and lift pass. Shared bookings are paid by one person and settled the same evening.',
            'people': [{'who': 'Each girl', 'total': girl_total, 'rows': [{'k': k, 'v': v, 'how': h} for k, v, h in girls]}, {'who': 'Each boy', 'total': boy_total, 'rows': [{'k': k, 'v': v, 'how': h} for k, v, h in boys]}]},
  'kit': kit,
  'photos': {'hero': photo('Mont Blanc from'), 'end': photo('overview')},
}
tpl = open(os.path.join(ROOT, 'tools', 'book_template.html')).read()
open(os.path.join(ROOT, 'book.html'), 'w').write(tpl.replace('/*__DATA__*/', 'window.BN = ' + json.dumps(DATA, ensure_ascii=False) + ';'))
print('book.html built | girl', round(girl_total), 'boy', round(boy_total), '| flat pp', round(flat_pp))
