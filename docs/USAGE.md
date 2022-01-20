# Usage

This is a guide to using each tool in the repository.

## Individual Tools

Each tool is in its own folder named appropriately i.e.

```txt
├── LICENSE.md
├── Pipfile
├── Pipfile.lock
├── README.md
├── __init__.py
├── crack
│   ├── crack.py
│   ├── dictionary.txt
│   └── passwords.txt
├── crack_zip
│   ├── crack_zip.py
│   ├── password-reference.txt
│   ├── target-archive-aescrypto.zip
│   └── target-archive-zipcrypto.zip
├── docs
│   └── USAGE.md
├── encrypt_sample.py
├── ftp_banner_grabber
│   ├── ftp_banner_grabber.py
│   └── vuln_banners.txt
├── poetry.lock
├── port_scanner
│   ├── __init__.py
│   └── portscanner.py
├── pyproject.toml
├── rc4_bruteforce
│   ├── rc4_bruteforce.py
│   └── sample_rc4_encrypted.txt
├── requirements-dev.txt
├── requirements.txt
├── ssh_botnet
│   ├── sshBrute.py
│   ├── sshBruteKey.py
│   └── ssh_botnet.py
├── usb_pcap_hid_parser.py
├── violent_python.py
├── virusshare
│   └── virusshare_md5_downloader.py
└── whois_query
    └── whois_lookup.py
```

## Install

Clone the repository.
`git clone https://github.com/axi0m/violent_python`

Use pipenv or poetry to create a new virtualenv to work in and install all dependencies.
`pipenv install`
OR
`poetry install`

## Parameters

Each tool uses argparse and as such you can use `-h` to get the help menu to display.

Furthermore if you want to see examples of usage, feel free to pass the `--examples` parameter.

## Example 1: port_scanner.py

```shell
pipenv shell
port_scanner.py --help
port_scanner.py --examples
port_scanner.py --mode async --host 10.1.1.1 --ports 22, 443
port_scanner.py --mode processes --host 10.1.1.1 --ports 22, 80, 23
port_scanner.py --mode threads --host www.google.com --ports 443, 80
```

## Example 2: crack_zip.py

```shell
pipenv shell
crack_zip.py --examples
crack_zip.py --passfile passwords.txt --hashtype md5 --hashfile hashes.txt
```

## Unit Tests

Unit tests are written with pytest and only if you use `pipenv install --dev`.
Run tests after pytest is installed using the following command.
`python -m pytest tests/`
