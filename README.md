## Upload Turtle

This script uploads `.ttl` files (uncompressed or compressed using bz2, gzip or xz) to an rdf4j repository. 

### Dependencies

* Python 3.x
* httplib2 (`apt-get install python3-httplib2`)


### Usage


```bash
usage: upload_turtle.py [-h] [--encoding ENCODING]
                        [--repository-url REPOSITORY_URL]
                        [--chunksize CHUNKSIZE] [--skip SKIP]
                        fname [fname ...]

positional arguments:
  fname                 File(s) to upload.

optional arguments:
  -h, --help            show this help message and exit
  --encoding ENCODING   Encoding used in the turtle files (default: utf-8).
  --repository-url REPOSITORY_URL
                        URL of the SPARQL repository to use.
  --chunksize CHUNKSIZE
                        Number of lines to upload at ones (default: 25000).
  --skip SKIP           Number of lines to skip prior to the next upload
                        (default: 0).
```

### Examples

```bash
   ./upload_turtle.py ./data/wikidata-*.gz \
           --repository-url http://localhost:8080/rdf4j-server/repositories/wikidata
```
