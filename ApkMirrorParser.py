import time
import os
from pathlib import Path
from logger import apkmirror_logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

download_dir = str(Path(os.path.realpath(__file__)).parent.joinpath('download'))

chrome_options = webdriver.ChromeOptions()
prefs = {}
prefs["download.prompt_for_download"] = False
prefs["download.directory_upgrade"] = True
prefs["default_content_setting_values.notifications"] = 0
prefs["content_settings.exceptions.automatic_downloads.*.setting"] = 1
prefs["safebrowsing.disable_download_protection"] = True
prefs["safebrowsing.enabled"] = False
prefs["default_content_settings.popups"] = 0
prefs["managed_default_content_settings.popups"] = 0
prefs["profile.password_manager_enabled"] = False
prefs["profile.default_content_setting_values.notifications"] = 2
prefs["profile.default_content_settings.popups"] = 0
prefs["profile.managed_default_content_settings.popups"] = 0
prefs["profile.default_content_setting_values.automatic_downloads"] = 1
prefs["download.default_directory"] = download_dir
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_extension('extensions/adblock.crx')

ADBLOCK_TIMEOUT = 20

def downloadFromApkMirror(apkmirror_page_url: str) -> str:
    apkmirror_logger.info(f'\nDownloading file from url: {apkmirror_page_url}')

    driver = webdriver.Chrome(options=chrome_options)
    params = {'behavior' : 'allow', 'downloadPath':download_dir}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

    # start download
    driver.get(apkmirror_page_url)
    download_button = driver.find_element(By.CLASS_NAME, 'downloadButton')
    ActionChains(driver).move_to_element(download_button).click(download_button).perform()

    # wait for adblock warning to disapear
    apkmirror_logger.info(f"Waiting {ADBLOCK_TIMEOUT} seconds for adblock warning to disappear...")
    time.sleep(ADBLOCK_TIMEOUT)

    apkmirror_logger.info(f"Starting download...")
    try:
        download_button.click()
    except StaleElementReferenceException:
        # download was already started because no adblock warning appeared
        pass

    # wait for download to complete
    time.sleep(5)
    while any(filename.endswith('.crdownload') for filename in os.listdir(download_dir)):
        time.sleep(3)
    driver.quit()
    apkmirror_logger.info(f"Download finished.")
