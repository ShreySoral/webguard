import datetime as dt
import json
import os
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

def normalize_url(value):
    value = value.strip()
    if not value:
        raise ValueError('Please provide a website URL.')
    if '://' not in value:
        value = 'https://' + value
    parsed = urlparse(value)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Only valid HTTP(S) website URLs are supported.')
    return value

def check_site(url, max_links=20):
    url = normalize_url(url)
    DATA.mkdir(parents=True, exist_ok=True)
    result = {'requested_url': url, 'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'status': 'FAIL', 'title': '', 'final_url': '', 'http_status': None,
              'load_seconds': None, 'links_checked': 0, 'broken_links': [],
              'screenshot': None, 'error': None}
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1440,900')
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(35)
        started = time.perf_counter()
        driver.get(url)
        result['load_seconds'] = round(time.perf_counter() - started, 2)
        result['title'] = driver.title
        result['final_url'] = driver.current_url
        driver.save_screenshot(str(DATA / 'latest.png'))
        result['screenshot'] = 'data/latest.png'
        response = requests.get(result['final_url'], timeout=15, headers={'User-Agent':'WebGuard/1.0'}, stream=True)
        result['http_status'] = response.status_code
        response.close()
        hrefs = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, 'a[href]')]
        seen = set()
        for href in hrefs:
            if result['links_checked'] >= max_links:
                break
            if not href:
                continue
            absolute = urljoin(result['final_url'], href)
            parsed = urlparse(absolute)
            if parsed.scheme not in ('http', 'https') or parsed.netloc != urlparse(result['final_url']).netloc:
                continue
            absolute = parsed._replace(fragment='').geturl()
            if absolute in seen:
                continue
            seen.add(absolute)
            result['links_checked'] += 1
            try:
                check = requests.get(absolute, timeout=10, stream=True, allow_redirects=True, headers={'User-Agent':'WebGuard/1.0'})
                status = check.status_code
                check.close()
                if status >= 400:
                    result['broken_links'].append({'url': absolute, 'status': status})
            except requests.RequestException as exc:
                result['broken_links'].append({'url': absolute, 'status': 'ERROR', 'detail': str(exc)[:180]})
        result['status'] = 'PASS' if result['http_status'] < 400 and not result['broken_links'] else 'FAIL'
    except (Exception) as exc:
        result['error'] = str(exc)[:500]
    finally:
        if driver:
            try:
                driver.quit()
            except WebDriverException:
                pass
    return result

def save_result(result):
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / 'latest.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    history_path = DATA / 'history.json'
    try:
        history = json.loads(history_path.read_text(encoding='utf-8'))
        if not isinstance(history, list):
            history = []
    except (OSError, json.JSONDecodeError):
        history = []
    history.insert(0, {k: result.get(k) for k in ('requested_url','checked_at','status','http_status','load_seconds','links_checked')})
    history_path.write_text(json.dumps(history[:30], indent=2), encoding='utf-8')
