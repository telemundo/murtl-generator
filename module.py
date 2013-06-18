#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import time
import csv
from optparse import OptionParser

parser = OptionParser(usage='usage: %prog [options] inputfile')
parser.add_option('-v', action='count', dest='verbosity', default=0, help='increase output verbosity')
parser.add_option('-q', '--quiet', action='store_true', dest='quiet', help='hide all output')
parser.add_option('-b', '--base', dest='base_domain', default='www.telemundo.com', type='string', help='base domain (default: www.telemundo.com)')
parser.add_option('-m', '--mobile', dest='mobile_domain', default='movil.telemundo.com', type='string', help='mobile domain (default: m.telemundo.com)')
parser.add_option('-f', '--file', dest='file', default=None, type='string', help='file where to store the output')
(options, args) = parser.parse_args()

def create_rule(name, url, target, type='static', extra=''):
    rule = []
    rule.append(name)
    rule.append(type)
    rule.append('http://%s' % (url))
    if type == 'static':
        rule.append('http://%s' % (target))
    elif type == 'rss':
        rule.append('')
    elif type == 'advanced':
        rule.append('http://%s' % (target))
        rule.append('%s' % (extra))
    elif type == 'passthru':
        rule.append('%d' % (int(target)))

    return '\t'.join(rule)

def main():
    if len(args) < 1:
        parser.error('you must specify an input file to parse.')

    filename = args[0]
    if not os.path.exists(filename):
        parser.error('the input file "%s" does not exist.' % filename)

    rules = []
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            name, url, vanity = row
            clean_url = url.rstrip('/')

            rules.append(create_rule(name, options.base_domain + clean_url, options.mobile_domain + url, 'static'))
            rules.append(create_rule(name + ' (DNR)', options.base_domain + clean_url, '3', 'passthru'))

            for part in [s.strip() for s in vanity.split('|')]:
                if part:
                    rules.append(create_rule(name + ' - Vanity', options.base_domain + part, options.mobile_domain + url, 'static'))
                    rules.append(create_rule(name + ' - Vanity (DNR)', options.base_domain + part, '3', 'passthru'))

            hubregex = re.compile('^/([a-z0-9_\-]+)?/?$', re.IGNORECASE)
            if not hubregex.match(url):
                rules.append(create_rule(name + ' - Articles', options.base_domain + clean_url + '/articles', options.mobile_domain + clean_url + '/articles'))
                rules.append(create_rule(name + ' - Articles (DNR)', options.base_domain + clean_url + '/article', '3', 'passthru'))
                #rules.append(create_rule(name + ' - Article', options.base_domain + clean_url + '/article/', options.mobile_domain + '/lib/redirect.php?hub=\\1&path=\\2/\\3/\\4', 'advanced', '#/([a-z0-9_\\-]+)/([a-z0-9_\\-]+)/([a-z0-9_\\-]+)/(.*)#i'))
                rules.append(create_rule(name + ' - Article', options.base_domain + clean_url + '/article/', options.mobile_domain + '/\\1/\\2/\\3/\\4', 'advanced', '#/([a-z0-9_\\-]+)/([a-z0-9_\\-]+)/([a-z0-9_\\-]+)/(.*)#i'))
                rules.append(create_rule(name + ' - Article (DNR)', options.base_domain + clean_url + '/article/', '3', 'passthru'))
                rules.append(create_rule(name + ' - Photo Galleries', options.base_domain + clean_url + '/photos', options.mobile_domain + clean_url + '/photos', 'static'))
                rules.append(create_rule(name + ' - Photo Galleries (DNR)', options.base_domain + clean_url + '/photos', '3', 'passthru'))
                #rules.append(create_rule(name + ' - Photo Gallery', options.base_domain + clean_url + '/photo_gallery/', options.mobile_domain + '/lib/redirect.php?hub=\\1&path=\\2/\\3/\\4', 'advanced', '#/([a-z0-9_\\-]+)/([a-z0-9_\\-]+)/([a-z0-9_\\-]+)/(.*)#i'))
                rules.append(create_rule(name + ' - Photo Gallery', options.base_domain + clean_url + '/photo_gallery/', options.mobile_domain + '/\\1/\\2/\\3/\\4', 'advanced', '#/([a-z0-9_\\-]+)/([a-z0-9_\\-]+)/([a-z0-9_\\-]+)/(.*)#i'))
                rules.append(create_rule(name + ' - Photo Gallery (DNR)', options.base_domain + clean_url + '/photo_gallery/', '3', 'passthru'))
                rules.append(create_rule(name + ' - Rankit', options.base_domain + clean_url + '/rankit/', options.mobile_domain + clean_url + '/rankits', 'static'))
                rules.append(create_rule(name + ' - Rankit (DNR)', options.base_domain + clean_url + '/rankit/', '3', 'passthru'))
                rules.append(create_rule(name + ' - Videos', options.base_domain + clean_url + '/videos', options.mobile_domain + clean_url + '/rankits', 'static'))
                rules.append(create_rule(name + ' - Videos (DNR)', options.base_domain + clean_url + '/videos', '3', 'passthru'))
                rules.append(create_rule(name + ' - Video Player SEO', options.base_domain + clean_url + '/video/', options.mobile_domain + clean_url + '/videos', 'static'))
                rules.append(create_rule(name + ' - Video Player SEO (DNR)', options.base_domain + clean_url + '/video/', '3', 'passthru'))
                rules.append(create_rule(name + ' - Video Player Legacy', options.base_domain + clean_url + '/video_player', options.mobile_domain + clean_url + '/videos', 'static'))
                rules.append(create_rule(name + ' - Video Player Legacy (DNR)', options.base_domain + clean_url + '/video_player', '3', 'passthru'))

                novelaregex = re.compile('/novelas/', re.IGNORECASE)
                if novelaregex.match(url):
                    rules.append(create_rule(name + ' - Historia & Personajes', options.base_domain + clean_url + '/historias_y_personajes', options.mobile_domain + clean_url + '/historias_y_personajes', 'static'))
                    rules.append(create_rule(name + ' - Historia & Personajes (DNR)', options.base_domain + clean_url + '/historias_y_personajes', '3', 'passthru'))

    if len(rules) > 0:
        if options.verbosity >= 1 and not options.quiet:
            print '[%s] NOTICE: created %d rules' % (time.strftime('%Y-%m-%d %H:%M:%S'), len(rules))

        if options.file is not None:
            outputfile = options.file
        else:
            filepath = os.path.basename(filename)
            (filebase, _) = os.path.splitext(filepath)
            outputfile = '%s_%s_%s.txt' % (filebase, options.base_domain, options.mobile_domain)

        with open(outputfile, 'wb') as outfile:
            for rule in rules:
                outfile.write(rule + os.linesep)
                if options.verbosity >= 2 and not options.quiet:
                    print '[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), rule)
    else:
        if options.verbosity >= 1 and not options.quiet:
            print '[%s] WARNING: no rules created' % (time.strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    main()

