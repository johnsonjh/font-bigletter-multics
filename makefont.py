#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: Multics
# Copyright (c) 1972 Massachusetts Institute of Technology
# Copyright (c) 1972-1982 Honeywell Information Systems, Inc.
# Copyright (c) 2006 Bull HN Information Systems, Inc.
# Copyright (c) 2006 Bull SAS
# Copyright (c) 2017 Stewart C. Russell (scruss.com)
# Copyright (c) 2025 Jeffrey H. Johnson
# Copyright (c) 2025 The DPS8M Development Team
# scspell-id: c43e10fa-940c-11f0-8021-80ee73e9b8e7

import json
import fontforge
import math
import psMat
import argparse

fnt_name = "BigletterMultics"

parser = argparse.ArgumentParser(description="Generate a font from a JSON definition.")

parser.add_argument("-n", "--name", type=str, help="Set the font name")


parser.add_argument(
    "-i", "--italic", type=float, default=0.0, help="Italic angle (0.0 to 90.0)"
)

parser.add_argument(
    "-j",
    "--json",
    type=str,
    default="big.json",
    help="Input JSON file",
)

parser.add_argument("-b", "--bold", action="store_true", help="Set bold to True")

parser.add_argument(
    "-r", "--radius", type=int, default=30, help="Dot radius (1 to 100)"
)

parser.add_argument(
    "--scale", type=float, default=1.0, help="Scale factor for dot radius"
)

parser.add_argument(
    "--xy-scale",
    type=float,
    default=1.0,
    help="Scale factor for glyph size on X and Y axes",
)

parser.add_argument(
    "-s",
    "--shape",
    type=str,
    default="Round",
    choices=["Round", "Diamond", "Star", "Asterisk"],
    help="Dot shape (Round, Diamond, Star, or Asterisk)",
)

args = parser.parse_args()

if args.name:
    fnt_name = args.name

if not (0.0 <= args.italic <= 90.0):
    parser.error("Italic angle must be between 0.0 and 90.0")

if not (1 <= args.radius <= 100):
    parser.error("Radius must be between 1 and 100")

if args.bold and args.italic > 0.0:
    fnt_name += "-BoldItalic"
elif args.bold:
    fnt_name += "-Bold"
elif args.italic > 0.0:
    fnt_name += "-Italic"
else:
    fnt_name += "-Regular"

# dot radius: for round dots, ~50 is usual, 30 is light.
# square dots are a bit heavier than round
# star and diamond dots are a bit lighter than round
r = args.radius * args.scale

# italic angle: 0.0 for none; 12.08° looks nice
italic = args.italic

# bold?
bold = args.bold

# dot shape: Square, Diamond or Star.
shape = args.shape

with open(args.json) as data_file:
    chars = json.load(data_file)

# Get font dimensions from the first character
first_char = next(iter(chars))
matrix_height = len(chars[first_char])
matrix_width = len(chars[first_char][0])

# coordinates of centres of dots:
#  eg lower left dot is at (340, 250)
x_center = 500
y_center = 310
x_width = 320 * args.xy_scale
y_height = 500 * args.xy_scale
x_start = x_center - x_width / 2
x_end = x_center + x_width / 2
y_start = y_center + y_height / 2
y_end = y_center - y_height / 2

xvals = (
    [x_start + i * (x_end - x_start) / (matrix_width - 1) for i in range(matrix_width)]
    if matrix_width > 1
    else [x_start]
)
yvals = (
    [
        y_start - i * (y_start - y_end) / (matrix_height - 1)
        for i in range(matrix_height)
    ]
    if matrix_height > 1
    else [y_start]
)


# matrix translations:
# italic 1: shift LL corner to origin
mat_origin = psMat.translate(-xvals[0], -yvals[-1])

# italic 2: skew by italic angle
mat_skew = psMat.skew(math.pi * italic / 180.0)  # it likes radians

# italic 3: restore from origin to LL corner
mat_restore = psMat.translate(xvals[0], yvals[-1])

# bold: double-strike shift is half point diameter
mat_bold = psMat.translate(r, 0)

# a 'magic' value for approximating a circle with Bézier segments
magic = 4.0 / 3.0 * (math.sqrt(2) - 1)

# diamonds are just circles with relaxed control points
if shape == "Diamond":
    magic = magic / 2.0
# don't be tempted to make magic too large or you end up
#  with blocky yet frilly fonts that look disturbingly intestinal.

# parameters for stars
star = (3.0 + math.sqrt(5)) / 2.0
inner = r / star

# segment angle (72°), radians
seg = math.pi * (360.0 / 5.0) / 180.0

font = fontforge.font(
    em=1000,
    encoding="UnicodeFull",
    ascent=710,
    descent=290,
    design_size=12.0,
    is_quadratic=False,
    fontname=fnt_name,
)

# helps with glyph naming (usually)
fontforge.loadNamelist("glyphlist.txt")

# try to make a glyph for every char in json
for uch in chars:
    glyph = font.createChar(ord(uch))
    pts = []
    print("*** ", ord(uch), ": ", flush=True)
    yline = 0
    # go through glyph bitmap, placing dots where we find #s
    for li in chars[uch]:
        cy = yvals[yline]
        a_li = li
        xcol = 0
        for b in list(a_li):
            cx = xvals[xcol]
            if b == "#":
                # we have a pixel at cx, cy, so add it to the list
                pts.append(fontforge.point(cx, cy, False))
            xcol = xcol + 1
        yline = yline + 1

    # get the glyph's layer to draw on
    lyr = glyph.layers[glyph.activeLayer]
    # now transform the points and place contours in layer
    for p in pts:
        # italicize!
        if italic > 0.0:
            p.transform(mat_origin)
            p.transform(mat_skew)
            p.transform(mat_restore)
        cx = p.x
        cy = p.y

        if shape == "Asterisk":
            # Draw a 6-pointed star as three intersecting strokes
            stroke_width = r / 2.5
            for i in range(3):
                angle = i * math.pi / 3.0  # 0, 60, 120 degrees
                c_stroke = fontforge.contour()

                # Define corners of a horizontal rectangle
                points = [
                    (-r, -stroke_width / 2.0),
                    (r, -stroke_width / 2.0),
                    (r, stroke_width / 2.0),
                    (-r, stroke_width / 2.0),
                ]

                # Rotate and translate points
                rotated_points = []
                for x, y in points:
                    x_rot = x * math.cos(angle) - y * math.sin(angle)
                    y_rot = x * math.sin(angle) + y * math.cos(angle)
                    rotated_points.append((cx + x_rot, cy + y_rot))

                # Create contour from points
                c_stroke.moveTo(rotated_points[0][0], rotated_points[0][1])
                c_stroke.lineTo(rotated_points[1][0], rotated_points[1][1])
                c_stroke.lineTo(rotated_points[2][0], rotated_points[2][1])
                c_stroke.lineTo(rotated_points[3][0], rotated_points[3][1])
                c_stroke.closed = True
                lyr += c_stroke
            continue

        c = fontforge.contour()
        # draw a printer dot at (cx, cy) using chosen shape
        if shape == "Square":
            # Draw a dot by drawing a square of side 2r
            # move to start position
            c.moveTo(cx + r, cy + r)
            # draw the outline
            c.lineTo(cx + r, cy - r)
            c.lineTo(cx - r, cy - r)
            c.lineTo(cx - r, cy + r)
            c.lineTo(cx + r, cy + r)
        elif shape == "Star":
            # Draw a 5 pointed star!
            # move to start position (vertical; 90°)
            c.moveTo(cx, cy + r)
            for k in range(5):
                angle = math.pi / 2 + (k + 1) * seg
                inangle = angle - seg / 2.0
                c.lineTo(cx + inner * math.cos(inangle), cy + inner * math.sin(inangle))
                c.lineTo(cx + r * math.cos(angle), cy + r * math.sin(angle))
            # I drew this anticlockwise, so fix it (ahem)
            c.reverseDirection()
        else:
            # Draw a printer dot by approximating a circle
            #  (default; also draws diamonds if magic is low)
            # move to start position
            c.moveTo(cx + r, cy)
            # cubic sector 1: from 0° to 270°, clockwise
            c.cubicTo((cx + r, cy - magic * r), (cx + magic * r, cy - r), (cx, cy - r))
            # cubic sector 2: from 270° to 180°, clockwise
            c.cubicTo((cx - magic * r, cy - r), (cx - r, cy - magic * r), (cx - r, cy))
            # cubic sector 3: from 180° to 90°, clockwise
            c.cubicTo((cx - r, cy + magic * r), (cx - magic * r, cy + r), (cx, cy + r))
            # cubic sector 4: from 90° to 0°, clockwise
            c.cubicTo((cx + magic * r, cy + r), (cx + r, cy + magic * r), (cx + r, cy))
        # ensure path is closed (important!)
        c.closed = True
        lyr += c

    # do double-strike effect on glyph if bold
    if bold:
        new_lyr = lyr.dup()
        new_lyr.transform(mat_bold)
        lyr += new_lyr
    # update the glyph layers with our drawing
    glyph.layers[glyph.activeLayer] = lyr
    # some auto cleanups on each glyph to avoid manual work later
    # fix overlapping paths
    glyph.removeOverlap()
    # seems you have to set this too if you deliberately overlap
    glyph.unlinkRmOvrlpSave = True
    # add curve extrema (it's a font convention)
    glyph.addExtrema()
    # round all coordinates to integers
    glyph.round()
    # add PS hints, because we can
    glyph.autoHint()

# Find the maximum glyph width
max_width = 0
for g in font.glyphs():
    if g.glyphname == "space":
        continue
    bbox = g.boundingBox()
    width = bbox[2] - bbox[0]
    if width > max_width:
        max_width = width

# Set font width based on matrix_width
if matrix_width == 8:  # bigletter
    advance_width = round(max_width * 10 / 8)
elif matrix_width == 5:  # littleletter
    advance_width = round(max_width * 6 / 5)
else:
    advance_width = round(max_width)

# one last blat through all the glyphs to set monospace parameters
for g in font.glyphs():
    if g.glyphname == "space":
        continue
    bbox = g.boundingBox()
    width = bbox[2] - bbox[0]
    g.width = advance_width
    # Center the glyph in the advance width
    space_around = advance_width - width
    lsb = space_around / 2
    rsb = space_around - lsb
    g.left_side_bearing = round(lsb)
    g.right_side_bearing = round(rsb)
    print(
        f"Glyph: {g.glyphname}, BBox: {bbox}, Width: {width}, LSB: {g.left_side_bearing}, RSB: {g.right_side_bearing}",
        flush=True,
    )

# poor old space, always left to the end ...
space = font.createChar(ord(" "))
space.width = advance_width

# these need to restated for some reason,
#  and even then they don't always stick in FontForge
font.encoding = "UnicodeFull"
font.fontname = fnt_name
font.design_size = 12.0
# italic angle is negative for $reasons_i_dont_understand
font.italicangle = -italic

# save it and exit
font.save(fnt_name + ".sfd")
