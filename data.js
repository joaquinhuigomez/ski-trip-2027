/* Trip data — every number traces to research/*.md (checked 2026-10-04).
   status: VERIFIED = seen live on a booking page for our dates; PUBLISHED = official 2026/27 tariff; ESTIMATE = reasoned (basis in note). */
(function () {
  const W = 'https://upload.wikimedia.org/wikipedia/commons/thumb/';

  // Cost line items. adv/beg = per person; group:true + amount = whole-group total split by headcount.
  // girlsSplit:true = total split across the beginners only (shared private instructor).
  const flightGVA = { label: 'Return flight London ⇄ Geneva', note: 'easyJet Southend, out Sat 14:15, back Sat 10:00, fare for 6 seats', adv: 72, beg: 72, cur: 'GBP', status: 'VERIFIED', src: 'https://www.google.com/travel/flights?q=Flights%20from%20London%20to%20Geneva%20on%202027-01-23%20through%202027-01-30%20for%206%20adults&hl=en-GB&curr=GBP' };
  const bagEasyJet = { label: '23 kg hold bag, both ways', note: 'easyJet dynamic pricing; ski-week Saturdays sit near the top. Two people can share one bag to halve this.', adv: 85, beg: 85, cur: 'GBP', status: 'ESTIMATE' };
  const insurance = { label: 'Travel insurance with winter-sports cover', note: 'Single trip, under 40, mountain rescue included. UK residency counts, so HK passports are fine.', adv: 27, beg: 27, cur: 'GBP', status: 'ESTIMATE', src: 'https://www.which.co.uk/money/insurance/travel-insurance/best-and-worst-ski-insurance-aTDsF4R8CXZ8' };

  const A_S1 = [
    flightGVA, bagEasyJet,
    { label: "Ben's Bus shared transfer, Geneva ⇄ Val Thorens", note: 'About 3 h. Runs Saturdays and Sundays.', adv: 94, beg: 94, cur: 'GBP', status: 'PUBLISHED', src: 'https://www.bensbus.co.uk/ski-transfer/geneva-val-thorens/' },
    { label: 'Le Tikal 3-bedroom apartment, 7 nights', note: '€5,148 for the flat, refundable until 24 Dec', group: true, amount: 5148, cur: 'EUR', status: 'VERIFIED', src: 'https://www.booking.com/hotel/fr/residence-pierre-vacances-le-tikal.en-gb.html?checkin=2027-01-23&checkout=2027-01-30&group_adults=6&no_rooms=1&group_children=0&selected_currency=EUR' },
    { label: 'Tourist tax', note: 'About €2.50 per person per night', adv: 17, beg: 17, cur: 'EUR', status: 'ESTIMATE' },
    { label: 'Lift pass', note: 'Advanced: 3 Vallées 6-day (Méribel and Courchevel included). The girls: free village carpets on Sunday, then EasyRider beginner pass Mon–Fri.', intAs: 'adv', adv: 421, beg: 184, cur: 'EUR', status: 'PUBLISHED', src: 'https://www.les3vallees.com/en/skipass/adult-week-solo-pass' },
    { label: 'Carré Neige piste-rescue cover', note: '€3.50 a day, added to the lift pass', intAs: 'adv', adv: 21, beg: 17.5, cur: 'EUR', status: 'PUBLISHED', src: 'https://ski.valthorens.com/en/ski-insurance-carre-neige/' },
    { label: 'Ski school: private ESF instructor for the four girls', note: '6 mornings × 2h45, Sun–Fri, about €1,485 for the instructor, split 4 ways', intAs: 0, adv: 0, beg: 371.25, cur: 'EUR', status: 'ESTIMATE', src: 'https://www.ski-school-valthorens.co.uk/private-lessons/skiing/' },
    { intAs: 'beg', label: 'Rental for the girls: skis, boots, poles, helmet', note: 'Skiset in-store €186; online prebook usually 20–50% off', adv: 0, beg: 150, cur: 'EUR', status: 'ESTIMATE', src: 'https://www.skiset.co.uk/ski-resort/val-thorens/shops/goitschel-sports-2' },
    insurance,
    { intAs: 0, label: 'Performance ski rental (if not bringing your own)', adv: 220, beg: 0, cur: 'EUR', status: 'VERIFIED', optional: true }
  ];
  const A_S2 = A_S1.map(x => x.label.startsWith('Le Tikal') ? { ...x, label: 'Le Tikal 7 nights + 1 night in Les Menuires (Chalet Petzu)', note: '€5,148 + €260. You move flats on Saturday morning. A single 8-night flat in Val Thorens costs €8,332.', amount: 5408 }
    : x.label.startsWith('Lift pass') ? { ...x, note: x.note + ' Plus a Saturday day ticket.', adv: 421 + 67.3, beg: 184 + 36.75 }
    : x.label === 'Tourist tax' ? { ...x, adv: 19.5, beg: 19.5 }
    : x.label.startsWith('Carré') ? { ...x, adv: 24.5, beg: 21 } : x);

  const B_S1 = [
    { label: 'Return flight London ⇄ Innsbruck', note: 'TUI Gatwick, out Sat 14:30, back Sat 18:40. Includes a 10 kg cabin bag.', adv: 214, beg: 214, cur: 'GBP', status: 'VERIFIED', src: 'https://www.google.com/travel/flights?q=Flights%20from%20London%20to%20Innsbruck%20on%202027-01-23%20through%202027-01-30%20for%206%20adults&hl=en-GB&curr=GBP' },
    { label: 'Hold bag, both ways', note: 'TUI 15–25 kg add-on', adv: 100, beg: 100, cur: 'GBP', status: 'ESTIMATE' },
    { label: 'Private 7-seat minibus, Innsbruck airport ⇄ Fulpmes', note: '25 min. €288 return for the group.', group: true, amount: 288, cur: 'EUR', status: 'PUBLISHED', src: 'https://kiwitaxi.com/de/austria/innsbruck-airport-neustift-im-stubaital' },
    { label: 'Apartments on Kirchplatz, Type C, 7 nights', note: '€3,410 for the flat, free cancellation until 24 Dec', group: true, amount: 3410, cur: 'EUR', status: 'VERIFIED', src: 'https://www.airbnb.co.uk/rooms/876679139510040180?check_in=2027-01-23&check_out=2027-01-30&adults=6&currency=EUR' },
    { label: 'Tourist tax', note: '€4.80 per person per night, paid locally', adv: 33.6, beg: 33.6, cur: 'EUR', status: 'PUBLISHED' },
    { label: 'Lift pass', note: 'Advanced: 6-day Stubai Skipass, which covers the glacier and Schlick 2000. The girls: 3 days of beginner tickets, then a 3-day Schlick pass.', intAs: 'adv', adv: 355, beg: 296, cur: 'EUR', status: 'PUBLISHED', src: 'https://www.stubaier-gletscher.com/fileadmin/userdaten/stubaier-gletscher/Downloads/Downloads_DE/Preisliste-DE.pdf' },
    { label: 'Ski school: private Skischule Stubai instructor for the four girls', note: '5 mornings × 2 h, Sun–Thu. €310 a day for 4 people (€190 + €40 per extra person), €1,550 total.', intAs: 0, adv: 0, beg: 387.5, cur: 'EUR', status: 'PUBLISHED', src: 'https://www.schischule-stubai.at/en/courses/privatelessons.html' },
    { intAs: 'beg', label: 'Rental for the girls: skis, boots, helmet', note: 'Intersport Pittl, at the Schlick valley station', adv: 0, beg: 226, cur: 'EUR', status: 'VERIFIED', src: 'https://www.intersportrent.at/skirent-fulpmes-stubaital/intersport-pittl_12610' },
    insurance,
    { intAs: 0, label: 'Performance ski rental (if not bringing your own)', adv: 239, beg: 0, cur: 'EUR', status: 'VERIFIED', optional: true }
  ];
  const B_S2 = B_S1.map(x => x.label.startsWith('Return flight') ? { ...x, note: 'easyJet Gatwick, out Sat 13:15, back Sun 10:55', adv: 238, beg: 238 }
    : x.label.startsWith('Hold bag') ? { ...x, adv: 85, beg: 85, note: 'easyJet' }
    : x.label.startsWith('Apartments on Kirchplatz') ? { ...x, label: 'Wintergarten apartment, Medraz, 8 nights', note: 'The only good 3-bedroom in Fulpmes that allows a Sunday checkout. Not walkable to a lift (9–12 min ski bus). New listing, no reviews yet.', amount: 2780, src: 'https://www.airbnb.co.uk/rooms/1753701729816077777?check_in=2027-01-23&check_out=2027-01-31&adults=6&currency=EUR' }
    : x.label === 'Tourist tax' ? { ...x, adv: 38.4, beg: 38.4 }
    : x.label.startsWith('Lift pass') ? { ...x, note: x.note + ' Plus a 7th day.', adv: 400, beg: 339, status: 'ESTIMATE' } : x);

  const C_S1 = [
    flightGVA, bagEasyJet,
    { label: "Ben's Bus shared transfer, Geneva ⇄ Arc 1800", note: 'About 3 h. Saturdays only.', adv: 96, beg: 96, cur: 'GBP', status: 'PUBLISHED', src: 'https://www.bensbus.co.uk/ski-transfer/geneva-to-les-arcs/' },
    { label: 'Belles Challes 3-bedroom apartment, 7 nights', note: '£2,709 for the flat, ski-in/ski-out, free cancellation until 9 Jan', group: true, amount: 2709, cur: 'GBP', status: 'VERIFIED', src: 'https://www.airbnb.co.uk/rooms/16923511?check_in=2027-01-23&check_out=2027-01-30&adults=6' },
    { label: 'Lift pass', note: 'Advanced: Paradiski Essential 6-day (Les Arcs + La Plagne). The girls: free lifts on Sunday, then the €45 beginner day pass Mon–Fri.', intAs: 'adv', adv: 412, beg: 225, cur: 'EUR', status: 'PUBLISHED', src: 'https://www.lesarcs-peiseyvallandry.com/en/forfaits_offre' },
    { label: 'Carré Neige piste-rescue cover', intAs: 'adv', adv: 21, beg: 21, cur: 'EUR', status: 'PUBLISHED' },
    { label: 'Ski school: private ESF instructor for the four girls', note: '5 mornings × 3h30. €1,250 for the instructor (same price for 1 to 4 people), split 4 ways.', intAs: 0, adv: 0, beg: 312.5, cur: 'EUR', status: 'VERIFIED', src: 'https://www.ski-school-arc1800.co.uk/private-lessons/book-an-instructor/' },
    { intAs: 'beg', label: 'Rental for the girls: skis, boots, poles, helmet', note: 'Sport 2000 published rate €200, online about 20% off', adv: 0, beg: 160, cur: 'EUR', status: 'ESTIMATE', src: 'https://www.sport2000rent.com/en/skirental/destinations/france/savoie/arcs-1800' },
    insurance,
    { intAs: 0, label: 'Performance ski rental (if not bringing your own)', adv: 176, beg: 0, cur: 'EUR', status: 'ESTIMATE', optional: true }
  ];
  const C_S2 = C_S1.map(x => x.label.startsWith('Belles Challes') ? { ...x, label: 'Le Ridge duplex, Arc 1600, 8 nights', note: '5-crystal residence with indoor pool, sauna and gym. £3,451, free cancellation until 24 Dec. Belles Challes only rents Saturday to Saturday.', amount: 3451, src: 'https://www.airbnb.co.uk/rooms/41788990?check_in=2027-01-23&check_out=2027-01-31&adults=6' }
    : x.label.startsWith("Ben's Bus") ? { ...x, label: "Ben's Bus out, private minibus back on Sunday", note: "Ben's Bus doesn't run on Sundays", adv: 122, beg: 122, cur: 'EUR', status: 'ESTIMATE' }
    : x.label.startsWith('Lift pass') ? { ...x, note: x.note + ' Advanced need a 7-day pass.', adv: 475, beg: 270, status: 'ESTIMATE' }
    : x.label.startsWith('Carré') ? { ...x, adv: 28, beg: 28 }
    : x.label.startsWith('Beginner rental') ? { ...x, beg: 185 } : x);

  const img = (path, file, subject, author, license) => ({ url: W + path + '/' + file + '/1920px-' + file, subject, author, license, page: 'https://commons.wikimedia.org/wiki/File:' + file });

  window.TRIP = {
    updated: '4 Oct 2026',
    voteApi: 'https://script.google.com/macros/s/AKfycbx0xpQ9m3imgIU_5_4CmxtLu7ZN25M8bm75yihH3UCwl_4WYvLk50gJM9m-LfPcY2tR8w/exec',
    fx: { eurPerGbp: 1.1764, source: 'XE mid-market', date: '4 Oct 2026' },
    crew: [
      { name: 'Joaquin', level: 'adv', skill: 3, role: 'Organiser · advanced', status: 'No lessons needed', tag: 'Snores, so he sleeps at the far end of the flat.' },
      { name: 'Juan', level: 'adv', skill: 3, role: 'Advanced', status: 'No lessons needed', tag: 'Six-plus seasons. Skis with Joaquin and meets everyone for lunch.' },
      { name: 'Natasha', level: 'int', skill: 2, role: 'Intermediate', status: 'Lessons with the girls', tag: 'A level ahead; learns with the girls and skis with the boys when she likes.' },
      { name: 'Chloe', level: 'beg', skill: 1, role: 'Beginner · has skied before', status: 'Lessons, then blues by Friday', tag: 'A few days on skis already. This week is about confidence.' },
      { name: 'Kannes', level: 'beg', skill: 1, role: 'Beginner · has skied before', status: 'Lessons, then blues by Friday', tag: 'A few days on skis already. This week is about confidence.' },
      { name: 'Ina', level: 'beg', skill: 1, role: 'Beginner · has skied before', status: 'Lessons at her own pace', tag: 'Had a fall last time and feels the cold. Patient instructor, warm layers, hot-chocolate breaks.' }
    ],
    dates: {
      firstLift: '2027-01-24T09:00:00',
      voteClose: '2026-10-11T22:00:00+01:00', voteCloseLabel: 'Sun 11 Oct',
      bookBy: '2026-10-18', bookByLabel: 'Sun 18 Oct',
      nights: { S1: 7, S2: 8 },
      scenarios: { S1: 'Sat 23 → Sat 30 Jan', S2: 'Sat 23 → Sun 31 Jan' }
    },
    // filled per proposal below
    proposals: [
      {
        id: 'val-thorens', letter: 'A', kanji: '一', short: 'Val Thorens', name: 'Val Thorens, Les 3 Vallées',
        country: 'France', airport: 'Geneva', recommended: false,
        tagline: 'The highest resort in Europe and the biggest linked ski area in the world. Beginners learn on free carpets in the village, and the advanced pair can ski over to Méribel and Courchevel for lunch.',
        keywords: ['2,300 m village', '600 km of pistes', 'Ski-in/ski-out', 'Folie Douce', 'Freeride World Tour that week'],
        feel: 'High-altitude party town with a snow guarantee. Everyone meets at Folie Douce at three.',
        stats: [
          { k: 'Village altitude', v: '2,300 m', s: 'Snow-sure; no trees' },
          { k: 'Pistes', v: '600 km', s: 'Whole 3 Vallées on one pass' },
          { k: 'Door to slope', v: '0 min', s: 'Ski-to-door residence' },
          { k: 'Geneva transfer', v: '≈3 h', s: "Ben's Bus, Sat & Sun" }
        ],
        compare: {
          fly: 'Geneva · from £72 return', transfer: '≈3 h shared bus', base: 'Val Thorens, 2,300 m',
          beginner: { score: 4, text: 'Free carpets in the village; exposed and cold on bad days' },
          advanced: { score: 5, text: 'Whole 3 Vallées, 600 km' },
          snow: { score: 5, text: 'Highest resort in Europe' },
          lift: '0 min, ski-to-door', beds: 'Couple’s double + 2 twin rooms; 3 bathrooms',
          apres: { score: 5, text: 'Folie Douce, Malaysia club, gay-friendly bars' },
          week: 'Freeride World Tour in town, 24–30 Jan', cold: { score: 2, text: 'Coldest of the three: 2,300 m and no trees' },
          watch: 'Most expensive flat; extra night costs ≈ £75 pp'
        },
        baseWhy: 'Val Thorens beat six other 3 Vallées villages on our weighted score (4.25 of 5). It has the most reliable snow, free beginner carpets in the village, ski-in/ski-out at budget prices and the best après. Les Menuires, one lift away, costs half as much if budget matters more than nightlife.',
        stays: [
          { name: 'Le Tikal, Pierre & Vacances', where: 'Val Thorens centre, superior 3-bed', beds: 'Double · 2 singles · 2 singles · 3 baths', lift: '0 min (ski-to-door)', total: 5148, cur: 'EUR', rating: 'Booking 7.6 (181)', status: 'VERIFIED', pick: true, url: 'https://www.booking.com/hotel/fr/residence-pierre-vacances-le-tikal.en-gb.html?checkin=2027-01-23&checkout=2027-01-30&group_adults=6&no_rooms=1&group_children=0&selected_currency=EUR', tier: 'own-bed', note: 'Refundable until 24 Dec. Booking.com showed only 1 left.' },
          { name: 'Résidence Olympic, on the snow', where: 'Val Thorens, ground floor on the piste', beds: 'Queen · king · 2 bunks · 3 baths', lift: 'On the piste', total: 5065, cur: 'EUR', rating: 'Airbnb 4.88 (16)', status: 'VERIFIED', url: 'https://www.airbnb.co.uk/rooms/902633059492668671?check_in=2027-01-23&check_out=2027-01-30&adults=6&currency=EUR', tier: 'comfort', note: 'Nicer flat; strict cancellation, €950 deposit' },
          { name: 'Brelin apartment, Les Menuires', where: 'Les Menuires Croisette, next to the beginner zone', beds: 'Double · bunk + trundle · bunk + trundle · 2 baths', lift: 'Ski-in/ski-out', total: 2118, cur: 'EUR', rating: 'Airbnb 5.0 (7)', status: 'VERIFIED', url: 'https://www.airbnb.co.uk/rooms/1261005692460599991?check_in=2027-01-23&check_out=2027-01-30&adults=6&currency=EUR', tier: 'value', note: 'Half the price; quieter village, one lift from Val Thorens' }
        ],
        stayNote: 'Val Thorens rents Saturday to Saturday. A smaller group pays the same per flat: Le Tikal is €5,122 for 4 people, or switch to its 2-bedroom flat at €4,058.',
        costs: { S1: A_S1, S2: A_S2 },
        dateNote: { S1: 'Le Tikal. Recommended.', S2: 'Le Tikal + 1 night in Les Menuires, moving with luggage. One 8-night flat costs €8,332.' },
        partial: "Arriving Sunday works: Ben's Bus runs Sundays. Leaving Friday: easyJet 18:55 from Geneva (£39), but no shared shuttle, so allow about 5 h by train and bus.",
        foodPerDay: 60, foodNote: 'Mountain lunch €25–35, 4–5 dinners cooked at home, 2 dinners out',
        pros: [
          'Snow is close to guaranteed in late January: the village sits at 2,300 m',
          'Ski-in/ski-out is normal here, even in budget flats',
          'Free beginner carpets in the village, and beginner lift tickets come to only about €184',
          'Le Tikal gives the couple a double and each girl her own single bed, with 3 bathrooms',
          '600 km of linked pistes for Joaquin and Juan: Cime Caron, Orelle, Méribel, Courchevel',
          'The best après in the Alps, with gay-friendly bars in the village',
          'Freeride World Tour in town 24–30 Jan: free big-screen village, concerts, parties'
        ],
        cons: [
          'The coldest, most exposed village in the 3 Vallées: wind and flat light are hard on first-timers',
          'Longest Geneva transfer of the three, about 3 h or more',
          "The best flat is £105 per person per night, just above our £100 ideal",
          'Saturday-to-Saturday rentals; a Sunday return means moving flats or paying about £75 more per person',
          '1970s concrete village with little old-Alpine charm'
        ],
        school: {
          rec: 'A private ESF instructor for the four girls, 6 mornings Sun–Fri (about €371 each). It costs about €86 more each than ESF group classes, the four stay together at their own pace, and nobody is rushed by strangers. ESF Val Thorens has 263 English-speaking instructors, and its private lessons are rated 4.9 from 172 reviews.',
          options: [
            { name: 'ESF Val Thorens, shared private', format: 'One instructor for the 4 of you', schedule: '6 mornings × 2h45, Sun–Fri', pp: 371, size: '4 (just you)', reviews: '4.9★ (172) for private lessons', status: 'ESTIMATE', pick: true, url: 'https://www.ski-school-valthorens.co.uk/private-lessons/skiing/' },
            { name: 'Prosneige, shared private', format: 'Independent school', schedule: '5 mornings × 3 h', pp: 374, size: '4', reviews: '4.8★ (1,148) TripAdvisor', status: 'PUBLISHED', url: 'https://en.prosneige.fr/info-prices-and-lesson-times-val-thorens/' },
            { name: 'ESF group beginner course', format: 'Mixed group', schedule: '6 mornings 9:00–11:30', pp: 285, size: '≈10–12', reviews: '4.9★ (47) CheckYeti', status: 'VERIFIED', url: 'https://www.ski-school-valthorens.co.uk/adults-discover-and-progress/alpine-skiing/beginners/' },
            { name: 'Ski Cool group', format: 'Small group, max 8', schedule: 'Sun + 5 mornings 9–12', pp: 270, size: 'max 8', reviews: '4.9★ (503) TripAdvisor', status: 'PUBLISHED', url: 'https://www.ski-cool.com/en/book/Cours-Collectifs-Ski-1.html' }
          ],
          ladder: [
            { day: 'Sun', piste: 'g', what: 'Free carpets in the village. Learn to stop (snowplough).' },
            { day: 'Mon–Tue', piste: 'g', what: 'EasyRider lifts, first green runs and turning.' },
            { day: 'Wed–Thu', piste: 'b', what: 'Linked turns on easy blues around 2 Lacs.' },
            { day: 'Fri', piste: 'b', what: 'Lunch with the boys at Chalet des 2 Lacs, skiing there on your own.' }
          ],
          tips: [
            'Book by early November: six consecutive private mornings go first.',
            'No school lists a Cantonese-speaking instructor. Supreme Ski offers Chinese lessons on request, if you want to ask.',
            'On white-out days, ask the instructor to take lessons down to the tree-lined Les Menuires side.'
          ]
        },
        kitNote: 'Rent skis, boots, poles and a helmet in resort; booking with Le Tikal gets at least 25% off. Buy jacket, trousers, gloves and goggles before you go (Decathlon in London: about £80–120 for jacket and trousers), or rent clothing from O’rentees at about €90 a week.',
        food: [
          { name: 'La Folie Douce', what: 'The famous on-piste après: live music 2–5:30pm, and La Fruitière for lunch', price: '€€€', url: 'https://www.lafoliedouce.com/en/val-thorens' },
          { name: 'Chalet des 2 Lacs', what: 'Sunny mountain terrace the girls can ski to by Friday', price: '€€' },
          { name: 'Chalet de la Marine', what: 'Long sit-down mountain lunch', price: '€€€' },
          { name: 'La Fondue', what: 'Group fondue and raclette night on Place de l’Église', price: '€€' },
          { name: 'Malaysia', what: 'The biggest club in the Alps, for the last night', price: '€€' }
        ],
        transport: [
          { text: 'Fly London → Geneva. Around 50 departures on a Saturday, from £72 return.', url: 'https://www.google.com/travel/flights?q=Flights%20from%20London%20to%20Geneva%20on%202027-01-23%20through%202027-01-30%20for%206%20adults&hl=en-GB&curr=GBP' },
          { text: "Ben's Bus shared shuttle to Val Thorens, about 3 h, £94 return (Sat & Sun).", url: 'https://www.bensbus.co.uk/ski-transfer/geneva-val-thorens/' },
          { text: 'A private 8-seat minibus costs about the same per person and leaves when we land.', url: 'https://3valley-transfers.com/transfer/geneva-airport-gva/val-thorens' },
          { text: 'Groceries: Carrefour Montagne (7:30–20:30) or Sherpa, which takes online orders to collect on arrival.' }
        ],
        images: [
          img('a/a5', 'Vue_du_village_de_Val_Thorens_en_hiver_%28f%C3%A9vrier_2024%29.JPG', 'Val Thorens village', 'see credits', 'CC BY-SA')
        ],
        sources: [
          { label: 'Booking.com Val Thorens 3-bedroom search, our dates', url: 'https://www.booking.com/searchresults.en-gb.html?ss=Val+Thorens&checkin=2027-01-23&checkout=2027-01-30&group_adults=6&no_rooms=1&nflt=entire_place_bedroom_count%3D3&order=price' },
          { label: '3 Vallées lift pass 2026/27', url: 'https://www.les3vallees.com/en/skipass/adult-week-solo-pass' },
          { label: 'Val Thorens beginner lifts', url: 'https://ski.valthorens.com/en/beginners/' }
        ]
      },
      {
        id: 'stubai', letter: 'B', kanji: '二', short: 'Stubai', name: 'Stubai Valley, Tyrol',
        country: 'Austria', airport: 'Innsbruck', recommended: false,
        tagline: 'A Tyrolean village week, 25 minutes from Innsbruck airport. The beginners learn on Schlick 2000, the gentlest and warmest slopes of the three options. The same pass takes Joaquin and Juan up Austria’s largest glacier ski area.',
        keywords: ['Fulpmes village', 'Schlick 2000', 'Glacier to 3,210 m', '25-min transfer', 'Kaiserschmarrn'],
        feel: 'Snug Tyrolean village, cheap and sunny, with the glacier up the road for the boys.',
        stats: [
          { k: 'Glacier top', v: '3,210 m', s: 'Snow-sure; 50 min by free bus' },
          { k: 'Beginner slopes', v: '5 / 5', s: 'Blue run to the valley from every lift' },
          { k: 'Flat to lift', v: '5 min', s: 'Free ski bus every 15 min' },
          { k: 'Airport transfer', v: '25 min', s: 'Shortest of the three' }
        ],
        compare: {
          fly: 'Innsbruck · from £214 return', transfer: '25 min private minibus', base: 'Fulpmes village, 940 m',
          beginner: { score: 5, text: 'Schlick 2000: wide, gentle, among trees' },
          advanced: { score: 3, text: 'Schlick is small; glacier days are 50 min away' },
          snow: { score: 4, text: 'Glacier guaranteed; Schlick 90% snowmaking' },
          lift: '5 min ski bus (≈10 min walk)', beds: 'Couple’s queen; each girl her own bed; 2 baths',
          apres: { score: 2, text: 'Quiet village; Innsbruck bars 30 min away' },
          week: 'Quiet low-season week', cold: { score: 5, text: 'Warmest: Schlick is 1,000–2,240 m, among trees' },
          watch: 'Innsbruck flights cost 3× Geneva and can divert in bad weather'
        },
        baseWhy: 'Fulpmes beat Neustift, the glacier station and Innsbruck city on our weighted score (4.2 of 5). Nowhere in the valley is walkable to the glacier, so we chose the village whose own ski area is best for first-timers. The pass still covers the glacier for big days.',
        stays: [
          { name: 'Apartments on Kirchplatz, Type C', where: 'Fulpmes centre, 135 m²', beds: 'Queen · queen + single · queen + single · 2 baths', lift: '5 min ski bus from the door', total: 3410, cur: 'EUR', rating: 'Airbnb 4.94', status: 'VERIFIED', pick: true, url: 'https://www.airbnb.co.uk/rooms/876679139510040180?check_in=2027-01-23&check_out=2027-01-30&adults=6&currency=EUR', tier: 'own-bed', note: 'Free cancellation until 24 Dec. Plus €202 tourist tax.' },
          { name: 'Aparthotel Krösbacher (2 flats)', where: 'Bahnstraße, 9 min walk to the gondola', beds: 'Flat 1: couple + 2 girls in a twin · Flat 2: 2 girls in a twin', lift: '9 min walk', total: 3629, cur: 'EUR', rating: 'Booking 8.7 (317)', status: 'VERIFIED', url: 'https://www.booking.com/hotel/at/aparthotel-krosbacher.en-gb.html?checkin=2027-01-23&checkout=2027-01-30&group_adults=6&no_rooms=3&group_children=0&selected_currency=EUR', tier: 'comfort', note: 'Two separate flats, so the snoring stays in another flat' },
          { name: 'Königin Serles', where: 'Fulpmes, Gröbenweg', beds: '3 bedrooms, each with one large double · 2 baths', lift: '12 min walk / 6 min to bus', total: 2668, cur: 'EUR', rating: 'Booking 9.9 (10)', status: 'VERIFIED', url: 'https://www.booking.com/hotel/at/haus-dorfblick-apartment-serles-co2-neutral.en-gb.html?checkin=2027-01-23&checkout=2027-01-30&group_adults=6&no_rooms=1&group_children=0&selected_currency=EUR', tier: 'value', note: 'Girls share two doubles in pairs. Free cancellation until 9 Jan.' }
        ],
        stayNote: 'Fulpmes rents Saturday to Saturday. Kirchplatz costs the same for 4 people (€3,410); Königin Serles drops to €2,354 for 4.',
        costs: { S1: B_S1, S2: B_S2 },
        dateNote: { S1: 'Kirchplatz flat. Recommended.', S2: 'The best flats refuse a Sunday checkout, so this uses Wintergarten in Medraz: cheaper, but a bus ride to the lift and no reviews yet.' },
        partial: "Arriving Sunday is easy: the airport bus plus line 590 costs about €9. Leaving Friday is harder: the last direct Innsbruck–London flight is 15:10, so that person loses Friday's skiing.",
        foodPerDay: 60, foodNote: 'Schnitzel or Kaiserschmarrn lunches €16–22. Fulpmes supermarkets close on Sunday, so shop on arrival day.',
        pros: [
          'Schlick 2000 is ideal for beginners: a practice meadow at the mid-station and a blue run to the valley from every lift',
          'One €355 pass covers Austria’s largest glacier ski area (up to 3,210 m) plus Schlick, Serles and Elfer',
          'Shortest transfer of the three: 25 minutes, about €48 per person return by private minibus',
          'Good 3-bedroom flats at €64–86 per person per night, with free cancellation into December or January',
          'Largest ski-school review base of any option: 4.9★ from 1,807 reviews',
          'Innsbruck’s old town and small LGBTQ+ bar scene are 30 minutes away by bus'
        ],
        cons: [
          'Innsbruck flights cost about 3× Geneva (£214 vs £72 per person), and there are far fewer of them',
          'Innsbruck airport sometimes diverts to Munich or Salzburg in bad winter weather',
          'Glacier days mean 50 minutes on the bus each way for Joaquin and Juan',
          'Quiet après: Fulpmes is a working village, not a party resort',
          'Not ski-in/ski-out: a 5-minute ski bus or 10-minute walk to the gondola',
          'Sunday checkout knocks out the best flats'
        ],
        school: {
          rec: 'A private instructor from Skischule Stubai Tirol for the four girls, 2 hours every morning Sun–Thu (€387.50 each). Its office sits beside the beginner meadow at Froneben, it has the biggest review base (4.9★ from 1,807), and afternoons are free practice with the boys. Cheaper twin: Schischule Fulpmes, same format, €312.50 each.',
          options: [
            { name: 'Skischule Stubai Tirol, shared private', format: 'One instructor for the 4 of you', schedule: '5 mornings × 2 h, Sun–Thu', pp: 387.5, size: '4 (just you)', reviews: '4.9★ (1,807) CheckYeti', status: 'PUBLISHED', pick: true, url: 'https://www.schischule-stubai.at/en/courses/privatelessons.html' },
            { name: 'Schischule Fulpmes, shared private', format: 'Office next to the flat', schedule: '5 mornings × 2 h', pp: 312.5, size: '4', reviews: '4.9★ (176) CheckYeti', status: 'PUBLISHED', url: 'https://www.schischule-fulpmes.at/preise/' },
            { name: 'Skischule Stubai Tirol, beginner group', format: 'Absolute beginners, 4 h/day', schedule: 'Sun–Thu 10–12 + 13–15', pp: 290, size: 'mixed group', reviews: '4.9★ (140) first-timer course', status: 'PUBLISHED', url: 'https://www.schischule-stubai.at/en/courses/ski.html' }
          ],
          ladder: [
            { day: 'Sun', piste: 'g', what: 'Schanzlin practice meadow at Froneben.' },
            { day: 'Mon–Tue', piste: 'g', what: 'Galtbergbahn and the wide Panorama run.' },
            { day: 'Wed–Thu', piste: 'b', what: 'Blue runs all the way to the valley.' },
            { day: 'Fri', piste: 'b', what: 'Ski Schlick with the boys, then a hot-chocolate stop at Galtalm.' }
          ],
          tips: [
            'Check with Schlick 2000 that the €43 beginner ticket includes the gondola up to Froneben; if not, add €15.80 a day.',
            'Beginner group courses start on Sunday or Monday only. A private instructor adjusts if someone arrives late.',
            'No Stubai school advertises Mandarin or Cantonese speakers. English instructors are the norm.'
          ]
        },
        kitNote: 'Rent at Intersport Pittl at the Schlick valley station: €226 for a full beginner kit, 7 days for the price of 6, with overnight ski storage. HP-Sports rents jackets and trousers; otherwise buy at Decathlon before you go.',
        food: [
          { name: 'Froneben Alm', what: 'Family hut beside the beginner meadow; burgers and soups', price: '€' },
          { name: 'Galtalm', what: 'The sunniest terrace on Schlick, with game and Tyrolean dishes', price: '€€' },
          { name: 'Jochdohle, 3,150 m', what: 'Tyrol’s highest restaurant, famous for its XXL schnitzel (glacier days)', price: '€€', url: 'https://www.stubaier-gletscher.com/en/winter/restaurants/' },
          { name: 'Dorfkrug · Zur Huisler Stube', what: 'Valley dinners, both 4.5★', price: '€€–€€€' },
          { name: 'Innsbruck: Dom Café-Bar, Bacchus', what: 'A city night out on the gay-friendly circuit; 30 min by bus', price: '€€' }
        ],
        transport: [
          { text: 'Fly London → Innsbruck. A seasonal ski route, mostly Saturdays: TUI from Gatwick, £214 return.', url: 'https://www.google.com/travel/flights?q=Flights%20from%20London%20to%20Innsbruck%20on%202027-01-23%20through%202027-01-30%20for%206%20adults&hl=en-GB&curr=GBP' },
          { text: 'Private 7-seat minibus to Fulpmes, 25 min, €288 return for the group.', url: 'https://kiwitaxi.com/de/austria/innsbruck-airport-neustift-im-stubaital' },
          { text: 'Plan B: if the flight diverts to Munich, a private minibus to Fulpmes takes about 2h15 and costs about €350–450.' },
          { text: 'Public option: airport bus F, then line 590/591 to Fulpmes, about 1 h, about €9 per person.' }
        ],
        images: [],
        sources: [
          { label: 'Booking.com Fulpmes search, our dates', url: 'https://www.booking.com/searchresults.en-gb.html?ss=Fulpmes&checkin=2027-01-23&checkout=2027-01-30&group_adults=6&no_rooms=1&group_children=0&selected_currency=EUR' },
          { label: 'Stubai 2026/27 lift price list (PDF)', url: 'https://www.stubaier-gletscher.com/fileadmin/userdaten/stubaier-gletscher/Downloads/Downloads_DE/Preisliste-DE.pdf' },
          { label: 'Schlick 2000 prices', url: 'https://www.stubai.at/en/skiing-resorts/schlick2000/winter/rates/' }
        ]
      },
      {
        id: 'les-arcs', letter: 'C', kanji: '三', short: 'Les Arcs', name: 'Les Arcs 1800, Paradiski',
        country: 'France', airport: 'Geneva', recommended: true,
        recommendReason: 'It meets every rule at the lowest price: ski-in/ski-out with each girl in her own bed at £64 per person per night, lessons that start at the front door, the cheapest flights (Geneva), and enough terrain for Joaquin and Juan.',
        tagline: 'A 1970s design classic with a Folie Douce soundtrack. The beginners clip in at the front door, and Joaquin and Juan go looking for 2,000 m of vertical on the Aiguille Rouge.',
        keywords: ['Arc 1800', 'Paradiski 425 km', 'Up to 3,226 m', 'Funicular from the station', 'Best value'],
        feel: 'Retro-modern ski-in/ski-out village: lively, good value, and easy on beginners.',
        stats: [
          { k: 'Top of the ski area', v: '3,226 m', s: 'Aiguille Rouge; 2,000 m vertical' },
          { k: 'Pistes', v: '425 km', s: 'Les Arcs + La Plagne' },
          { k: 'Door to slope', v: '0 min', s: 'Ski school meets at the door' },
          { k: 'Geneva transfer', v: '≈3 h', s: "Ben's Bus, or rail + funicular" }
        ],
        compare: {
          fly: 'Geneva · from £72 return', transfer: '≈3 h shared bus or rail + funicular', base: 'Arc 1800, 1,800 m',
          beginner: { score: 5, text: 'Lessons at the door, free weekend lifts, €45 beginner pass' },
          advanced: { score: 5, text: 'Paradiski 425 km, Aiguille Rouge' },
          snow: { score: 4, text: '1,800 m base, ski area up to 3,226 m' },
          lift: '0 min, ski-in/ski-out', beds: 'Couple’s king; girls each have a single in one room; 2 baths',
          apres: { score: 4, text: 'Folie Douce, Red Hot Saloon' },
          week: 'Quiet low-season week', cold: { score: 4, text: '1,800 m base; tree-lined runs at Arc 1600 on cold days' },
          watch: 'Saturday-only rentals; no shuttle on weekdays'
        },
        baseWhy: 'Arc 1800 is where the beginner set-up is best. ESF meets on the snow in front of the flat, the Piste des Minis is one gondola away, and most bars are here. The Transarc gondola takes the advanced pair to 2,600 m.',
        stays: [
          { name: 'Belles Challes, Charvet', where: 'Arc 1800, south-facing 5th floor, renovated', beds: 'King (couple) · room with 4 singles · spare double · 2 baths', lift: '0 min (skis on at the door)', total: 2709, cur: 'GBP', rating: 'Airbnb 4.84 (57), Superhost', status: 'VERIFIED', pick: true, url: 'https://www.airbnb.co.uk/rooms/16923511?check_in=2027-01-23&check_out=2027-01-30&adults=6', tier: 'own-bed', note: 'Free cancellation until 9 Jan. The spare double lets two girls split off.' },
          { name: 'Le Ridge “best view” duplex', where: 'Arc 1600, 5-crystal residence with indoor pool, sauna and gym', beds: 'Queen · queen · double + 2 bunks · 3 baths', lift: '0 min (on the piste)', total: 3018, cur: 'GBP', rating: 'Airbnb 4.98 (57)', status: 'VERIFIED', url: 'https://www.airbnb.co.uk/rooms/41788990?check_in=2027-01-23&check_out=2027-01-30&adults=6', tier: 'comfort', note: 'The only top flat that also takes Sat 23 → Sun 31 (£3,451)' },
          { name: 'Chalet Yves', where: 'Arc 1800 Charmettoger, standalone chalet with log fire', beds: 'Double · twin · single + bunk · 1 bath', lift: '6–10 min walk', total: 1951, cur: 'GBP', rating: 'Airbnb 4.95 (39)', status: 'VERIFIED', url: 'https://www.airbnb.co.uk/rooms/52664023?check_in=2027-01-23&check_out=2027-01-30&adults=6', tier: 'value', note: 'Cheapest, and free to cancel until 22 Jan' }
        ],
        stayNote: 'Les Arcs rents Saturday to Saturday. Prices are per flat: Belles Challes is still £2,700 for 4 people (£96 per person per night).',
        costs: { S1: C_S1, S2: C_S2 },
        dateNote: { S1: 'Belles Challes. Recommended.', S2: 'Upgrade to Le Ridge (pool, sauna). Ben’s Bus doesn’t run Sundays, so it’s a private minibus home.' },
        partial: 'Les Arcs is the hardest of the three for staggered arrivals. There is no shared shuttle on Sundays or weekdays, so a late joiner takes the train from Geneva to Bourg-St-Maurice (4.5–5 h, about €60–100) and then the funicular, or a solo taxi from about €367.',
        foodPerDay: 65, foodNote: 'Tartiflette lunches €25–35. Sherpa Arc 1800 delivers groceries to the flat before you arrive.',
        pros: [
          'The cheapest good flat of the three: ski-in/ski-out, each girl in her own bed, £64 per person per night',
          'Beginner set-up at the door: ESF meets on the snow outside, there are free lifts at weekends and a €45 beginner pass',
          'The private instructor costs the same for 1 to 4 people, so 5 private mornings come to €312.50 each for the four girls',
          'Serious terrain for the couple: Aiguille Rouge (3,226 m), 2,000 m of vertical, and La Plagne on the same pass',
          'Tree-lined runs at Arc 1600 and Peisey for flat-light days',
          'Proper après (Folie Douce, Red Hot Saloon) at lower prices than Val Thorens',
          'Car-free from the train: a funicular runs from Bourg-St-Maurice station'
        ],
        cons: [
          'Strict Saturday-to-Saturday market; Friday 22 is effectively impossible',
          'No shared shuttle on Sundays or weekdays, so a late joiner pays for a train or taxi',
          'The Belles Challes layout puts the girls in one 4-single room, though a spare double lets two split off',
          '1970s Charlotte Perriand architecture: compact flats, a few residences dated',
          'Late-January cold on exposed lifts: −10 to −20 °C'
        ],
        school: {
          rec: 'A private ESF Arc 1800 instructor for the four girls, 5 mornings × 3h30 (€312.50 each). It costs only €76.50 each more than the group course, gives 40% more hours, guarantees English and no strangers, and meets on the snow front outside the flat. Budget fallback: Arc Aventures private, 2h30 a day, about €206 each.',
          options: [
            { name: 'ESF Arc 1800, shared private', format: 'One instructor for the 4 of you', schedule: '5 mornings × 3h30', pp: 312.5, size: '4 (just you)', reviews: '4.1★ (62) TripAdvisor, ESF Arc 1800', status: 'VERIFIED', pick: true, url: 'https://www.ski-school-arc1800.co.uk/private-lessons/book-an-instructor/' },
            { name: 'Arc Aventures (Evolution 2), private', format: 'Independent, max 4', schedule: '5 × 2h30', pp: 206, size: '≤4', reviews: '4.7★ (16)', status: 'PUBLISHED', url: 'https://arc-aventures.com/en/product/private-ski-lesson/' },
            { name: 'ESF Arc 1800, group “Ski discovery”', format: 'Mixed group', schedule: '6 × 2h30, Sun–Fri 9:15', pp: 236, size: '≈12–14', reviews: 'Some complaints about first-day sorting', status: 'PUBLISHED', url: 'https://www.ski-school-arc1800.co.uk/adults/alpine-ski/beginners/' },
            { name: 'Maison Sport freelancers', format: 'Pick a named instructor', schedule: 'Flexible', pp: 300, size: '≤6', reviews: '4.8–4.9★ (400–2,100)', status: 'ESTIMATE', url: 'https://maisonsport.com/en/resort/les-arcs-1800/skiing-lessons' }
          ],
          ladder: [
            { day: 'Sun', piste: 'g', what: 'Free Charmettoger lift right by the flat.' },
            { day: 'Mon–Tue', piste: 'g', what: 'Piste des Minis and the Charvet snow front.' },
            { day: 'Wed–Thu', piste: 'b', what: 'First blues around Arc 1800.' },
            { day: 'Fri', piste: 'b', what: 'Ski with the boys, then après at Folie Douce.' }
          ],
          tips: [
            'Send ESF’s “Complete my request” form by late October and ask for a confident English speaker.',
            'If they’re on blues by Thursday, a 1-day Classic pass (€71) lets them join the boys.',
            'No Cantonese instructor found in the resort. Supreme Ski says it can provide Chinese, probably Mandarin.'
          ]
        },
        kitNote: 'Sport 2000 or Intersport in Charvet, about €160 online for a full beginner pack with helmet. Clothing rental is about €100–250 a week, so buy a Decathlon jacket and trousers in London instead (about £80–120).',
        food: [
          { name: 'La Folie Douce Les Arcs', what: 'Headline après: DJs and cabaret from 3pm; La Fruitière restaurant inside', price: '€€€', url: 'https://www.lafoliedouce.com/' },
          { name: 'Red Hot Saloon', what: 'Live bands and a steakhouse in Charvet; arrive early', price: '€€' },
          { name: 'Belliou La Fumée', what: 'Old hunting lodge on the piste with Savoyard food by the fire', price: '€€–€€€' },
          { name: 'Benji’s', what: 'Piste-side Tex-Mex and burgers on a sunny terrace', price: '€€' },
          { name: 'Chalet de Luigi', what: 'Northern Italian; the splurge lunch for the advanced pair', price: '€€€€' }
        ],
        transport: [
          { text: 'Fly London → Geneva, from £72 return (same flights as Val Thorens).', url: 'https://www.google.com/travel/flights?q=Flights%20from%20London%20to%20Geneva%20on%202027-01-23%20through%202027-01-30%20for%206%20adults&hl=en-GB&curr=GBP' },
          { text: "Ben's Bus straight to Arc 1800, about 3 h, £96 return (Saturdays).", url: 'https://www.bensbus.co.uk/ski-transfer/geneva-to-les-arcs/' },
          { text: 'Car-free alternative: train to Bourg-St-Maurice, then the 7-minute funicular, which is free with a train ticket.', url: 'https://www.genevatourism.org/geneva-to-les-arcs-la-plagne/' },
          { text: 'Flight-free idea: Eurostar Snow train London → Bourg-St-Maurice (from £125 each way per Seat61; not on sale yet).', url: 'https://www.seat61.com/trains-and-routes/eurostar-ski-train.htm' }
        ],
        images: [],
        sources: [
          { label: 'Airbnb Arc 1800 3-bedroom search, our dates', url: 'https://www.airbnb.co.uk/s/Arc-1800--Bourg-Saint-Maurice--France/homes?checkin=2027-01-23&checkout=2027-01-30&adults=6&min_bedrooms=3' },
          { label: 'Les Arcs lift passes 2026/27', url: 'https://www.lesarcs-peiseyvallandry.com/en/forfaits_offre' },
          { label: 'Les Arcs beginner pass', url: 'https://www.lesarcs-peiseyvallandry.com/en/pass-debutant' }
        ]
      }
    ],
    decisions: [
      { id: 'resort', type: 'rank', required: true, short: 'Resort', title: 'Rank the three resorts', help: 'Put your favourite first. Tick “happy with any” if you don’t mind.',
        options: [{ id: 'A', label: 'Val Thorens, 3 Vallées (France)' }, { id: 'B', label: 'Stubai, Tyrol (Austria)' }, { id: 'C', label: 'Les Arcs 1800 (France)' }] },
      { id: 'dates', type: 'single', required: true, short: 'Dates', title: 'Which dates?', help: 'Both fit inside the same 5 days of leave (Mon 25 – Fri 29). Prices for each resort are in the dates table.',
        options: [{ id: 'S1', label: 'Sat 23 → Sat 30 Jan', hint: 'Cheapest, and works with the best flat at every resort' }, { id: 'S2', label: 'Sat 23 → Sun 31 Jan', hint: 'One more ski day. Costs more and changes which flat we get.' }, { id: 'any', label: 'I don’t mind' }] },
      { id: 'attend', type: 'single', required: true, short: 'Are you in?', title: 'Can you make it?', help: 'The trip goes ahead with whoever can come. This tells us how many beds to book.',
        options: [{ id: 'full', label: 'Yes, the whole trip' }, { id: 'late', label: 'Yes, but arriving a day late' }, { id: 'early', label: 'Yes, but leaving a day early' }, { id: 'maybe', label: 'Not sure yet (I’ll confirm by Sun 11 Oct)' }, { id: 'out', label: 'Can’t make it this time' }] },
      { id: 'stay', type: 'single', required: true, short: 'Where we stay', title: 'What matters most in the flat?', help: 'Each resort has a pick for every answer. They’re listed under “Where we’d stay”.',
        options: [{ id: 'own-bed', label: 'Each girl has her own bed (planner’s picks)', hint: 'Le Tikal · Kirchplatz · Belles Challes' }, { id: 'value', label: 'Cheapest that still fits the rules', hint: 'Girls may share a double or walk a bit further' }, { id: 'comfort', label: 'Pay more for a nicer flat', hint: 'On-snow / two separate flats / pool and sauna' }, { id: 'any', label: 'I don’t mind' }] },
      { id: 'flight', type: 'single', required: false, short: 'Flights', title: 'Flight times', help: 'Optional. We’ll book one booking for everyone.',
        options: [{ id: 'cheap', label: 'Cheapest, any London airport (Southend, Luton…)' }, { id: 'comfort', label: 'Gatwick or Heathrow at sensible times (+£30–100)' }, { id: 'any', label: 'I don’t mind' }] },
      { id: 'lessons', type: 'single', required: false, short: 'Lessons', title: 'Lessons for the girls', who: 'Chloe · Kannes · Ina · Natasha', help: 'Optional. Joaquin and Juan can skip this.',
        options: [{ id: 'private', label: 'One private instructor for the four of us (recommended)' }, { id: 'group', label: 'Group classes, about £65–85 cheaper each' }, { id: 'any', label: 'I don’t mind' }] }
    ],
    steps: [
      { when: 'Sun 4 Oct', what: 'Read the three options', detail: 'Share this page in the group chat.' },
      { when: 'by Sun 11 Oct', what: 'Vote', detail: 'Resort, dates, can you come, and what matters in the flat. Majority wins; nobody needs to agree on everything.' },
      { when: 'Mon 12 Oct', what: 'Book the flat on a refundable rate', detail: 'Joaquin books; everyone sends their share. Free cancellation until 24 Dec or 9 Jan, depending on the flat.' },
      { when: 'by Wed 14 Oct', what: 'Book flights as one booking', detail: 'Within 48 h of the flat. Fares for 6 seats are already thinner than for 1.' },
      { when: 'by end Oct', what: 'Book lessons', detail: 'The beginners’ private instructor first (six consecutive mornings fill fast), then Natasha’s intermediate group. Free cancellation where possible.' },
      { when: 'Nov', what: 'Transfers, insurance, GHIC', detail: 'Book Ben’s Bus or the minibus. Each person buys winter-sports insurance.' },
      { when: 'Early Jan', what: 'Pre-book rental and lift passes online', detail: 'Online rental saves 20–50%. Last chance to cancel the flat free: 24 Dec / 9 Jan.' }
    ],
    checklist: [
      'Passport valid for the whole trip. HK SAR and BN(O) passports are visa-free for Schengen stays.',
      'Non-UK passports: make sure your UK eVisa is linked to the passport you travel on, or the return flight may cause problems.',
      'ETIAS (the EU’s €20 travel authorisation) is due to launch late 2026, with a grace period at first. Apply if it’s open by January.',
      'The EU’s new biometric border check (EES) runs at your first Schengen entry. Allow extra time at Geneva or Innsbruck.',
      'GHIC card (free from the NHS site only). It doesn’t cover mountain rescue, so insurance is a must.',
      'For the beginners: thermal base layers, ski socks, gloves, goggles, neck tube. Decathlon has all of it.',
      'If you feel the cold: merino base layer, mid-layer fleece, mittens rather than gloves, and hand warmers (about £5 a pack). Heated gloves are about £40–80.',
      'For the boys: pack boots in a hold bag and rent skis. Flying skis on easyJet costs about £74 return.'
    ],
    method: 'Research run on 4 Oct 2026 by a team of AI research agents. Prices were checked on Google Flights, Airbnb, Booking.com, and the official 2026/27 tariffs of resorts and ski schools. Every price is tagged as live, published, or estimate, with a link. Full working notes, with every search link, are kept by Joaquin. Ask if you want them.'
  };

  // What Joaquin & Juan do while the beginners are in lessons (aligned to the ladder rows: Sun, Mon–Tue, Wed–Thu, Fri)
  const T = window.TRIP;
  T.proposals[0].boys = ['Warm-up laps on Péclet, then Cime Caron', 'Over to Méribel and Courchevel for lunch', 'Orelle and the Thorens glacier; Freeride World Tour finals in the village', 'Easy blues with everyone, then Folie Douce'];
  T.proposals[1].boys = ['Schlick 2000 reds to find their legs', 'Bus up to the glacier: Schaufelspitze 3,333 m, Jochdohle schnitzel', 'Glacier again, or Innsbruck Nordkette if it’s clear', 'Schlick with everyone, then après at Schluss Liacht'];
  T.proposals[2].boys = ['Transarc up to 2,600 m, Grand Col', 'Aiguille Rouge, 3,226 m, then 2,000 m down to Villaroger', 'Vanoise Express over to La Plagne', 'Blues with everyone, then Folie Douce'];
})();
