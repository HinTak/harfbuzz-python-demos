# HarfBuzz python demos

This project currently has one script: `hb-view.py`, a re-implementation of some of the functionalilty of upstream HarfBuzz's C++
based `hb-view` utilility, with some extra functionality inspired by and taken from `hb-shape`.

Specifically, it does ink-box tight-cropping by default, and output PNG images. It also calculates margin adjustments, so that you
can use upstream HarfBuzz's C++ based `hb-view` utilility to generate vector images with tight-cropping.
Upstream HarfBuzz's C++ based `hb-view` utilility uses descender/ascender, which could be substantially larger or smaller than
the ink area.

There is an option for `hb-view.py` to use descender/ascender . The drawing code is not a step-by-step translation of C code to
pycairo python code, so in both kinds of outputs (ink-box based or descender/ascender based), sub-pixel differences are expected.
However, differences should not be beyond fractional pixels.

See below for output demos.

# Requirement

The descender/ascender code depends on a recent bug fix ( https://github.com/harfbuzz/harfbuzz/pull/1209 ) to harfbuzz from me.
This was merged after HarfBuzz version 1.9.0 .

You need to build and install harfbuzz with introspection (`./configure --with-gobject --enable-introspection`), and pygobject
(https://wiki.gnome.org/Projects/PyGObject). The latter should be readily available as pre-packaged on many systems. 

Highly recommended is pgi-docgen, with the HarfBuzz example
( https://github.com/pygobject/pgi-docgen/pull/172 ) to generate the HarfBuzz python API reference documentation. API doc
generation from gobject doc tool is at best described as both incorrect and incomplete
( https://gitlab.gnome.org/GNOME/gobject-introspection/issues/235 ) .

# Background

This comes about from a need for generating figures for the purpose of illustrating /demonstrating complex text layout.

While playing with Sanskrit ligatures in Devanagari (which has hugh ascender/decender and plenty of empty spaces)
and also Arabic (which can have strokes outside and clipped by the ascender/decender area), I decided that I don't like C++
( https://github.com/behdad/harfbuzz/issues/79 ) and thought this kind of tasks should be done by a scripting tool
instead of a compiled one.

Sanskrit ligatures use diacritics both above and below the main shape extensively, so have hugh ascender/decenders.
The C++ tool's default (with `--background="#000000" --foreground="#FFFFFF"` for clarity) shows this, especially with the
default margin of 16:

![upstream](images/sanskrit-ligature1.png)

Here is the ink-box image from the python tool:

![upstream](images/sanskrit-ligature2.png)

On the other hand, Arabic writing can go beyond the area declared by ascender/decenders.
( `--background="#000000" --foreground="#FFFFFF" --margin=0,0,0,0`). The uneven margins on the 4 directions
would also be difficult to set manually. Here is the Persian word for "HarfBuzz":

![upstream](images/arabic-cropped.png)

Here is the ink-box image from the python tool:

![upstream](images/arabic-boxed.png)
