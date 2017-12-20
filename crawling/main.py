#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Get_data():
    def __init__(self, url, mode, data=None, params=None, **kwargs):
        assert mode, "invalid params"
        self.headers = {
            'Accept': 'text / html, application / xhtml + xml, application / xml',
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'zh - CN, zh',
            'Cache - Control': 'max - age = 0',
            'Connection': 'keep - alive',
            'Host': 'www.mzitu.com',
            'Referer': 'http: // www.mzitu.com / xinggan /',
            'User - Agent': 'Mozilla / 5.0',
        }
        self.url = url
        mode = mode.lower()
        if "get".__eq__(mode):
            self.response = requests.get(self.url, params=params, headers=self.headers, **kwargs)
        elif "post".__eq__(mode):
            self.response = requests.post(self.url, data=data, json=params, headers=self.headers, **kwargs)

    def get_img(self, file):
        assert file, "invalid file"
        img_list = []
        text = self.response.text
        # print("text:",text)
        soup = BeautifulSoup(text, "html.parser")
        for i in soup.find_all("img"):
            try:
                img_list.append(self._repair_url(i.get("data-original")))
            except:
                img_list.append(self._repair_url(i.get("src")))
        return img_list

    def _repair_url(self, url):
        assert url, "invalid url"
        if url.startswith("//"):
            repair_url = self.url.split("//")[0] + url
        elif url.startswith("/"):
            repair_url = urljoin(self.url, url)
        else:
            repair_url = url
        return repair_url

    def _save_file(self, file, data):
        try:
            with open(file, "wb") as f:
                f.write(data)
        except Exception as e:
            return e


if __name__ == "__main__":
    url = "http://www.mzitu.com/"
    data = Get_data(url, "GET")
    img_urls = data.get_img("abc")
    print(img_urls)
    print("数量：", len(img_urls))
