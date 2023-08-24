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

font_size = 256
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
max_ix = -upem
min_iy = upem
max_iy = -upem

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
        min_ix = min(min_ix, x + pos.x_offset + extents.x_bearing)
        max_ix = max(max_ix, x + pos.x_offset + extents.x_bearing + extents.width)
        max_iy = max(max_iy, y + pos.y_offset + extents.y_bearing)
        min_iy = min(min_iy, y + pos.y_offset + extents.y_bearing + extents.height)
    x += x_advance
    y += y_advance

def sc(value):
        return (value * font_size)/upem

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
                     sc(font_extents.descender - min_iy),
                     -sc(min_ix))

    print("default:", sc(x) + 32, sc(font_height) + 32)
else:
    # (top,right,bottom,left)
    # default is: 0, font_height + positions[0].x_offset, y, positions[0].x_offset
    _margin = Margin(sc(max_iy),
                     sc(max_ix - font_height - positions[0].x_offset),
                     sc(y - min_iy),
                     -sc(min_ix - positions[0].x_offset))

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
      (height,width) = ((font_height * font_size)/upem + 32, (x * font_size)/upem + 32)

#####################################################################
### Derived from freetype-py:examples/hello-world-cairo.py

from freetype import *

from skia_glfw_module import glfw_window, skia_surface

face = Face(sys.argv[1])
face.set_char_size( font_size*64 )

from skia_ot_svg_module import hooks
import skia
from skia import ImageInfo, ColorType, AlphaType
import glfw

library = get_handle()
FT_Property_Set( library, b"ot-svg", b"svg-hooks", byref(hooks) ) # python 3 only syntax

if (not wantRotate):
    WIDTH, HEIGHT = int(round(width+0.5)), int(round(height+0.5))
else:
    WIDTH, HEIGHT = int(round(height+0.5)), int(round(width+0.5))

with glfw_window(WIDTH, HEIGHT) as window:
    if (wantRotate):
        ctx.set_matrix(Matrix(xx=0.0,xy=-1.0,yx=1.0,yy=0.0,x0=height))
    x, y = -sc(min_ix), height + sc(min_iy)
    if (emulate_default):
        x = 16
        y = sc(font_extents.asscender) + 16
    if (wantTTB):
        x = sc(max_ix)
        y = sc(max_iy)
    with skia_surface(window) as surface:
        with surface as canvas:
            for info,pos,extent in zip(infos, positions, glyph_extents):
                face.load_glyph(info.codepoint, FT_LOAD_COLOR | FT_LOAD_RENDER)
                x += sc(extent.x_bearing + pos.x_offset)
                y -= sc(extent.y_bearing + pos.y_offset)
                if (face.glyph.bitmap.width > 0):
                    glyphBitmap = skia.Bitmap()
                    bitmap = face.glyph.bitmap
                    glyphBitmap.setInfo(ImageInfo.Make(bitmap.width, bitmap.rows,
                                                       ColorType.kBGRA_8888_ColorType,
                                                       AlphaType.kPremul_AlphaType),
                                        bitmap.pitch)
                    glyphBitmap.setPixels(pythonapi.PyMemoryView_FromMemory(cast(bitmap._FT_Bitmap.buffer, c_char_p),
                                                                            bitmap.rows * bitmap.pitch,
                                                                            0x200), # Read-Write
                                          )
                    canvas.drawBitmap(glyphBitmap, x, y)
                x += sc(pos.x_advance - extent.x_bearing - pos.x_offset)
                y -= sc(pos.y_advance - extent.y_bearing - pos.y_offset)
        surface.flushAndSubmit()
        image = surface.makeImageSnapshot()
        #image.save("hb-view-ot-svg-skia-GL.png", skia.kPNG) # why does it shows RuntimeError?
    glfw.swap_buffers(window)
    while (glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS
           and not glfw.window_should_close(window)):
        glfw.wait_events()
### Derived from freetype-py:examples/hello-world-cairo.py ends.
#####################################################################
