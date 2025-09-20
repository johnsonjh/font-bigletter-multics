/*
 * vim: filetype=c:tabstop=2:softtabstop=2:shiftwidth=2:ai:expandtab:cc=80:
 * SPDX-License-Identifier: Multics
 * scspell-id: 9af43172-9653-11f0-942c-80ee73e9b8e7
 *
 * ---------------------------------------------------------------------------
 *
 * Copyright (c) 1972 Massachusetts Institute of Technology
 * Copyright (c) 1972-1982 Honeywell Information Systems, Inc.
 * Copyright (c) 2006 Bull HN Information Systems, Inc.
 * Copyright (c) 2006 Bull SAS
 * Copyright (c) 2025 Jeffrey H. Johnson
 * Copyright (c) 2025 The DPS8M Development Team
 *
 * ---------------------------------------------------------------------------
 */

/*****************************************************************************/

#include <ctype.h>
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*****************************************************************************/

static const bool never = false;

#if defined(FREE)
# undef FREE
#endif

#define FREE(p)   \
  do              \
    {             \
      free((p));  \
      (p) = NULL; \
    } while (never)

/*****************************************************************************/

struct glyph
{
  int character;
  char * rows [64];
};

/*****************************************************************************/

static int g_glyph_height = -1;
static int g_glyph_width  = -1;

/*****************************************************************************/

static int
parse_json (FILE * file, struct glyph * glyphs, int * glyph_count)
{
  enum
    {
      LOOKING_FOR_KEY,
      IN_KEY,
      LOOKING_FOR_VALUE,
      IN_STRING_ARRAY,
      IN_STRING
    } state = LOOKING_FOR_KEY;

  int c;
  char buffer [512];
  int buffer_pos  = 0;
  int current_row = 0;
  int error_found = 0;

  while ((c = fgetc (file)) != EOF)
    {
      switch (state)
        {
          case LOOKING_FOR_KEY:
            if (c == '"' || c == '\'')
              {
                state      = IN_KEY;
                buffer_pos = 0;
              }
            break;

          case IN_KEY:
            if (c == '\\')
              {
                c = fgetc (file);

                if (c == EOF)
                  {
                    error_found = 1;
                    break;
                  }

                if (c == 'u')
                  {
                    char hex [5];

                    if (fread (hex, 1, 4, file) != 4)
                      {
                        error_found = 1;
                        break;
                      }

                    hex [4] = '\0';
                    buffer [buffer_pos++] = (char)strtol (hex, NULL, 16);
                  }
                else
                  buffer [buffer_pos++] = (char)c;
              }
            else if (c == '"' || c == '\'')
              {
                buffer [buffer_pos] = '\0';
                glyphs [* glyph_count] . character = (unsigned char)buffer [0];
                state = LOOKING_FOR_VALUE;
              }
            else
              buffer [buffer_pos++] = (char)c;
            break;

          case LOOKING_FOR_VALUE:
            if (c == '[')
              {
                state       = IN_STRING_ARRAY;
                current_row = 0;
              }
            break;

          case IN_STRING_ARRAY:
            if (c == '"' || c == '\'')
              {
                state      = IN_STRING;
                buffer_pos = 0;
              }
            else if (c == ']')
              {
                if (g_glyph_height == -1)
                  g_glyph_height = current_row;

                (* glyph_count)++;
                state = LOOKING_FOR_KEY;
              }
            break;

          case IN_STRING:
            if (c == '"' || c == '\'')
              {
                buffer [buffer_pos] = '\0';

                if (g_glyph_width == -1)
                  g_glyph_width = (int)strlen (buffer);

                glyphs [* glyph_count] . rows [current_row] = strdup (buffer);
                current_row++;
                state = IN_STRING_ARRAY;
              }
            else
              buffer [buffer_pos++] = (char)c;
            break;

          default:
            (void)fprintf (stderr, "FATAL: Internal error in parse_json.\n");
            abort ();
        }

      if (error_found)
        break;
    }

  if (ferror (file))
    {
      const char * read_error = "FATAL: Read error parsing file";

      (void)(errno
        ? fprintf (stderr, "%s: %s (Error %d)\n",
                   read_error, strerror (errno), errno)
        : fprintf (stderr, "%s\n", read_error));

      clearerr (file);

      return -1;
    }

  return 0;
}

/*****************************************************************************/

static char *
xstrcasestr (const char * haystack, const char * needle)
{
  if (! * needle)
    return (char *)haystack;

  for (; * haystack; haystack++)
    {
      const char * h = haystack;
      const char * n = needle;

      while (* h && * n)
        {
          char ch1 = * h;
          char ch2 = * n;

          if (ch1 >= 'A' && ch1 <= 'Z')
            ch1 += 32;

          if (ch2 >= 'A' && ch2 <= 'Z')
            ch2 += 32;

          if (ch1 != ch2)
            break;

          h++;
          n++;
        }

      if (! * n)
        return (char *)haystack;
    }

  return NULL;
}

/*****************************************************************************/

static void
write_flf (FILE * file, const char * font_name, struct glyph * glyphs,
           int glyph_count)
{
  char * empty_row;
  char * modified_row;
  int i;
  int j;
  int k;
  bool littleletter;
  struct glyph * g;

  littleletter = NULL != xstrcasestr (font_name, "littleletter");

  modified_row = malloc ((size_t)g_glyph_width + 2);

  if (NULL == modified_row)
    abort ();

  empty_row = malloc ((size_t)g_glyph_width + 2);

  if (NULL == empty_row)
    {
      FREE (modified_row);
      abort ();
    }

  if (littleletter)
    (void)fprintf (file, "flf2a$ %d %d %d -1 1 0 0\n",
                   g_glyph_height + 1, g_glyph_height, g_glyph_width + 1);
  else
    (void)fprintf (file, "flf2a$ %d %d %d -1 1 0 0\n",
                   g_glyph_height, g_glyph_height - 1, g_glyph_width + 1);

  (void)fprintf (file, "Font generated by makefiglet: %s\n",
                 font_name);

  (void)memset (empty_row, '$', (size_t)g_glyph_width + 1);

  empty_row [g_glyph_width + 1] = '\0';

  for (i = 32; i <= 126; i++)
    {
      g = NULL;

      for (j = 0; j < glyph_count; j++)
        if (glyphs [j] . character == i)
          {
            g = & glyphs [j];
            break;
          }

      if (g)
        {
          for (j = 0; j < g_glyph_height; j++)
            {
              for (k = 0; k < g_glyph_width; k++)
                {
                  char ch = g -> rows [j] [k];

                  if (ch == '.')
                    modified_row [k] = '$';
                  else if (ch == '#')
                    modified_row [k] = '*';
                  else
                    modified_row [k] = ch;
                }
              modified_row [g_glyph_width]     = '$';
              modified_row [g_glyph_width + 1] = '\0';

              if (j == g_glyph_height - 1 && ! littleletter)
                (void)fprintf (file, "%s@@\n", modified_row);
              else
                (void)fprintf (file, "%s@\n", modified_row);
            }

          if (littleletter)
            (void)fprintf (file, "%s@@\n", empty_row);
        }
      else
        {
          for (j = 0; j < g_glyph_height; j++)
            {
              if (j == g_glyph_height - 1 && ! littleletter)
                (void)fprintf (file, "%s@@\n", empty_row);
              else
                (void)fprintf (file, "%s@\n", empty_row);
            }

          if (littleletter)
            (void)fprintf (file, "%s@@\n", empty_row);
        }
    }

  FREE (modified_row);
  FREE (empty_row);
}

/*****************************************************************************/

static int
compare_glyphs (const void * a, const void * b)
{
  const struct glyph * ga = (const struct glyph *)a;
  const struct glyph * gb = (const struct glyph *)b;

  return ga -> character - gb -> character;
}

/*****************************************************************************/

int
main (int argc, char * argv [])
{
  const char * program_name =
    (argv [0] && * argv [0]) ? argv [0] : "makefiglet";
  char * json_filename;
  char * flf_filename;
  char * font_name;
  FILE * json_file;
  FILE * flf_file;
  struct glyph glyphs [256];
  int glyph_count = 0;
  int i;
  int j;

  if (4 != argc)
    {
      (void)fprintf (stderr,
                     "Usage: %s <input.json> <output.flf> <font_name>\n",
                     program_name);

      return EXIT_FAILURE;
    }

  json_filename = argv [1];
  flf_filename  = argv [2];
  font_name     = argv [3];

  json_file = fopen (json_filename, "r");

  if (! json_file)
    {
      (void)fprintf (stderr, "FATAL: Error opening JSON file: %s (Error %d)\n",
                     strerror (errno), errno);

      return EXIT_FAILURE;
    }

  (void)memset (glyphs, 0, sizeof (glyphs));

  if (0 != parse_json (json_file, glyphs, & glyph_count))
    {
      const char * read_error = "FATAL: Error parsing JSON file";

      (void)(errno
        ? fprintf (stderr, "%s: %s (Error %d)\n",
                   read_error, strerror (errno), errno)
        : fprintf (stderr, "%s\n", read_error));

      (void)fclose (json_file);

      return EXIT_FAILURE;
    }

  (void)fclose (json_file);

  qsort (glyphs, (size_t)glyph_count, sizeof (struct glyph), compare_glyphs);

  flf_file = fopen (flf_filename, "w");

  if (! flf_file)
    {
      const char * read_error = "FATAL: Error opening FLF file";

      (void)(errno
        ? fprintf (stderr, "%s: %s (Error %d)\n",
                   read_error, strerror (errno), errno)
        : fprintf (stderr, "%s\n", read_error));

      return EXIT_FAILURE;
    }

  write_flf (flf_file, font_name, glyphs, glyph_count);

  (void)fclose (flf_file);

  for (i = 0; i < glyph_count; i++)
    if (g_glyph_height > 0)
      for (j = 0; j < g_glyph_height; j++)
        FREE (glyphs [i] . rows [j]);

  return EXIT_SUCCESS;
}

/*****************************************************************************/
