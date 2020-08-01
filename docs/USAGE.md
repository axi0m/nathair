# Usage

This is a guide to using each tool in the repository.

## Individual Tools

Each tool is in its own folder named appropriately i.e.

```txt
violent_python
  -- crack_zip
    --- crack_zip.py
  -- port_scanner
    --- portscanner.py
  -- ftp_banner_grabber
    --- ftp_banner_grabber.py
  -- crack
    --- crack.py
  -- ssh_botnet
    --- sshBrute.py
    --- sshBruteKey.py
    --- ssh_botnet.py
...
```

## Install

Pull the repository down.
`git pull https://github.com/axi0m/violent_python`

Use `pipenv` to create a new virtualenv to work in and install all dependencies.
`pipenv install`

## Parameters

Each tool uses argparse and as such you can use `-h` to get the help menu to display.

Furthermore if you want to see examples of usage, feel free to pass the `--examples` parameter.

## Example 1: port_scanner.py

## Example 2: crack_zip.py



## Unit Tests

Unit tests are written with `pytest` and only if you use `pipenv install --dev`.
Run tests after pytest is installed using the following command.
`python -m pytest tests/`
