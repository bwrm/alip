from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.views.generic.base import TemplateView, ContextMixin, View, TemplateResponseMixin
import requests
from django.http import HttpResponse
from bs4 import BeautifulSoup
import html.parser
from lxml.etree import fromstring
import string

class DelLetter:
  # delete all symbols except digits
  def __init__(self, keep=string.digits):
    self.comp = dict((ord(c),c) for c in keep)
  def __getitem__(self, k):
    return self.comp.get(k)

class ParcerView(TemplateView):
    template_name = 'edg/parcer.html'

    def find_price(self, country, id_tag, val):
        value = []
        links = []
        if country == "pl":
            url = "http://www.ikea.com/pl/pl/catalog/products/"
        elif country == "lt":
            url = "http://www.ikea.com/lt/lt/catalog/products/"
        else:
            return None
        DD = DelLetter()
        art = self.request.GET.get('articles', None)
        try:
            art = art.split('\r\n')
            for a in art:
                link = url + a + '/'
                page = requests.get(link).text
                soup = BeautifulSoup(page, 'html.parser')
                try:
                    price_str = soup.find(id=id_tag).get_text()
                    price_str = price_str.replace(',','.')
                    price_str = ''.join([c for c in price_str if c in '1234567890.'])
                    # price_str = int(price_str.translate(DD))
                    links.append(a)
                    value.append(price_str)
                    #delete all symbols except digits
                except:
                    value.append('No item')
        except:
            return None
        if val == 1:
            return value
        elif val == 2:
            return links

    def find_text(self, url, id_tag):
        value = []
        art = self.request.GET.get('articles', None)
        try:
            art = art.split('\r\n')
            for a in art:
                link = url + a + '/'
                page = requests.get(link).text
                soup = BeautifulSoup(page, 'html.parser')
                try:
                    price_str = soup.find(id=id_tag).get_text()
                    value.append(price_str)
                except:
                    value.append('No item')
        except:
            return None
        return value

    #this method search stock available on set country LT or PL
    def find_available(self, country):
        ans = []
        if country == "pl":
            coun = "http://www.ikea.com/pl/pl/iows/catalog/availability/"
            path = './/*[@buCode="307"]/stock/availableStock'
        elif country == "lt":
            coun = "http://www.ikea.com/lt/lt/iows/catalog/availability/"
            path = "availability/localStore/stock/availableStock"
        else:
            return None
        DD = DelLetter()
        art = self.request.GET.get('articles', None)
        try:
            art = art.split('\r\n')
            for prod in art:
                url = coun+prod
                headers = {'Host': 'www.ikea.com',
                           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
                           'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                           'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
                           'X-Requested-With': 'XMLHttpRequest', 'X-Prototype-Version': '1.7',
                           'Referer': 'http://www.ikea.com/ru/ru/catalog/availability/'+prod,
                           'Cookie': 's_pers=%20s_ev44%3D%255B%255B%2527Direct%2520Load%2527%252C%25271488778649163%2527%255D%252C%255B%2527Referrers%2527%252C%25271489924509726%2527%255D%252C%255B%2527Direct%2520Load%2527%252C%25271500799939251%2527%255D%252C%255B%2527Referrers%2527%252C%25271501047359855%2527%255D%252C%255B%2527Direct%2520Load%2527%252C%25271501096860080%2527%255D%252C%255B%2527Referrers%2527%252C%25271501134603043%2527%255D%255D%7C1658901003043%3B%20gpv_p51%3Dproduct%2520information%2520page%253Eprodview%7C1501136876450%3B%20s_fid%3D0FBCA9481C6527E6-0CDBF51BE73C9793%7C1658901559626%3B%20s_lv%3D1501135159637%7C1595743159637%3B%20s_lv_s%3DLess%2520than%25201%2520day%7C1501136959637%3B%20s_nr%3D1501135159643-Repeat%7C1503727159643%3B%20cm_dl%3D1%7C1501136959646%3B%20gpv_p5%3Dno%2520value%7C1501136959654%3B; s_vi=[CS]v1|2C5E7ACC851D0DA4-4000014320011479[CE]; utag_main=v_id:015aa21f66ab00132d19103695b30604c001a00900718$_sn:17$_ss:0$_st:1501136918845$ses_id:1501132932383%3Bexp-session$_pn:21%3Bexp-session; WC_PERSISTENT=CMH96Tho06Gob5kf2QeXSAvOiEs%3D%0A%3B2017-07-27+05%3A25%3A52.278_1488778656314-2172314_19_2101526216%2C-27%2CPLN%2C2017-07-24+12%3A55%3A37.206_23_2100428620%2C-31%2CRUB%2C2017-07-23+08%3A55%3A33.918_12_-1002%2C-1%2CUSD%2C2017-03-06+05%3A37%3A36.638_19; user_accept_cookie_us=true; user_info_12=notloggedin; user_info_23=U2lhcmhlaSUzQiUzQiUzQiUzQiUzQg==; _ga=GA1.2.376243443.1488867157; jv_visits_count_C0ntYNMi8D=5; MiniPriceFilter=7; MaxPriceFilter=80; user_accept_cookie_lt=true; user_info_50=notloggedin; selected_store_num_ru_RU=464; eaesssn=cb56949f24280000c16374593a010000be5d0200; device=desktop; s_sess=%20s_ria%3Dflash%252026%257C%3B%20icamp%3Ditl%257Cru%257Ctop_links%257C201507201030208972_3%3B%20omtrpfm%3Dinternal%2520campaign%3B%20s_sq%3D%3B%20s_cc%3Dtrue%3B%20c_m%3Dundefined127.0.0.1%253A8000127.0.0.1%253A8000%3B%20s_ppv%3D-%252C60%252C59%252C1148%3B; surveySessionCookie=survey-session; _ym_uid=1500799941447551330; RT="sl=3&ss=1501135048379&tt=5713&obo=0&sh=1501135073911%3D3%3A0%3A5713%2C1501135060267%3D2%3A0%3A3937%2C1501135051023%3D1%3A0%3A2130&dm=ikea.com&si=cdc198e6-f3a2-4084-9990-521d69041edc&bcn=%2F%2F36c3f6db.mpstat.us%2F"; jv_enter_ts_C0ntYNMi8D=1500799944839; jv_utm_C0ntYNMi8D=; jv_pages_count_C0ntYNMi8D=2; WC_SESSION_ESTABLISHED=true; WC_ACTIVEPOINTER=-27%2C50; WC_USERACTIVITY_2100428620=2100428620%2C23%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CpOLi5uNKqZ5UrwWj5UlQDetY7Rs4QJwVsDQnewqA0xoszCDsbOouuy5GBcihHSeVXcWZ2i6OScZVXDUmJTVoSF7yHOUdKWCNgfdGEv5DAJJzSWZr2%2BwwSYF68zbDEdPF72M47hnv%2BCrhdWscEFH%2FzU6DMadKLWBuHm3gmCNEChGC2pwH%2BxBKsXdwEZwDgBBd7rEIck8rhOFZo8l%2FcY%2Fybw%3D%3D; selected_store_ru_RU=335; lastVisitedUrl=http%3A//www.ikea.com/pl/pl/catalog/categories/departments/bedroom/; _ceg.s=otqj8j; _ceg.u=otqj8j; __gfp_64b=sKdxQ_.S1fnkDpui4hmtSHNa_THkTEbpcSXrG84snbL.e7; WC_USERACTIVITY_2101526216=2101526216%2C19%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C2xqjV8O1SBVjriKJbeuXBPKpM%2BE7APx3w5jX9hZsOveRlfccqK0qOlO4vlQdY9Unb8%2FC1wLnchy2w0dqb1ad5HL3vjUQPxYTIp9snovWlq1onVHPhJJgILxz9rPy%2BlZFZp%2Fln2UhxiWCK32%2BigbShO3u4NCEncM6kYafz1QArRbzwTE3V6CCOSIivyU4Swq55Yl%2BWu9qPXW0vvW1ccmsfg%3D%3D; user_accept_cookie_pl=true; selected_store_num_lt_LT=235; selected_store_num_pl_PL=307; _ym_isad=2; _gid=GA1.2.276395513.1501132939; WC_USERACTIVITY_-1002=-1002%2C50%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CmXIwEawmhfAFWH9mpoAyFD2fhJqR7iRkaN2oP6ZUw3bOQhsvo9JCfnjdW109Zixw27iatX%2FzwunDXSAJU76oXS57mhvMYsFECX9hkWbhRNH5onMZRerOTghdT%2BloZ39%2FrnnTBn3HGoOwAvEF2UgI8qZohu6fzSXvsA5GEURQOWlSdmIE0wQKp5TUMuKZ879Qu0d20B%2BS2rsHixuRor017A%3D%3D; WC_GENERIC_ACTIVITYDATA=[27764621510%3Atrue%3Afalse%3A0%3AtTkUgmf9jeomJs5fxpdulkDK3Cs%3D][com.ibm.commerce.context.audit.AuditContext|null][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|-73%26EUR%26-73%26EUR][com.ibm.commerce.catalog.businesscontext.CatalogContext|null%26null%26false%26false%26false][com.ibm.commerce.context.base.BaseContext|50%26-1002%26-1002%26-1][com.ibm.commerce.context.entitlement.EntitlementContext|15304%2615304%26null%26-2000%26null%26null%26null]; selected_store_pl_PL=307; mmapi.store.p.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%22pd%22%3A%221532668931528%7C%5C%222106451795%7CAQAAAApVAgCUYNByFA8AAREAAUIsSqFBAQCXyxFvr9TUSJfLEW%2Bv1NRIAAAAAP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FAAx3d3cuaWtlYS5jb20CFA8BAAAAAAAAAAAA%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FAAAAAAAAAAFF%5C%22%22%2C%22srv%22%3A%221532668931534%7C%5C%22fravwcgeu12%5C%22%22%7D%7D; mmapi.store.s.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%7D%7D; IRWStats.trailingTag=IRWStats.stockCheckPerformed%2Cyes%7CIRWStats.stockCheckPerformed%2Cyes%7CIRWStats.stockCheckPerformed%2Cyes%7CIRWStats.stockCheckPerformed%2Cyes%7CIRWStats.stockCheckPerformed%2Cyes%7C',
                           'DNT': '1',
                           'Connection': 'keep-alive',
                           }

                page = requests.get(url, params=None, headers=headers).content
                # soup = BeautifulSoup(page, 'lxml').text
                tree = fromstring(page)
                answer = tree.find(path)
                ans.append(answer.text)
        except:
            return None
        return ans

    def get_context_data(self, **kwargs):
        context = super(ParcerView, self).get_context_data(**kwargs)
        name = self.find_text('http://www.ikea.com/pl/pl/catalog/products/', 'name')
        type = self.find_text('http://www.ikea.com/lt/lt/catalog/products/', 'type')
        # info = self.find_text('http://www.ikea.com/lt/lt/catalog/products/', 'packageInfo2')
        price2 = self.find_price('pl', 'price1', 1)
        price3 = self.find_price('lt', 'price1', 1)
        art = self.find_price('lt', 'price1', 2)
        avail_lt = self.find_available('lt')
        avail_pl = self.find_available('pl')
        context['data'] = zip(name,type,price3,price2,avail_lt,avail_pl,art)
        return context

