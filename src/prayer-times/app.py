#!/usr/bin/env python
# coding: utf-8

import bottle
from bottle import route
from suds.client import Client

db = dict(
    istanbul=9541,
    ankara=9206,
    bursa=9335,
    erzurum=9541,
    eskisehir=9471,
    gaziantep=9479,
    izmir=9560,
    kayseri=9620,
    konya=9676,
    sakarya=9807,
    tekirdag=9879,
)

class Api(object):
    client = Client('http://namazvakti.diyanet.gov.tr/wsNamazVakti.svc?wsdl')
    # client.service.GunlukNamazVakti(9541, "namazuser", "NamVak!14")
    service = client.service
    # ssnns = ('ssn', 'http://namespaces/sessionid')
    # ssn = Element('SOAP:Action', ns=ssnns).setText('123')
    # client.set_options(soapheaders=sn)
    auth = dict(username="namazuser", password="NamVak!14")

    def ulkeler(self):
        return self.service.Ulkeler(**self.auth)['Ulke']

    def sehirler(self, ulkeid):
        return self.service.Sehirler(ulkeid, **self.auth)['Sehir']

    def ilceler(self, sehirid):
        return self.service.Ilceler(sehirid, **self.auth)['Ilce']

    def aylik(self, ilceid):
        return self.service.AylikNamazVakti(ilceid, **self.auth)[0]

    def haftalik(self, ilceid):
        return self.service.HaftalikNamazVakti(ilceid, **self.auth)[0]

    def gunluk(self, ilceid):
        return self.service.GunlukNamazVakti(ilceid, **self.auth)[0][0]

    def gunluk_sehir(self, sehiradi):
        return self.service.GunlukNamazVakti_SehirAdinaGore(sehiradi,
                                                            **self.auth)

    def bayram(self, ilceid):
        return dict(self.service.BayramNamaziVakti(ilceid, **self.auth))

    def bayram_tum(self, sehirid):
        return dict(self.service.BayramNamaziVaktiIlceListesi(sehirid, **self.auth))

    def imsakiye(self, ilceid):
        return self.service.Imsakiye(ilceid, **self.auth)[0]

    def ilcedetay(self, ilceid):
        return self.service.IlceBilgisiDetay2(ilceid, **self.auth)[1]

        # // return Api.Ulkeler;
        # //return Api.Sehirler(ulkeID: 2);
        # //return Api.Ilceler(sehirID: 539);
        #
        # //return Api.Aylik(9541);
        # //return Api.Haftalik(9541);
        #
        # //return Api.Gunluk(9541);
        # //return Api.BayramNamazi(9541);
        # //return Api.IlceDetay(9541);
        # return Api.BayramNamaziSehir(539);
        # //return Api.Imsakiye(9541);

class DiyanetApi(Api):
    def __init__(self):
        super(DiyanetApi, self).__init__()

    def vakit_parser(self, namazvakti):
        return dict(
            Imsak=namazvakti['Imsak'],
            Gunes=namazvakti['Gunes'],
            Ogle=namazvakti['Ogle'],
            Ikindi=namazvakti['Ikindi'],
            Aksam=namazvakti['Aksam'],
            Yatsi=namazvakti['Yatsi'],
            Moon=namazvakti['AyinSekliURL'],
            KibleSaati=namazvakti['KibleSaati'],
            HicriKisa=namazvakti['HicriTarihKisa'],
            HicriUzun=namazvakti['HicriTarihUzun'],
            MiladiKisa=namazvakti['MiladiTarihKisa'],
            MiladiUzun=namazvakti['MiladiTarihUzun'])

    def ulkeler(self):
        data = []
        for _ in super(DiyanetApi, self).ulkeler():
            data.append(dict(Id=_['UlkeID'], Ad=_['UlkeAdi']))

        return dict(data=data)

    def sehirler(self, ulkeid):
        data = []
        for _ in super(DiyanetApi, self).sehirler(ulkeid):
            data.append(dict(Id=_['SehirID'], Ad=_['SehirAdi']))

        return dict(data=data)

    def ilceler(self, sehirid):
        data = []
        for _ in super(DiyanetApi, self).ilceler(sehirid):
            data.append(dict(Id=_['IlceID'], Ad=_['IlceAdi']))

        return dict(data=data)

    def haftalik(self, ilceid):
        data = []
        for _ in super(DiyanetApi, self).haftalik(ilceid):
            data.append(self.vakit_parser(_))

        return dict(data=data)

    def aylik(self, ilceid):
        data = []
        for _ in super(DiyanetApi, self).aylik(ilceid):
            data.append(self.vakit_parser(_))

        return dict(data=data)

    def imsakiye(self, ilceid):
        data = []
        for _ in super(DiyanetApi, self).imsakiye(ilceid):
            data.append(self.vakit_parser(_))

        return dict(data=data)

    def gunluk(self, ilceid):
        return self.vakit_parser(super(DiyanetApi, self).gunluk(ilceid))

class DiyanetApiV1(object):
    __api = DiyanetApi()

    @staticmethod
    def adapter(namazvakti):
        return dict(
            fajr=namazvakti['Imsak'],
            sunrise=namazvakti['Gunes'],
            dhuhr=namazvakti['Ogle'],
            asr=namazvakti['Ikindi'],
            maghrib=namazvakti['Aksam'],
            isha=namazvakti['Yatsi'],
            hijri=namazvakti['HicriUzun'],
        )

    def __init__(self):
        super(DiyanetApiV1, self).__init__()

    def daily(self, nid):
        return self.adapter(self.__api.gunluk(nid))

    def name(self, nid):
        detay = self.__api.ilcedetay(nid)
        return detay


api = DiyanetApiV1()


@route('/api/<nid:int>')
def index(nid):
    return api.daily(nid)


# @route('/api/istanbul')
# def index():
#     return api.daily(9541)


@route('/api/<name:re:[a-z]+>')
def index(name):
    return api.daily(nid=db.get(name))


# @route('/api/<name:re:[a-z]+>/info')
# def index(name):
#     return api.name(nid=db.get(name))


if __name__ == '__main__':
    # print(api.ulkeler())
    bottle.run(host='0.0.0.0', port=8080, debug=False, reloader=False)

app = bottle.default_app()


