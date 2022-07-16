import argparse
import glob
import logging
import os


class PasskeyFix:
    def __init__(self, args) -> None:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s"
        )
        old_passkey = bytes(args.old, encoding="latin1")
        new_passkey = bytes(args.new, encoding="latin1")
        torrents = [torrent for torrent in glob.glob(pathname="*.torrent", root_dir=args.dir)]
        stats = {"total": len(torrents), "updated": 0, "skipped": 0}

        logging.info(f"{stats['total']} torrent(s) found")

        for index, file in enumerate(torrents):
            progress = f"[{index + 1}/{stats['total']}]"
            path = os.path.join(args.dir, file)

            if old_passkey not in open(path, "rb").read():
                logging.info(f"{progress} Skipped {file}, passkey not found")
                stats["skipped"] += 1
                continue

            with open(path, "rb") as f:
                data = f.read()

            with open(path, "wb") as f:
                f.write(data.replace(old_passkey, new_passkey))

            logging.info(f"{progress} Updated {file}, passkey rewritten")
            stats["updated"] += 1

        logging.info(
            (
                f"Operation completed. {stats['total']} torrent(s) found. "
                f"{stats['updated']} torrent(s) rewritten. "
                f"{stats['skipped']} torrent(s) skipped."
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple utility to bulk replace passkeys in .torrent files")
    parser.add_argument("--old", help="old passkey to be replaced", type=str, metavar="<old passkey>", required=True)
    parser.add_argument("--new", help="new passkey to replace with", metavar="<new passkey>", type=str, required=True)
    parser.add_argument("--dir", help="directory containing .torrents", metavar="<path>", type=str, required=True)
    args = parser.parse_args()
    PasskeyFix(args)
