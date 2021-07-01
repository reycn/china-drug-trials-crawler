import asyncio
import re
import time

import pandas as pd
from pyppeteer import browser, launch, target
from termcolor import cprint

from lib.extract import extract_info

PARMS = {
    "headless":
    False,
    "args": [
        '--disable-infobars',  # 关闭自动化提示框
        '--log-level=30',  # 日志保存等级， 建议设置越好越好，要不然生成的日志占用的空间会很大 30为warning级别
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',  # UA
        # '--single-process',
        # '--disable-gpu',
        '--no-sandbox',  # 关闭沙盒模式
        '--start-maximized',  # 窗口最大化模式
        # '--proxy-server=127.0.0.1:1080'
        '--window-size=1680,1050',  # 窗口大小
        # '--proxy-server=http://localhost:1080'  # 代理
        # '--enable-automation'
    ],
}

JS_TEXT = """
    () =>{
        Object.defineProperties(navigator, { webdriver:{ get: () => false } });
        window.navigator.chrome = { runtime: {},  };
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins',   { get: () => [1, 2, 3, 4, 5,6], });
    }
    """

BROWSER = None


async def wait_to_click(page, selector: str):
    await page.waitForSelector(selector, timeout=5000)
    await page.click(selector)


async def wait_to_shot(page,
                       name: str = '',
                       path: str = './screenshots/') -> None:
    time.sleep(2)
    if name == '':
        name = time.strftime("%m-%d-%H-%M-%S", time.localtime())
    await page.screenshot({
        'path': path + name + '.png',
        'x': 0,
        'y': 0,
        'width': 1680,
        'height': 1050
    })


async def get_detail(trial_id: str):
    url_detail = 'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml?id='
    url_search = 'http://www.chinadrugtrials.org.cn/clinicaltrials.prosearch.dhtml'
    global BROWSER
    BROWSER = await launch(args=PARMS['args'],
                           handleSIGINT=False,
                           handleSIGTERM=False,
                           handleSIGHUP=False)
    page = await BROWSER.newPage()
    await page.evaluateOnNewDocument(JS_TEXT)  # 本页刷新后值不变，自动执行js
    await page.goto(url_search)
    await page.waitForSelector('.indexSearchInput', timeout=5000)
    await page.type('.indexSearchInput', trial_id)
    cprint(f"Searching: {trial_id}", 'white', 'on_blue')
    await wait_to_click(page, '.indexSearchBtn')
    selector_detail = 'tbody tr:nth-child(2) td:nth-child(2) a'
    try:
        await page.waitForSelector(selector_detail, timeout=5000)
        trial_id_hash = await page.evaluate(
            pageFunction=f'$("{selector_detail}")[0].getAttribute("id");')
        cprint(f'Fetching {trial_id_hash}', 'white', 'on_blue')
        await page.evaluate(
            f'getDetail($("{selector_detail}")[0].getAttribute("id"));')
        pages = await BROWSER.pages()
        await page.goto(url_detail + trial_id_hash)
        await wait_to_click(page, 'h4  a')
        page = pages[len(pages) - 1]
        # print([page.url for page in pages])
        await wait_to_shot(page)
        result = await page.content()
        await BROWSER.close()
        return (extract_info(result, trial_id, trial_id_hash))
    except:
        pass


if __name__ == '__main__':
    trial_id = 'CTR20211247'
    try:
        time_start = time.time()
        cprint('Start running...', 'white', 'on_green')
        asyncio.get_event_loop().run_until_complete(get_detail(trial_id))
        time_end = time.time()
        cprint(f"Total time: {str(time_end-time_start)[:5]}s.", 'white',
               'on_green')
    except KeyboardInterrupt as k:
        cprint('\nKey pressed to interrupt...', 'white', 'on_red')
