from pirc522 import RFID
import time
import datetime
import RPi.GPIO as GPIO
import mysql.connector

ledpin = 37
sensorpin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledpin, GPIO.OUT)
GPIO.setup(sensorpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

rdr = RFID()
util = rdr.util()
util.debug = True
sayac = 0
timestamp = time.time()
stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

tur_sayisi = 0
kontrol = 0
yolculuk = 0

##veritabanı = {'user':'emreu', 'password':'Emre123', 'host':'127.0.0.1', 'database':'rfid'}

    
def dbGonder():
    cnx = mysql.connector.connect(user='emreu', password='Emre123', host='127.0.0.1', database='rfid')
    cursor = cnx.cursor()
    #print('Veritabanına bağlanıldı! ' + stamp)
    veri_ekle = ("INSERT INTO table1 (rfid,Yolculuk,Baslangic,Bitis) VALUES (%s,%s,%s,%s)")
    veri = (kart_uid,yolculuk,baslangic,bitis)
    cursor.execute(veri_ekle,veri)
    cnx.commit()
    print(cursor.rowcount,'Yolculuk kaydı tamamlandı.')
    
def sensorCallback(channel):
  global yolculuk 
  global tur_sayisi

  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
  time.sleep(0.1)
  

  if GPIO.input(channel):
      pass
  else:
    print("Mıknatıs algılandı " + stamp)
    tur_sayisi = tur_sayisi + 1
    print("Tur sayisi = "  ,tur_sayisi)
    yolculuk = (157 * tur_sayisi) * 0.01
    return yolculuk

GPIO.add_event_detect(sensorpin, GPIO.BOTH, callback=sensorCallback, bouncetime = 200)
while True:
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
  time.sleep(1)
  rdr.wait_for_tag()
  (error, data) = rdr.request()
  if not error:
   print("\nKart Algilandi!")
   (error, uid) = rdr.anticoll()
   if not error:
    kart_uid = str(uid[0])+" "+str(uid[1])+" "+str(uid[2])+" "+str(uid[3])+" "+str(uid[4])
    print(kart_uid)
    if kart_uid == "135 202 127 98 80":

     sayac = sayac + 1
     if sayac%2 != 0:
         baslangic = stamp
         print("Hoşgeldiniz! {0} tarihinde yolculuğunuz başladı".format(baslangic))
         GPIO.output(ledpin,True)
         print("Manyetik sensör başlatılıyor...")
         sensorCallback(sensorpin)
         #kontrol(sensorpin)                  
         
     else:
         bitis = stamp
         print("Tebrikler! {0}m mesafe ile {1} tarihinde yolculuğunuz tamamlandı".format(yolculuk,stamp))
         dbGonder()
         tur_sayisi = 0
         yolculuk = 0
         GPIO.output(ledpin, False)
         
    else: 
     print("Kullanıcı kayıtlı değil!")
     sayac = 0
     GPIO.output(ledpin, False)
     

