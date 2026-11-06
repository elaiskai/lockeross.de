from pathlib import Path
import json,re,html
src=Path('lichtros/recovery-emails')
p=Path('research/lockeross/recovery-emails')
keys=['subject','pre','title','intro','cta','angle','detail']
de=[
['Deine Auswahl für dein Pferd wartet noch','Schau dir deine Auswahl in Ruhe noch einmal an.','Deine Auswahl ist<br>noch im Warenkorb.','Du hattest etwas für dein Pferd ausgesucht. Ob nach dem Reiten oder für einen ruhigen Moment im Stall: Schau dir deine Auswahl noch einmal an.','Meinen Warenkorb ansehen','Bestell in Ruhe.','Wir versenden kostenlos mit Sendungsverfolgung. Du hast nach Erhalt 30 Tage Zeit, deinen Kauf auszuprobieren. Bei Fragen hilft dir unser Team gern.'],
['Was andere Pferdebesitzer erzählen','Lies ihre Erfahrungen und probiere deinen Kauf in Ruhe aus.','Wie kommt die Pflege<br>bei deinem Pferd an?','Jedes Pferd reagiert anders. Die Erfahrungen anderer Pferdebesitzer geben dir einen Einblick, wie ein ruhiger Pflegemoment im Stall aussehen kann.','Zurück zu meiner Auswahl','Finde heraus, was zu euch passt.','Ob deine Auswahl zu euch passt, merkst du am besten im Alltag. Wenn du innerhalb von 30 Tagen nach Erhalt nicht zufrieden bist, kannst du deinen Kauf nach unseren Rückgabebedingungen zurücksenden.'],
['Für euch beide: 10 % Rabatt','Deine Auswahl mit 10 % Rabatt und kostenloser Lieferung.','Zeit für euch.<br>Mit 10 % Rabatt.','Du hattest bereits etwas für dein Pferd ausgesucht. Mit 10 % Rabatt machen wir dir den nächsten Schritt leichter. Gib deinen Rabattcode beim Bezahlen ein.','Zu meinem Warenkorb','Du sparst. Dein Pferd bekommt deine Zeit.','Zu deinem Rabatt kommen kostenloser Versand mit Sendungsverfolgung und unsere Garantie von 30 Tagen. Hast du noch Fragen zu deiner Auswahl? Schreib uns an info@lockeross.de.'],
['Fast geschafft. Schließ deine Bestellung ab','Setz deine Bestellung dort fort, wo du aufgehört hast.','Nur noch<br>ein Schritt.','Du hast mit dem Bezahlen begonnen, aber deine Bestellung noch nicht abgeschlossen. Prüfe deine Angaben und setze deine Bestellung fort.','Bestellung abschließen','Das kannst du von uns erwarten.','Dein Paket wird kostenlos und mit Sendungsverfolgung verschickt. Passt dein Kauf nicht zu euch, kannst du dich innerhalb von 30 Tagen nach Erhalt bei uns melden.'],
['Passt dein Kauf nicht zu euch?','30 Tage zum Ausprobieren und Hilfe bei der Rücksendung.','Probier es<br>in Ruhe aus.','Du musst nicht allein anhand von Produktfotos entscheiden. Ab Erhalt hast du 30 Tage Zeit, deinen Kauf auszuprobieren und zu sehen, ob er zu dir und deinem Pferd passt.','Mit meiner Bestellung fortfahren','Wir sind für dich da.','Hast du Fragen zur Anwendung, zur Lieferung oder zur Rückgabe? Schreib uns an info@lockeross.de. Wir helfen dir gern weiter.'],
['Schließ deine Bestellung mit 10 % Rabatt ab','Gib deinen Rabattcode beim Bezahlen ein.','Deine Bestellung.<br>Jetzt mit 10 % Rabatt.','Deine Bestellung ist noch offen. Wir geben dir 10 % Rabatt auf deinen Einkauf. Kehre zu deiner Bestellung zurück und gib den Code ein, bevor du bezahlst.','Mit 10 % Rabatt bestellen','Bestell mit einem guten Gefühl.','Du bekommst kostenlosen Versand mit Sendungsverfolgung und kannst deinen Kauf 30 Tage lang ausprobieren. Wenn du Fragen hast, hilft dir unser Team gern.']]
common={
'Adele S.':'Michael J.','Krystal S.':'Simon H.','Angela F.':'Jana F.',
'5.000+':'2.199','productbeoordelingen over ons assortiment':'Bewertungen zum Massagegerät',
'VOOR JE PAARD. VOOR JULLIE BAND.':'FÜR DEIN PFERD. FÜR EURE VERBINDUNG.',
'Voor je paard. Voor jullie band.':'Für dein Pferd. Für eure Verbindung.',
'Wat paardeneigenaren vertellen':'Was Pferdebesitzer erzählen',
'Hij houdt ervan. Hij viel bijna in slaap.':'Er liebt es. Er ist fast eingeschlafen.',
'Mijn paarden vinden het heerlijk':'Meine Pferde lieben es',
'Mijn paard is dol op het massagepistool.':'Mein Pferd liebt die Massagepistole.',
'Over het massageapparaat':'Zum Massagegerät',
'Fragmenten van productervaringen, vertaald uit HorseHalo beoordelingen.':'Auszüge aus übersetzten Bewertungen zum selben Produkt, international als HorseHalo angeboten.',
'Lees meer ervaringen':'Weitere Erfahrungen lesen',
'Onze garantie. Jouw vertrouwen.':'Unsere Garantie für dich.',
'Je hebt <strong>30 dagen om je aankoop uit te proberen</strong>, ook als je het product hebt gebruikt. Past het niet bij jou en je paard? Neem contact op met ons team. Je kunt het volgens onze retourvoorwaarden terugsturen en krijgt je aankoopbedrag terug.':'Du hast ab Erhalt <strong>30 Tage Zeit, deinen Kauf auszuprobieren</strong>. Passt das Produkt nicht zu dir und deinem Pferd? Melde dich bei unserem Team. Wenn du es nach unseren Rückgabebedingungen zurücksendest, erstatten wir dir den Kaufpreis.',
'Wij helpen je met je retour. De kosten van het terugsturen zijn voor jouw rekening.':'Wir helfen dir bei der Rücksendung. Die Kosten dafür trägst du bei einer regulären Rückgabe selbst.',
'Bekijk onze garantie en retourvoorwaarden':'Garantie und Rückgabebedingungen ansehen',
'Gratis verzending':'Kostenloser Versand','Met tracking naar Nederland':'Mit Sendungsverfolgung nach Deutschland',
'30 dagen garantie':'30 Tage Garantie','Probeer je aankoop rustig uit':'Probier deinen Kauf in Ruhe aus',
'Eenvoudig retourneren':'Einfache Rückgabe','We helpen je met je retour':'Wir helfen dir bei der Rücksendung',
'Klantenservice':'Kundenservice','Neem gerust contact met ons op':'Melde dich gern bei uns',
'EEN EXTRAATJE VOOR JULLIE':'EIN EXTRA FÜR EUCH','10% korting':'10 % Rabatt','Vul je code in bij het afrekenen.':'Gib deinen Code beim Bezahlen ein.',
'DAGEN':'TAGE','Uitschrijven':'Abmelden','Privacybeleid':'Datenschutz',
'Een rustig moment samen met je paard':'Ein ruhiger Moment mit deinem Pferd','Litouwen':'Litauen','Lichtros':'Lockeross','LICHTROS':'LOCKEROSS',
'lichtros.eu':'lockeross.de','lichtros-massageapparaat':'lockeross-massagegeraet',
'assets/logo.webp':'assets/lockeross-logo.webp','assets/guarantee.webp':'assets/home-guarantee.webp',
**{'assets/'+x+'.webp':'assets/home-'+x+'.webp' for x in ['shipping','moneyback','returns','support']},
'#111111':'#0B3B2A','#BD9855':'#E4A95C','#806537':'#0B3B2A','#EEE7DB':'#F0C493','#F7F6F3':'#FBF3E8','#E5E3DF':'#FBF3E8','#FAF9F6':'#FBF3E8',
'lang="nl"':'lang="de"'}
rows=json.loads((src/'copy.json').read_text())
lt=(src/'translations-lt.html').read_text()
parts=[]
copy=[]
for row, tr in zip(rows,de):
 id=row['id'];pairs={**common,**dict(zip((row[k] for k in keys),tr))}
 pat=re.compile('|'.join(map(re.escape,sorted(pairs,key=len,reverse=True))))
 s=pat.sub(lambda m:pairs[m.group()],(src/(id+'.html')).read_text())
 s=s.replace('https://lockeross.de/collections/all','https://lockeross.de/products/lockeross-massagegeraet#product-reviews')
 # Use compact mobile safe headlines and remove fixed breaks from the translated versions.
 s=re.sub(r'(<h1[^>]*>)(.*?)(</h1>)',lambda m:m[1]+m[2].replace('<br>',' ')+m[3],s)
 (p/(id+'.html')).write_text(s)
 (p/(id+'-lt.html')).write_text((src/(id+'-lt.html')).read_text().replace('Lichtros','Lockeross').replace('LICHTROS','LOCKEROSS').replace('lichtros.eu','lockeross.de').replace('lichtros-massageapparaat','lockeross-massagegeraet').replace('į Nyderlandus','į Vokietiją').replace('5 000+ atsiliepimų apie mūsų asortimento produktus','2 199 atsiliepimai apie masažuoklį').replace('Daugiau nei 5 000 atsiliepimų apie produktus. Atrask kitą jūsų priežiūros akimirką.','Dar kartą ramiai peržiūrėk savo pasirinkimą.').replace('assets/logo.webp','assets/lockeross-logo.webp').replace('assets/guarantee.webp','assets/home-guarantee.webp').replace('assets/shipping.webp','assets/home-shipping.webp').replace('assets/moneyback.webp','assets/home-moneyback.webp').replace('assets/returns.webp','assets/home-returns.webp').replace('assets/support.webp','assets/home-support.webp').replace('#111111','#0B3B2A'))
 copy.append(f'## {id}\n\n**Betreff:** {tr[0]}\n\n**Preheader:** {tr[1]}\n\n**{tr[2].replace("<br>"," ")}**\n\n{tr[3]}\n\n**CTA:** {tr[4]}\n\n**{tr[5]}**\n\n{tr[6]}')
 def panel(file,label):
  doc=(p/file).read_text(); body=re.search(r'<body[^>]*>(.*)</body>',doc,re.S)[1]
  return f'<article><h3>{label}</h3><div class="mail">{body}</div></article>'
 parts.append(f'<section id="{id}"><h2>{id}</h2><p><b>Tema:</b> {tr[0]}<br><b>Preheader:</b> {tr[1]}</p><div class="pair">{panel(id+".html","DE · Originalas")}{panel(id+"-lt.html","LT · Skaitymui")}</div></section>')
(p/'COPY-DE.md').write_text('# Lockeross laiškai\n\n'+'\n\n'.join(copy))
(p/'index.html').write_text('<!doctype html><html lang="lt"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lockeross · DE ir LT</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap"><style>body{margin:0;background:#fbf3e8;color:#172d24;font:16px Arial}main{max-width:1250px;margin:auto;padding:24px}.pair{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}article{background:white;min-width:0}h3{margin:0;padding:14px;background:#0b3b2a;color:white}nav a{display:inline-block;margin:4px;padding:10px;background:white;color:#0b3b2a}.mail a{pointer-events:none}section{margin:32px 0}@media(max-width:800px){.pair{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>Lockeross · Vokiški laiškai ir lietuviškos kopijos</h1><p>Peržiūra. Tikrus produktų blokus ir nuolaidos kodą reikia prijungti Omnisend.</p><nav>'+''.join(f'<a href="#{r["id"]}">{r["id"]}</a>' for r in rows)+'</nav>'+''.join(parts)+'</main></html>')
