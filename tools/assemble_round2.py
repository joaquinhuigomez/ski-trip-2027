"""Assemble data2.js: generated round-2 cells + human-written copy and decisions."""
import json, os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gen = json.load(open(os.path.join(ROOT, 'data2.generated.json')))
def maybe(key):
    path = os.path.join(ROOT, 'research', f'round2_{key}.json')
    return json.load(open(path)) if os.path.exists(path) else None
EXTRAS = [x for x in (maybe('geneva2'), maybe('tarentaise')) if x and '_resort' in x]
# Photos per candidate resort (all licence-checked in research/images*.json)
PHOTOS = {
  'Avoriaz': lambda: [ui('avoriaz', 0), ui('avoriaz', 2), wi('avoriaz', 1)],
  'Flaine': lambda: [wi('flaine', 0), wi('flaine', 1), ui('mood_fondue', 2), ui('mood_lesson', 0)],
  'La Plagne': lambda: [wi('la_plagne', 0), wi('la_plagne', 1), ui('mood_apres', 0), ui('mood_gondola', 1)],
  'Les Menuires': lambda: [ui('les_menuires', 1), ui('les_menuires', 2), wi('3vallees', 4)],
}
def photos_for(name):
    for k, f in PHOTOS.items():
        if k.lower() in name.lower():
            return f()
    return []
W = json.load(open(os.path.join(ROOT, 'research', 'images.json')))
U = json.load(open(os.path.join(ROOT, 'research', 'images_unsplash.json')))
def wi(k, i): x = dict(W[k][i]); x['src'] = 'Wikimedia Commons'; return x
def ui(k, i): x = dict(U[k][i]); x['src'] = 'Unsplash'; return x

R2 = dict(gen)
R2.update({
  'closeLabel': 'Wed 14 Oct',
  'lead': 'Round 1 gave us a favourite and two practical problems. Round 2 keeps the best of round 1, adds shorter and cheaper trips, and asks only about length, leave and resort. Every price is live for our dates (checked 4 October).',
  'changes': [
    {'k': 'Round 1', 't': 'Les Arcs came first', 'd': 'Les Arcs 7 points, Val Thorens 6, Stubai 5, with 4 of 6 votes in. Val Thorens and Stubai drop out: Val Thorens has the priciest flats, and Innsbruck flights cost two to three times Geneva’s.'},
    {'k': 'Flying together', 't': 'Every trip now starts on Sunday or later', 'd': 'One of us can only fly from Sunday afternoon, so the full week now runs Sunday to Saturday and we all travel together. Same leave as before, and the flats are cheaper.'},
    {'k': 'Price', 't': 'Shorter, cheaper options', 'd': 'Some of us asked for a cheaper version. There are now 3–5 night trips using 2–3.5 days of leave, a budget tier, and cost levers to switch on.'},
    {'k': 'New options', 't': 'Two snow-sure alternatives', 'd': 'Both villages sit at 1,600 m or higher, so the snow is reliable, and both are priced against Les Arcs. Details below the price table.'},
  ],
  'matrixHelp': 'Per person, all-in except food: flights, bag, transfer, flat, lift pass, lessons, rental and insurance. Budget is the cheapest flat that fits the rules, plus group lessons where they run. Comfort is an own-bed flat plus a private instructor for the four girls. Natasha learns with the girls, so she has the girls’ price. Tap a price for the full breakdown.',
  'voteLead': 'Two questions are needed: which lengths you could do, and your resort ranking. The rest is optional. Answers about dates, leave and budget appear as counts only, never next to names. Vote by Wednesday 14 October.',
  'flexRule': 'Anyone who joins for only part of the week pays for the flat by the night, plus their own flights, pass and lessons. Full-week flats (Sun → Sat), split six ways:',
  'rules': [
    'Length: the longest trip everyone ticked. If no length works for everyone, the one most people ticked, and the rest join for part of it.',
    'Resort: most points wins (3 for first, 2 for second, 1 for third).',
    'Budget or comfort: decided from the budget answers and accepted levers.',
    'Privacy: dates, leave, budget, lever and part-trip answers are shown as counts only. Only the resort ranking shows names.',
    'Booking: within 48 hours of the vote closing, on refundable rates.',
  ],
  'newOptions': [{'id': x['_resort']['id'], 'kanji': x['_resort']['kanji'], 'name': x['_resort']['short'], 'why': x['why'], 'pros': x['pros'], 'cons': x['cons'], 'food': x['food'], 'vibe': x['vibe'],
                  'transfer': x['transfer_time'], 'images': photos_for(x['_resort']['short']), 'photoNote': ''} for x in EXTRAS],
  'guideCopy': {'C': {
    'why': 'Arc 1800 has the best beginner set-up of the three: lessons meet on the snow in front of the flat, and most of the bars are here. Flexible agencies make Sunday and midweek check-ins possible.',
    'pros': ['Came first in round 1', 'Ski-in/ski-out flats for every trip length, from about £50 per person per night', 'Beginner set-up at the door: ESF meets outside, free beginner chairlifts at weekends, €45 beginner day pass', 'Serious terrain for the advanced pair: Aiguille Rouge (3,226 m), 2,000 m of vertical, La Plagne on the same pass', 'Tree-lined runs at Arc 1600 and Peisey for cold or flat-light days', 'Proper après: Folie Douce, Red Hot Saloon'],
    'cons': ['Longest transfer of the three: about 3 hours from Geneva', 'No shared shuttle midweek, so short trips use a private minibus', 'Group lessons only start on Sundays, so the shorter trips need a private instructor', 'Late-January cold on exposed lifts: −10 to −20 °C', 'The cheapest flats are compact 1970s apartments']}},
  'guideFacts': {
    'C': None,
    'F': [{'k': 'Village altitude', 'v': '1,600 m', 's': 'Chalets up to 1,800 m'}, {'k': 'Pistes', 'v': '265 km', 's': 'Grand Massif'}, {'k': 'Door to slope', 'v': '0 min', 's': 'Ski-in/ski-out flats'}, {'k': 'Geneva transfer', 'v': '≈1h15', 's': 'Private minibus'}],
    'L': [{'k': 'Village altitude', 'v': '1,970–2,100 m', 's': 'Higher than Arc 1800'}, {'k': 'Pistes', 'v': '425 km', 's': 'Paradiski, with Les Arcs'}, {'k': 'Door to slope', 'v': '0 min', 's': 'Ski-in/ski-out duplexes'}, {'k': 'Geneva transfer', 'v': '≈2h45', 's': 'Private minibus or Ben’s Bus (Sat)'}],
  },
  'decisions': [
    {'id': 'lengths', 'type': 'multi', 'required': True, 'anon': True, 'short': 'Lengths that work', 'title': 'Which trip lengths could you do?', 'help': 'Tick every one you could do, including leave. This is about what’s possible, not what you prefer. Results show counts only.',
     'options': [{'id': 'LS', 'label': 'Sun 24 → Sat 30 · 6 nights', 'hint': '5 days of leave'}, {'id': 'M', 'label': 'Tue 26 → Sun 31 · 5 nights', 'hint': '3–3.5 days of leave'}, {'id': 'S', 'label': 'Wed 27 → Sun 31 · 4 nights', 'hint': '3 days of leave'}, {'id': 'XS', 'label': 'Thu 28 → Sun 31 · 3 nights', 'hint': '2 days of leave'}]},
    {'id': 'leave', 'type': 'single', 'required': False, 'anon': True, 'short': 'Leave you could take', 'title': 'How many days of leave could you take, at most?', 'help': 'Pick the most you could take. It’s a ceiling, not a commitment: we can always do fewer days depending on what suits the group. Results show counts only.',
     'options': [{'id': '2', 'label': 'Up to 2 days'}, {'id': '3', 'label': 'Up to 3 days'}, {'id': '4', 'label': 'Up to 4 days'}, {'id': '5', 'label': 'Up to 5 days'}, {'id': 'unsure', 'label': 'Not sure yet'}]},
    {'id': 'favourite', 'type': 'single', 'required': False, 'anon': True, 'short': 'Favourite length', 'title': 'Which length would you prefer?',
     'options': [{'id': 'LS', 'label': '6 nights, Sun → Sat'}, {'id': 'M', 'label': '5 nights, Tue → Sun'}, {'id': 'S', 'label': '4 nights, Wed → Sun'}, {'id': 'XS', 'label': '3 nights, Thu → Sun'}, {'id': 'any', 'label': 'I don’t mind'}]},
    {'id': 'resort', 'type': 'rank', 'required': True, 'short': 'Resort', 'title': 'Rank the resorts', 'help': 'Put your favourite first.',
     'options': [{'id': r['id'], 'label': r['label']} for r in gen['resorts']]},
    {'id': 'budget', 'type': 'single', 'required': False, 'anon': True, 'short': 'Comfortable budget', 'title': 'What all-in budget feels comfortable, excluding food?',
     'options': [{'id': 'u700', 'label': 'Under £700'}, {'id': '700', 'label': '£700–1,000'}, {'id': '1000', 'label': '£1,000–1,300'}, {'id': '1300', 'label': 'I don’t mind'}, {'id': 'skip', 'label': 'Prefer not to say'}]},
    {'id': 'levers', 'type': 'multi', 'required': False, 'anon': True, 'short': 'Cost levers', 'title': 'Which cost levers would you accept?', 'help': 'Try them on the price table above first.',
     'options': [{'id': 'ski1', 'label': 'Ski one day less (rest or sightseeing day instead)'}, {'id': 'lessons', 'label': 'Fewer lesson days'}, {'id': 'group', 'label': 'Group lessons instead of a private instructor for the girls'}, {'id': 'share', 'label': 'Share a room or double bed for a cheaper flat'}, {'id': 'bags', 'label': 'Share hold bags'}, {'id': 'none', 'label': 'None of these'}]},
    {'id': 'flex', 'type': 'single', 'required': False, 'anon': True, 'short': 'Part of a longer trip', 'title': 'If the group picks a longer trip than suits you, would you join for part of it?',
     'options': [{'id': 'yes', 'label': 'Yes, I’d join for part of it'}, {'id': 'same', 'label': 'I’d rather we all do the same dates'}, {'id': 'any', 'label': 'I don’t mind'}]},
  ],
})
# Strip names that came from offline notes (only vote results may name people)
def scrub(o):
    if isinstance(o, str):
        for a, b in [('(warmer for Ina)', '(warmer and less exposed)'), ('warmer for Ina', 'warmer and less exposed'), ('Kannes', 'a late joiner'), ('for Ina', 'for a nervous beginner'), ('Adv + Natasha', 'Advanced'), ('Natasha', 'the intermediate skier')]:
            o = o.replace(a, b)
        return o
    if isinstance(o, list): return [scrub(x) for x in o]
    if isinstance(o, dict): return {k: (v if k == 'round1' else scrub(v)) for k, v in o.items()}
    return o
R2 = scrub(R2)
R2['round1']['taken'] = '4 Oct 2026, 20:45'
R2['round1']['note'] = 'Round 1 is kept as a record. Everyone votes again in round 2, which uses new options and prices.'

steps = [
  {'when': 'Sun 4 Oct', 'what': 'Round 1', 'detail': 'Closed. Les Arcs came first; results kept above.'},
  {'when': 'by Wed 14 Oct', 'what': 'Round 2 vote', 'detail': 'Lengths you could do, resort ranking, and optional budget and levers.'},
  {'when': 'Thu 15 Oct', 'what': 'Book the flat on a refundable rate', 'detail': 'Joaquin books; everyone sends their share.'},
  {'when': 'by Sat 17 Oct', 'what': 'Book flights as one booking', 'detail': 'Within 48 hours of the flat. Fares for 6 seats are already thinner than for 1.'},
  {'when': 'by end Oct', 'what': 'Book lessons', 'detail': 'One instructor or group course for the four girls.'},
  {'when': 'Nov', 'what': 'Transfer and insurance', 'detail': 'Book the minibus or shuttle. Everyone buys winter-sports insurance.'},
  {'when': 'Early Jan', 'what': 'Pre-book rental and passes online', 'detail': 'Online rental saves 10–50%. Last free-cancellation dates fall between late Dec and mid Jan, depending on the flat.'},
]
js = ('/* Round 2 data. Generated by tools/build_round2.py + tools/assemble_round2.py from research/round2_*.json. */\n'
      'window.ROUND2 = ' + json.dumps(R2, ensure_ascii=False, indent=1) + ';\n'
      'window.TRIP.steps = ' + json.dumps(steps, ensure_ascii=False, indent=1) + ';\n'
      "window.TRIP.proposals.forEach(p => { if (p.id === 'val-thorens' || p.id === 'stubai') p.dropped = true; });\n"
      "window.TRIP.dates.voteCloseLabel = 'Wed 14 Oct';\nwindow.TRIP.dates.bookByLabel = 'Sun 18 Oct';\n")
open(os.path.join(ROOT, 'data2.js'), 'w').write(js)
print('data2.js', len(js))
