#!/usr/bin/env python3
import fnmatch
import os


def process(s):
    print('Processing %s ...' % s, end=' ')
    hdrs = {}
    pkgs = {}
    f = os.popen('lzma -c -d %s.txt.lzma' % s)
    g = open(s+'.sql', 'w')

    g.write('''
    BEGIN;
    CREATE TABLE headers(id_hdr INT PRIMARY KEY NOT NULL, header VARCHAR(64) NOT NULL, id_pkg INT NOT NULL);
    CREATE TABLE packages(id_pkg INT PRIMARY KEY NOT NULL, package VARCHAR(64) NOT NULL);
    ''')

    for line in f:
        line = line.strip().split(' ')
        if line[0] not in pkgs:
            pkgs[line[0]] = len(pkgs)
            g.write('INSERT INTO packages(id_pkg, package) '
                    "VALUES(%s, '%s');\n" % (pkgs[line[0]], line[0]))
        if (line[0]+line[1]) not in hdrs:
            hdrs[line[0]+line[1]] = len(hdrs)
            g.write('INSERT INTO headers(id_hdr, header, id_pkg) '
                    "VALUES(%s, '%s', %s);\n" % (
                        hdrs[line[0]+line[1]], line[1], pkgs[line[0]]))
    g.write('CREATE INDEX headers_header_idx ON headers(header);\n')

    g.write('COMMIT;\n')
    f.close()
    g.close()
    print('done')


for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'header-*.txt.lzma'):
        process(file[:-9])
