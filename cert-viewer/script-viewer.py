import os

confx_old = open("confx.ini","r")
confx_new = open("confx2.ini","w")

osdir = os.listdir("cert_data/")

line = 'recent_certids='

for certids in osdir:
    if((certids != 'blockchain_certificates') and (certids != 'backup') and (certids != '.DS_Store')):
        line += str(certids[:36])
        print('Processing certificate: ', str(certids[:36]))
        line += ','

confx_new.write(str(line))

confx_new.write('\n')

readline = confx_old.readline()
readline = confx_old.readline()

confx_new.write(readline)
readline = confx_old.readline()
confx_new.write(readline)
readline = confx_old.readline()
confx_new.write(readline)
readline = confx_old.readline()
confx_new.write(readline)
readline = confx_old.readline()
confx_new.write(readline)
readline = confx_old.readline()
confx_new.write(readline)
readline = confx_old.readline()
confx_new.write(readline)
readline = confx_old.readline()
confx_new.write(readline)
readline = confx_old.readline()
