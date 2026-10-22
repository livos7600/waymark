# Builds waymark.html (the page published as the artifact) from the template + world map data.
import pathlib
here = pathlib.Path(__file__).parent
html = (here / "app.template.html").read_text().replace("__WORLD__", (here / "countries-50m.json").read_text())
(here.parent / "waymark.html").write_text(html)
print("wrote waymark.html", len(html), "bytes")
