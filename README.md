# selenium-pytest-skeleton
selenium skeleton project using the pytest test framework

## required software
Python 3.6.4
pip

## installing required packages
```bash
pip install -r requirements.txt
```

## running the tests
Default usage (runs the chromedriver for windows os in headless mode)
```bash
pytest --html=test_output/report.html -v -s src/tests
```

Specific browser and os usage (replace {browser} and replace {os} with desired parameters)
```bash
pytest --html=test_output/report.html -v -s src/tests --browser {browser} --os {os}
```
Example
```bash
pytest --html=test_output/report.html -v -s src/tests --browser firefox --os windows
```

Browser Options: chrome, chrome_headless, firefox, internet_explorer
OS Options: windows, mac, linux


