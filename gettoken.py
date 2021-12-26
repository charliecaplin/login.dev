from flask import Flask, Response, jsonify, abort, make_response,  render_template, redirect, request, send_from_directory
#from faster_than_requests import requests
import requests
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json, requests, traceback, os, lxml, re, urllib, urllib3, urllib.parse, argparse, pytz, urllib.request, time, httpx


app = Flask(__name__, static_url_path="/qrimage")

@app.route('/')
def home():
    """Landing page."""
    return render_template('FILE-HTML-LO.html')

@app.route("/api/<path:nazri>", methods=['GET', 'POST'])
def api(nazri):
    if nazri == "nazri":
        ret = "Nazri Ganteng"
        return make_response(jsonify(ret))
    elif nazri == "arti":
        twit = request.args.get("nama", "")
        link = "http://primbon.com/arti_nama.php?nama1={}&proses=+Submit%21+".format(urllib.parse.quote(twit))
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        a = soup.find('div', attrs={'id':'body','class':'width'}).text
        ret = {}
        ret["result"] = a.replace("\n","").replace("Nama:ARTI NAMA (JAWA)Berikut ini adalah kumpulan arti nama lengkap dari A-Z dalam budaya (bahasa) Jawa untuk Laki-laki (L) dan Perempuan (P).Arti Nama (L) Arti Nama (P)ARTI NAMA (ARAB / ISLAM)Berikut ini adalah kumpulan arti nama lengkap dari A-Z dalam budaya (bahasa) Arab atau bernuansa Islami untuk Laki-laki (L) dan Perempuan (P).Arti Nama (L) Arti Nama (P)Catatan: Gunakan juga aplikasi numerologi Kecocokan Nama, untuk melihat sejauh mana keselarasan nama anda dengan diri anda.","")
        return make_response(jsonify(ret))

@app.route("/crlgs/<path:q>")
def one(q):
    class BEAPI():
        def __init__(self):
            self.host = "https://beta.beapi.me"
            self.version = "1.3"
            self.http = httpx.Client(http2=True,timeout=120)
        def lineAppname(self):
            resp = self.http.get(self.host+"/lineappname").json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineAppnameRandom(self, osname):
            #["android","ios","androidlite","chromeos","desktopmac","desktopwin","iosipad"]
            params = {"osname": osname}
            resp = self.http.get(self.host+"/lineappname_random",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def linePrimary2Secondary(self, appName, authToken):
            params = {"appname": appName, "authtoken": authToken}
            resp = self.http.get(self.host+"/lineprimary2secondary",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQr(self, appName, cert=None):
            params = {"appname": appName}
            if cert: params["cert"] = cert
            resp = self.http.get(self.host+"/lineqr",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQrPincode(self, session):
            resp = self.http.get(self.host+"/lineqr/pincode/"+session).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQrAuth(self, session):
            resp = self.http.get(self.host+"/lineqr/auth/"+session).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
    if q == "ch":
        try:
            api = BEAPI()
            resultdict = {}
            qr = api.lineGetQr("CHROMEOS\t2.4.5\tChrome OS\t1")
            resultdict["qr"] = qr
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            r = requests.get(qrcode)
            file = open("/qrimage/{}.png".format(crypto), "wb")
            file.write(r.content)
            file.close()
            imagenya = "/qrimages/{}.png".format(crypto)
            baseurl = request.base_url.split("/crlgs/")[0]
            resultdict["qrimage"] = baseurl + imagenya
            return make_response(jsonify(resultdict))
        except Exception as error:
            return error
            #print ("error, contact the creator")
    elif q == "dm":
        try:
            api = BEAPI()
            resultdict = {}
            qr = api.lineGetQr("DESKTOPMAC\t7.0.3\tMAC\t10")
            resultdict["qr"] = qr
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            r = requests.get(qrcode)
            file = open("/qrimage/{}.png".format(crypto), "wb")
            file.write(r.content)
            file.close()
            imagenya = "/qrimage/{}.png".format(crypto)
            baseurl = request.base_url.split("/crlgs/")[0]
            resultdict["qrimage"] = baseurl + imagenya
            return make_response(jsonify(resultdict))
        except Exception as error:
            return error
            #print ("error, contact the creator")

@app.route("/crqr/<path:q>")
def two(q):
    class BEAPI():
        def __init__(self):
            self.host = "https://beta.beapi.me"
            self.version = "1.3"
            self.http = httpx.Client(http2=True,timeout=120)
        def lineAppname(self):
            resp = self.http.get(self.host+"/lineappname").json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineAppnameRandom(self, osname):
            #["android","ios","androidlite","chromeos","desktopmac","desktopwin","iosipad"]
            params = {"osname": osname}
            resp = self.http.get(self.host+"/lineappname_random",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def linePrimary2Secondary(self, appName, authToken):
            params = {"appname": appName, "authtoken": authToken}
            resp = self.http.get(self.host+"/lineprimary2secondary",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQr(self, appName, cert=None):
            params = {"appname": appName}
            if cert: params["cert"] = cert
            resp = self.http.get(self.host+"/lineqr",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQrPincode(self, session):
            resp = self.http.get(self.host+"/lineqr/pincode/"+session).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQrAuth(self, session):
            resp = self.http.get(self.host+"/lineqr/auth/"+session).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
    try:
        api = BEAPI()
        pincode = api.lineGetQrPincode(q)
        sys = "rm /qrimage/{}.png"
        os.system(sys)
        return make_response(jsonify(pincode))
    except Exception as error:
        return error
        #print ("error, contact the creator")

@app.route("/crlgs2/<path:q>")
def three(q):
    class BEAPI():
        def __init__(self):
            self.host = "https://beta.beapi.me"
            self.version = "1.3"
            self.http = httpx.Client(http2=True,timeout=120)
        def lineAppname(self):
            resp = self.http.get(self.host+"/lineappname").json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineAppnameRandom(self, osname):
            #["android","ios","androidlite","chromeos","desktopmac","desktopwin","iosipad"]
            params = {"osname": osname}
            resp = self.http.get(self.host+"/lineappname_random",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def linePrimary2Secondary(self, appName, authToken):
            params = {"appname": appName, "authtoken": authToken}
            resp = self.http.get(self.host+"/lineprimary2secondary",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQr(self, appName, cert=None):
            params = {"appname": appName}
            if cert: params["cert"] = cert
            resp = self.http.get(self.host+"/lineqr",params=params).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQrPincode(self, session):
            resp = self.http.get(self.host+"/lineqr/pincode/"+session).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
        def lineGetQrAuth(self, session):
            resp = self.http.get(self.host+"/lineqr/auth/"+session).json()
            if resp["status"] != 200: raise Exception (resp["reason"])
            return resp
    try:
        api = BEAPI()
        resultnya = {}
        auth = api.lineGetQrAuth(q)
        d = auth["result"]["accessToken"]
        e = auth["result"]["certificate"]
        resultnya["token"] = d
        return make_response(jsonify(resultnya))
    except Exception as error:
        return error
        #print ("error, contact the creator")

@app.route('/getqrimage/<path:path>')
def send_static_content(path):
    try:
        return send_from_directory('qrimage', path)
    except Exception as error:
        return error
        #print ("error, contact the creator")

if __name__ == "__main__":
    app.run()
