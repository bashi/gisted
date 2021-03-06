# -*- coding: utf-8 -*-

import sys
import optparse
import gisted.tools as tools
import logging
import urllib2

def upload(options):
    u = tools.Uploader.make()
    r = u.upload(options.url, options.title, open(options.file).read())
    print r["url"]

def print_post(post):
    print u"gist id: {gist_id}".format(gist_id=post.gist_id)
    print u"title:   {title}".format(title=post.title)
    print u"url:     {url}".format(url=post.source_url)
    print post.to_markdown()

def download(options):
    d = tools.Downloader.make()
    post = d.get(options.gist)
    print_post(post)

def fetch(options):
    f = tools.Fetcher(options.url)
    print_post(f.post)

def parse_args(args):
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="url", help="The URL of the talk", metavar="URL")
    parser.add_option("-t", "--title", dest="title", help="The title of the talk", metavar="TALK")
    parser.add_option("-f", "--file", dest="file", help="The transcript file", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", help="Output log louder", action="store_true")
    parser.add_option("-g", "--gist", dest="gist", help="Gist ID", metavar="ID")
    return parser.parse_args(args)

def die(message):
    logging.error(message)
    sys.exit(1)

def run(args):
    (options, args) = parse_args(args)

    if 1 == len(args):
        die("No command given")
    elif "upload" == args[1]:
        upload(options)
    if "download" == args[1]:
        download(options)
    if "fetch" == args[1]:
        fetch(options)
    else:
        die("No such command:" + args[1])
