"""Assemble data2.js: generated round-2 cells + human-written copy and decisions."""
import json, os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gen = json.load(open(os.path.join(ROOT, 'data2.generated.json')))
piv = json.load(open(os.path.join(ROOT, 'research', 'round2_pivot.json')))
W = json.load(open(os.path.join(ROOT, 'research', 'images.json')))
U = json.load(open(os.path.join(ROOT, 'research', 'images_unsplash.json')))
def wi(k, i): x = dict(W[k][i]); x['src'] = 'Wikimedia Commons'; return x
def ui(k, i): x = dict(U[k][i]); x['src'] = 'Unsplash'; return x

R2 = dict(gen)
R2.update({
  'closeLabel': 'Wed 14 Oct',
  'lead': 'Round 1 gave us a favourite and two practical problems. Round 2 keeps the best of round 1, adds shorter and cheaper trips, and asks only about length, leave and resort. Every price is live for our dates (checked 4 October).',
  'changes': [
    {'k': 'Round 1', 't': 'Les Arcs came first', 'd': 'Les Arcs 7 points, Val Thorens 6, Stubai 5, with 4 of 6 votes in. Val Thorens is the most expensive, so it drops out of round 2.'},
    {'k': 'Flying together', 't': 'Every trip now starts on Sunday or later', 'd': 'One of us can only fly from Sunday afternoon, so the full week now runs Sunday to Saturday and we all travel together. Same leave as before, and the flats are cheaper.'},
    {'k': 'Price', 't': 'Shorter, cheaper options', 'd': 'Some of us asked for a cheaper version. There are now 3–5 night trips using 2–3.5 days of leave, a budget tier, and cost levers to switch on.'},
    {'k': 'New option', 't': 'Les Carroz, an hour from Geneva', 'd': 'Built for short trips: sheltered, tree-lined beginner slopes, a €63 day pass, and flats from £16 a night.'},
  ],
  'matrixHelp': 'Per person, all-in except food: flights, bag, transfer, flat, lift pass, lessons, rental and insurance. Budget is the cheapest flat that fits the rules, plus group lessons where they run. Comfort is an own-bed flat plus a private instructor for the beginners. Tap a price for the full breakdown.',
  'voteLead': 'Two questions are needed: which lengths you could do, and your resort ranking. The rest is optional. Budget answers are shown as counts only. Vote by Wednesday 14 October.',
  'flexRule': 'Anyone who joins for only part of the week pays for the flat by the night, plus their own flights, pass and lessons. Full-week flats (Sun → Sat), split six ways:',
  'rules': [
    'Length: the longest trip everyone ticked. If no length works for everyone, the one most people ticked, and the rest join for part of it.',
    'Resort: most points wins (3 for first, 2 for second, 1 for third).',
    'Budget or comfort: decided from the budget answers and accepted levers, shown as counts rather than names.',
    'Booking: within 48 hours of the vote closing, on refundable rates.',
  ],
  'pivot': {'name': 'Les Carroz, Grand Massif', 'why': piv['why'], 'pros': piv['pros'], 'cons': piv['cons'], 'food': piv['food'], 'vibe': piv['vibe'], 'transfer': piv['transfer_time'],
            'images': [wi('flaine', 0), wi('flaine', 1), ui('mood_fondue', 2)]},
  'decisions': [
    {'id': 'lengths', 'type': 'multi', 'required': True, 'short': 'Lengths that work', 'title': 'Which trip lengths could you do?', 'help': 'Tick every one you could do, including leave. This is about what’s possible, not what you prefer.',
     'options': [{'id': 'LS', 'label': 'Sun 24 → Sat 30 · 6 nights', 'hint': '5 days of leave'}, {'id': 'M', 'label': 'Tue 26 → Sun 31 · 5 nights', 'hint': '3–3.5 days of leave'}, {'id': 'S', 'label': 'Wed 27 → Sun 31 · 4 nights', 'hint': '3 days of leave'}, {'id': 'XS', 'label': 'Thu 28 → Sun 31 · 3 nights', 'hint': '2 days of leave'}]},
    {'id': 'favourite', 'type': 'single', 'required': False, 'short': 'Favourite length', 'title': 'Which length would you prefer?',
     'options': [{'id': 'LS', 'label': '6 nights, Sun → Sat'}, {'id': 'M', 'label': '5 nights, Tue → Sun'}, {'id': 'S', 'label': '4 nights, Wed → Sun'}, {'id': 'XS', 'label': '3 nights, Thu → Sun'}, {'id': 'any', 'label': 'I don’t mind'}]},
    {'id': 'resort', 'type': 'rank', 'required': True, 'short': 'Resort', 'title': 'Rank the resorts', 'help': 'Put your favourite first.',
     'options': [{'id': 'C', 'label': 'Les Arcs 1800 (France)'}, {'id': 'B', 'label': 'Stubai, Fulpmes (Austria)'}, {'id': 'P', 'label': 'Les Carroz, Grand Massif (France)'}]},
    {'id': 'budget', 'type': 'single', 'required': False, 'anon': True, 'short': 'Comfortable budget', 'title': 'What all-in budget feels comfortable, excluding food?',
     'options': [{'id': 'u700', 'label': 'Under £700'}, {'id': '700', 'label': '£700–1,000'}, {'id': '1000', 'label': '£1,000–1,300'}, {'id': '1300', 'label': 'Over £1,300'}, {'id': 'skip', 'label': 'Prefer not to say'}]},
    {'id': 'levers', 'type': 'multi', 'required': False, 'short': 'Cost levers', 'title': 'Which cost levers would you accept?', 'help': 'Try them on the price table above first.',
     'options': [{'id': 'ski1', 'label': 'Ski one day less (rest or sightseeing day instead)'}, {'id': 'lessons', 'label': 'Fewer lesson days'}, {'id': 'group', 'label': 'Group lessons instead of a private instructor'}, {'id': 'share', 'label': 'Share a room or double bed for a cheaper flat'}, {'id': 'bags', 'label': 'Share hold bags'}, {'id': 'none', 'label': 'None of these'}]},
    {'id': 'flex', 'type': 'single', 'required': False, 'short': 'Part of a longer trip', 'title': 'If the group picks a longer trip than suits you, would you join for part of it?',
     'options': [{'id': 'yes', 'label': 'Yes, I’d join for part of it'}, {'id': 'same', 'label': 'I’d rather we all do the same dates'}, {'id': 'any', 'label': 'I don’t mind'}]},
  ],
})
# Strip names that came from offline notes (only vote results may name people)
def scrub(o):
    if isinstance(o, str):
        for a, b in [('(warmer for Ina)', '(warmer and less exposed)'), ('warmer for Ina', 'warmer and less exposed'), ('Kannes', 'a late joiner'), ('for Ina', 'for a nervous beginner')]:
            o = o.replace(a, b)
        return o
    if isinstance(o, list): return [scrub(x) for x in o]
    if isinstance(o, dict): return {k: (v if k == 'round1' else scrub(v)) for k, v in o.items()}
    return o
R2 = scrub(R2)
R2['round1']['taken'] = datetime.datetime.now().strftime('%-d %b %Y, %H:%M')
R2['round1']['note'] = 'Round 1 is kept as a record. Everyone votes again in round 2, which uses new options and prices.'

steps = [
  {'when': 'Sun 4 Oct', 'what': 'Round 1', 'detail': 'Closed. Les Arcs came first; results kept above.'},
  {'when': 'by Wed 14 Oct', 'what': 'Round 2 vote', 'detail': 'Lengths you could do, resort ranking, and optional budget and levers.'},
  {'when': 'Thu 15 Oct', 'what': 'Book the flat on a refundable rate', 'detail': 'Joaquin books; everyone sends their share.'},
  {'when': 'by Sat 17 Oct', 'what': 'Book flights as one booking', 'detail': 'Within 48 hours of the flat. Fares for 6 seats are already thinner than for 1.'},
  {'when': 'by end Oct', 'what': 'Book lessons', 'detail': 'Beginners’ instructor or group course first, then Natasha’s class.'},
  {'when': 'Nov', 'what': 'Transfer and insurance', 'detail': 'Book the minibus or shuttle. Everyone buys winter-sports insurance.'},
  {'when': 'Early Jan', 'what': 'Pre-book rental and passes online', 'detail': 'Online rental saves 10–50%. Last free-cancellation dates fall between late Dec and mid Jan, depending on the flat.'},
]
js = ('/* Round 2 data. Generated by tools/build_round2.py + tools/assemble_round2.py from research/round2_*.json. */\n'
      'window.ROUND2 = ' + json.dumps(R2, ensure_ascii=False, indent=1) + ';\n'
      'window.TRIP.steps = ' + json.dumps(steps, ensure_ascii=False, indent=1) + ';\n'
      "window.TRIP.dates.voteCloseLabel = 'Wed 14 Oct';\nwindow.TRIP.dates.bookByLabel = 'Sun 18 Oct';\n")
open(os.path.join(ROOT, 'data2.js'), 'w').write(js)
print('data2.js', len(js))
