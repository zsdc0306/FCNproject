import commands
import sys
import os

def grep(filename):
    print filename
    print "first name:"
    commands.getoutput("egrep -io 'Alexander' " + filename +" | sort | uniq -c")
    print "last name:"
    commands.getoutput("egrep -io 'Burkhart' " + filename +" | sort | uniq -c")
    print "email:"
    print commands.getoutput("egrep -io 'tranhkrub.*gmail' " + filename + " | sort | uniq -c")
    print "username:"
    print commands.getoutput("egrep -io 'tranhkrub123' " + filename +" | sort | uniq -c")
    print "birth"
    print commands.getoutput("egrep -io 'jan.*1990|1990.*jan' " + filename +" | sort | uniq -c")
    print "password:"
    print commands.getoutput("egrep -io 'projectRecon567' " + filename +" | sort | uniq -c")
    print "home zip:"
    print commands.getoutput("egrep -io '10028' " + filename +" | sort | uniq -c")
    print "gender"
    print commands.getoutput("egrep -io 'Male' " + filename +" | sort | uniq -c")
    print "location zip"
    print commands.getoutput("egrep -io '02115' " + filename +" | sort | uniq -c")
    print "address:"
    print commands.getoutput("egrep -io 'huntington|snell|new.{,10}york' " + filename +" | sort | uniq -c")
    print "MAC address:"
    print commands.getoutput("egrep -io '68.{0,10}db.{0,10}ca.{0,10}83.{0,10}6f.{0,10}7f' " + filename +" | sort | uniq -c")
    print "phone:"
    print commands.getoutput("egrep -io '781.{,10}333.{,10}7899' " + filename +" | sort | uniq -c")
    print "phonename:"
    print commands.getoutput("egrep -io 'shengdong' " + filename +" | sort | uniq -c")
    print "build:"
    print commands.getoutput("egrep -io '13E238' " + filename +" | sort | uniq -c")
    print "version:"
    print commands.getoutput("egrep -io '9.3.1' " + filename +" | sort | uniq -c")
    print "personal info:"
    print commands.getoutput("egrep -io 'zsdc0306|zhu' " + filename +" | sort | uniq -c")
    print "ADID:"
    print commands.getoutput("egrep -io '1DC58FB0-8A12-4970-8A80-38B1D11BDAC8' " + filename +" | sort | uniq -c")
    print "MEID:"
    print commands.getoutput("egrep -io '35329407254916' " + filename +" | sort | uniq -c")
    print "IMEI:"
    print commands.getoutput("egrep -io '35.{0,10}329407.{0,10}254916' " + filename +" | sort | uniq -c")
    print "ICCID:"
    print commands.getoutput("egrep -io '89014103278549305426' " + filename +" | sort | uniq -c")
    print "SEID:"
    print commands.getoutput("egrep -io '041c11c355338' " + filename +" | sort | uniq -c")
    print "modem firm:"
    print commands.getoutput("egrep -io 'f2lqn5d0grwx' " + filename +" | sort | uniq -c")
    print "latitude:"
    print commands.getoutput("egrep -io '[^a-zA-Z]?lat([^a-zA-Z]|itude).*[0-9]+(\.?)[0-9]+' " + filename +" | sort | uniq -c")
    print "latitude2:"
    print commands.getoutput("egrep -io '[^0-9]42\.[0-9]{5,14}' " + filename +" | sort | uniq -c")
    print "company contact1:"
    print commands.getoutput("egrep -io '.{40}amazon.{40}|.{40}google.{40}|.{40}linkedin.{40}|.{40}facebook.{40}|.{40}wechat.{40}|.{40}whatsapp.{40}|.{40}admob.{40}' " + filename +" | sort | uniq -c")
    print "company contact2:"
    print commands.getoutput("egrep -io 'www.{0,50}com' " + filename +" | sort | uniq -c")
    return

rootDir = sys.argv[1]
print rootDir

list_dir = os.walk(rootDir)
for root, dirs,files in list_dir:
    for f in files:
        filename = os.path.join(root,f)
        grep(filename)