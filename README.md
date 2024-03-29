[![GitHub](https://img.shields.io/github/license/axi0m/nathair?color=bright-green&style=flat-square)](https://github.com/axi0m/nathair/blob/master/LICENSE.md)
![Maintenance](https://img.shields.io/maintenance/yes/2023?style=flat-square)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/axi0m/nathair?style=flat-square)
[![Python Build with poetry](https://github.com/axi0m/nathair/actions/workflows/build-poetry.yml/badge.svg?style=flat-square)](https://github.com/axi0m/nathair/actions/workflows/build-poetry.yml)
[![Python Build with pipenv](https://github.com/axi0m/nathair/actions/workflows/build-pipenv.yml/badge.svg?style=flat-square)](https://github.com/axi0m/nathair/actions/workflows/build-pipenv.yml)
[![Python Build with pip](https://github.com/axi0m/nathair/actions/workflows/build-pip.yml/badge.svg?style=flat-square)](https://github.com/axi0m/nathair/actions/workflows/build-pip.yml)
[![flake8 lint](https://github.com/axi0m/nathair/actions/workflows/flake8-lint.yml/badge.svg?style=flat-square)](https://github.com/axi0m/nathair/actions/workflows/flake8-lint.yml)

# Nathair

Selection of various scripts inspired by TJ O'Connor's Violent Python by Syngress. The scripts tend to be targeted at specific security related needs, including:

1. Encrypted zip file dictionary cracker. **Do not use this IRL, use [Hashcat](https://hashcat.net/hashcat/).**
2. Rudimentary port scanner. **Do not use this IRL, use [Nmap](https://nmap.org/).**
3. Offline Linux password cracker (dictionary based, only supports MD5 currently). **Do not use this IRL, go over to [Hashcat](https://hashcat.net/hashcat/).**
4. SSH client/server botnet (WIP - requires rewrite to leverage paramiko)
5. Whois DB client (Requires whoisxml API key). **Use the `whois` command baked into Linux or Mac OS.**
6. MD5 hash generator for VirusShare.com malware corpus (Scrapes public hash URLs). **Use [VirusTotal](https://www.virustotal.com/gui/home/search).**

## Getting Started

Please don't use this repo for anything legitimate. You're free to copy the code, clone it, and modify it (see license).

### Prerequisites

- Minimum required versions: 3.7
- Pinned Pipenv version: 3.9
- Incompatible versions: <3.7
- git
- pip or pipenv or poetry

## Using/Installing

⚠ I expect much of this not to work. Use at your own peril.

Ensure you have the prerequisites.
Navigate to your preferred directory.

```bash
git clone https://github.com/axi0m/nathair.git
```

### Install via pipenv

```bash
pipenv install
pipenv run python <filename>.py
```

### Install via poetry

```bash
poetry install
poetry run python <filename>.py
```

### Install via pip

```bash
pip install -r requirements.txt
```

## Help with tools

```bash
python <filname>.py -h
python <filename>.py --examples
```

## Coding Style

[Black](https://github.com/psf/black) and [PEP8](https://www.python.org/dev/peps/pep-0008/)

## Deployment

I do not recommend you use this code on a live system, this was created purely to host my code as I learned more about Python.

## Built With

- [Poetry](https://python-poetry.org/) - 📦 Package management and virtual environment handling
- [Pipenv](https://pipenv.readthedocs.io/en/latest/) - 📦 Package management and virtual environment handling (Legacy)
- [VSCode](https://code.visualstudio.com/) - 🔥 IDE from Microsoft
- [LGTM](https://lgtm.com) - 🔐 Code quality and security scanning by LGTM/Semmle

## Contributing

If you want to contribute, I recommend you fork it and do with it what you will.

### Contributor Agreement

[DCO](https://developercertificate.org/)

```text


Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.


```

## Versioning

No specific versioning system/format defined/selected.

## Author(s)

[axi0m](https://github.com/axi0m)

## License

This project is licensed under MIT license - see the [LICENSE.md](https://github.com/axi0m/nathair/blob/master/LICENSE.md) file for details.

## Acknowledgements

1. Syngress for publishing the book Violent Python.
2. TJ O'Connor for writing the book and doing the hard work of coming up with all the examples and sharing his years of
knowledge with his readers.
3. All the projects mentioned in the Built With section. Almost all the code is other people's hardwork, I just cobbled it together.
