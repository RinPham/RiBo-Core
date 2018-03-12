from shinobi_api.services.base import BaseService
from html.parser import HTMLParser
import re
from html import unescape
from lxml import etree
from bs4 import BeautifulSoup
import hashlib
import cv2
from shinobi_api.models.page import Page
from mongoengine.queryset.visitor import Q
from django.conf import settings

interesting_normal = re.compile('[&<]')
incomplete = re.compile('&[a-zA-Z#]')

entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')

starttagopen = re.compile('<[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile(r'--\s*>')

class PageService(BaseService):

    # reduce text in html
    def reduceTextHTML(html):
        parserHTML = MyHTMLParser()
        soup = BeautifulSoup(html, 'html.parser')
        root = etree.HTML(str(soup))
        for child in root.iter("*"):
            child.text = None
            attrs = child.attrib
            for key in attrs.keys():
                # child.set(key,"")
                etree.strip_attributes(child, key)
        html1 = str(etree.tostring(root, pretty_print=True, method="html"))
        parserHTML.feed(html1)
        temp = 0
        for o in parserHTML.result:
            html1 = html1[:o[0] - temp] + html1[o[1] - temp:]
            temp += o[1] - o[0]
        return html1

    # get number of leaves node in html
    def countLeavesNode(html):
        count = 0
        soup = BeautifulSoup(html, 'html.parser')
        root = etree.HTML(str(soup))
        body = root.getchildren()[1]
        for child in body.iter("*"):
            if not child.getchildren():
                count += 1
        return count

    # get max depth value
    def getMaxDepthTree(html):
        maxDepth = 0
        d = 0
        soup = BeautifulSoup(html, 'html.parser')
        root = etree.HTML(str(soup))
        body = root.getchildren()[1]
        for child in body.iter("*"):
            d = PageService.depth(child)
            if d > maxDepth:
                maxDepth = d
        return maxDepth

    def depth(node):
        d = 0
        n = node
        while node is not None:
            d += 1
            node = node.getparent()
        return d

    # hash md5
    def computeMD5hash(string):
        m = hashlib.md5()
        m.update(string.encode('utf-8'))
        return m.hexdigest()

    # get histogram color value
    def getHistogramColor(file_path):
        img = cv2.imread(settings.MEDIA_URL[1:]+file_path)
        color = ('b', 'g', 'r')
        hist = []
        for i, col in enumerate(color):
            histr = cv2.calcHist([img], [i], None, [256], [0, 256])
            hist.append(histr)
        return hist

    # compare full screen of 2 pages
    def compareFullScreen(img1Path, img2Path):
        img1 = cv2.imread('{0}/{1}'.format(settings.MEDIA_ROOT, img1Path), 0)
        img2 = cv2.imread('{0}/{1}'.format(settings.MEDIA_ROOT, img2Path), 0)

        # Apply template Matching
        res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val

    # check page has exists in DB
    def checkPage(data):
        checkUrl = Q(url=data['url']) | Q(dom_origin_md5=data['dom_origin_md5'])
        if Page.objects(checkUrl).count():
            continueVar = False
            term = Q(url=data['url']) | Q(dom_origin_md5=data['dom_origin_md5']) | Q(dom_reduce_md5=data['dom_reduce_md5']) | Q(leaves_node=data['leaves_node']) | Q(max_depth=data['max_depth'])
            pages = Page.objects(term)
            print(pages.count())
            list_point = []
            if pages.count():
                for page in pages:
                    if page.dom_origin_md5 == data['dom_origin_md5']:
                        print("same dom")
                        return {
                            'page': page,
                            'warning_changed': False
                        }
                        continueVar = True
                        break
                    point = 0
                    priority = 0
                    if page.url == data['url']:
                        point += 1
                        priority += 5
                    if page.dom_reduce_md5 == data['dom_reduce_md5']:
                        point += 1
                        priority += 4
                    if page.leaves_node == data['leaves_node']:
                        point += 1
                        priority += 3
                    if page.max_depth == data['max_depth']:
                        point += 1
                        priority += 2
                    if page.histogram_color == str(data['histogram_color']):
                        point += 1
                        priority += 1
                    list_point.append((point,priority))
                if continueVar == False:
                    temp = sorted(list_point, reverse=True)[:3]
                    candidates = []

                    # detect 3 best pages in DB
                    for i, item in enumerate(list_point):
                        if item in temp:
                            candidates.append(pages[i])
                        if len(candidates) == 3:
                            break
                    # compare full screen of page
                    confidence = [0, 0, 0]
                    result = {
                        'warning_changed': False,
                    }
                    for i,candidate in enumerate(candidates):
                        confidence[i] = PageService.compareFullScreen(candidate.full_screen[-44:],data['full_screen'][-44:])
                    if len(candidates) == 3:
                        if confidence[0] < 0.8 and confidence[1] < 0.8 and confidence[2] < 0.8:
                            result['page'] = None
                            print("thay doi nhieu, len = 3")
                        elif max(confidence) < 0.95:
                            result['warning_changed'] = True
                            if confidence[0] == max(confidence):
                                result['page'] = candidates[0]
                            elif confidence[1] == max(confidence):
                                result['page'] = candidates[1]
                            else:
                                result['page'] = candidates[2]
                        else:
                            print("ko thay doi nhieu, len =3")
                            result['warning_changed'] = False
                            if confidence[0] == max(confidence):
                                result['page'] = candidates[0]
                            elif confidence[1] == max(confidence):
                                result['page'] = candidates[1]
                            else:
                                result['page'] = candidates[2]
                        return result
                    elif len(candidates) == 2:
                        if confidence[0] < 0.8 and confidence[1] < 0.8:
                            result['page'] = None
                            print("thay doi nhieu, len = 2")
                        elif max(confidence) < 0.95:
                            result['warning_changed'] = True
                            if confidence[0] == max(confidence):
                                result['page'] = candidates[0]
                            else:
                                result['page'] = candidates[1]
                        else:
                            print("ko thay doi nhieu, len =2")
                            result['warning_changed'] = False
                            if confidence[0] == max(confidence):
                                result['page'] = candidates[0]
                            else:
                                result['page'] = candidates[1]
                        return result
                    else:
                        if confidence[0] < 0.8:
                            result['page'] = None
                            print("thay doi nhieu, len = 1")
                        elif confidence[0] < 0.95:
                            result['warning_changed'] = True
                            result['page'] = candidates[0]
                        else:
                            print("ko thay doi nhieu, len =1")
                            result['warning_changed'] = False
                            result['page'] = candidates[0]
                        return result
        else:
            print("khong cung URL hoac md5")
            return {
                'page': None,
                'warning_changed': False
            }

class MyHTMLParser(HTMLParser):

    result = []

    # Override def goahead of HTMLParser
    # Internal -- handle data as far as reasonable.  May leave state
    # and data to be processed by a subsequent call.  If 'end' is
    # true, force handling all data as if followed by EOF marker.
    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            if self.convert_charrefs and not self.cdata_elem:
                j = rawdata.find('<', i)
                if j < 0:
                    # if we can't find the next <, either we are at the end
                    # or there's more text incoming.  If the latter is True,
                    # we can't pass the text to handle_data in case we have
                    # a charref cut in half at end.  Try to determine if
                    # this is the case before proceeding by looking for an
                    # & near the end and see if it's followed by a space or ;.
                    amppos = rawdata.rfind('&', max(i, n - 34))
                    if (amppos >= 0 and
                            not re.compile(r'[\s;]').search(rawdata, amppos)):
                        break  # wait till we get all the text
                    j = n
            else:
                match = self.interesting.search(rawdata, i)  # < or &
                if match:
                    j = match.start()
                else:
                    if self.cdata_elem:
                        break
                    j = n
            if i < j:
                if self.convert_charrefs and not self.cdata_elem:
                    self.result.append([i, j])
                    self.handle_data(unescape(rawdata[i:j]))
                else:
                    self.handle_data(rawdata[i:j])
            i = self.updatepos(i, j)
            if i == n: break
            startswith = rawdata.startswith
            if startswith('<', i):
                if starttagopen.match(rawdata, i):  # < + letter
                    k = self.parse_starttag(i)
                elif startswith("</", i):
                    k = self.parse_endtag(i)
                elif startswith("<!--", i):
                    k = self.parse_comment(i)
                elif startswith("<?", i):
                    k = self.parse_pi(i)
                elif startswith("<!", i):
                    k = self.parse_html_declaration(i)
                elif (i + 1) < n:
                    self.result.append([i, i + 1])
                    self.handle_data("<")
                    k = i + 1
                else:
                    break
                if k < 0:
                    if not end:
                        break
                    k = rawdata.find('>', i + 1)
                    if k < 0:
                        k = rawdata.find('<', i + 1)
                        if k < 0:
                            k = i + 1
                    else:
                        k += 1
                    if self.convert_charrefs and not self.cdata_elem:
                        self.result.append([i, k])
                        self.handle_data(unescape(rawdata[i:k]))
                    else:
                        self.result.append([i, k])
                        self.handle_data(rawdata[i:k])
                i = self.updatepos(i, k)
            elif startswith("&#", i):
                match = charref.match(rawdata, i)
                if match:
                    name = match.group()[2:-1]
                    self.handle_charref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                else:
                    if ";" in rawdata[i:]:  # bail by consuming &#
                        self.result.append([i, i + 2])
                        self.handle_data(rawdata[i:i + 2])
                        i = self.updatepos(i, i + 2)
                    break
            elif startswith('&', i):
                match = entityref.match(rawdata, i)
                if match:
                    name = match.group(1)
                    self.handle_entityref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                match = incomplete.match(rawdata, i)
                if match:
                    # match.group() will contain at least 2 chars
                    if end and match.group() == rawdata[i:]:
                        k = match.end()
                        if k <= i:
                            k = n
                        i = self.updatepos(i, i + 1)
                    # incomplete
                    break
                elif (i + 1) < n:
                    # not the end of the buffer, and can't be confused
                    # with some other construct
                    self.result.append([i, i + 1])
                    self.handle_data("&")
                    i = self.updatepos(i, i + 1)
                else:
                    break
            else:
                assert 0, "interesting.search() lied"
        # end while
        if end and i < n and not self.cdata_elem:
            if self.convert_charrefs and not self.cdata_elem:
                self.result.append([i, n])
                self.handle_data(unescape(rawdata[i:n]))
            else:
                self.result.append([i, n])
                self.handle_data(rawdata[i:n])
            i = self.updatepos(i, n)
        self.rawdata = rawdata[i:]

    # Override def parse_comment of HTMLParser
    # Internal -- parse comment, return length or -1 if not terminated
    def parse_comment(self, i, report=1):
        rawdata = self.rawdata
        if rawdata[i:i + 4] != '<!--':
            self.error('unexpected call to parse_comment()')
        match = commentclose.search(rawdata, i + 4)
        if not match:
            return -1
        if report:
            j = match.start(0)
            self.result.append([i + 4, j])
            self.handle_comment(rawdata[i + 4: j])
        return match.end(0)
