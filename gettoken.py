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

@app.route("/impossible/<path:nazri>", methods=['GET', 'POST'])
def api(nazri):
    if nazri == "nazri":
        ret = "Access Denied"
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
    if q == "ch@@":
        try:
            api = BEAPI()
            resultdict = {}
            qr = api.lineGetQr("CHROMEOS\t2.4.5\tChrome OS\t1")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                r = "cd qrimage && curl -k {} > {}.png".format(qrcode,crypto)
                os.system(r)
                url = "https://logindevz.herokuapp.com/getqrimage/{}.png".format(crypto)
                resultdict["qrimage"] = url
            except Exception as error:
                #resultdict["error"] = str(error)
                pass
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "dm@@":
        try:
            api = BEAPI()
            resultdict = {}
            qr = api.lineGetQr("DESKTOPMAC\t7.0.3\tMAC\t10")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                r = "cd qrimage && curl -k {} > {}.png".format(qrcode,crypto)
                os.system(r)
                url = "https://logindevz.herokuapp.com/getqrimage/{}.png".format(crypto)
                resultdict["qrimage"] = url
            except Exception as error:
                #resultdict["error"] = str(error)
                pass
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "ch":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["chromeos"]
                qr = api.lineGetQr(sv2)
            except:
                qr = api.lineGetQr("CHROMEOS\t2.4.9\tChrome OS\t1")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "dm":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["desktopmac"]
                qr = api.lineGetQr(sv2)
            except:
                qr = api.lineGetQr("DESKTOPMAC\t7.5.0\tMAC\t10")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "dw":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["desktopwin"]
                qr = api.lineGetQr(sv2)
            except:
                qr = api.lineGetQr("DESKTOPWIN\t7.5.0\tWindows\t10")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "io":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["ios"]
                qr = api.lineGetQr(sv2)
            except:
                qr = api.lineGetQr("IOS\t11.22.2\tIphoneX\t14")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "ip":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["iosipad"]
                qr = api.lineGetQr(sv2)
            except:
                qr = api.lineGetQr("IOSIPAD\t11.22.2\tIphoneX\t14")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "an":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["android"]
                qr = api.lineGetQr(sv2)
            except:
                qr = api.lineGetQr("ANDROID\t11.22.2\tMI10\t10")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "al":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["androidlite"]
                qr = api.lineGetQr(sv2)
            except:
                qr = api.lineGetQr("ANDROIDLITE\t2.17.1\tMI10\t10")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
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
        #pincodejson = pincode.json()
        pin = pincode["result"]["pincode"]
        #sys = "rm /qrimage/{}.png"
        #os.system(sys)
        pindict = {}
        pindict["pin"] = pin
        return make_response(jsonify(pindict))
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

@app.route("/crlgsvip/<path:q>")
def onevip(q):
    cert = request.args.get("cert", "")
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
    if q == "ch@@":
        try:
            api = BEAPI()
            resultdict = {}
            qr = api.lineGetQr("CHROMEOS\t2.4.5\tChrome OS\t1")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                r = "cd qrimage && curl -k {} > {}.png".format(qrcode,crypto)
                os.system(r)
                url = "https://logindevz.herokuapp.com/getqrimage/{}.png".format(crypto)
                resultdict["qrimage"] = url
            except Exception as error:
                #resultdict["error"] = str(error)
                pass
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "dm@@":
        try:
            api = BEAPI()
            resultdict = {}
            qr = api.lineGetQr("DESKTOPMAC\t7.0.3\tMAC\t10")
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                r = "cd qrimage && curl -k {} > {}.png".format(qrcode,crypto)
                os.system(r)
                url = "https://logindevz.herokuapp.com/getqrimage/{}.png".format(crypto)
                resultdict["qrimage"] = url
            except Exception as error:
                #resultdict["error"] = str(error)
                pass
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "ch":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["chromeos"]
                qr = api.lineGetQr(sv2,cert)
            except:
                qr = api.lineGetQr("CHROMEOS\t2.4.9\tChrome OS\t1",cert)
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "dm":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["desktopmac"]
                qr = api.lineGetQr(sv2,cert)
            except:
                qr = api.lineGetQr("DESKTOPMAC\t7.5.0\tMAC\t10",cert)
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "dw":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["desktopwin"]
                qr = api.lineGetQr(sv2,cert)
            except:
                qr = api.lineGetQr("DESKTOPWIN\t7.5.0\tWindows\t10",cert)
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "io":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["ios"]
                qr = api.lineGetQr(sv2,cert)
            except:
                qr = api.lineGetQr("IOS\t11.22.2\tIphoneX\t14",cert)
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "ip":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["iosipad"]
                qr = api.lineGetQr(sv2,cert)
            except:
                qr = api.lineGetQr("IOSIPAD\t11.22.2\tIphoneX\t14",cert)
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "an":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["android"]
                qr = api.lineGetQr(sv2,cert)
            except:
                qr = api.lineGetQr("ANDROID\t11.22.2\tMI10\t10",cert)
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")
    elif q == "al":
        try:
            api = BEAPI()
            resultdict = {}
            try:
                sv = requests.get("https://beta.beapi.me/lineappname",timeout=7)
                sv1 = sv.json()
                sv2 = sv1["result"]["androidlite"]
                qr = api.lineGetQr(sv2,cert)
            except:
                qr = api.lineGetQr("ANDROIDLITE\t2.17.1\tMI10\t10",cert)
            qrlink = qr["result"]["qrlink"] #your qrlink
            resultdict["qrlink"] = qrlink
            qrcode = qr["result"]["qrcode"] #your qrcode
            #resultdict["qrcode"] = qrcode
            crypto = qr["result"]["session"] #your qrcode
            resultdict["crypto"] = crypto
            try:
                origins = "https://api.imgbb.com/1/upload"
                key = "f743bab7cbc0a853fb0614a2440b1457"
                expiration = "60"
                data = {"key":key,"image":qrcode,"expiration":expiration}
                r = requests.post(origins,data=data)
                rjson = r.json()
                url = rjson["data"]["display_url"]
                resultdict["qrimage"] = url
            except Exception as error:
                resultdict["qrimage"] = "qrimage error, contact creator for fix"
            return make_response(jsonify(resultdict))
        except Exception as error:
            return resultdict
            #print ("error, contact the creator")

@app.route("/crlgs2vip/<path:q>")
def threevip(q):
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
        resultnya["cert"] = e
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
