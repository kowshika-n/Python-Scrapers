from selenium import webdriver
import time
import sys

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_experimental_option("useAutomationExtension", False);
options.add_experimental_option("excludeSwitches", ["safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

driver = webdriver.Chrome(options=options)

MOurls = ["https://www.realtor.com/realestateandhomes-search/Worth-County_MO/", "https://www.realtor.com/realestateandhomes-search/Webster-County_MO/"]

def catch(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    lineNo = str(exc_tb.tb_lineno)
    print('Error : %s : %s at Line %s.' % (type(e), e, lineNo))


def wait_loading():
    wait_time = 0
    try:
        while driver.execute_script('return document.readyState;') != 'complete' and wait_time < 10:
            wait_time += 0.1
            time.sleep(0.1)
        print('Load Complete.')
    except Exception as e:
        pass

def LoadGoogle():
    driver.get('https://www.google.com/')
    time.sleep(2)
    wait_loading()


def GetElement(driver, elementTag, locator='ID'):
    '''Wait for element and then select when it is available'''
    try:
        if locator == 'ID':
            if is_element_present(driver, By.ID, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_id(elementTag))
            else:
                print('%s Not Found.' % elementTag)
                return None

        elif locator == 'NAME':
            if is_element_present(driver, By.NAME, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_name(elementTag))
            else:
                print('%s Not Found.' % elementTag)
                return None

        elif locator == 'XPATH':
            if is_element_present(driver, By.XPATH, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_xpath(elementTag))
            else:
                print('%s Not Found.' % elementTag)
                return None

        elif locator == 'CSS':
            if is_element_present(driver, By.CSS_SELECTOR, elementTag):
                return WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_element_by_css_selector(elementTag))
            else:
                print('%s Not Found.' % elementTag)
                return None

    except Exception as e:
        catch(e)
        return None


def ActionClick(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView();", element)
        webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
    except Exception as e:
        catch(e)


def is_element_present(driver, how, what):
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def WaitTillElementPresent(driver, elementTag, locator='ID'):
    '''Wait till element present'''
    for i in range(60):
        try:
            if locator == 'ID':
                if is_element_present(driver, By.ID, elementTag):
                    break
            elif locator == 'NAME':
                if is_element_present(driver, By.NAME, elementTag):
                    break
            elif locator == 'XPATH':
                if is_element_present(driver, By.XPATH, elementTag):
                    break
            elif locator == 'CSS':
                if is_element_present(driver, By.CSS_SELECTORS, elementTag):
                    break
        except Exception as e:
            print('Exception when WaitTillElementPresent : %s' % e)
            pass
        time.sleep(0.99)
    else:
        print("Timed out. Unable to find %s" % elementTag)


def tearDown(driver):
    try:
        driver.close()
    except Exception as e:
        pass

    try:
        driver.quit()
    except Exception as e:
        catch(e)
        pass


def getHomeURLs(urls):
    try:
        homeurls = list()
        for i in range(0, len(urls)):
            url = urls[i] + "pg-1"
            print(url)
            driver.get(url)
            wait_loading()
            time.sleep(3)
            homeurls = getDatailsInPage(driver, homeurls)
            driver.delete_all_cookies()
            j = 1
            while (GetElement(driver,"//a[@title='Go to Next Page']", "XPATH") is not None):
                LoadGoogle()
                url = urls[i] + "pg-" + str(j+1)
                print(url)
                driver.get(url)
                time.sleep(3)
                wait_loading()
                homeurls = getDatailsInPage(driver, homeurls)
                time.sleep(3)

            print(f"{homeurls}")
    except Exception as e:
        catch(e)


def getDatailsInPage(driver, homeurls):
    time.sleep(2)
    driver.execute_script("if (document.getElementsByClassName('rdc-global-footer').length >= 1){document.getElementsByClassName('rdc-global-footer')[0].scrollIntoView(false)};")
    time.sleep(2)
    links = driver.find_elements_by_xpath('//a[@href]')
    urlCount = len(links)
    print(f"URL count = {urlCount}")
    if (urlCount > 100):
        for a in links:
            if ("realestateandhomes-detail" in a.get_attribute('href')):
                homeurls.append(a.get_attribute('href'))
    print("Found " + str(len(homeurls)) + " urls in page")
    uniqueSet = set(homeurls)
    homeurls = list(uniqueSet)
    return homeurls


try:
    LoadGoogle()
    getHomeURLs(MOurls)
except Exception as e:
    catch(e)
finally:
    tearDown(driver)

