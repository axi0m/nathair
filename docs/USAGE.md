# Usage

## Individual Tools

Each tool is in its own folder named appropriately i.e.

```
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

## Parameters

Each tool uses argparse and as such you can use `-h` to get the help menu to display.

Furthermore if you want to see examples of usage, feel free to pass the `--examples` parameter. 

## Unit Tests

Unit tests are written with `pytest` and only if you use `pipenv install --dev`.
Run tests after pytest is installed using the following command.
`python -m pytest tests/`
