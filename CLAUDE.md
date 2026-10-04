# Waymark — notes for Claude

Waymark is a travel-log web app published as a claude.ai artifact. The owner (Olivier) is beta-testing it on a trip and may ask for changes from a phone.

## Where things live
- **Live app (source of truth):** https://claude.ai/artifact/VoEoHtepSYciZXkd8Uvspo
- **Business plan page:** https://claude.ai/artifact/T3Ut4zHmKMGTgJujHvNcjo
- `src/app.template.html` — app source. `__WORLD__` is replaced by `src/countries-50m.json` (world-atlas 50m TopoJSON, sharp enough for coastlines at city zoom) at build time.
- `src/build.py` — `python3 src/build.py` writes `waymark.html` at the repo root, the file that gets published.
- `src/playbook.html` — source of the business plan page.

## How to change the app
1. **Read the live artifact first** (Artifact tool, `action: "read"`, the URL above). If it differs from `src/app.template.html`, the live version wins; bring the repo up to date before editing.
2. Edit `src/app.template.html`, run `python3 src/build.py`.
3. Republish **to the same URL**: Artifact tool, `file_path: waymark.html`, `url: https://claude.ai/artifact/VoEoHtepSYciZXkd8Uvspo`. Omit `capabilities` so the stored ones carry over (db, assets, sample, downloads). Omit `icon`.
4. Commit the change to this repo with a short message.

## Never
- Don't write to, reset or reseed the database unless the owner asks. Trips, places, photos and expenses are real data.
- Don't delete uploaded photos (assets).
- Don't change the artifact's sharing or capabilities without asking.

## Data model (artifact `db` collections)
- `trips`: name, startDate, endDate, currency, notes
- `stops` (cities): tripId, city, country, countryA2, countryN3, lat, lon, arrive, depart, home (bool, for the home city), photoIds[]
- `legs`: tripId, mode (plane|car|train|bus|ferry|walk), fromId, toId, date, km, kmEstimated, cost, currency, notes
- `places` (shown as "activities"): tripId, stopId, name, category, date, status (want|done), rating 0–5, cost, currency, notes, photoIds[], lat, lon (pin on the trip map; from photo GPS or Claude)
- `expenses`: tripId, label, amount, currency, category, date, city, stopId (set when city matches a trip stop), paidBy, notes, photoIds[] (receipt photos; "Scan" reads them with `sample` images)
- Photos are artifact assets, shown via `/_blob/<id>`.

## Runtime
- Plain HTML/JS, no build tooling beyond `build.py`. d3 7.9.0 and topojson 3.0.2 load from cdnjs.
- Capabilities used: `db` (data), `assets` (photos), `sample` (Claude for city/activity coordinates, reading photos and receipts, Top 10), `downloads` (share image).
- Trip page: zoomable map (pinch with two fingers or +/−, tap a pin, ▶ replays the route), then a Days timeline. "From photo" reads a picture's EXIF date/GPS and asks Claude what it shows; a receipt becomes an expense, anything else an activity.
- Share (trip header, or the share icon on a day): pick dates/city, format (post 4:5, square, story 9:16), title, map/stats/activities, up to 4 photos; drawn on a canvas, saved via `downloads` or the phone's share sheet.
- Artifacts can't embed other sites (no map tiles, no iframes); the map is drawn with d3 from the inlined world data.
