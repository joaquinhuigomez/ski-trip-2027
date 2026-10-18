# Content for trip.html. Exec'd inside build_trip.py, so X, SKI, TF, ADM, gbp, FX are in scope.
UPDATED = 'Sunday 18 October'
FOOT = 'Bookings from the confirmation emails and screenshots. Prices for things not yet booked were checked on 18 Oct 2026 and are marked as estimates where the 2026/27 rates aren’t out yet.'

DAYS_LEAD = 'Lessons in the mornings, the whole Grand Massif in the afternoons, a proper dinner every night.'
DAYS = [
  {'d': 'Wed 27 Jan', 'h': 'Travel day', 'items': [['07:30', 'Train from Liverpool Street to Southend Airport (about 55 min)'], ['08:40', 'Bag drop opens; it closes at 10:00'], ['10:40', 'easyJet to Geneva'], ['13:15', 'Land, T1. Border check, then minibus (about 1 h 15)'], ['15:30', 'Carrefour in the centre; collect skis downstairs'], ['16:00', 'Chalet check-in, smart lock'], ['20:00', 'First dinner out']]},
  {'d': 'Thu 28 Jan', 'h': 'First tracks', 'items': [['08:45', 'Bus or 10-min walk to the Kédeuze gondola'], ['09:30', 'Girls: lesson 1 (2 h)'], ['09:00', 'Boys: up to Flaine and the Grandes Platières'], ['12:30', 'Lunch on a mountain terrace'], ['14:00', 'Girls practise on the easy runs'], ['19:30', 'Fondue night']]},
  {'d': 'Fri 29 Jan', 'h': 'Getting it', 'items': [['09:30', 'Girls: lesson 2'], ['09:00', 'Boys: Samoëns and the Cascades run'], ['13:00', 'Everyone meets for lunch'], ['16:30', 'Après in the village'], ['20:00', 'Dinner in the chalet']]},
  {'d': 'Sat 30 Jan', 'h': 'All together', 'items': [['09:30', 'Girls: lesson 3'], ['12:30', 'Lunch together up top'], ['14:00', 'One easy run as six'], ['20:00', 'Last big dinner out']]},
  {'d': 'Sun 31 Jan', 'h': 'Home', 'items': [['09:30', 'Pack, clean up, leave by 10:00'], ['10:00', 'Bags with Carole if she agrees; morning ski or a long brunch'], ['14:00', 'Minibus from the chalet'], ['15:30', 'Geneva; bag drop closes 17:35'], ['18:25', 'Fly'], ['19:05', 'Gatwick North']]},
]

AROUND_LEAD = 'The chalet is in the centre, next to the tourist office. Every free ski bus stops there, and the gondola is a ten-minute walk.'
AROUND_CARDS = ["""<h4>Chalet → slopes</h4>
<div class="tw"><table><thead><tr><th>Route</th><th class="r">Time</th></tr></thead><tbody>
<tr><td>Walk to the ski-bus stop at the tourist office</td><td class="r num">2–5 min</td></tr>
<tr><td>Bus, tourist office → Kédeuze gondola</td><td class="r num">3 min</td></tr>
<tr><td>Walk straight to the gondola</td><td class="r num">about 10 min</td></tr>
</tbody></table></div>
<p class="small"><b>Rule of thumb:</b> if a bus isn’t due within 5 minutes, walk. For a 9:30 lesson, leave at 09:10.</p>
<p class="small"><b>Skip the carrying:</b> leave skis and boots overnight at the gondola (rental shops or the ski room) and walk over in snow boots.</p>""",
"""<h4>Free ski bus, morning departures</h4>
<p class="small">From the tourist office to the gondola, about every 10–15 min:</p>
<p class="num" style="font:500 1rem/1.9 var(--f-label)">08:03 · 08:16 · 08:19 · 08:33 · 08:45 · 08:58 · 09:10 · 09:19 · 09:35 · 09:43 · 10:00 · 10:09</p>
<p class="small">Back from the gondola about every 15 min until about 18:30. Skis allowed on board.</p>
<p class="small muted">2025/26 timetable; the 2026/27 one comes out in December. The walk to the stop is an estimate until Airbnb releases the address.</p>
<div class="links"><a class="btn soft" href="https://www.lescarroz.com/navettes-skibus/" target="_blank" rel="noopener">Ski-bus page ↗</a><a class="btn soft" href="https://www.lescarroz.com/content/uploads/2025/12/FINAL-2CCAM_DEPLIANT_SKIBUS_26_WEB.pdf" target="_blank" rel="noopener">Timetable PDF ↗</a></div>"""]

KIT_LEAD = 'Rent the hard kit by the gondola. Buy the warm layers before you go; they’re yours for every trip after.'
KIT = [{'item': k['item'].replace('(for the one who feels the cold)', '(extra warm)'), 'buy_or_rent': k['buy_or_rent'].capitalize(),
        'price': (f"£{k['price_gbp']:.2f}" if isinstance(k['price_gbp'], (int, float)) else f"£{k['price_gbp']}"), 'url': k.get('url', ''),
        'note': k.get('note', '').replace('For the one who feels the cold', 'If you feel the cold').replace('for the one who feels the cold', 'if you feel the cold')} for k in X['kit']]
KIT += [{'item': 'Snow boots with grip', 'buy_or_rent': 'Bring', 'price': 'own pair', 'url': '', 'note': 'For the walk to the gondola; nobody wants 10 minutes in ski boots'},
        {'item': 'Portable carbon-monoxide alarm', 'buy_or_rent': 'Buy, one for the chalet', 'price': 'about £20', 'url': 'https://www.amazon.co.uk/s?k=portable+carbon+monoxide+alarm', 'note': 'Airbnb says the chalet has no CO alarm and suggests bringing one'},
        {'item': 'EU plug adapters', 'buy_or_rent': 'Bring', 'price': 'about £5', 'url': '', 'note': 'France uses type E/F sockets'}]

# ---------- transfer + food (from pt_transfer_food.json) ----------
A2A = next(o for o in TF['transfers']['options'] if o['id'] == 'alps2alps_private')
TRANSFER_PP = gbp(float(A2A['total_eur']) / 6)
TRANSFER_STEP = {'id': 'transfer', 'title': 'Minibus, Geneva ⇄ Les Carroz', 'who': 'One volunteer books for six', 'when': 'By 2 December', 'tag': 'to do',
  'lead': 'No shared or public bus runs from Geneva to Les Carroz on a Wednesday, so a private minivan is the way up. Book the return with flight tracking. Sunday pickup at 14:00 gets us to Geneva around 15:30, comfortably ahead of the new border check and the 17:35 bag-drop close.',
  'opts': [{'name': 'Alps2Alps private minivan', 'price': '€371', 'unit': '≈ €62 each · return, 6 people + 6 bags', 'note': 'Cheapest live door-to-door quote. Free cancellation to 24 h. The quote used an 11:30 Sunday pickup: change it to 14:00 and re-check the price.', 'url': A2A['booking'], 'rec': True, 'cta': 'Alps2Alps ↗'},
           {'name': 'Suntransfers private minivan', 'price': '€439', 'unit': '≈ €73 each · return', 'note': 'Our exact flights entered; free cancellation.', 'url': 'https://www.suntransfers.com/geneva-airport-to-les-carroz-daraches', 'cta': 'Suntransfers ↗'},
           {'name': 'Sunday only: FlixBus shuttle', 'price': '€39.50', 'unit': 'each, one way', 'note': 'Leaves the tourist office (next to the chalet) 14:20, Geneva 15:40. Pair with a private transfer up on Wednesday.', 'url': 'https://global.flixbus.com/bus-routes/bus-geneva-airport-les-carroz', 'cta': 'FlixBus ↗'}],
  'how': 'Arrival: flight U2 5741, Geneva 13:15. Return: pickup Les Carroz centre Sun 31 Jan 14:00 for U2 8490 at 18:25. 6 adults, 6 suitcases, no skis.'}

# ---------- money still to come (estimates) ----------
LES_EUR = 480 / 4                     # ESI private, ESTIMATE ~€160 x 3 mornings for 4
BEG_PASS_EUR = 3 * 28 + 2             # Les Carroz Débutant, day by day + skicard
GM_PASS_EUR = 3 * 63 + 2              # Grand Massif 3 days + skicard
INS_SKI_EUR = 3 * 3.7                 # Mon Assurance Ski, ESTIMATE
RENT_BEG_EUR, RENT_PERF_EUR = 86.80, 101.25
TRAVEL_INS_GBP = 35                   # ESTIMATE, winter-sports single trip
transfer_pp = TRANSFER_PP             # set from pt_transfer_food.json below
common_est = [{'k': 'Minibus, Geneva ⇄ Les Carroz', 'v': transfer_pp, 'how': 'One volunteer books for six', 'tag': 'estimate'},
              {'k': 'Travel insurance, winter sports', 'v': TRAVEL_INS_GBP, 'how': 'Each of us buys our own', 'tag': 'estimate'}]
EST_GIRL = common_est + [{'k': 'Lessons, 3 mornings', 'v': gbp(LES_EUR), 'how': 'One booking for the four girls', 'tag': 'estimate'},
                         {'k': 'Beginner lift pass, 3 days', 'v': gbp(BEG_PASS_EUR + INS_SKI_EUR), 'how': 'Day by day at the gondola, with ski insurance', 'tag': 'estimate'},
                         {'k': 'Skis, boots, helmet', 'v': gbp(RENT_BEG_EUR), 'how': 'Skiset, in the chalet building', 'tag': 'estimate'}]
EST_BOY = common_est + [{'k': 'Grand Massif pass, 3 days', 'v': gbp(GM_PASS_EUR + INS_SKI_EUR), 'how': 'Online the week before', 'tag': 'estimate'},
                        {'k': 'Performance skis (if not bringing own)', 'v': gbp(RENT_PERF_EUR), 'how': 'Skiset, in the chalet building', 'tag': 'estimate'}]

LESSON_REQ = """Subject: Private ski lessons for 4 adult women, Thu 28 – Sat 30 Jan 2027

Hello,

We would like to book one private instructor for 4 adult women on Thursday 28, Friday 29 and Saturday 30 January 2027, 2 hours each morning, ideally 10:00–12:00, meeting at the Kédeuze gondola in Les Carroz.

Three are near-beginners who have skied once or twice and are still on green runs; the fourth is a cautious intermediate happy to stay with the group. One of them is nervous after a fall and feels the cold, so we are looking for a patient, calm, English-speaking instructor who enjoys building confidence. We would love the same instructor all three days.

Could you confirm availability, the total price for the 4 of us, and your cancellation policy?

Thank you very much,
[Name]"""

CAROLE_MSG = """Hi Carole! Thank you, we're really looking forward to staying at Chalet Éline (27–31 Jan, 6 adults).
1. Could we check in a little earlier on Wed 27? We land in Geneva at 13:15 and should arrive around 15:00. If not, could we leave our bags?
2. Could we leave our bags after checkout on Sun 31? Our transfer leaves around 14:00.
3. Are linen and towels included for 6?
4. Is there a ski locker or boot dryer we can use, and any restaurant you'd recommend for a group of 6?
Merci beaucoup !"""

NEXT_LEAD = 'Each item has a deadline that keeps the best option open, a recommended choice and a backup. Pick one up, book it, then add what you paid to the list above.'

CHECK = [
  {'when': 'This week', 'items': [{'t': 'Passport issued after 28 Jan 2017 and valid to 1 May 2027', 'url': 'https://www.gov.uk/renew-adult-passport', 'cta': 'Renew ↗'},
                                  {'t': 'Travel insurance with winter sports and helicopter rescue', 'url': 'https://www.snowcard.co.uk', 'cta': 'Quote ↗'},
                                  {'t': 'Send your share of the flights to Kannes'}]},
  {'when': 'By early December', 'items': [{'t': 'GHIC card ordered (free, NHS site)', 'url': 'https://www.nhs.uk/using-the-nhs/healthcare-abroad/apply-for-a-free-uk-global-health-insurance-card-ghic/', 'cta': 'NHS ↗'},
                                          {'t': 'Ski sizes posted in the group chat (height, weight, shoe size)'},
                                          {'t': 'Warm layers bought: base layers, ski socks, gloves, goggles'},
                                          {'t': 'A card with no foreign-exchange fees (Monzo, Starling, Revolut…)'}]},
  {'when': 'Late December', 'items': [{'t': 'Send your chalet share to Joaquin (card charged 20 Dec)'},
                                      {'t': 'Passport details to Kannes for online check-in (opens 28 Dec)'},
                                      {'t': 'Boarding passes in your phone wallet'}]},
  {'when': 'The week before', 'items': [{'t': 'Check the Liverpool Street → Southend train for Wed 27 (engineering works)', 'url': 'https://www.greateranglia.co.uk', 'cta': 'Greater Anglia ↗'},
                                        {'t': 'Cabin bag under 45 × 36 × 20 cm unless you’ve paid for a large one'},
                                        {'t': 'Share bags sensibly: weigh the hold bags'},
                                        {'t': 'Download the Grand Massif app and the ski-bus timetable'}]},
  {'when': 'Packing', 'items': [{'t': 'Passport, GHIC, insurance number (screenshot), boarding pass'}, {'t': '€50–100 cash, card'},
                                {'t': 'Non-British UK residents: eVisa / share code access'}, {'t': 'Snow boots, gloves, goggles, sun cream, lip balm'},
                                {'t': 'Portable CO alarm (one for the chalet)'}, {'t': 'EU plug adapter, phone charger, power bank'}]},
]

# Calendar entries. Times in UTC (France/Switzerland = UTC+1 in winter, London = UTC+0). All-day entries use YYYYMMDD.
LOC_CHALET = 'Chalet Éline, 40 place des Aravis, 74300 Les Carroz d’Arâches, France'
TRIP_URL = 'https://joaquinhuigomez.github.io/ski-trip-2027/trip.html'
CAL = {
  'deadline1': {'title': 'Ski trip: check passport + buy travel insurance', 'start': '20261025', 'end': '20261026', 'loc': '', 'details': 'Passport issued on/after 28 Jan 2017 and valid to 1 May 2027. Winter-sports insurance with helicopter rescue.'},
  'lessons': {'title': 'Ski trip: book the girls’ lessons', 'start': '20261115', 'end': '20261116', 'loc': '', 'details': 'ESI Grand Massif first choice. Request text on the trip page.'},
  'dec2': {'title': 'Ski trip: book minibus, ski rental, GHIC', 'start': '20261202', 'end': '20261203', 'loc': '', 'details': 'Alps2Alps return (Sunday pickup 14:00). Skiset in the chalet building. GHIC free on the NHS site.'},
  'charge': {'title': 'Ski trip: Airbnb charges the chalet ($1,809.98)', 'start': '20261220', 'end': '20261221', 'loc': '', 'details': 'Send your chalet share to Joaquin.'},
  'checkin': {'title': 'Ski trip: easyJet online check-in opens', 'start': '20261228T104000Z', 'end': '20261228T110000Z', 'loc': '', 'details': 'Send passport details to Kannes, who checks in all six. Also the last day to cancel the chalet for free (16:00 French time).'},
  'out': {'title': '✈️ easyJet U2 5741 Southend → Geneva', 'start': '20270127T104000Z', 'end': '20270127T121500Z', 'loc': 'London Southend Airport (SEN)', 'details': 'Bag drop 08:40–10:00. Train from Liverpool Street around 07:30. Lands Geneva 13:15 (T1).'},
  'chalet': {'title': '🏔️ Chalet Éline, Les Carroz', 'start': '20270127T150000Z', 'end': '20270131T090000Z', 'loc': LOC_CHALET, 'details': 'Check-in from 16:00 (smart lock), checkout by 10:00. Host: Carole, via Airbnb.'},
  'transfer': {'title': '🚐 Minibus Les Carroz → Geneva Airport', 'start': '20270131T130000Z', 'end': '20270131T143000Z', 'loc': 'Les Carroz centre', 'details': 'Pickup 14:00 for the 18:25 flight. Bag drop at Geneva closes 17:35.'},
  'back': {'title': '✈️ easyJet U2 8490 Geneva → Gatwick', 'start': '20270131T172500Z', 'end': '20270131T190500Z', 'loc': 'Geneva Airport (GVA), T1', 'details': 'Bag drop 16:25–17:35. Lands Gatwick North 19:05.'},
}
for c in CAL.values():
    c['details'] += ' Trip page: ' + TRIP_URL
DATES = [
  {'date': 'By 25 Oct', 'what': 'Everyone checks their passport dates; insurance bought', 'hot': True, 'cal': 'deadline1'},
  {'date': 'Mid-November', 'what': 'Lessons booked for the girls', 'cal': 'lessons'},
  {'date': 'By 2 Dec', 'what': 'Minibus booked · GHIC ordered · ski rental booked (early Dec)', 'cal': 'dec2'},
  {'date': 'Sun 20 Dec', 'what': 'Airbnb charges Joaquin’s card ($1,809.98); chalet shares to Joaquin', 'cal': 'charge'},
  {'date': 'Sun 27 Dec', 'what': 'Airbnb sends the chalet’s exact address (about a month before)'},
  {'date': 'Mon 28 Dec', 'what': 'Online check-in opens 10:40 · last day to cancel the chalet free (16:00 French time)', 'hot': True, 'cal': 'checkin'},
  {'date': 'Week of 18 Jan', 'what': 'Boys buy Grand Massif passes; dinners booked; Carole confirms bag drop'},
  {'date': 'Wed 27 Jan', 'what': 'Southend by 08:45 · fly 10:40 · chalet from 16:00', 'hot': True, 'cal': ['out', 'chalet']},
  {'date': 'Sun 31 Jan', 'what': 'Checkout 10:00 · minibus 14:00 · fly 18:25', 'hot': True, 'cal': ['transfer', 'back']},
]


EAT_LEAD = 'Book the big dinners a couple of weeks ahead: six at one table fills small rooms fast in January. One chalet fondue night saves money and is half the fun.'
def _r(name, t, price, book, url=None, why=None, cta=None):
    r = next((x for x in TF['restaurants'] + TF['apres'] if x['name'].startswith(name)), {})
    return {'t': t, 'name': r.get('name', name), 'why': why or r.get('why', ''), 'price': price, 'book': book or r.get('phone', ''), 'url': url, 'cta': cta}
EAT = [
  _r('Le Refuge 1110m', 'Fondue & raclette · the big cheese night', '€€', 'Book ahead · +33 4 50 90 15 63', why='Best-rated Savoyard in the village (Google 4.8 from 699). The one to book first.'),
  _r('Bistro Grill du Gron', 'Fire-grilled steak', '€€–€€€', 'Book ahead · +33 4 50 18 62 12'),
  _r('Aux Petits Oignons', 'Bistro · tables for 8', '€€', 'Book ahead · +33 4 50 90 36 93', url='https://www.apo74.fr', cta='Website ↗'),
  _r('Le Carnotzet', 'Modern alpine, main square', 'Mains €17–25 · fondue €26', '+33 4 50 90 07 64'),
  _r('Le Take Off', 'Classic French · 5.0 everywhere', '€€', 'Small room, book early · +33 4 50 90 51 57'),
  _r('La Table des Dames', 'The splurge night', '€€€', 'Online booking · +33 4 50 90 00 26', url='https://www.lacroixdesavoie.fr', cta='Website ↗'),
  _r('Le Tire-Fesses', 'Pizza & burgers by the gondola', '€', '+33 4 50 90 38 48'),
  {'t': 'Lunch on the slopes', 'name': 'L’Anfionne or La Cupesse', 'why': 'Terraces at the Plein Soleil chairlift above Les Carroz; Le K at the top of the gondola for quick self-service.', 'price': '€€', 'book': 'Walk in', 'url': None},
  _r('Le Marlow', 'Après-ski · main square', '€€', 'No booking needed'),
  _r('Le Grizzly', 'Après-ski · pub', '€', 'Walk in'),
  {'t': 'Chalet fondue night', 'name': 'Fondue de Ski, Le Grenier Savoyard', 'why': 'Ready-to-melt fondue kits with the pot and burner lent free. Order online, collect after skiing.', 'price': 'Price on site', 'book': '+33 4 50 90 04 32', 'url': 'https://www.fonduedeski.com', 'cta': 'Order ↗'},
  {'t': 'Groceries', 'name': 'Carrefour Montagne, village centre', 'why': 'Open daily about 07:30–20:00, a short walk from the chalet. Fondue and raclette cheese, bread baked on site.', 'price': '', 'book': '04 50 18 60 00', 'url': None},
]
EAT_STEP = {'id': 'dinners', 'title': 'Book two dinners', 'who': 'Anyone · by phone or email', 'when': 'Two weeks before', 'tag': 'to do',
  'lead': 'Le Refuge for the big fondue night (Thursday) and one non-cheese night (Grill du Gron or Le Take Off, Saturday). Keep Friday for a chalet fondue kit.',
  'opts': [{'name': 'Le Refuge 1110m', 'price': '€€', 'note': 'Fondue & raclette, best-rated in the village', 'rec': True},
           {'name': 'Bistro Grill du Gron', 'price': '€€–€€€', 'note': 'Fire-grilled steak, small room'},
           {'name': 'Le Take Off', 'price': '€€', 'note': 'Classic French, perfect reviews'}],
  'how': 'Full list with phone numbers in the Eat section below.'}

INS = ADM['insurance']['providers']
STEPS = [
  {'id': 'passports', 'title': 'Check your passport', 'who': 'Everyone · 2 minutes', 'when': 'This week · by 25 Oct', 'tag': 'to do',
   'lead': 'The new EU border system is strict on two dates: your passport must be issued on or after 28 January 2017 and valid until at least 1 May 2027. British passports renewed before late 2018 can fail on the issue date even when the expiry looks fine. Renewing takes about 3 weeks in the UK and much longer for HKSAR from London.',
   'opts': [{'name': 'British passport renewal', 'note': 'About 3 weeks online', 'url': 'https://www.gov.uk/renew-adult-passport', 'cta': 'gov.uk ↗'},
            {'name': 'Entry rules, Switzerland & France', 'note': 'Official FCDO pages', 'url': 'https://www.gov.uk/foreign-travel-advice/switzerland/entry-requirements', 'cta': 'FCDO ↗'}]},
  {'id': 'insurance', 'title': 'Travel insurance with winter sports', 'who': 'Everyone · buy your own', 'when': 'This week', 'tag': 'to do',
   'lead': 'Buy now so cancellation cover starts while our bookings are still ahead. Must include helicopter rescue, piste skiing, ski equipment and lessons. The free GHIC card helps with French state healthcare but not rescue or repatriation.',
   'opts': [{'name': p['name'], 'price': p.get('indicative_price', '').replace('about ', '≈ ').split(';')[0], 'note': p['why'], 'url': p['link'], 'rec': i == 0, 'cta': 'Get a quote ↗'} for i, p in enumerate(INS[:3])]},
  {'id': 'lessons', 'title': 'Lessons for the girls', 'who': 'One of the girls books for four', 'when': 'By mid-November', 'tag': 'to do',
   'lead': 'One private instructor for all four, three mornings at 10:00, meeting at the Kédeuze gondola. Late January is quiet, but the best English-speaking instructors book up first. Send the message below to the first two; book whichever replies with a good instructor.',
   'opts': [{'name': 'ESI Grand Massif', 'price': '≈ €480', 'unit': '≈ €120 each · 4-person price on request', 'note': 'English, up to 4 per lesson, 5.0 from 128 reviews. Full refund if cancelled 48 h ahead.', 'url': 'https://www.esi-grandmassif.com/carroz-fr/produits/lp-ski-snowboard.html', 'rec': True, 'cta': 'ESI ↗'},
            {'name': 'Montagne Activités (Fred)', 'price': '€450', 'unit': '€112.50 each', 'note': 'Independent instructor, cheapest published price for 4. No public reviews found; ask about cancellation.', 'url': 'http://www.montagneactivites.com', 'cta': 'Website ↗'},
            {'name': 'ESF Les Carroz', 'price': '€732', 'unit': '€183 each · two instructors of 2', 'note': 'The big French school, max 2 per private instructor. Keeps 50% if cancelled within 15 days.', 'url': 'https://www.esf-lescarroz.com/adultes/lecons-particulieres-adultes/', 'cta': 'ESF ↗'}],
   'copy': LESSON_REQ, 'copyLabel': 'Request to email the school'},
  TRANSFER_STEP,
  {'id': 'rental', 'title': 'Skis, boots and helmets', 'who': 'One person books all six', 'when': 'Early December', 'tag': 'to do',
   'lead': 'The Skiset shop is in the chalet building itself, so there’s nothing to carry. Online prices are 25–30% below the shop. Booking early guarantees sizes; cancelling is free until 24 h before. Collect on Wednesday when we arrive.',
   'opts': [{'name': 'Skiset Les Carroz by Rossignol', 'price': '€86.80', 'unit': 'beginner pack + helmet, 3 days', 'note': 'In Chalet Éline, 40 place des Aravis. Boys: Performance €85.40 or Excellence €101.25 for 3 days.', 'url': 'https://www.skiset.co.uk/ski-resort/les-carroz/shops/alain-sport', 'rec': True, 'cta': 'Book on Skiset ↗'},
            {'name': 'Intersport, village centre', 'price': '€54', 'unit': 'beginner pack, 3 days, no helmet', 'note': 'Cheaper on paper; helmet extra and a short walk away.', 'url': 'https://www.intersportrent.com/en/ski-rental/france/les-carroz-daraches', 'cta': 'Intersport ↗'}],
   'how': 'Need everyone’s height, weight, shoe size and level. Collect the sizes in the group chat first.'},
  {'id': 'ghic', 'title': 'GHIC health card', 'who': 'Everyone, if you don’t have a valid one', 'when': 'By 2 December', 'tag': 'to do',
   'lead': 'Free, from the NHS site only (ignore paid lookalikes). It takes up to 15 working days to arrive. Non-British UK residents qualify for France too.',
   'opts': [{'name': 'Apply on the NHS site', 'price': 'Free', 'url': 'https://www.nhs.uk/using-the-nhs/healthcare-abroad/apply-for-a-free-uk-global-health-insurance-card-ghic/', 'rec': True, 'cta': 'NHS ↗'}]},
  {'id': 'carole', 'title': 'Message Carole', 'who': 'Joaquin, on Airbnb', 'when': 'Early January', 'tag': 'to do',
   'lead': 'We land well before the 16:00 check-in and leave hours after the 10:00 checkout. A bag drop on both days makes the first and last day relaxed.',
   'copy': CAROLE_MSG, 'copyLabel': 'Message for Airbnb'},
  {'id': 'checkin', 'title': 'Online check-in', 'who': 'Kannes, for all six', 'when': 'Opens Mon 28 Dec, 10:40', 'tag': 'to do',
   'lead': 'Kannes can check everyone in from the booking. Each of us sends passport details beforehand; boarding passes go straight to phone wallets.',
   'opts': [{'name': 'easyJet manage booking', 'url': 'https://www.easyjet.com/en/manage-bookings', 'rec': True, 'cta': 'easyJet ↗'}]},
  {'id': 'passes', 'title': 'Lift passes', 'who': 'Boys online · girls on the day', 'when': 'Week of 18 January', 'tag': 'to do',
   'lead': 'Buying online costs the same as the counter for short stays, so nobody needs to rush. The girls buy the Les Carroz beginner pass each morning (€28) and only upgrade if the instructor wants bigger runs. Two village carpet lifts are free for a warm-up.',
   'opts': [{'name': 'Les Carroz beginner pass', 'price': '€28', 'unit': 'per day, buy each morning', 'note': 'Kiosks in the village centre from 08:30, or at the gondola. Add the ski insurance (about €3.70 a day).', 'url': 'https://www.skipass-grand-massif.com/en/shopping-cart', 'rec': True, 'cta': 'Pass shop ↗'},
            {'name': 'Grand Massif pass (boys)', 'price': '€189', 'unit': '3 days · €252 for 4', 'note': 'All five resorts incl. Flaine. Add €9 “Avantage Sérénité” to cancel up to the night before.', 'url': 'https://www.skipass-grand-massif.com/en/shopping-cart', 'cta': 'Pass shop ↗'}]},
  EAT_STEP,
]

# ---------- gear: rent vs buy (from pt_gear.json) ----------
GR = R('pt_gear.json')
def _verdict(it):
    r = it['recommendation'].upper()
    if r.startswith('RENT'): return 'Rent', 'rent'
    if 'OR RENT' in r or 'OTHERWISE RENT' in r: return 'Buy budget · or rent', 'either'
    return 'Buy', 'buy'
def _rent(it):
    ro = it.get('rent_option') or {}
    if not ro.get('price'): return ''
    return f"{ro['who'].split(' (')[0]}: {ro['price'].split(';')[0]}"
NAMES_G = {1: 'Base layers (top + bottoms)', 2: 'Mid layer', 3: 'Ski jacket', 4: 'Ski pants', 5: 'Ski socks ×2', 6: 'Gloves / mittens', 7: 'Goggles', 8: 'Helmet', 9: 'Neck warmer + beanie', 10: 'Small extras'}
WHY_G = {1: 'Worn against skin all day, so nobody rents them, and they cost less than a day’s hire. Reusable all winter.',
         2: 'Most of us own a fleece or light down already. Whoever feels the cold: add a synthetic insulated layer.',
         3: 'Decathlon’s £40 jacket (10,000 mm, warm to −8°C) costs about the same as hiring one. Hire makes sense for a premium look on a one-off trip.',
         4: 'Beginners sit in the snow a lot: a waterproof seat matters more than the brand. Rent together with the jacket if hiring.',
         5: 'Never rented. One thin ski sock beats two thick ones in rental boots.',
         6: 'Mittens for the girls: noticeably warmer than gloves, and beginners don’t need the dexterity.',
         7: 'No goggle rental found in Les Carroz. An all-weather lens copes with flat light and snow.',
         8: 'Skiset rents one for €12.60 for 3 days (about £11), added to the ski pack and fitted on the spot. Buy only if you’ll ski again soon.',
         9: 'Pennies, and worn on the face. The neck warmer matters more than the beanie on the slopes.',
         10: 'Hand warmers and SPF50 for face and lips; share one bottle between two or three.'}
import re as _re
def _note(n):
    n = _re.sub(r'(Bottoms|Leggings|Hat|Beanie|Sun cream|Step-up[^:]*|Gloves 100 version[^:]*):?\s*https?://\S+', '', str(n))
    n = _re.sub(r'https?://\S+', '', n).strip(' .;:')
    return n.split('. ')[0][:90]
GEAR_ITEMS = []
for idx, it in enumerate(GR['items'], 1):
    v, vc = _verdict(it)
    GEAR_ITEMS.append({'item': NAMES_G.get(idx, it['item']), 'verdict': v, 'vclass': vc, 'why': WHY_G.get(idx, it['why']), 'rent': _rent(it),
                       'tiers': [{'tier': t['tier'].capitalize(), 'name': f"{t['brand'].split(' (')[0]} · {t['product'].split(' £')[0].split(' x2')[0][:60]}", 'price': f"£{float(t['price_gbp']):.2f}".replace('.00', ''),
                                  'notes': _note(t.get('notes', '')), 'url': t.get('url', '')} for t in it['tiers']]})
GEAR_ITEMS[2]['rent'] = 'Adventure Kit Hire: jacket + pants together £75 for 10 days (premium £115), plus shipping from £15'
GEAR_ITEMS[3]['rent'] = 'Bundle with the jacket (left). Trousers alone £30 for 3 days'
GEAR_ITEMS[7]['rent'] = 'Skiset, downstairs: €12.60 for 3 days, add it to the ski booking'
KT = GR['kit_totals']
rv = KT.get('rent_outerwear_variant', {})
def _rv(k):
    vals = [v for kk, v in rv.items() if kk.startswith(k + '_') and isinstance(v, (int, float))] if isinstance(rv, dict) else []
    return f" · £{vals[-1]:,.0f} if you hire the jacket + pants" if vals else ''
GEAR = {
  'lead': 'Everyone rents skis, boots and poles at Skiset downstairs. For the rest: buy what touches skin, rent the helmet, and choose your tier for the jacket and pants. Prices checked on 18 Oct at UK shops; women’s versions shown, men’s cost about the same.',
  'totals': [{'k': 'Budget kit · Decathlon', 'v': f"£{KT['budget']['helmet_rented_at_skiset_gbp']:,.0f}", 's': 'everything below, helmet rented' + _rv('budget'), 'gold': True},
             {'k': 'Mid kit', 'v': f"£{KT['mid']['helmet_rented_at_skiset_gbp']:,.0f}", 's': 'Uniqlo, Wedze 500, Columbia, Smith, Giro' + _rv('mid')},
             {'k': 'Premium kit', 'v': f"£{KT['premium']['helmet_rented_at_skiset_gbp']:,.0f}", 's': 'Icebreaker, The North Face, Arc’teryx, Oakley' + _rv('premium')},
             {'k': 'Our pick for the girls', 'v': '≈ £200', 's': 'budget kit + merino layer and warm mittens for whoever feels the cold'}],
  'items': GEAR_ITEMS,
  'extra': ["""<h4>Renting clothes instead</h4>
<p class="small"><b>Adventure Kit Hire</b> posts to you, no deposit: jacket + pants £55 (3 days), £65 (7) or £75 (10 days, covers travel); premium £115. Shipping £15 and up, covering the return. One combined order for the group cuts shipping; ask for delivery around Mon 25 Jan.</p>
<p class="small"><b>Expedition Kit Hire:</b> full kit (jacket, salopettes, base layers, fleece, mitts) £140 a week, plus a £70 refundable deposit.</p>
<p class="small"><b>Ski Stuff</b> is closing down and selling ex-hire jackets and salopettes at £10 each plus postage, cheaper than any hire.</p>
<div class="links"><a class="btn soft" href="https://www.adventurekithire.co.uk/collections/adult-skiwear-hire" target="_blank" rel="noopener">Adventure Kit Hire ↗</a><a class="btn soft" href="https://ski-stuff.co.uk/" target="_blank" rel="noopener">Ski Stuff ↗</a></div>""",
"""<h4>Second-hand and timing</h4>
<p class="small"><b>Decathlon Second Life</b> is the safest used option: inspected, returnable, Decathlon sizing. Vinted and eBay have jackets from £5–25; check the seat and knees.</p>
<p class="small"><b>Order by 1 December.</b> Decathlon lets you try and return in store; leave room in the jacket and pants for a mid layer. Black Friday (27 Nov) is the low point for premium brands.</p>
<p class="small"><b>Layer, don’t bulk:</b> a waterproof shell + base layer + fleece beats one heavy jacket. Boys: usually only goggles and merino socks are missing.</p>
<div class="links"><a class="btn soft" href="https://www.decathlon.co.uk/browse/c0-sports/c1-skiing-snowboarding/_/N-1gzqtj2" target="_blank" rel="noopener">Decathlon ski ↗</a><a class="btn soft" href="https://www.vinted.co.uk/catalog?search_text=womens%20ski%20jacket" target="_blank" rel="noopener">Vinted ↗</a></div>"""],
}
KIT_LEAD = 'The bits people forget.'
KIT = KIT[-3:]
