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
3. Republish **to the same URL**: Artifact tool, `file_path: waymark.html`, `url: https://claude.ai/artifact/VoEoHtepSYciZXkd8Uvspo`. Omit `capabilities` so the stored ones carry over (db, assets, sample, downloads, mcp/Strava). Omit `icon`.
4. Commit the change to this repo with a short message.

## Never
- Don't write to, reset or reseed the database unless the owner asks. Trips, places, photos and expenses are real data.
- Don't delete uploaded photos (assets).
- Don't change the artifact's sharing or capabilities without asking.

## Data model (artifact `db` collections)
- `trips`: name, startDate, endDate, currency, notes
- `stops` (cities): tripId, city, country, countryA2, countryN3, lat, lon, arrive, depart, home (bool, for the home city), photoIds[]
- `legs`: tripId, mode (plane|car|train|bus|ferry|walk), fromId, toId, date, time (optional HH:MM), km, kmEstimated, cost, currency, notes
- `places` (shown as "activities"): tripId, stopId, name, category, date, time (optional HH:MM), status (want|done), rating 0–5, cost, currency, notes, photoIds[], lat, lon (pin on the trip map; from photo GPS or Claude); imported runs/rides/hikes also carry track [[lat,lon],…] (≤400 pts), distanceKm, movingS, elevM, sport, stravaId
- `expenses`: tripId, label, amount, currency, category, date, time (optional HH:MM), city, stopId (set when city matches a trip stop), paidBy, notes, photoIds[] (receipt photos; "Scan" reads them with `sample` images)
- Photos are artifact assets, shown via `/_blob/<id>`.

## Runtime
- Plain HTML/JS, no build tooling beyond `build.py`. d3 7.9.0 and topojson 3.0.2 load from cdnjs.
- Capabilities used: `db` (data), `assets` (photos), `sample` (Claude for city/activity coordinates, reading photos and receipts, Top 10), `downloads` (share image), `mcp` (the owner's Strava connector, read-only tools `list_activities` and `get_activity_streams`; added at the owner's request).
- Strava import (Days → From Strava): reads tool input schemas at runtime with `describeTool`, falls back to Claude to normalize an unfamiliar payload. GPX import (Days → GPX file) is parsed in the page.
- When republishing with `capabilities`, pass the full set: {db:{}, assets:{}, sample:{}, downloads:{}, mcp:{servers:[{server:"Strava", tools:["list_activities","get_activity_streams"]}]}}. Omitting `capabilities` keeps the stored ones, which is the normal case.
- Trip page: zoomable map (pinch with two fingers or +/−, tap a pin, ▶ replays the route), then a Days timeline. "From photo" reads a picture's EXIF date/GPS and asks Claude what it shows; a receipt becomes an expense, anything else an activity.
- Days order (dayOrder): a manual order wins once set (drag ⠿ in a day writes `dayPos` 10,20,… on that day's legs/places/expenses; changing an item's date clears it; unpositioned items slot in after their automatic neighbour). Otherwise: times win when known; untimed items go with their city between the legs (after the leg arriving there, before the leg leaving); items with no city go last. Time is pre-filled from photo EXIF/receipt, Strava/GPX start, or now when logging on the same day.
- Share (trip header, or the share icon on a day): pick dates/city, format (post 4:5, square, story 9:16), title, map/stats/activities, up to 4 photos; drawn on a canvas, saved via `downloads` or the phone's share sheet.
- Photos: tapping any photo opens the viewer (swipe, make cover = first in photoIds, replace, delete everywhere). Forms show ✕ / tap-for-cover and apply on Save. The app calls `assets.delete` only for files nothing references any more, after the owner deletes or replaces them.
- Artifacts can't embed other sites (no map tiles, no iframes); the map is drawn with d3 from the inlined world data.
