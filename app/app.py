import pickle
import datetime as dt

from sklearn.datasets import load_svmlight_file

model = pickle.load(open('KF45_TunedSVM_4000.sav', 'rb'))
X, Y = load_svmlight_file('data/shhs1-205804_svmlight')
Y_pred = model.predict(X)

print "----------------------"
print "This is the initial prototype of SmAlarm. It pulls EEG data from one of the test record."
print "----------------------"
print "Wake up fresh!"
print "Today is July 18th, 2016. It is now 11PM"
print "Our alarm system is powered by machine learning-based calculation, so you will wake up fresh and energized!"

size = 0
fake = (2016, 7, 18)
sttime = dt.datetime(fake[0], fake[1], fake[2], 23, 0, 0)
b = False

while size < 3600:
    print "Please input your desired (min. 1 hour window) time window (hour+minute, e.g '0700' or '0730')"
    frm = raw_input("From: ")
    unt = raw_input("Until: ")

    hf = int(frm[:2])
    mf = int(frm[2:4])
    hu = int(unt[:2])
    mu = int(unt[2:4])

    fromtime = dt.datetime(fake[0], fake[1], fake[2] + 1, hf, mf)
    untiltime = dt.datetime(fake[0], fake[1], fake[2] + 1, hu, mu)

    size = (untiltime - fromtime).seconds

for second in range(len(Y_pred)):
    label = Y_pred[second]
    curtime = sttime + dt.timedelta(0, second)
    if curtime - fromtime < dt.timedelta(0, 0):
        print "%d seconds elapsed. Not in time window." % second
    else:
        if label == 0:
            print "It is now " + str(curtime.time()) + " but you are not in wake stage."
        else:
            print "It is now " + str(curtime.time()) + " and you are in wake stage!"
            b = True
            break

if b:
    print "ALARM RINGS. RINGGGGGG"
    print "Thank you for using SmAlarm!"
else:
    print "You have woken up without alarm."
