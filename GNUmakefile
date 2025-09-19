##############################################################################
# Bigletter Multics Font - GNUmakefile
# SPDX-License-Identifier: Multics
# Copyright (c) 1972 Massachusetts Institute of Technology
# Copyright (c) 1972-1982 Honeywell Information Systems, Inc.
# Copyright (c) 2006 Bull HN Information Systems, Inc.
# Copyright (c) 2006 Bull SAS
# Copyright (c) 2025 Jeffrey H. Johnson
# Copyright (c) 2025 The DPS8M Development Team
# scspell-id: 0b41f1f4-9405-11f0-8351-80ee73e9b8e7
##############################################################################

##############################################################################
# Configuration

SHELL=/bin/sh
RM=rm -f
FONTFORGE?=fontforge
FONTFORGE_ARGS?=-lang=ff -c \
  'Open($$1); SetFontNames($$2, $$2, $$2); Generate($$3)'
CC?=cc
CFLAGS?=-O
LDFLAGS?=-s
CP?=cp -f
MAKE?="$$(command -v gnumake 2> /dev/null || \
          command -v gmake   2> /dev/null || \
          command -v make    2> /dev/null || \
          printf '%s\n' 'make')"
.NOTPARALLEL:

##############################################################################
# Target: all

.PHONY: all
all: \
		BigletterMultics-Regular.ttf            \
		BigletterMultics-Bold.ttf               \
		LittleletterMultics-Regular.ttf         \
		LittleletterMultics-Bold.ttf            \
		BigletterStarMultics-Regular.ttf        \
		BigletterStarMultics-Bold.ttf           \
		LittleletterStarMultics-Regular.ttf     \
		LittleletterStarMultics-Bold.ttf        \
		BigletterAsteriskMultics-Regular.ttf    \
		BigletterAsteriskMultics-Bold.ttf       \
		LittleletterAsteriskMultics-Regular.ttf \
		LittleletterAsteriskMultics-Bold.ttf

##############################################################################
# Target: makefont

makefont: \
		makefont.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o "$@" "$<"

##############################################################################
# Target: big.json

big.json: \
		makefont
	./makefont "big" > "$@"

##############################################################################
# Target: little.json

little.json: \
		makefont
	./makefont "little" > "$@"

##############################################################################
# Target: BigletterMultics-Regular.sfd

BigletterMultics-Regular.sfd: \
		big.json ./makefont.py
	./makefont.py --name BigletterMultics \
		--shape Diamond --xy-scale 1.32 --radius 40 --json "big.json"

##############################################################################
# Target: BigletterStarMultics-Regular.sfd

BigletterStarMultics-Regular.sfd: \
		big.json ./makefont.py
	./makefont.py --name BigletterStarMultics \
		--shape Star --xy-scale 1.32 --radius 40 --json "big.json"

##############################################################################
# Target: BigletterAsteriskMultics-Regular.sfd

BigletterAsteriskMultics-Regular.sfd: \
		big.json ./makefont.py
	./makefont.py --name BigletterAsteriskMultics \
		--shape Asterisk --xy-scale 1.47 --radius 40 --json "big.json"

##############################################################################
# Target: BigletterMultics-Bold.sfd

BigletterMultics-Bold.sfd: \
		big.json ./makefont.py
	./makefont.py --name BigletterMultics --bold \
		--shape Diamond --xy-scale 1.32 --radius 38 --json "big.json"

##############################################################################
# Target: BigletterStarMultics-Bold.sfd

BigletterStarMultics-Bold.sfd: \
		big.json ./makefont.py
	./makefont.py --name BigletterStarMultics --bold \
		--shape Star --xy-scale 1.32 --radius 38 --json "big.json"

##############################################################################
# Target: BigletterAsteriskMultics-Bold.sfd

BigletterAsteriskMultics-Bold.sfd: \
		big.json ./makefont.py
	./makefont.py --name BigletterAsteriskMultics --bold \
		--shape Asterisk --xy-scale 1.47 --radius 38 --json "big.json"

##############################################################################
# Target: LittleletterMultics-Regular.sfd

LittleletterMultics-Regular.sfd: \
		little.json ./makefont.py
	./makefont.py --name LittleletterMultics \
		--shape Diamond --xy-scale 1.08 --radius 60 --json "little.json"

##############################################################################
# Target: LittleletterStarMultics-Regular.sfd

LittleletterStarMultics-Regular.sfd: \
		little.json ./makefont.py
	./makefont.py --name LittleletterStarMultics \
		--shape Star --xy-scale 1.08 --radius 60 --json "little.json"

##############################################################################
# Target: LittleletterAsteriskMultics-Regular.sfd

LittleletterAsteriskMultics-Regular.sfd: \
		little.json ./makefont.py
	./makefont.py --name LittleletterAsteriskMultics \
		--shape Asterisk --xy-scale 1.20 --radius 60 --json "little.json"

##############################################################################
# Target: LittleletterMultics-Bold.sfd

LittleletterMultics-Bold.sfd: \
		little.json ./makefont.py
	./makefont.py --name LittleletterMultics --bold \
		--shape Diamond --xy-scale 1.08 --radius 58 --json "little.json"

##############################################################################
# Target: LittleletterStarMultics-Bold.sfd

LittleletterStarMultics-Bold.sfd: \
		little.json ./makefont.py
	./makefont.py --name LittleletterStarMultics --bold \
		--shape Star --xy-scale 1.08 --radius 58 --json "little.json"

##############################################################################
# Target: LittleletterAsteriskMultics-Bold.sfd

LittleletterAsteriskMultics-Bold.sfd: \
		little.json ./makefont.py
	./makefont.py --name LittleletterAsteriskMultics --bold \
		--shape Asterisk --xy-scale 1.20 --radius 58 --json "little.json"

##############################################################################
# Target: .sfd -> .ttf

%.ttf: %.sfd
	$(FONTFORGE) $(FONTFORGE_ARGS) "$<" "$(basename $@)" "$@"

##############################################################################
# Target: distdir

.PHONY: distdir
distdir: \
		all ./TrueType
	$(CP) ./*.ttf ./TrueType/
	$(MAKE) clean

##############################################################################
# Target: clean

.PHONY: clean
clean:
	$(RM) ./makefont ./*.json ./*.sfd ./*.ttf

##############################################################################
# vim: set ft=make noexpandtab tabstop=4 cc=78 :
##############################################################################
