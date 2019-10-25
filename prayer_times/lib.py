from suds import Client
import logging

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
            # hijri_short=namazvakti['HicriKisa'],
            gregorian=namazvakti['MiladiUzun'],
            # gregorian_short=namazvakti['MiladiKisa'],
            # kiblah_time=namazvakti['KibleSaati'],
            # moon=namazvakti['Moon']

        )

    def __init__(self):
        super(DiyanetApiV1, self).__init__()

    def daily(self, nid):
        raw_response = self.__api.gunluk(nid)
        response = self.adapter(raw_response)
        return response

    def weekly(self, nid):
        result = self.__api.haftalik(nid)
        return  dict(data=list(map(self.adapter, result['data'])))

    def monthly(self, nid):
        result = self.__api.aylik(nid)
        return  dict(data=list(map(self.adapter, result['data'])))

    def countries(self):
        return self.__api.ulkeler()

    def cities(self, country_id):
        return self.__api.sehirler(country_id)

    def counties(self, city_id):
        return self.__api.ilceler(city_id)

    def county_detail(self, county_id):
        return self.__api.ilcedetay(county_id)

    def county_daily(self, county_id):
        return self.__api.gunluk_sehir(county_id)


api = DiyanetApiV1()
