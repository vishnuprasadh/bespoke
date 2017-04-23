class context:
    _categoryid =""
    _productid =""
    _url =""
    _appid = 0

    def __init__(self):
        pass

    def __init__(self,appid=1, categoryid=None,productid=None,url=None):
        self._appid = appid
        if not categoryid == None: self._categoryid = categoryid
        if not productid == None: self._productid = productid
        if not url == None: self._url = url

    @property
    def categoryId(self):
        return self._categoryid

    @categoryId.setter
    def categoryId(self,value):
        'setting'
        self._categoryid = value

    @property
    def productId(self):
        return self._productid

    @productId.setter
    def productId(self,value):
        self._productid = value


    @property
    def url(self):
        return self._url

    @url.setter
    def url(self,value):
        self._url = value

    @property
    def appId(self):
        return self._appid

