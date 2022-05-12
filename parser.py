#!/usr/bin/python3

'''Importing core libraries'''
import csv
import requests
from bs4 import BeautifulSoup as bs

'''importing additional libraries'''
import os
from tqdm import tqdm
import datetime as dt
from multiprocessing import Pool

"""Importing project modules"""
import utils
from const import HEADERS, DOMEN

class Parser:

    __DOMEN = DOMEN
    __HEADERS = HEADERS

    def __init__(self, section: str) -> None:
        self._URL = self.__DOMEN + section + '?page='
        self._ID = 1
        self.DATA = []
        self.file_name = section[1:]


    @classmethod
    def _get_html(cls, url: str) -> str:
        """
            Return html response as text
        """
        response = requests.get(url=url, headers=cls.__HEADERS)
        return response.text


    @staticmethod
    def _get_total_pages(html: str) -> int:
        """
            Return total page of pagination
        """
        soup = bs(html, 'lxml')   
        try: 
            pages_ul = soup.find('ul', class_="pagination pagination-sm")
            last_page = pages_ul.find_all('li')[-1]
            total_page = last_page.find('a').get('href').split('=')[-1]
            return int(total_page)
        except Exception as ex:
            return 1


    def _write_to_csv(self, data: list) -> None:
        """
            Write parsed data to csv file
        """
        path = utils.create_directory()

        with open(f'{path}/{self.file_name}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Price', 'Image'])
            for item in data:
                writer.writerow([
                    item.get('ID'), 
                    item.get('Title'), 
                    item.get('Price'),
                    item.get('Image')
                    ]
                )


    def _get_page_data(self, html: str) -> None:
        """
            Get data about product
        """
        soup = bs(html, 'lxml')
        product_list = soup.find('div', 
            class_="list-view").find_all('div', 
            class_="item product_listbox oh")
        
        for product in product_list:
            try:
                title = product.find('div', class_="listbox_title oh").text
            except Exception as ex:
                title = ''
            # -----------------------------------------------------------------
            try:
                price = product.find('div', class_="listbox_price text-center")
                price = price.text
            except Exception:
                price = ''
            # -----------------------------------------------------------------
            try:
                image = self.__DOMEN + product.find('img').get('src')
            except Exception as ex:
                image = ''
            data = dict(ID=self._ID,
                        Title=title.strip(), 
                        Price=price.strip(), 
                        Image=image, 
                    )
            self.DATA.append(data)
            self._ID += 1


    def _fast_parse(self, link: str) -> None:
        """
            Function for multiproceesing 
        """
        html = self._get_html(url=link)
        self._get_page_data(html=html)

    @classmethod
    def create_new_instance(cls, section):
        return cls(section) 


    def main(self):
        """
            Main function is activate all functions
        """
        html = self._get_html(url=self._URL)
        last_page = self._get_total_pages(html=html)
        for i in tqdm(range(1, last_page+1)):
            new_url = self._URL + str(i)
            with Pool(processes=os.cpu_count()) as p:
                self._fast_parse(new_url)
        self._write_to_csv(data=self.DATA)
        utils.send_message(self.DATA)




