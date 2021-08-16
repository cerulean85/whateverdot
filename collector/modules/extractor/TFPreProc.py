from bs4 import BeautifulSoup
import re
import html5lib
from modules.extractor import TFExtractorConfig as tfg

if __name__ == "__main__":

    ccc = """
    <!-- 20150813 추가 -->
<em>[중앙일보]
</em>
<em>입력 2021.06.30 17:38
</em>
</div>
<div class="tool_area" id="changefont" style="display:none;">
<!-- 20150813 추가 -->
<a class="btn_print" href="#none" id="btnPrint">인쇄
</a>
<a class="btn_scrap" href="#none" id="btnScrap">기사 보관함(스크랩)
</a>
<button class="btn_minus" data-type="minus" type="button">글자 작게
</button>
<button class="btn_plus" data-type="plus" type="button">글자 크게
    
    """
    
    # print(ccc)
    result = re.search("입력 [0-9]{4,}.[0-9]{2,}.[0-9]{2,}", ccc).group()
    result = re.search("[0-9]{4,}.[0-9]{2,}.[0-9]{2,}", result).group()
    print(result)

class TFPreProc:

    def create_dom(self, filename):
        f = open(filename, 'rb')
        html = f.read()
        f.close()

        html = html.decode('utf-8')
        html = re.sub('<', '\n<', html)
        # html = re.sub('(<!--)[\sa-zA-Z0-9-{>}]+', '', html)
        soup = BeautifulSoup(html, "html.parser")

        # 중앙일보 날짜 추출
        # date = re.search("입력 [0-9]{4,}.[0-9]{2,}.[0-9]{2,}", str(soup)).group()
        # date = re.search("[0-9]{4,}.[0-9]{2,}.[0-9]{2,}", date).group()
        # date = date.replace('.', '')
        #####

        # 동아일보 날짜 추출
        # date = re.search("입력 [0-9]{4,}-[0-9]{2,}-[0-9]{2,}", str(soup)).group()
        # date = re.search("[0-9]{4,}-[0-9]{2,}-[0-9]{2,}", date).group()
        # date = date.replace('-', '')
        #####

        # for script in soup(tfg.PRE_PROC_TAG_LIST):
        #     script.decompose()

        return html5lib.parse(str(soup)), soup.get_text()

    def replace_words_prev(self, text):
        for r_word in tfg.PRE_PROC_REPLACE_DICT.items():
            text = text.replace(r_word[0], r_word[1])
        return text

    def replace_words_post(self, text):
        for r_word in tfg.POST_PROC_REPLACE_DICT.items():
            text = text.replace(r_word[0], r_word[1])
        return text

    def clean_stopwords(self, text):
        for stopword in tfg.PRE_PROC_STOPWORD_DICT.items():
            from_word, to_word = stopword[0], stopword[1]
            try:
                # print("from_word, to_word: {}, {}".format(from_word, to_word))
                # pattern = re.compile(r'' + from_word)
                text = re.sub(from_word, to_word, text)
            except Exception as e:
                print(e)
        return text

    def evil_text(self, text):

        for etxt in tfg.PRE_PROC_EVIL_TEXT:
            if etxt in text:
                return True

        return False



