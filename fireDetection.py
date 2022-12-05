import cv2         # OpenCV kütüphanesini import ettik
import threading   # Kodun arka planda çalışabilmesi için threading kütüphanesini import ettik  
import playsound   # Alarm sesi icin playsound kütüphanesini import ettik
import smtplib     # Mail gönderebilmek için smtplib kütüphanesini import ettik

fire_cascade = cv2.CascadeClassifier('fire_detection.xml') # Haar cascade ile eğittiğimiz yangın görüntülerin bulunduğu xml dosyasına erişmek için.                                                                       

vid = cv2.VideoCapture(0) # Dizüstü kameraya erişmek için '0'yazdık. Harici bir kamera oldugunda '0' yerine  '1' yazmamız gerekiyor
runOnce = False # Boolean olusturduk
runOnce1 = False # Boolean olusturduk
def play_alarm_sound_function(): # yangın algilama sonrası alarmı çalmak için fonksiyon tanımladım
    playsound.playsound('fire_alarm.mp3',True) # Alarmı çalmak için (mp3 uzantılı fire_alarm dosyasını açar)
    print("Yangin alarm sonu") # consolda yangın alarmın bitişi yazdırdım
def send_mail_function(): # defined function to send mail post fire detection using threading 
    recipientmail = "yanginalgilamasistemi@gmail.com" # Alıcı mail adresi
    recipientmail = recipientmail.lower() # Küçük harfli mail için 
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("yanginalgilamasistemi@gmail.com", 'fkgdpjefylfgxigr') # gönderici mail adresi ve şifresi
        server.sendmail('yanginalgilamasistemi@gmail.com', recipientmail, "1 numarali bolgede yangin tespit edildi") # Alıcı mail'ine '1 numarali bolgede yangin tespit edildi' mailini gönderir.
        print("{} Mail adresine uyari basarı ile gonderildi".format(recipientmail)) # consolda 'Mail adresine uyari basarı ile gonderildi' yazısını yazdırır.
        server.close() ## server'ı kapatır     
    except Exception as e:
        print(e) # Varsa hatayı yazdırır		
while(True):
    Alarm_Status = False
    ret, frame = vid.read() # retdeki değer doğruysa # framede Videoyu okur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # framei gri renge dönüştürmek için
    fire = fire_cascade.detectMultiScale(frame, 1.2, 3) # çözünürlüğü ayarlar
    ## ateşi kare ile vurgulamak için 
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Yangin alarmi baslatildi")
        threading.Thread(target=play_alarm_sound_function).start()  # Alarm dizisini aramak için

        if runOnce == False:
            print("Mail gonderme baslatildi")
            threading.Thread(target=send_mail_function).start() # mail dizisini aramak için
            runOnce = True
        if runOnce == False:
            print("Mail zaten bir kez gonderildi")
            runOnce = True
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # kapatmak için 'q' ya bas
        break
