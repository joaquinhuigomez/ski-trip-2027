"""Build trip.html (the post-booking hub) from locked booking facts + research/pt_*.json. All money is computed here."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda f: json.load(open(os.path.join(ROOT, 'research', f)))
X, P3 = R('bn_extras.json'), R('round3_flaine.json')
SKI, TF, ADM = R('pt_ski.json'), R('pt_transfer_food.json'), R('pt_admin.json')
VOTE_API = 'https://script.google.com/macros/s/AKfycbx0xpQ9m3imgIU_5_4CmxtLu7ZN25M8bm75yihH3UCwl_4WYvLk50gJM9m-LfPcY2tR8w/exec'

CREW = ['Joaquin', 'Juan', 'Chloe', 'Kannes', 'Ina', 'Natasha']
GIRLS = ['Chloe', 'Kannes', 'Ina', 'Natasha']
FX = 0.87                    # £ per €, used only to convert euro entries in the ledger and estimates
FLIGHTS_TOTAL = 1104.80      # Kannes, easyJet, Apple Pay Amex, 17 Oct
CHALET_TOTAL = 1359.00       # Airbnb shows $1,809.98; GBP figure is the listing price, final pound amount set when charged 20 Dec
gbp = lambda eur: eur * FX

photo3 = lambda key: next(p for p in P3['photos'] if key.lower() in p['subject'].lower())
IMG = R('images.json')
mood = lambda k, i=0: {**IMG[k][i], 'page': IMG[k][i].get('page', IMG[k][i].get('source', '')), 'author': IMG[k][i].get('author', ''), 'license': IMG[k][i].get('license', '')}
CARROZ = {'url': 'https://upload.wikimedia.org/wikipedia/commons/9/96/Lescarroz.jpg', 'page': 'https://commons.wikimedia.org/wiki/File:Lescarroz.jpg',
          'subject': "Les Carroz d'Arâches in winter", 'author': 'Jabou', 'license': 'CC BY-SA 3.0'}

exec(open(os.path.join(ROOT, 'tools', 'trip_content.py')).read())  # defines STEPS, EST_GIRL, EST_BOY, EAT, CHECK, DATES, DAYS, AROUND_CARDS

locked_pp = (FLIGHTS_TOTAL + CHALET_TOTAL) / 6
girl_rows = [{'k': 'Flights, out and back', 'v': FLIGHTS_TOTAL / 6, 'how': 'Paid by Kannes · send her your share', 'tag': 'booked'},
             {'k': 'Chalet Éline, 4 nights', 'v': CHALET_TOTAL / 6, 'how': 'Paid by Joaquin (card charged 20 Dec) · send him your share', 'tag': 'booked'}] + EST_GIRL
boy_rows = girl_rows[:2] + EST_BOY
tot = lambda rows: sum(r['v'] for r in rows)

DATA = {
  'voteApi': VOTE_API, 'crew': CREW, 'girls': GIRLS, 'fx': FX, 'updated': UPDATED,
  'heroTag': 'Flights and the chalet are locked: six of us, four nights in the heart of Les Carroz, the whole Grand Massif on the doorstep. Here’s the money, what’s left to book, and the plan, all in one place.',
  'lockedLead': 'Both are paid or scheduled, and both have a safety net. Here are the details everyone needs.',
  'locked': [
    {'k': 'Flights · booked by Kannes', 'title': 'easyJet, six seats, one booking', 'total': FLIGHTS_TOTAL, 'sub': f"£{FLIGHTS_TOTAL / 6:.2f} each · paid 17 Oct",
     'rows': [['Out', 'Wed 27 Jan · Southend 10:40 → Geneva 13:15 (T1)'], ['Bag drop', 'Southend 08:40–10:00'],
              ['Back', 'Sun 31 Jan · Geneva 18:25 → Gatwick 19:05 (North)'], ['Bag drop', 'Geneva 16:25–17:35'], ['Check-in', 'Opens Mon 28 Dec, 10:40']],
     'note': 'Cancelling was only possible in the first 24 hours (minus a fee), so these are fixed now. Not ATOL protected. Names must match passports; spelling fixes are free.',
     'links': [{'url': 'https://www.easyjet.com/en/manage-bookings', 'label': 'Manage booking on easyJet ↗'}]},
    {'k': 'Chalet · booked by Joaquin', 'title': 'Chalet Éline, Les Carroz centre', 'total': CHALET_TOTAL, 'sub': f"about £{CHALET_TOTAL / 6:.2f} each · card charged 20 Dec",
     'rows': [['Check-in', 'Wed 27 Jan from 16:00 · self check-in, smart lock'], ['Checkout', 'Sun 31 Jan by 10:00'], ['Rooms', 'Suite with own bathroom + two twin rooms + sofa bed'],
              ['Host', 'Carole · accepted, sends arrival details before we come'], ['Address', 'Released by Airbnb about a month before']],
     'note': 'Free to cancel until 16:00 (French time) on 28 December; partial refund until 16:00 on 20 January. Airbnb lists the price in dollars ($1,809.98), so the exact pound amount is set on 20 Dec.',
     'links': [{'url': 'https://www.airbnb.co.uk/rooms/48263726', 'label': 'See the chalet ↗'}]},
  ],
  'money': {
    'lead': 'Two bookings paid, the rest forecast. Use the list below whenever someone pays for others; it works out who owes whom with the fewest transfers.',
    'lockedPP': locked_pp,
    'tiles': [{'k': 'Paid so far', 'v': f"£{FLIGHTS_TOTAL + CHALET_TOTAL:,.0f}", 's': 'flights + chalet, for all six'},
              {'k': 'Your share so far', 'v': f"£{locked_pp:,.0f}", 's': f"£{FLIGHTS_TOTAL / 6:.0f} flights + £{CHALET_TOTAL / 6:.0f} chalet", 'gold': True},
              {'k': 'Still to book', 'v': str(len(STEPS)), 's': 'each with a deadline below'},
              {'k': 'Next deadline', 'v': '25 Oct', 's': 'passports checked, insurance bought'}],
    'people': [{'who': 'Each girl', 'total': tot(girl_rows), 'rows': girl_rows}, {'who': 'Each boy', 'total': tot(boy_rows), 'rows': boy_rows}],
  },
  'seed': [
    {'id': 'seed-flights', 'payer': 'Kannes', 'amount': FLIGHTS_TOTAL, 'cur': 'GBP', 'for': CREW, 'what': 'Flights for all six (easyJet)'},
    {'id': 'seed-chalet', 'payer': 'Joaquin', 'amount': CHALET_TOTAL, 'cur': 'GBP', 'for': CREW, 'what': 'Chalet Éline, 4 nights', 'note': 'card charged 20 Dec; exact £ then'},
  ],
  'nextLead': NEXT_LEAD, 'steps': STEPS,
  'daysLead': DAYS_LEAD, 'days': DAYS,
  'around': {'lead': AROUND_LEAD, 'cards': AROUND_CARDS},
  'eat': {'lead': EAT_LEAD, 'photos': [mood('mood_fondue', 0), mood('mood_apres', 1), mood('mood_fondue', 2)], 'list': EAT},
  'check': CHECK, 'kitLead': KIT_LEAD, 'kit': KIT, 'dates': DATES, 'cal': CAL,
  'endTag': 'First turns on Thursday morning, fondue by Thursday night, Mont Blanc across the valley all week.',
  'foot': FOOT,
  'photos': {'hero': {**photo3('Mont Blanc from'), 'page': photo3('Mont Blanc from').get('page', '')}, 'end': CARROZ},
}
tpl = open(os.path.join(ROOT, 'tools', 'trip_template.html')).read()
open(os.path.join(ROOT, 'trip.html'), 'w').write(tpl.replace('/*__DATA__*/', 'window.TRIP = ' + json.dumps(DATA, ensure_ascii=False) + ';'))
print(f"trip.html built | locked pp £{locked_pp:.2f} | girl £{tot(girl_rows):.0f} | boy £{tot(boy_rows):.0f}")
