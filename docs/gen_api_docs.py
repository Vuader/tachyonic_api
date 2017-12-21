#!/usr/bin/env python3
import sys, os
import re
from tachyonic.neutrino.wsgi import app
from operator import itemgetter

usage = """
Usage:
%s module output_dir [-s split] [-f]

Where:
    split is the column number (where URL is split by '/') to use for unique output file.
    -f Force Overwrite if output file exists.
""" % sys.argv[0]

# Check args
if len(sys.argv) < 3:
    print(usage)
    sys.exit(0)

if not '-s' in sys.argv:
    s = 0
else:
    s = sys.argv[sys.argv.index('-s') + 1]
    s = int(s)

force = False
if '-f' in sys.argv:
    force = True

module = sys.argv[1]
output_dir = sys.argv[2]
method_order = ['get', 'put', 'post', 'delete']
sections = set()

__import__(module)
routes = sorted(app.router.routes, key=itemgetter(1))
uris = []

# Prepare the list of dicts that contain all the info (uris)
for r in routes:
    if r[1]:
        section = r[1].split('/')[s]
        route = r[1]
    else:
        section = "index"
        route = "/"
    sections.add(section)
    desc = r[2].__doc__
    if desc is None:
        desc = oneliner = ''
    else:
        oneliner = desc.split('\n')[1]
        # Need to make sure first line and minimum indent of
        # docstring is 4 spaces to be correct in rst file.
        indent = re.match(' +', oneliner)
        indent = indent.group(0)
        desc = re.sub('^' + indent, ' '*4, desc, flags=re.MULTILINE)

    uris.append({'method': r[0],
                 'route': route,
                 'oneliner': oneliner,
                 'desc': desc,
                 'policy': r[3],
                 'section': section})


# Write output

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Create Output Files
title_template = module
for section in sections:
    if os.path.isfile("%s/%s.rst" % (output_dir,section))\
            and not force:
        print("%s.rst exists, skipping" % section)
    else:
        print("Creating %s.rst" % section)
        title = title_template + ' - ' + section
        title = title.replace('.','\.')
        title = title.replace('_','\_')
        with open(output_dir+'/'+section+'.rst','w') as f:
            f.write(title + '\n')
            f.write('=' * len(title))
            f.write('\n\n')

# Add routes to output files
hline = '\n----\n\n'
for u in uris:
    fname = "%s/%s.rst" % (output_dir, u['section'])
    with open(fname, 'a') as f:
        f.write(".. container:: toggle\n\n")
        f.write("    .. container:: header\n\n")
        es = ' ' * 8
        heading = "%s%s **%s** %s" % (es, u['method'], u['route'], u['oneliner'])
        f.write(heading + '\n\n')
        f.writelines(u['desc'] + hline)

