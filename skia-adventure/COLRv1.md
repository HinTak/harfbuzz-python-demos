This is a patch to adds 3 other OT-SVG hooks to FreeType2-demos. There is an extension on top of it, to
add COLRv1 rendering, too.

The COLRv1 extension currently has a limitation - it works by over-writing
the SVG rendering with a toggle key, so it depends on the font having a SVG table. In one without, it overwrites
the glyh rendering and does gray. (Hope to fix). So it is convenient that both Rsvg and Adobe SVG rendering are flawed.
[Adobe SVG Native](https://github.com/adobe/svg-native-viewer/issues/185) , and [Rsvg issue](https://gitlab.gnome.org/GNOME/librsvg/-/issues/997).

It is a toggle-key to toggle SVG<->COLRv1 rendering ("z" for "color layered glyphs" as for COLRv0),
and overloads the palette toggle key ("C" for switching palettes for color-blind-friendiness in glyf mode)
to switch CPAL entries. Binaries at the [FontVal binary archive](https://github.com/FontVal-extras/binary-archive/) ).

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
