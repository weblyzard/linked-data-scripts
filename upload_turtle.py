#!/usr/bin/env python3
'''
Upload turtle files from DBpedia, Wikidata, etc. to an RDF4J server.

(C)opyrights Albert Weichselbraun 2011-2016
'''

from gzip import GzipFile
from bz2 import BZ2File
from argparse import ArgumentParser
from os.path import basename
import lzma
import httplib2

def parse_arguments():
    ''' prepares the argument parser '''
    parser = ArgumentParser()
    parser.add_argument("fname", help="File(s) to upload.", nargs="+", default=None)
    parser.add_argument("--encoding", help="Encoding used in the turtle files (default: utf-8).", default="utf-8")
    parser.add_argument("--repository-url", help="URL of the SPARQL repository to use.")
    parser.add_argument("--chunksize", help="Number of lines to upload at ones (default: 25000).", default=25000)
    parser.add_argument("--skip", help="Number of lines to skip prior to the next upload (default: 0).", type=int, default=0)
    return parser.parse_args()

def upload_content(triple_list, repository_url, context):
    '''
    Serializes the triples to the given repository.
    '''
    data = '\n'.join(triple_list).encode('utf-8')
    endpoint = '{repository_url}/rdf-graphs/{context}'.format(repository_url=repository_url,
                                                              context=context)
    (response, msg) = httplib2.Http().request(endpoint, 'POST', body=data, headers={'Content-Type': 'text/plain'})

    if response.status != 204:
        print("Response {}: {}".format(response.status, msg))
        print("Saving invalid data.")
        with open("invalid.ttl", "wb") as outfile:
            outfile.write(data)
        exit(-1)


def upload_ttl(fname, encoding, chunksize, skip, repository_url):
    '''
    uploads a triple file.
    '''
    if fname.endswith('.gz'):
        fopen = GzipFile
    elif fname.endswith('.bz2'):
        fopen = BZ2File
    elif fname.endswith('.xz'):
        fopen = lzma.open
    else:
        fopen = open

    count = 0
    with fopen(fname, 'rb') as infile:
        triple_list = []
        for no, line in enumerate(infile):
            if no < skip:
                continue
            line = line.strip()
            if line:
                triple_list.append(line.decode(encoding))

            if no % chunksize != chunksize - 1:
                continue

            print("Total number of triples: {}. Adding another chunk of {} triples.".format(count, len(triple_list)))
            count += len(triple_list)
            upload_content(triple_list, repository_url, context=basename(fname))
            triple_list = []

        # uploading the final batch of triples
        print("Total number of triples: {}. Adding another chunk of {} triples.".format(count, len(triple_list)))
        count += len(triple_list)
        upload_content(triple_list, repository_url, context=basename(fname))


# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    args = parse_arguments()

    for filename in args.fname:
        print("Uploading file '{}'.".format(filename))
        upload_ttl(filename, args.encoding, args.chunksize, args.skip, args.repository_url)
