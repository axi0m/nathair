# Usage

## Individual Tools

Each tool is in its own folder named appropriately i.e.

```
violent_python
  -- zip crack
    --- crack_zip.py
  -- port_scanner
    --- portscanner.py
  -- ftp_banner_grabber
    --- ftp_banner_grabber.py
...
```

## Unit Tests

Unit tests are written with `pytest` and only if you use `pipenv install --dev`.
Run tests after pytest is installed using the following command. 
`python -m pytest tests/`
