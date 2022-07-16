# passkeyfix
A simple utility to bulk replace passkeys in .torrent files. 

## Requirements
- Python 3.6+
- No external dependencies.

## Usage
```
> python passkeyfix.py -h
usage: passkeyfix.py [-h] --old <old passkey> --new <new passkey> --dir <path>

A simple utility to bulk replace passkeys in .torrent files

options:
  -h, --help           show this help message and exit
  --old <old passkey>  old passkey to be replaced
  --new <new passkey>  new passkey to replace with
  --dir <path>         directory containing .torrents
```
