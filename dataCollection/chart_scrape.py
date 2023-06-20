import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from datetime import date


def downloadChart():
    """ function iterates over the 3 possible tracks, opens a Chrome window to the Equibase page corresponding to
    today's date, and auto-downloads the chart into the set download directory """

    trackID = ["SAR", "BEL", "AQU"]  # set possible tracks
    today = (date.today()).strftime("%m/%d/%y")

    downloadDir = f"C:\\Users\\Eagle\\Charts\\NewChart"

    # set options to auto-download the chart
    options = Options()
    options.add_experimental_option('prefs', {
        "download.default_directory": downloadDir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
                                    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    for track in trackID:
        driver.get(f"https://www.equibase.com/premium/eqbPDFChartPlus.cfm?RACE=A&BorP=P&TID={track}&CTRY=USA&"
                   f"DT={today}&DAY=D&STYLE=EQB.pdf")
        time.sleep(10)
        driver.quit()