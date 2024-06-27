import csv
import io
import os
import pathlib
import requests
import argparse
import zipfile

def download_dataset(version_file: str, cache: str):
    with open(version_file, "r") as f:
        file = csv.reader(f, delimiter=';')


        _lines = iter(file)
        next(_lines)
        for [name, hyperlink] in _lines:
            print(f'{name} :) {hyperlink}')

            path = pathlib.Path(cache, name)
            if path.exists():
                continue
            os.mkdir(path)

            response = requests.get(hyperlink)
            assert(response.ok)

            zf = zipfile.ZipFile(io.BytesIO(response.content))
            zf.extractall(path)

def consolidate_datasets(datasets: list[str]):

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version', type=str, help='Version file of dataset to use')
    parser.add_argument('-c', '--cache', type=str, default='cache', help='Cache directory to use')

    return parser.parse_args()


def main():
    args = parse_args()
    download_dataset(args.version, args.cache)

if __name__ == '__main__':
    main()
