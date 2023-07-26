This is a patch to adds 3 other OT-SVG hooks to FreeType2-demos. There is an extension on top of it, to
add COLRv1 rendering, too.

## Librsvg/Cairo SVG Rendering vs SKia SVG Rendering

See the top of the RSVG rendering. There are a few very pale pixels over the bound box. This difference
is consistent across rendering different glyphs.

Librsvg:

![RSVG rendering](screenshots/ftgrid-rsvg.png)

Skia:

![SKIA rendering](screenshots/ftgrid-skia.png)

This seems to be a bug in rsvg-based (2.56.2 and 2.56.90-12-g1b589574) SVG rendering:

Librsvg:

![RSVG rendering](screenshots/ftgrid-Nabla-rsvg.png)

Skia:

![SKIA rendering](screenshots/ftgrid-Nabla-skia.png)

Filed as https://gitlab.gnome.org/GNOME/librsvg/-/issues/997 . Apparently it
is due to the use of CSS `var()` to reference colors. Looks like the
librsvg folks will try to support `var(--foo, #rrggbb)` fallbacks
as a workaround.

Interestingly, [SVG Native](https://github.com/adobe/svg-native-viewer) renders it half-way.
( filed as https://github.com/adobe/svg-native-viewer/issues/185 )

![SVG Native](../svg-native/ftgrid-14.png)

More screenshots about SVG Native in [the directory above](../svg-native/).

Inkscape also have problems with this SVG ( https://gitlab.com/inkscape/inbox/-/issues/8857 , moved from
https://gitlab.com/inkscape/inkscape/-/issues/4423 )

## Skia COLRv1 Rendering

Skia COLRv1:

![Skia COLRv1](screenshots/ftgrid-colrv1.png)

The glyf data:

![Glyph](screenshots/ftgrid-glyf.png)

Skia COLRv1 to Alpha channel:

![Skia to Alpha](screenshots/ftgrid-kAlpha.png)

Skia COLRv1 to Gray:
![Skia to Gray](screenshots/ftgrid-kGray.png)

## COLRv1 Glyphs vs SVG Glyphs, both rendered via Skia

Skia COLRv1:

![Skia COLRv1](screenshots/ftgrid-colrv1.png)

Skia SVG:

![Skia COLRv1](screenshots/ftgrid-SVG.png)

Difficult to tell the difference by the naked eye. Here is the programmatic highlights (with ImageMagick's `compare`):

![Skia COLRv1](screenshots/ftgrid-diff.png)

## COLRv1 palettes

index 0:

![palette 0](screenshots/ftgrid-palette0.png)

index 1:

![palette 1](screenshots/ftgrid-palette1.png)

index 2:

![palette 2](screenshots/ftgrid-palette2.png)

index 3:

![palette 3](screenshots/ftgrid-palette3.png)

index 4:

![palette 4](screenshots/ftgrid-palette4.png)

index 5:

![palette 5](screenshots/ftgrid-palette5.png)

index 6:

![palette 6](screenshots/ftgrid-palette6.png)
