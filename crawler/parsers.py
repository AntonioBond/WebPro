#!/usr/bin/python3
import io
import re
import logging
from lxml import etree
from collections import Counter

def _count_words(words_list, words_dict):
    """
        words_list - список слов для поиска и подсчета
        words_dict - словарь {"person_id": [person_words]}
        возвращает словарь {"person_id": "person_rank"}
    """
    c = Counter(words_list)
    result = {}
    for person_id, person_words in words_dict.items():
        pr_sum = sum([c[word] for word in person_words])
        result[person_id] = pr_sum
    return result


def _extract_text(page_content):
    """
        page_content(html) -> html_text текст без тегов 
    """
    parser = etree.HTMLParser()
    html_body = etree.parse(io.BytesIO(page_content.encode()), parser)
    html_text = ' '.join([text.strip() for text in html_body.xpath('body//*/text()')])
    return html_text


def _split_text(page_text, min_len):
    """
        функция разбивает текст на слова и возвращает список со словами длинне max_len
        page_text - текст страницы
        над регуляркой можно поработать, это самая простая и вроде дает адекватный результат
    """
    return [word.lower() for word in re.split(r'\W+', page_text) if len(word) > min_len]

def parse_html(page_content, words_dict):
    """
        page_content - контент страницы
        words_dict - {"person_id":[words_list]}
        возвращает словарь {"person_id": "rank"}
    """
    min_len = 3 # минимальная длина слова которе считается словом 
    result = {}
    try:
        html_text = _extract_text(page_content)
        words_list = _split_text(html_text, min_len)
        result = _count_words(words_list, words_dict)
    except Exception as ex:
        logging.error("parsers.parse_html: error %s", ex)

    return result
