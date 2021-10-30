from flask import Flask, jsonify, request, render_template,Flask,url_for,request,redirect,make_response
from flask_cors import CORS
from pymongo import MongoClient
import requests,json,base64,uuid,os
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import datetime
from cryptography.fernet import Fernet
from opencage.geocoder import OpenCageGeocode
import haversine as hs

app = Flask(__name__)
cors = CORS(app)
key = b'6calkOBHsKDNFC3ZRuk5U60vjLqjB1kreYViM6qvxjA='
fernet = Fernet(key)
geo_key = 'd9854712656649d2b338910e3e9e5c8a'
geocoder = OpenCageGeocode(geo_key)

global txx,txx2,pid,passcde,userpi,txn_id,txxn,ad_number,passcde
passcde = 4567

uuidOne = uuid.uuid4()
newuuidv4 = "MYAADHAAR:" + str(uuidOne)


app.config["MONGO_URI"] = "mongodb+srv://codesploit:codesploit@cluster0.xcehq.mongodb.net/test"
client = MongoClient("mongodb+srv://codesploit:codesploit@cluster0.xcehq.mongodb.net/test")
db = client['Aadhaar']
coll = db["Userdb"]
uadd = db["Updated address"]

#=>Geolocation for getting the co_ordinates of the address
def geoloc(postal_address):
    results = geocoder.geocode(postal_address)
    x1=results[0]['geometry']['lat']
    y1=results[0]['geometry']['lng']
    return (x1, y1)

#=> Message service
def msg(number, name, refid):
    url = "https://www.fast2sms.com/dev/bulk"
    mess = f"{name} has requested you to share your address with him to upate his aadhar address. please use the following link, http://127.0.0.1:5000/approval/{refid}"
    payload = f"sender_id=FSTSMS&message={mess}&language=english&route=p&numbers={number},8667688729,9092269687"
    headers = {
        'authorization': "B7UXClFIymn8MfJrzSD4ERs0Qd935WYT2NiVoHGhLbat1ucwAKno2XEcK8GIyTuh6Zlq3MUvHxYpFDm0",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

#=> Message service
def msg2(number, name, addrss):
    url = "https://www.fast2sms.com/dev/bulk"
    mess = f"{name} has successfully updated his aadhaar address. Here is the updated address of his for your reference, {addrss}"
    payload = f"sender_id=FSTSMS&message={mess}&language=english&route=p&numbers={number},8667688729,9092269687"
    headers = {
        'authorization': "B7UXClFIymn8MfJrzSD4ERs0Qd935WYT2NiVoHGhLbat1ucwAKno2XEcK8GIyTuh6Zlq3MUvHxYpFDm0",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

#=> get the file xml
def foo(path):
    return os.listdir(path)[0]

#=> Get the address and name from zip file
def getadress():
    global pid
    zip_file = 'file.zip'
    password = str(passcde)
    with ZipFile(zip_file) as zf:
        zf.extractall(path=os.getcwd()+"/extract", pwd=bytes(password,'utf-8'))

    x=foo(os.getcwd()+"/extract")
    tree = ET.parse(os.getcwd()+"/extract/"+x)
    root = tree.getroot()

    pid=root.attrib
    pid=pid["referenceId"]
    pp=root[0][0].attrib
    address=root[0][1].attrib
    name = pp["name"]
    print(address)
    house=address["house"]
    street=address["street"]
    lamark=address["landmark"]
    locality=address["loc"]
    vtc=address["vtc"]
    dist=address["dist"]
    state=address["state"]
    pincode=address["pc"]

    lis=[house, street, lamark, locality, vtc, dist, state, pincode ]

    final_address=[]
    for i in lis:
        if(len(i)!=0):
            final_address.append((i))

    final = ", ".join(final_address)+"."
    return final, name, pid, x

def getadressdonor():
    zip_file = 'file.zip'
    password = str(passcde)
    with ZipFile(zip_file) as zf:
        zf.extractall(path=os.getcwd()+"/extract", pwd=bytes(password,'utf-8'))

    x=foo(os.getcwd()+"/extract")
    tree = ET.parse(os.getcwd()+"/extract/"+x)
    root = tree.getroot()

    pidd=root.attrib
    pidd=pidd["referenceId"]
    pp=root[0][0].attrib
    address=root[0][1].attrib
    return address

#=> Otp generator function inputs aadhar number(UID), transactionId, captcha
def otpgen(uid_no, txnid, cap):
    url = "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/generate/aadhaar/otp"
    payload = json.dumps({
      "uidNumber": uid_no,
      "captchaTxnId": txnid,
      "captchaValue": cap,
      "transactionId": newuuidv4
    })
    headers = {
      'x-request-id': str(uuidOne),
      'appid': 'MYAADHAAR',
      'Accept-Language': 'en_in',
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response

#=> Otp verifier function inputs aadhar number(UID), transactionId, OTP
def otpverify(ad_number, otpn, txxn, passcode=4567):
    global passcde
    passcde = passcode
    url = "https://stage1.uidai.gov.in/eAadhaarService/api/downloadOfflineEkyc"
    payload = json.dumps({
      "txnNumber": str(txxn),
      "otp": str(otpn),
      "shareCode": str(passcode),
      "uid": str(ad_number)
    })
    headers = {
      'Content-Type': 'application/json'
    }
    print(ad_number, otpn, txxn)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response

#=> Function to verify captcha and makes a call to otpgen
@app.route('/func',methods=['GET','POST'])
def func():
    global ad_numbe,txxn
    if(request.method=="POST"):
        try:
            number = request.form.get("capcha")
            ad_numbe = request.form.get("aadhaar_num")
            p = otpgen(ad_numbe, txn_id, number)
            jobj = json.loads(p.text)
            txxn = jobj["txnId"]
            sta = jobj["status"]
            print(sta)
            if(sta == "Success"):
                return render_template('success.html')
            else:
                return render_template('login.html')
        except:
            sta = jobj["status"]
            sta1= jobj["message"]
            return render_template('login.html', error=sta, error1=sta1)

        print(number, ad_number)

#=> Function to verify captcha and makes a call to otpgen for donor
@app.route('/func2',methods=['GET','POST'])
def func2():
    global ad_number, txxn
    if(request.method=="POST"):
        try:
            number = request.form.get("capcha")
            ad_number = request.form.get("aadhaar_num")
            print(number, ad_number, txn_i)
            p = otpgen(ad_number, txn_i, number)
            jobj = json.loads(p.text)
            txxn = jobj["txnId"]
            sta = jobj["status"]
            print(sta)
            if(sta == "Success"):
                return redirect(url_for('success2'))
            else:
                return render_template('login2.html')
        except:
            sta = jobj["status"]
            sta1= jobj["message"]
            return render_template('login2.html', error=sta, error1=sta1)

        print(number, ad_number)

#=> Index page of the app
@app.route('/',methods=['GET','POST'])
def index():
    if(request.cookies.get('ReferenceId') != None):
        return redirect(url_for('appstatus'))
    return render_template("index.html")

#=> About page has the tutorial!
@app.route('/about',methods=['GET','POST'])
def about():
    return render_template("about.html")

#=> Login page where captcha image is generated whenever reloaded
@app.route('/login',methods=['GET','POST'])
def login():
    global txn_id
    url = "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/get/captcha"
    payload = json.dumps({
      "langCode": "en",
      "captchaLength": "3",
      "captchaType": "2"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    json_object = json.loads(response.text)
    cap_code = json_object["captchaBase64String"]
    status = json_object["status"]
    txn_id = json_object["captchaTxnId"]
    st_code = json_object["statusCode"]
    print(status, txn_id)
    decodeit = open('static/captcha.jpeg', 'wb')
    decodeit.write(base64.b64decode((cap_code)))
    decodeit.close()
    return render_template('login.html')

#=> Login page where captcha image is generated whenever reloaded for donor
@app.route('/logindonor',methods=['GET','POST'])
def login2():
    global txn_i
    url = "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/get/captcha"
    payload = json.dumps({
      "langCode": "en",
      "captchaLength": "3",
      "captchaType": "2"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    json_object = json.loads(response.text)
    cap_code = json_object["captchaBase64String"]
    status = json_object["status"]
    txn_i = json_object["captchaTxnId"]
    st_code = json_object["statusCode"]
    print(status, txn_i)
    decodeit = open('static/captcha.jpeg', 'wb')
    decodeit.write(base64.b64decode((cap_code)))
    decodeit.close()
    return render_template('login2.html')

#=> Succes page is where OTP is verified and here we make call to otpverify
@app.route('/success',methods=['GET','POST'])
def success():
    if(request.method=="POST"):
        try:
            otp = request.form.get("otp")
            print(otp)
            res = otpverify(ad_numbe, otp, txxn)
            jobj = json.loads(res.text)
            sta = jobj["status"]
            if(sta == "Success"):
                cap_code = jobj["eKycXML"]
                decodeit = open('file.zip', 'wb')
                decodeit.write(base64.b64decode((cap_code)))
                decodeit.close()
                return redirect(url_for('change_address'))
            else:
                sta1 = jobj["message"]
                return render_template("success.html", error=sta, error1=sta1)

        except:
            sta = jobj["status"]
            sta1 = jobj["message"]
            return render_template("success.html", error=sta, error1=sta1)

    return render_template("success.html")

#=> Succes page is where OTP is verified and here we make call to otpverify
@app.route('/successful',methods=['GET','POST'])
def success2():
    global txx2, userpi
    userpi = request.cookies.get('UserReferenceId')
    print(userpi)
    if(request.method=="POST"):
        try:
            otp = request.form.get("otp")
            passc = request.form.get("passcode")
            print(otp)
            res = otpverify(ad_number, otp, txxn, passc)
            jobj = json.loads(res.text)
            sta = jobj["status"]
            if(sta == "Success"):
                cap_code = jobj["eKycXML"]
                decodeit = open('file.zip', 'wb')
                decodeit.write(base64.b64decode((cap_code)))
                decodeit.close()
                donor_address, donor_name, donor_pid, fn = getadress()
                raw_donor_address = getadressdonor()
                encMessage = fernet.encrypt(donor_address.encode())
                raw_donor_address=str(raw_donor_address)
                encM = fernet.encrypt(raw_donor_address.encode())
                coll.find_one_and_update({"ReferenceId": userpi },{'$set': { "Donor_Address" : encMessage }})
                coll.find_one_and_update({"ReferenceId": userpi },{'$set': { "Raw_Donor_Address" : encM }})
                coll.find_one_and_update({"ReferenceId": userpi },{"$push":{"logs":{"Activity":"Donor Approval Login","Time stamp": datetime.datetime.now(),"TransactionId": txxn,"ReferenceId": ad_number, "Message":"Donor has successfully shared his address." }}})
                os.remove(os.getcwd()+"/file.zip")
                os.remove(os.getcwd()+"/extract/"+fn)
                resp = make_response(redirect(url_for('donorsuccess')))
                resp.set_cookie('ReferenceId_donor', donor_pid )
                return resp
            else:
                sta1 = jobj["message"]
                coll.find_one_and_update({"ReferenceId": userpi },{"$push":{"logs":{"Activity":"Donor Approval Login","Status":"Login error","Time stamp": datetime.datetime.now(),"TransactionId": txxn,"ReferenceId": ad_num, "Error": sta1 }}})
                return render_template("success2.html", error=sta, error1=sta1)

        except:
            sta = jobj["status"]
            sta1 = jobj["message"]
            return render_template("success2.html", error=sta, error1=sta1)

    return render_template("success2.html")

#=> Finally here display the user address and request for landlord number or aadhar number
@app.route('/change-address',methods=['GET','POST'])
def change_address():
    if(request.cookies.get('User_Address') != None and request.method != "POST"):
        return render_template('change-address.html', output=request.cookies.get('User_Address'))

    address, name, pid, fn = getadress()
    dbfind = coll.find_one({"ReferenceId": pid })
    print(address, name, pid)

    if(request.method=="POST"):
        number = request.form.get("Number")
        msg(number, name, pid)
        print(number)
        ennumber = fernet.encrypt(number.encode())
        coll.find_one_and_update({"ReferenceId": pid },{'$set': { "Donor_Number" : ennumber }})
        coll.find_one_and_update({"ReferenceId": pid },{"$push":{"logs":{"Activity":"User_Requested","Time stamp": datetime.datetime.now(),"ReferenceId": pid,"Request-Status":"Sent Successfully"}}})
        os.remove(os.getcwd()+"/file.zip")
        os.remove(os.getcwd()+"/extract/"+fn)
        return redirect(url_for('appstatus'))
        #return render_template('change-address.html', output=address, out1=name, out2="Request sent successfully", out3="yes")

    encMessage = fernet.encrypt(address.encode())
    if(dbfind == None):
        coll.insert_one({"ReferenceId": pid ,"Name": name ,"User_Address": encMessage,"Donor_Address": "Null","Raw_Donor_Address": "Null","Donor_Number":"Null","Status":"Null","type":"User_update","logs": [] })
        coll.find_one_and_update({"ReferenceId": pid },{"$push":{"logs":{"Activity":"User_Logined","Time stamp": datetime.datetime.now(),"TransactionId": txxn,"ReferenceId": pid,"Status":"Successfull"}}})
    else:
        coll.find_one_and_update({"ReferenceId": pid },{"$push":{"logs":{"Activity":"Logined","Time stamp": datetime.datetime.now(),"TransactionId": txxn,"ReferenceId": pid,"Status":"Successfull"}}})

    resp = make_response(render_template('change-address.html', output=address, out1=name))
    resp.set_cookie('ReferenceId', pid )
    resp.set_cookie('User_Address', address)
    return resp

@app.route('/approval/<userpid>',methods=['GET','POST'])
def approval(userpid):
    global userpi
    userpi = userpid
    print(userpi)
    if(request.method=="POST"):
        option = request.form.get('opt')
        print(option)
        coll.find_one_and_update({"ReferenceId": userpid },{'$set': { "Status" : option }})
        if(option == "YES"):
            coll.find_one_and_update({"ReferenceId": userpid },{"$push":{"logs":{"Activity":"Donor Approval Status","Time stamp": datetime.datetime.now(),"Approval-status": option, "Message":"Donor has accepted the request of change of address." }}})
            return redirect(url_for('login2'))
        else:
            coll.find_one_and_update({"ReferenceId": userpid },{"$push":{"logs":{"Activity":"Donor Approval Status","Time stamp": datetime.datetime.now(),"Approval-status": option, "Message":"Donor has rejected the reqeust of change of address." }}})
            return render_template('approval.html', out="THANKS for your response!!", o1=userpi)

    nm = coll.find_one({"ReferenceId": userpi})["Name"]
    resp = make_response(render_template('approval.html', o1=userpi, name=nm))
    resp.set_cookie('UserReferenceId', userpi )
    return resp

@app.route('/donorsuccess',methods=['GET','POST'])
def donorsuccess():
    return render_template('finaldonor.html')

@app.route('/appstatus',methods=['GET','POST'])
def appstatus():
    global userpid
    userpid = request.cookies.get('ReferenceId')
    print(userpid)
    stat = coll.find_one({"ReferenceId": userpid})["Status"]
    if(request.method=="POST"):
        print("HIII")
        apart = request.form.get('ad1')
        strr = request.form.get('ad2')
        lmk = request.form.get('ad3')
        atc = request.form.get('ad4')
        vtc = request.form.get('ad5')
        po = request.form.get('ad6')
        sd = request.form.get('ad7')
        dt = request.form.get('ad8')
        stt = request.form.get('ad9')
        pin = request.form.get('ad10')
        addlist = [apart, strr, lmk, vtc, dt, stt, pin]
        fina_add = ", ".join(addlist)
        daddres = coll.find_one({"ReferenceId": userpid})["Donor_Address"]
        daddres = fernet.decrypt(daddres).decode()
        co_ord1 = geoloc(fina_add)
        co_ord2 = geoloc(daddres)
        dist = hs.haversine(co_ord1, co_ord2, unit=hs.Unit.METERS)
        uaddres = coll.find_one({"ReferenceId": userpid})["User_Address"]
        uaddres = fernet.decrypt(uaddres).decode()
        daddres = coll.find_one({"ReferenceId": userpid})["Donor_Address"]
        daddres = fernet.decrypt(daddres).decode()
        dist = round(dist)
        nme = coll.find_one({"ReferenceId": userpid})["Name"]
        nom = coll.find_one({"ReferenceId": userpid})["Donor_Number"]
        nome = fernet.decrypt(nom).decode()
        print(dist, co_ord1, co_ord2)
        if(dist < 250):
            suc_mes = "Address updated successfully!!"
            uadd.insert_one({"ReferenceId": userpid, "Adrress": fina_add, "Time stamp": datetime.datetime.now()})
            coll.find_one_and_update({"ReferenceId": userpid },{"$push":{"logs":{"Activity":"User Address Update","Status":"Success","Time stamp": datetime.datetime.now(),"Update-status": "Updated", "Message":"The User has successfully updated his aadhaar address" }}})
            msg2(nome, nme, fina_add)
            resp = make_response(redirect(url_for('updatesuccess')))
            resp.delete_cookie('ReferenceId')
            resp.delete_cookie('User_Address')
            return resp
        else:
            suc_mes = "Address you gave has major change, please rechech the address!!"
            coll.find_one_and_update({"ReferenceId": userpid },{"$push":{"logs":{"Activity":"User Address Update","Status":"Fail","Time stamp": datetime.datetime.now(),"Update-status": "Error-Try again", "Message":"Geolocation error occured due to major change of address" }}})
            return render_template('userapprovalstatus.html', out=stat, usera=uaddres, donora=daddres, o1=apart, o2=strr, o3=lmk, o4=atc, o5=vtc, o6=po, o7=sd, o8=dt, o9=stt, o10=pin, mess=suc_mes)

    if(stat == "YES"):
        uaddres = coll.find_one({"ReferenceId": userpid})["User_Address"]
        uaddres = fernet.decrypt(uaddres).decode()
        daddres = coll.find_one({"ReferenceId": userpid})["Donor_Address"]
        daddres = fernet.decrypt(daddres).decode()
        raw_donora = coll.find_one({"ReferenceId": userpid})["Raw_Donor_Address"]
        raw_donora = fernet.decrypt(raw_donora).decode()
        raw_donora = eval(raw_donora)
        house = raw_donora["house"]
        street = raw_donora["street"]
        lamark = raw_donora["landmark"]
        locality = raw_donora["loc"]
        vtc = raw_donora["vtc"]
        po = raw_donora["po"]
        subd = raw_donora["subdist"]
        dist = raw_donora["dist"]
        state = raw_donora["state"]
        pincode = raw_donora["pc"]
        return render_template('userapprovalstatus.html', out=stat, usera=uaddres, donora=daddres, o1=house, o2=street, o3=lamark, o4=locality, o5=vtc, o6=po, o7=subd, o8=dist, o9=state, o10=pincode)
    else:
        return render_template('userapprovalstatus.html', out=stat)

@app.route('/updatesuccess',methods=['GET','POST'])
def updatesuccess():
    return render_template('updatesucess.html')


if __name__ == "__main__":
    app.run(debug=False, port = int(os.environ.get("PORT", 5000)))
