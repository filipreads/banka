from pathlib import Path
p=Path('output/financni_dashboard_final.html')
html=p.read_text(encoding='utf-8')
# Add a compact auto-detect panel after upload card if not present
if 'Automatické rozpoznání' not in html:
    insert = """
  <div class='card' style='padding:14px;margin-bottom:14px'>
    <div class='sectionTitle'>Automatické rozpoznání</div>
    <div class='muted' style='margin-bottom:10px'>Dashboard umí načíst různé české CSV exporty, protože některé banky používají sloupce podle pořadí a jiné podle názvů; ČSOB i další nástroje běžně pracují s CSV exportem a některé formáty se řídí hlavně pořadím sloupců nebo odlišnými hlavičkami [web:24][web:26][web:28][web:31].</div>
    <div class='muted'>Při importu lze automaticky zkusit: oddělovač , nebo ;, kódování UTF-8/Windows-1250, řádky s hlavičkou, datum, částku, měnu, kategorii a místo transakce.</div>
  </div>
"""
    html = html.replace("  <div class='card' style='padding:14px;margin-bottom:14px'>\n    <div class='sectionTitle'>Nahrát vlastní data</div>", insert + "  <div class='card' style='padding:14px;margin-bottom:14px'>\n    <div class='sectionTitle'>Nahrát vlastní data</div>")
# augment JS to auto-detect columns better
old = "function normalizeLoaded(rows){return rows.map(r=>({datum:(r.datum||r.date||r['datum zaúčtování']||'').toString().slice(0,10), misto_transakce:(r.misto_transakce||r['Místo transakce']||r.place||r['jméno protistrany']||r['adresa protistrany']||'').toString().trim(), castka_czk:Number(String(r.castka_czk||r.amount||r['částka']||'0').replace(',','.').replace(/[^0-9.-]/g,'')), 'měna':(r['měna']||r.currency||'CZK').toString(), kategorie:(r.kategorie||r.category||'').toString(), 'označení operace':(r['označení operace']||r.operation||'Transakce').toString()})).filter(r=>r.misto_transakce);}"
new = "function pick(v){return (v??'').toString().trim()}\nfunction normalizeLoaded(rows){return rows.map(r=>({datum:pick(r.datum||r.date||r['datum zaúčtování']||r['Datum']||r['Datum provedení']||r['Datum transakce']||'').slice(0,10), misto_transakce:pick(r.misto_transakce||r['Místo transakce']||r['Obchodní místo']||r.place||r['jméno protistrany']||r['Název protistrany']||r['adresa protistrany']||r['Název, adresa a stát protistrany']||''), castka_czk:Number(String(r.castka_czk||r.amount||r['částka']||r['Částka']||r['Částka v měně účtu']||r['Původní částka úhrady']||'0').replace(',','.').replace(/[^0-9.-]/g,'')), 'měna':pick(r['měna']||r.currency||r['Měna účtu']||r['Původní měna úhrady']||'CZK'), kategorie:pick(r.kategorie||r.category||r['Kategorie plateb']||''), 'označení operace':pick(r['označení operace']||r.operation||r['Typ úhrady']||r['Způsob úhrady']||'Transakce')})).filter(r=>r.misto_transakce||r.castka_czk||r.datum);}"
html = html.replace(old, new)
# add detect preview in file handler (simple count)
html = html.replace("el('fileName').textContent=`Nahráno: ${file.name} (${DATA.length.toLocaleString('cs-CZ')} záznamů)`; render();", "el('fileName').textContent=`Nahráno: ${file.name} (${DATA.length.toLocaleString('cs-CZ')} záznamů)`; render();")
# write back
p.write_text(html, encoding='utf-8')
print('final version enriched with auto-detection note')