[![GitHub](https://img.shields.io/github/license/axi0m/violent_python?color=bright-green&style=flat-square)](https://github.com/axi0m/violent_python/blob/master/LICENSE.md)
![Maintenance](https://img.shields.io/maintenance/yes/2021?style=flat-square)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/axi0m/violent_python.svg?logo=lgtm&logoWidth=18&style=flat-square)](https://lgtm.com/projects/g/axi0m/violent_python/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/axi0m/violent_python.svg?logo=lgtm&logoWidth=18&style=flat-square)](https://lgtm.com/projects/g/axi0m/violent_python/context:python)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Updates](https://pyup.io/repos/github/axi0m/violent_python/shield.svg)](https://pyup.io/repos/github/axi0m/violent_python/)
[![Python 3](https://pyup.io/repos/github/axi0m/violent_python/python-3-shield.svg)](https://pyup.io/repos/github/axi0m/violent_python/)
[![Reviewed By Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg?style=flat-square)](https://houndci.com)
[![Python application](https://github.com/axi0m/violent_python/workflows/Python%20application/badge.svg?branch=master)](https://github.com/axi0m/violent_python/actions)

# Violent Python

Selection of various scripts from TJ O'Connor's Violent Python by Syngress. The scripts tend to be targeted at specific security related needs, including:

1. Dictionary attack based zip file cracker
2. Rudimentary vulnerability scanner
3. Offline Linux password cracker (dictionary based)
4. SSH Botnet

## Getting Started

Please don't use this repo for anything legitimate. You're free to copy the code, clone it, and modify it (see license)
but I'd rather you buy TJ O'Connor's book and do the exercises/projects yourself.

However, if you decide you want to use the code, you're welcome to do so, and you're even welcome to submit PR's and issues, just do not expect a ton of support as this is just side project work I use to learn and improve my security and Python skills.

### Prerequisites

- Python 3.6+
- git
- pipenv (if you want to use the pip lock file)

### Dependency Graph 05/02/2021

```shell
colorama==0.4.4
cryptography==3.4.6
  - cffi [required: >=1.12, installed: 1.14.5]
    - pycparser [required: Any, installed: 2.20]
numpy==1.20.1
pexpect==4.8.0
  - ptyprocess [required: >=0.5, installed: 0.7.0]
pyzipper==0.3.4
  - pycryptodomex [required: Any, installed: 3.10.1]
requests-html==0.10.0
  - bs4 [required: Any, installed: 0.0.1]
    - beautifulsoup4 [required: Any, installed: 4.9.3]
      - soupsieve [required: >1.2, installed: 2.2.1]
  - fake-useragent [required: Any, installed: 0.1.11]
  - parse [required: Any, installed: 1.19.0]
  - pyppeteer [required: >=0.0.14, installed: 0.2.5]
    - appdirs [required: >=1.4.3,<2.0.0, installed: 1.4.4]
    - pyee [required: >=8.1.0,<9.0.0, installed: 8.1.0]
    - tqdm [required: >=4.42.1,<5.0.0, installed: 4.57.0]
    - urllib3 [required: >=1.25.8,<2.0.0, installed: 1.26.4]
    - websockets [required: >=8.1,<9.0, installed: 8.1]
  - pyquery [required: Any, installed: 1.4.3]
    - cssselect [required: >0.7.9, installed: 1.1.0]
    - lxml [required: >=2.1, installed: 4.6.3]
  - requests [required: Any, installed: 2.25.1]
    - certifi [required: >=2017.4.17, installed: 2020.12.5]
    - chardet [required: >=3.0.2,<5, installed: 4.0.0]
    - idna [required: >=2.5,<3, installed: 2.10]
    - urllib3 [required: >=1.21.1,<1.27, installed: 1.26.4]
  - w3lib [required: Any, installed: 1.22.0]
    - six [required: >=1.4.1, installed: 1.15.0]
  ```

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

## Testing

```bash
pipenv install --dev
python -m pytest
```

### Testing Coverage

```bash
pipenv install --dev
python -m pytest --cov
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
- [Hound](https://houndci.com) - 🔐 Additional static security analyzer

## Contributing

If you want to contribute, I recommend you fork it and do with it what you will. I'm not looking at this time to accept contributions, I'm just expanding the code as I learn Python and add new security tooling I find useful.

## Versioning

No specific versioning system/format defined/selected.

## Author(s)

axi0m

## License

This project is licensed under MIT license - see the [LICENSE.md](https://github.com/axi0m/violent_python/blob/master/LICENSE.md) file for details.

## Acknowledgements

1. Syngress for publishing the book Violent Python
2. TJ O'Connor for writing the book and doing the hard work of coming up with all the examples and sharing his years of
knowledge with his readers.
3. All the projects mentioned in the Built With section. Almost all the code is other people's hardwork, I just cobbled it together.
