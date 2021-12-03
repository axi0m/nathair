[![GitHub](https://img.shields.io/github/license/axi0m/violent_python?color=bright-green&style=flat-square)](https://github.com/axi0m/violent_python/blob/master/LICENSE.md)
![Maintenance](https://img.shields.io/maintenance/yes/2021?style=flat-square)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/axi0m/violent_python.svg?logo=lgtm&logoWidth=18&style=flat-square)](https://lgtm.com/projects/g/axi0m/violent_python/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/axi0m/violent_python.svg?logo=lgtm&logoWidth=18&style=flat-square)](https://lgtm.com/projects/g/axi0m/violent_python/context:python)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Updates](https://pyup.io/repos/github/axi0m/violent_python/shield.svg?style=flat-square)](https://pyup.io/repos/github/axi0m/violent_python/)
[![Python Build with poetry](https://github.com/axi0m/violent_python/actions/workflows/build-poetry.yml/badge.svg?style=flat-square)](https://github.com/axi0m/violent_python/actions/workflows/build-poetry.yml)
[![Python Build with pipenv](https://github.com/axi0m/violent_python/actions/workflows/build-pipenv.yml/badge.svg?style=flat-square)](https://github.com/axi0m/violent_python/actions/workflows/build-pipenv.yml)
[![Python Build with pip](https://github.com/axi0m/violent_python/actions/workflows/build-pip.yml/badge.svg?style=flat-square)](https://github.com/axi0m/violent_python/actions/workflows/build-pip.yml)
[![flake8 lint](https://github.com/axi0m/violent_python/actions/workflows/flake8-lint.yml/badge.svg?style=flat-square)](https://github.com/axi0m/violent_python/actions/workflows/flake8-lint.yml)

# Violent Python

Selection of various scripts inspired by TJ O'Connor's Violent Python by Syngress. The scripts tend to be targeted at specific security related needs, including:

1. Encrypted zip file dictionary cracker
2. Rudimentary port scanner
3. Offline Linux password cracker (dictionary based, only supports MD5 currently)
4. SSH client/server botnet (Partially implemented)
5. Whois DB client (Requires whoisxml API key)
6. MD5 hash generator for VirusShare.com malware corpus (Scrapes public hash URLs)

## Getting Started

Please don't use this repo for anything legitimate. You're free to copy the code, clone it, and modify it (see license)
but I'd rather you buy TJ O'Connor's book and do the exercises/projects yourself.

However, if you decide you want to use the code, you're welcome to do so, and you're even welcome to submit PR's and issues, just do not expect a ton of support as this is just side project work I use to learn and improve my security and Python skills.

### Prerequisites

- Minimum required versions: 3.6
- Incompatible versions: 2
- git
- pipenv

## Using/Installing

⚠ I expect much of this not to work. Use at your own peril.

Ensure you have the required components.
Navigate to your preferred clone directory (/usr/local/src/ or /opt/ in Linux or wherever you want in Windows)

```bash
git clone https://github.com/axi0m/violent_python.git
```

```bash
pipenv install
python <filename>.py
```

## Help with tools

```bash
python <filname>.py -h
python <filename>.py --examples
```

## Coding Style

[Black](https://github.com/psf/black) and [PEP8](https://www.python.org/dev/peps/pep-0008/)

## Deployment

I do not recommend you use this code on a live system, this was created purely to host my code as I learned more about Python

## Built With

- [Pipenv](https://pipenv.readthedocs.io/en/latest/) - 📦 Package management and virtual environment handling
- [VSCode](https://code.visualstudio.com/) - 🔥 IDE from Microsoft
- [PyUp.io](https://pyup.io) - [ ~ Dependencies scanned by PyUp.io ~ ]
- [LGTM](https://lgtm.com) - 🔐 Code quality and security scanning by LGTM/Semmle

## Contributing

If you want to contribute, I recommend you fork it and do with it what you will. I'm not looking at this time to accept contributions, I'm just expanding the code as I learn Python and add new security tooling I find useful.

## Versioning

No specific versioning system/format defined/selected.

## Author(s)

[axi0m](https://github.com/axi0m)

## License

This project is licensed under MIT license - see the [LICENSE.md](https://github.com/axi0m/violent_python/blob/master/LICENSE.md) file for details.

## Acknowledgements

1. Syngress for publishing the book Violent Python
2. TJ O'Connor for writing the book and doing the hard work of coming up with all the examples and sharing his years of
knowledge with his readers.
3. All the projects mentioned in the Built With section. Almost all the code is other people's hardwork, I just cobbled it together.
