# Playwright E2E Testing Framework

![Playwright logo](/assets/playwright-python-logo.png "Playwright logo")

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Playwright](https://img.shields.io/badge/playwright-latest-green)

Demo automation testing framework created with Playwright, a NodeJS library made for browser automation. It's free, open source and backed up by Microsoft. 

Playwright supports all modern rendering engines including Chromium, WebKit, and Firefox. Test on Windows, Linux, and macOS, locally or on CI, headless or headed with native mobile emulation of Google Chrome for Android and Mobile Safari.

[Playwright Github](https://github.com/microsoft/playwright)

The goal of this repo is to rewrite the tests from [Typescript version](https://github.com/ovcharski/playwright-e2e) to Python 

# Usage

Get started by installing Playwright. You need Python and Pytest already installed.
```bash
pip install pytest-playwright
```
Install the required browsers:
```bash
playwright install
```
## Running tests

Run all the tests
```bash
pytest
```

## The most common options available in the command line

Enable headed mode:
```bash
pytest --headed
```
Increase logging verbosity for detailed test execution information:
```bash
pytest --verbose
```
Turn off all console output except errors and warnings:
```bash
pytest --quiet
```
Stop pytest immediately after encountering the first failed test, aiding in isolating issues:
```bash
pytest --exitfirst
```
Save test results as a JUnit XML file (useful for documentation or reporting):
```bash
pytest --junit-xml test-results/report.xml
```
