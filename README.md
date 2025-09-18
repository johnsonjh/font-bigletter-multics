<!-- SPDX-License-Identifier: Multics -->
<!-- Copyright (c) 1972 Massachusetts Institute of Technology -->
<!-- Copyright (c) 1972 Honeywell Information Systems, Inc. -->
<!-- Copyright (c) 2006 Bull HN Information Systems, Inc. -->
<!-- Copyright (c) 2006 Bull SAS -->
<!-- Copyright (c) 2025 Jeffrey H. Johnson -->
<!-- Copyright (c) 2025 The DPS8M Development Team -->
<!-- scspell-id: 9c26b4ce-9415-11f0-9013-80ee73e9b8e7 -->
# Bigletter (and Littleletter) Multics Fonts

## Overview

* The [Multics](https://swenson.org/multics_wiki/) I/O daemon (see [Multics printing software](https://multicians.org/printer.html)) uses the [`bigletter_`](https://dps8m.gitlab.io/sb/MR12.8/library_dir_dir/system_library_standard/source/bound_printing_cmds_.s.archive/bigletter_.pl1.html) procedure to create the large text used on print job head and tail (banner) pages.
* The fonts used on these pages are defined in [`letseg_.alm`](https://dps8m.gitlab.io/sb/MR12.8/library_dir_dir/system_library_standard/source/bound_printing_cmds_.s.archive/letseg_.alm.html) in the Multics source code.
* There are actually *two* fonts defined in these tables:
  * The "*big*" font which is **9×8** (a *large* font used in the body of the banner pages), and,
  * The "*little*" font which is **5×5** (a *small* font used for printing on the edges of the banner pages).
* You can read some anecdotes about this code at [multicians.org](https://multicians.org/bigletter_.html).

## Fonts

* This repository contains:
  * a [C program](makefont.c) which converts these tables to JSON files,
  * and [Python program](makefont.py) which converts the JSON files to [Spline Font Databases](https://github.com/fontforge/fontforge/blob/master/fontforge/sfd.c).
[]()

[]()
* [Fontforge](https://fontforge.org/) is used to convert the generated SFD files to monospaced TrueType fonts.

### Variants

* We build *two* different TrueType variants of each font:
  * the "normal" font optimized for the screen and smaller sizes, and,
  * a "star" variant optimized for larger print (like banner pages).

## Build

* Building the fonts from source requires [GNU Make](https://www.gnu.org/software/make/), a [C compiler](https://gcc.gnu.org/), [Python 3](https://www.python.org/), and [Fontforge](https://fontforge.org/).

## Download

* You may [download the built TrueType fonts here](TrueType) in case you cannot build them yourself.

## Future

* The creation of fully vectorized fonts (created with the help of [AutoTrace](https://github.com/autotrace/autotrace) or [Potrace](https://potrace.sourceforge.net/)) is planned.  For now, only dot‑matrix style fonts are generated.

## License

```
Multics License

Copyright © 1972 The Massachusetts Institute of Technology
Copyright © 1972 Honeywell Information Systems, Inc.
Copyright © 2006 Bull HN Information Systems, Inc.
Copyright © 2006 Bull SAS
Copyright © 2025 Jeffrey H. Johnson
Copyright © 2025 The DPS8M Development Team

All rights reserved.

 * This edition of the Multics software materials and documentation is
   provided and donated to The Massachusetts Institute of Technology by
   Group BULL including BULL HN Information Systems, Inc. as a contribution
   to computer science knowledge.

 * This donation is made also to give evidence of the common contributions
   of The Massachusetts Institute of Technology, Bell Laboratories, General
   Electric, Honeywell Information Systems, Inc., Honeywell BULL, Inc.,
   Groupe BULL and BULL HN Information Systems, Inc. to the development of
   this operating system.

 * Multics development was initiated by The Massachusetts Institute of
   Technology Project MAC (1963-1970), renamed the MIT Laboratory for
   Computer Science and Artificial Intelligence in the mid 1970s, under
   the leadership of Professor Fernando José Corbató. Users consider that
   Multics provided the best software architecture for managing computer
   hardware properly and for executing programs. Many subsequent operating
   systems incorporated Multics principles.

 * Multics was distributed in 1975 to 2000 by Group Bull in Europe, and in
   the U.S. by Bull HN Information Systems, Inc., as successor in interest
   by change in name only to Honeywell Bull, Inc. and Honeywell Information
   Systems, Inc.

Permission to use, copy, modify, and distribute these programs and their
documentation for any purpose and without fee is hereby granted, provided
that this copyright notice and the above historical background appear in all
copies and that both the copyright notice and historical background and this
permission notice appear in supporting documentation, and that the names of
MIT, HIS, BULL, or BULL HN not be used in advertising or publicity pertaining
to distribution of the programs without specific prior written permission.
```
