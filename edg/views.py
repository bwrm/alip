from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.views.generic.base import TemplateView, ContextMixin, View, TemplateResponseMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import requests
from django.http import HttpResponse
from bs4 import BeautifulSoup
import html.parser
from lxml.etree import fromstring
import string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests, requests.utils, pickle
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Order
from .forms import OrderForm
import json
from decimal import Decimal


class DelLetter:
  # delete all symbols except digits
  def __init__(self, keep=string.digits):
    self.comp = dict((ord(c),c) for c in keep)
  def __getitem__(self, k):
    return self.comp.get(k)

class OrderList(ListView):
    model = Order
    template_name = 'edg/order_list.html'
    context_object_name = 'order_list'

class ParcerView(CreateView):
    template_name = 'edg/parcer.html'
    model = Order
    form_class = OrderForm

    def clean_digits(self, value):
        value = value.replace(',', '.')
        value = ''.join([c for c in value if c in '1234567890.'])
        return value

    def get_page(self,a, country):
        if country == "pl":
            url = "http://www.ikea.com/pl/pl/catalog/products/"
        elif country == "lt":
            url = "http://www.ikea.com/lt/lt/catalog/products/"
        else:
            return None
        try:
            link = url + a + '/'
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'html.parser')
        except:
            soup = False
        return soup

    def find_price(self, page, id_tag, text=False):
        try:
            value = page.find(id=id_tag).get_text()
            if not text:
                value = self.clean_digits(value)
        except:
            value = 'No item'
        return value


    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.designer = self.request.user
    #     self.object.slug = slugify(unidecode(self.request.POST.get('name')))
    #     self.object.available = True
    #     myuserobj = User.objects.get(email=self.request.user)
    #     myuserobj.is_designer = True
    #     myuserobj.save()
    #     self.object.save()
    #     self.ind = Product.objects.get(slug=self.object.slug, designer=self.object.designer)
    #     self.request.session['prod_id'] = self.ind.id
    #     return super(ProductCreate, self).form_valid(form)

    #this method search stock available on set country LT or PL
    def find_available(self, art, country):
        if country == "pl":
            coun = "http://www.ikea.com/pl/pl/iows/catalog/availability/"
            path = './/*[@buCode="307"]/stock/availableStock'
        elif country == "lt":
            coun = "http://www.ikea.com/lt/lt/iows/catalog/availability/"
            path = "availability/localStore/stock/availableStock"
        else:
            return None
        try:
            url = coun+art
            headers = {'Host': 'www.ikea.com',
                       'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
                       'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                       'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
                       'X-Requested-With': 'XMLHttpRequest', 'X-Prototype-Version': '1.7',
                       'Referer': 'http://www.ikea.com/ru/ru/catalog/availability/'+art,
                       'Cookie': 's_pers=%20s_ev44%3D%255B%255B%2527Direct%2520Load%2527%252C%25271488778649163%2527%255D%252C%255B%2527Referrers%2527%252C%25271489924509726%2527%255D%252C%255B%2527Direct%2520Load%2527%252C%25271500799939251%2527%255D%252C%255B%2527Referrers%2527%252C%25271501047359855%2527%255D%252C%255B%2527Direct%2520Load%2527%252C%25271501096860080%2527%255D%252C%255B%2527Referrers%2527%252C%25271501134603043%2527%255D%255D%7C1658901003043%3B%20gpv_p51%3Dproduct%2520information%2520page%253Eprodview%7C1501136876450%3B%20s_fid%3D0FBCA9481C6527E6-0CDBF51BE73C9793%7C1658901559626%3B%20s_lv%3D1501135159637%7C1595743159637%3B%20s_lv_s%3DLess%2520than%25201%2520day%7C1501136959637%3B%20s_nr%3D1501135159643-Repeat%7C1503727159643%3B%20cm_dl%3D1%7C1501136959646%3B%20gpv_p5%3Dno%2520value%7C1501136959654%3B; s_vi=[CS]v1|2C5E7ACC851D0DA4-4000014320011479[CE]; utag_main=v_id:015aa21f66ab00132d19103695b30604c001a00900718$_sn:17$_ss:0$_st:1501136918845$ses_id:1501132932383%3Bexp-session$_pn:21%3Bexp-session; WC_PERSISTENT=CMH96Tho06Gob5kf2QeXSAvOiEs%3D%0A%3B2017-07-27+05%3A25%3A52.278_1488778656314-2172314_19_2101526216%2C-27%2CPLN%2C2017-07-24+12%3A55%3A37.206_23_2100428620%2C-31%2CRUB%2C2017-07-23+08%3A55%3A33.918_12_-1002%2C-1%2CUSD%2C2017-03-06+05%3A37%3A36.638_19; user_accept_cookie_us=true; user_info_12=notloggedin; user_info_23=U2lhcmhlaSUzQiUzQiUzQiUzQiUzQg==; _ga=GA1.2.376243443.1488867157; jv_visits_count_C0ntYNMi8D=5; MiniPriceFilter=7; MaxPriceFilter=80; user_accept_cookie_lt=true; user_info_50=notloggedin; selected_store_num_ru_RU=464; eaesssn=cb56949f24280000c16374593a010000be5d0200; device=desktop; s_sess=%20s_ria%3Dflash%252026%257C%3B%20icamp%3Ditl%257Cru%257Ctop_links%257C201507201030208972_3%3B%20omtrpfm%3Dinternal%2520campaign%3B%20s_sq%3D%3B%20s_cc%3Dtrue%3B%20c_m%3Dundefined127.0.0.1%253A8000127.0.0.1%253A8000%3B%20s_ppv%3D-%252C60%252C59%252C1148%3B; surveySessionCookie=survey-session; _ym_uid=1500799941447551330; RT="sl=3&ss=1501135048379&tt=5713&obo=0&sh=1501135073911%3D3%3A0%3A5713%2C1501135060267%3D2%3A0%3A3937%2C1501135051023%3D1%3A0%3A2130&dm=ikea.com&si=cdc198e6-f3a2-4084-9990-521d69041edc&bcn=%2F%2F36c3f6db.mpstat.us%2F"; jv_enter_ts_C0ntYNMi8D=1500799944839; jv_utm_C0ntYNMi8D=; jv_pages_count_C0ntYNMi8D=2; WC_SESSION_ESTABLISHED=true; WC_ACTIVEPOINTER=-27%2C50; WC_USERACTIVITY_2100428620=2100428620%2C23%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CpOLi5uNKqZ5UrwWj5UlQDetY7Rs4QJwVsDQnewqA0xoszCDsbOouuy5GBcihHSeVXcWZ2i6OScZVXDUmJTVoSF7yHOUdKWCNgfdGEv5DAJJzSWZr2%2BwwSYF68zbDEdPF72M47hnv%2BCrhdWscEFH%2FzU6DMadKLWBuHm3gmCNEChGC2pwH%2BxBKsXdwEZwDgBBd7rEIck8rhOFZo8l%2FcY%2Fybw%3D%3D; selected_store_ru_RU=335; lastVisitedUrl=http%3A//www.ikea.com/pl/pl/catalog/categories/departments/bedroom/; _ceg.s=otqj8j; _ceg.u=otqj8j; __gfp_64b=sKdxQ_.S1fnkDpui4hmtSHNa_THkTEbpcSXrG84snbL.e7; WC_USERACTIVITY_2101526216=2101526216%2C19%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C2xqjV8O1SBVjriKJbeuXBPKpM%2BE7APx3w5jX9hZsOveRlfccqK0qOlO4vlQdY9Unb8%2FC1wLnchy2w0dqb1ad5HL3vjUQPxYTIp9snovWlq1onVHPhJJgILxz9rPy%2BlZFZp%2Fln2UhxiWCK32%2BigbShO3u4NCEncM6kYafz1QArRbzwTE3V6CCOSIivyU4Swq55Yl%2BWu9qPXW0vvW1ccmsfg%3D%3D; user_accept_cookie_pl=true; selected_store_num_lt_LT=235; selected_store_num_pl_PL=307; _ym_isad=2; _gid=GA1.2.276395513.1501132939; WC_USERACTIVITY_-1002=-1002%2C50%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CmXIwEawmhfAFWH9mpoAyFD2fhJqR7iRkaN2oP6ZUw3bOQhsvo9JCfnjdW109Zixw27iatX%2FzwunDXSAJU76oXS57mhvMYsFECX9hkWbhRNH5onMZRerOTghdT%2BloZ39%2FrnnTBn3HGoOwAvEF2UgI8qZohu6fzSXvsA5GEURQOWlSdmIE0wQKp5TUMuKZ879Qu0d20B%2BS2rsHixuRor017A%3D%3D; WC_GENERIC_ACTIVITYDATA=[27764621510%3Atrue%3Afalse%3A0%3AtTkUgmf9jeomJs5fxpdulkDK3Cs%3D][com.ibm.commerce.context.audit.AuditContext|null][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|-73%26EUR%26-73%26EUR][com.ibm.commerce.catalog.businesscontext.CatalogContext|null%26null%26false%26false%26false][com.ibm.commerce.context.base.BaseContext|50%26-1002%26-1002%26-1][com.ibm.commerce.context.entitlement.EntitlementContext|15304%2615304%26null%26-2000%26null%26null%26null]; selected_store_pl_PL=307; mmapi.store.p.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%22pd%22%3A%221532668931528%7C%5C%222106451795%7CAQAAAApVAgCUYNByFA8AAREAAUIsSqFBAQCXyxFvr9TUSJfLEW%2Bv1NRIAAAAAP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FAAx3d3cuaWtlYS5jb20CFA8BAAAAAAAAAAAA%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FAAAAAAAAAAFF%5C%22%22%2C%22srv%22%3A%221532668931534%7C%5C%22fravwcgeu12%5C%22%22%7D%7D; mmapi.store.s.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%7D%7D; IRWStats.trailingTag=IRWStats.stockCheckPerformed%2Cyes%7CIRWStats.stockCheckPerformed%2Cyes%7CIRWStats.stockCheckPerformed%2Cyes%7CIRWStats.stockCheckPerformed%2Cyes%7CIRWStats.stockCheckPerformed%2Cyes%7C',
                       'DNT': '1',
                       'Connection': 'keep-alive',
                       }

            page = requests.get(url, params=None, headers=headers).content
            # soup = BeautifulSoup(page, 'lxml').text
            tree = fromstring(page)
            answer = tree.find(path)
            ans = answer.text
        except:
            ans = 'No item'
        return ans

    def get_context_data(self, **kwargs):
        context = super(ParcerView, self).get_context_data(**kwargs)
        name = []
        type = []
        price2 = []
        price3 = []
        article = []
        avail_lt = []
        avail_pl = []
        art = self.request.GET.get('articles', None)
        if art:
            art = art.split('\r\n')
            art = [e for e in art if e]
            for a in art:
                page_lt = self.get_page(a, 'lt')
                page_pl = self.get_page(a, 'pl')
                name.append(self.find_price(page_lt, 'name', True))
                type.append(self.find_price(page_lt, 'type', True))
                price2.append(self.find_price(page_lt, 'price1'))
                price3.append(self.find_price(page_pl, 'price1'))
                article.append(a)
                avail_lt.append(self.find_available(a, 'lt'))
                avail_pl.append(self.find_available(a, 'pl'))
            context['data'] = zip(name, type, price2, avail_lt, price3, avail_pl, article)
            context['articles'] = art
        return context


def invoce_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; ' \
                                      'filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    phone = request.POST.get('phone', None)
    amount = request.POST.get('price', None)

    p = canvas.Canvas(response)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
    p.drawString(30, 750, 'OFFICIAL COMMUNIQUE')
    p.drawString(30, 735, name)
    p.drawString(500, 750, email)
    p.drawString(600, 750, phone)
    p.line(480, 747, 580, 747)
    p.drawString(275, 725, 'AMOUNT OWED:')
    p.drawString(500, 725, amount+" EUR")
    p.line(378, 723, 580, 723)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def is_login(session):
    # loggin_check_url = "http://www.ikea.com/webapp/wcs/stores/servlet/GetUserInfo?storeId=23"
    loggin_check_url = "http://www.ikea.com/webapp/wcs/stores/servlet/GetUserInfo?storeId=19"
    with open('somefile', 'rb') as f:
        cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
    resp1 = session.post(loggin_check_url, cookies=cookies)
    res = resp1.text.find(">Y</")
    if res == -1:
        return False
    else:
        return True

def login(session):
    login_url = "https://secure.ikea.com/webapp/wcs/stores/servlet/Logon?storeId=23&langId=-31&URL=MyProfile%3FDM_PersistentCookieCreated%3Dtrue%26storeId%3D23%26isContactMethodPresent%3Dtrue%26identitySignature%3D03gsXdE%252BkCBiftGGgtQCJJkiwss%253D%26langId%3D-31%26rememberMe%3Dtrue%26previousCommand%3Dlogon&logonId=alby.sv%40gmail.com&logonPassword=vlv83g%2BxX"
    login_url_pl = "https://secure.ikea.com/webapp/wcs/stores/servlet/Logon?storeId=19&langId=-27&logonId=alby.sv%40ya.ru&logonPassword=shpeonka1&rememberMe=true&previousCommand=logon&identitySignature=03gsXdE%2BkCBiftGGgtQCJJkiwss%3D&isContactMethodPresent=true&URL=MyProfile&DM_PersistentCookieCreated=true"
    session.post(login_url_pl)
    with open('somefile', 'wb') as f:
        pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
    if is_login(session):
        return True
    else:
        return False

def add_to_list(session, item, quan=1):
    # add_to_list = "http://www.ikea.com/webapp/wcs/stores/servlet/IrwWSInterestItemAdd?partNumber="+item+"&langId=-27&storeId=19&listId=260857224&quantity="+quan
    add_to_list = "http://www.ikea.com/webapp/wcs/stores/servlet/IrwWSInterestItemAdd?partNumber="+item+"&langId=-27&storeId=19&listId=260547049&quantity="+quan
    with open('./somefile', 'rb') as f:
        cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
    r1 = session.get(add_to_list, cookies=cookies)
    res = r1.text.find("<msg>OK</msg>")
    if res == -1:
        return False
    else:
        return True

def add_to_shopping_list_view(request):
    # "127.0.0.1:8000/edg/add-to-list/?quantity=9&item=00316392"
    quan = request.GET.get('quantity', None)
    item = request.GET.get('item', None)
    session = requests.Session()
    if is_login(session):
        if add_to_list(session, item, quan):
            res = {'success': True}
        else:
            res = {'success': False}
    elif login(session):
        if add_to_list(session, item, quan):
            res = {'success': True}
        else:
            res = {'success': False}
    else:
        res = {'success': False}
    return JsonResponse(res)

def OrderAjax(request):
    res = Order.objects.all().values('id', 'name', 'price', 'email', 'is_paid', 'phone')
    # res = {'is_claimed': 'True', 'rating': '3.5'}
    # res_dict = {"total": res.count(), "rows": res}
    a = {"total": res.count(), "rows": list(res)}
    new_dlist = [str(s) for s in a]
    res_list = list(new_dlist)
    return JsonResponse(a, safe=False)

class OrderDetail(DetailView):
    template_name = 'edg/parcer.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['articles'] = ['70193321', '70193322']
        return context
