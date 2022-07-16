import argparse
import glob
import logging
import os


class PasskeyFix:
    def __init__(self, args) -> None:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s"
        )
        self.old_passkey = bytes(args.old, encoding="latin1")
        self.new_passkey = bytes(args.new, encoding="latin1")
        self.torrents = [torrent for torrent in glob.glob(pathname="*.torrent", root_dir=args.dir)]
        self.stats = {"total": len(self.torrents), "updated": 0, "skipped": 0}

        logging.info(f"{self.stats['total']} torrent(s) found")

        for index, file in enumerate(self.torrents):
            progress = f"[{index + 1}/{self.stats['total']}]"
            self.path = os.path.join(args.dir, file)

            if self.old_passkey not in open(self.path, "rb").read():
                logging.info(f"{progress} Skipped {file}, passkey not found")
                self.stats["skipped"] += 1
                continue

            with open(self.path, "rb") as f:
                data = f.read()

            with open(self.path, "wb") as f:
                data = data.replace(self.old_passkey, self.new_passkey)
                f.write(data)

            logging.info(f"{progress} Updated {file}, passkey rewritten")
            self.stats["updated"] += 1

        logging.info(
            (
                f"Operation completed. {self.stats['total']} torrent(s) found. "
                f"{self.stats['updated']} torrent(s) rewritten. "
                f"{self.stats['skipped']} torrent(s) skipped."
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--old", help="Old passkey to be replaced", required=True)
    parser.add_argument("--new", help="New passkey to replace with", required=True)
    parser.add_argument("--dir", help="Directory path containing the .torrents", required=True)
    args = parser.parse_args()
    PasskeyFix(args)
