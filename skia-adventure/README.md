See the top of the RSVG rendering. There are a few very pale pixels over the bound box. This difference
is consistent across rendering different glyphs.

![RSVG rendering](ftgrid-rsvg.png)
![SKIA rendering](ftgrid-skia.png)

This seems to be a bug in rsvg-based (2.56.2) SVG rendering:

![RSVG rendering](ftgrid-Nabla-rsvg.png)
![SKIA rendering](ftgrid-Nabla-skia.png)
