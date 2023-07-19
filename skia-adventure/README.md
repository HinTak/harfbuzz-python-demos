## Librsvg/Cairo SVG Rendering vs SKia SVG Rendering

See the top of the RSVG rendering. There are a few very pale pixels over the bound box. This difference
is consistent across rendering different glyphs.

![RSVG rendering](ftgrid-rsvg.png)
![SKIA rendering](ftgrid-skia.png)

This seems to be a bug in rsvg-based (2.56.2 and 2.56.90-12-g1b589574) SVG rendering:

![RSVG rendering](ftgrid-Nabla-rsvg.png)
![SKIA rendering](ftgrid-Nabla-skia.png)

Filed as https://gitlab.gnome.org/GNOME/librsvg/-/issues/997 . Apparently it
is due to the use of CSS `var()` to reference colors. Looks like the
librsvg folks will try to support `var(--foo, #rrggbb)` fallbacks
as a workaround.

## Skia COLRv1 Rendering

Skia COLRv1:

![Skia COLRv1](ftgrid-colrv1.png)

The glyf data:

![Glyph](ftgrid-glyf.png)

Skia COLRv1 to Alpha channel:

![Skia to Alpha](ftgrid-kAlpha.png)

Skia COLRv1 to Gray:
![Skia to Gray](ftgrid-kGray.png)

## COLRv1 Glyphs vs SVG Glyphs, rendered via Skia

Skia COLRv1:

![Skia COLRv1](ftgrid-colrv1.png)

Skia SVG:

![Skia COLRv1](ftgrid-SVG.png)

Difficult to tell the difference by the naked eye. Here is the programmatic highlights (with ImageMagick's `compare`):

![Skia COLRv1](ftgrid-diff.png)
