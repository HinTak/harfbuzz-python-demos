#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  Copyright 2018 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#
#  Significant portion of this code came from harfbuzz:src/sample.py by
#  Behdad Esfahbod, and freetype-py:examples/hello-world-cairo.py by
#  Hin-Tak Leung.
#
#  Usage:
#      python hb-view.py fontname.ttf "word phrase"
#
#  Note: change "emulate_default" a few lines below to "True" for
#  ascender/decender box.
#
# -----------------------------------------------------------------------------

from __future__ import print_function, division, absolute_import

# Change this to True to get the default uptream size
emulate_default = False

# wantTTB is auto-on for CJK, and wantRotate is on for Mongolian/Phags Pa.
wantTTB = False
wantRotate = False

import sys
import array
import gi
gi.require_version('HarfBuzz', '0.0')

from gi.repository import HarfBuzz as hb
from gi.repository import GLib

# Python 2/3 compatibility
try:
    unicode
except NameError:
    unicode = str

def tounicode(s, encoding='utf-8'):
    if not isinstance(s, unicode):
        return s.decode(encoding)
    else:
        return s

if (hb.version_atleast(2,1,2)):
    pass
else:
    raise RuntimeError('HarfBuzz too old')

#####################################################################
### Derived from harfbuzz:src/sample.py

fontdata = open (sys.argv[1], 'rb').read ()
text = tounicode(sys.argv[2])
# Need to create GLib.Bytes explicitly until this bug is fixed:
# https://bugzilla.gnome.org/show_bug.cgi?id=729541
blob = hb.glib_blob_create (GLib.Bytes.new (fontdata))
face = hb.face_create (blob, 0)
del blob
font = hb.font_create (face)
upem = hb.face_get_upem (face)
del face
hb.font_set_scale (font, upem, upem)
# select "ft" or "ot" for get the right margins - see:
# https://github.com/harfbuzz/harfbuzz/issues/1248
# https://github.com/harfbuzz/harfbuzz/issues/1262
# and also
# https://github.com/harfbuzz/harfbuzz/issues/537
hb.ft_font_set_funcs(font)
#hb.ot_font_set_funcs (font)

buf = hb.buffer_create ()
class Debugger(object):
    def message (self, buf, font, msg, data, _x_what_is_this):
        print(msg)
        return True
debugger = Debugger()
#hb.buffer_set_message_func (buf, debugger.message, 1, 0)

##
## Add text to buffer
##
#
# See https://github.com/harfbuzz/harfbuzz/pull/271
#
if False:
    # If you do not care about cluster values reflecting Python
    # string indices, then this is quickest way to add text to
    # buffer:
    hb.buffer_add_utf8 (buf, text.encode('utf-8'), 0, -1)
    # Otherwise, then following handles both narrow and wide
    # Python builds (the first item in the array is BOM, so we skip it):
elif sys.maxunicode == 0x10FFFF:
    hb.buffer_add_utf32 (buf, array.array('I', text.encode('utf-32'))[1:], 0, -1)
else:
    hb.buffer_add_utf16 (buf, array.array('H', text.encode('utf-16'))[1:], 0, -1)


hb.buffer_guess_segment_properties (buf)
if ((hb.buffer_get_script(buf) == hb.script_t.MONGOLIAN) or (hb.buffer_get_script(buf) == hb.script_t.PHAGS_PA)):
    wantRotate = True
if (hb.buffer_get_script(buf) == hb.script_t.HAN):
    hb.buffer_set_direction(buf, hb.direction_t.TTB)
    wantTTB = True

hb.shape (font, buf, [])
font_extents = hb.font_get_extents_for_direction(font, hb.buffer_get_direction(buf))
font_height = font_extents.ascender - font_extents.descender + font_extents.line_gap

infos = hb.buffer_get_glyph_infos (buf)
positions = hb.buffer_get_glyph_positions (buf)

x = 0
y = 0
glyph_extents = list()
min_ix = upem
max_ix = 0
min_iy = upem
max_iy = 0

for info,pos in zip(infos, positions):
    gid = info.codepoint
    cluster = info.cluster
    x_advance = pos.x_advance
    y_advance = pos.y_advance
    x_offset = pos.x_offset
    y_offset = pos.y_offset

    print("gid%d=%d@%d,%d+%d" % (gid, cluster, x_advance, x_offset, y_offset))

### Derived from harfbuzz:src/sample.py ends.
#####################################################################

    (results, extents) = hb.font_get_glyph_extents(font, info.codepoint)
    glyph_extents.append(extents)
    if ((extents.width != 0) and (extents.height !=0)):
        # don't want invisible glyph to pin the ink box
        # https://github.com/harfbuzz/harfbuzz/issues/1208
        # https://github.com/harfbuzz/harfbuzz/issues/1216
        min_ix = min(min_ix, x + extents.x_bearing)
        max_ix = max(max_ix, x + extents.x_bearing + extents.width)
        max_iy = max(max_iy, y + extents.y_bearing)
        min_iy = min(min_iy, y + extents.y_bearing + extents.height)
    x += x_advance
    y += y_advance

def sc(value):
        return (value * 256)/upem

class Margin:
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

if (not wantTTB):
    # (top,right,bottom,left)
    # default is: font_extents.ascender, x, font_extents.descender, 0
    _margin = Margin(sc(max_iy - font_extents.ascender),
                     sc(max_ix - x),
                     sc(font_extents.descender - font_extents.line_gap - min_iy),
                     -sc(glyph_extents[0].x_bearing))

    print("default:", sc(x) + 32, sc(font_height) + 32)
else:
    # (top,right,bottom,left)
    # default is: -positions[0].y_offset, font_height, y - positions[0].y_offset, 0
    _margin = Margin(sc(max_iy + positions[0].y_offset),
                     sc(max_ix - font_height),
                     sc(y - positions[-1].y_offset - min_iy),
                     -sc(min_ix))

    print("default:", sc(font_height) + 32, sc(-y) + 32)

print("ink box:", sc(max_ix - min_ix), sc(max_iy - min_iy))
print("margin:",
      _margin.top,
      _margin.right,
      _margin.bottom,
      _margin.left)
margin = "--margin=%f %f %f %f" % (_margin.top,
                                   _margin.right,
                                   _margin.bottom,
                                   _margin.left)
del font

(width,height) = (sc(max_ix - min_ix), sc(max_iy - min_iy))
if (emulate_default):
      (height,width) = ((font_height * 256)/upem + 32, (x * 256)/upem + 32)

#####################################################################
### Derived from freetype-py:examples/hello-world-cairo.py

from freetype import *

# cairo.Matrix shadows freetype.Matrix
from cairo import Context, ImageSurface, FORMAT_A8, Matrix
from bitmap_to_surface import make_image_surface
from PIL import Image

face = Face(sys.argv[1])
face.set_char_size( 256*64 )

if (not wantRotate):
    Z = ImageSurface(FORMAT_A8, int(round(width+0.5)), int(round(height+0.5)))
else:
    Z = ImageSurface(FORMAT_A8, int(round(height+0.5)), int(round(width+0.5)))
ctx = Context(Z)

if (wantRotate):
    ctx.set_matrix(Matrix(xx=0.0,xy=-1.0,yx=1.0,yy=0.0,x0=height))
# Second pass for actual rendering
x, y = -sc(glyph_extents[0].x_bearing), height + sc(min_iy)
if (emulate_default):
    x = 16
    y = sc(font_extents.asscender) + 16
if (wantTTB):
    x = -sc(glyph_extents[0].x_bearing) + min_ix
    y = sc(glyph_extents[0].y_bearing)
for info,pos,extent in zip(infos, positions, glyph_extents):
    face.load_glyph(info.codepoint)
    x += sc(extent.x_bearing)
    y -= sc(extent.y_bearing)
    # cairo does not like zero-width bitmap from the space character!
    if (face.glyph.bitmap.width > 0):
        glyph_surface = make_image_surface(face.glyph.bitmap)
        ctx.set_source_surface(glyph_surface, x, y)
        ctx.paint()
    x += sc(pos.x_advance - extent.x_bearing)
    y -= sc(pos.y_advance - extent.y_bearing)
Z.flush()
Z.write_to_png("hb-view.png")
Image.open("hb-view.png").show()

### Derived from freetype-py:examples/hello-world-cairo.py ends.
#####################################################################
