# Project Goal
Automatically download new releases of APKs and apply a custom patch to them.

## Status
What works:
- Watching for app updates
- Download newest app version

# Setup / Installation
This needs a webdriver to work, for example chromium:
https://sites.google.com/a/chromium.org/chromedriver/downloads
Store it under the name "webdriver" in the root folder
Please add the folder to your path so that Selenium can find the webdriver
PATH=$PATH:/path/to/here

To remove popups that could distract Selenium an Adblock .crx extension is needed.

Extension download:
https://www.crx4chrome.com/extensions/cgbcahbpdhpcegmbfconppldiemgcoii/

Place it under extension/ as adblock.crx

# Usage:
Create a listener by passing it the URL to an APKMirror RSS feed and the download method as a callback. Only feeds to specific Variants work (e.g. Android 8+ or Android 7+, not just Android).
