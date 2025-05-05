import requests
import smtplib
import time
import schedule

konu = "Bugunun Hava Durumu"

apı_key = "" #OpenWeatherMap'ten aldığım API anahtarı

gönderici_mail = "" #Gönderecek olan mail adresi
mail_sifre = "" #Uygulamalar için kullanılan şifre
alici_mail = "" #Mesajı alıcak olan mail adresi

city_name = "Balikesir"
country_code = 792

#Şehrimizin API verisini alıyoruz.
geometric_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={apı_key}"
requests_geo = requests.get(geometric_url).json()
print(requests_geo)

#Longitude ve Latitude değerlerine bu şekilde ulaşıyoruz.
lat = requests_geo[0]["lat"]
lon = requests_geo[0]["lon"]
print(lat,lon)

#Bu şekilde şehrimizdeki havadurumuna eriştik
weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apı_key}"
requests_weather = requests.get(weather_url).json()
print(requests_weather)

#Havanın id sine ulaştık çünkü OpenWeatherMap'te hava durumları id ile temsil ediliyor.
weather_id = requests_weather["weather"][0]["id"]

#Duruma göre mesajı hazırladık.
mesaj = ""
if 200 <= weather_id <=232:
    mesaj = "Fırtınalı bir hava! Şemsiyeni unutma ve sıkı giyin!!!"
elif 300 <= weather_id <= 321:
    mesaj = "Hava çiseliyor, şemsiye almasanda olur ama sıkı giyin!"
elif 500 <= weather_id <= 531:
    mesaj = "Hava yağmurlu, şemsiyeni unutma!"
elif 600 <= weather_id <= 622:
    mesaj = "Hava karlı. Eğlencesini çıkar ya da dikkatli ol!"
elif 701 <= weather_id <= 781:
    mesaj = "Hava gözgözü görmüyor!!!"
elif weather_id == 800:
    mesaj = "Hava tertemiz."
else:
    mesaj = "Hava bulutlu."
print(mesaj)

e_posta = f"Subject: {konu}\n\n{mesaj}" #Genelde spam klasörüne düşerler. Dikkat edilmeli!


#Bir port açıyoruz ve buradan mesajımızı yolluyoruz.Eğer yollanırsa olumlu çıktı, yollanmaz ise olumsuz çıktı vericek.
def e_posta_gonder():
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gönderici_mail, mail_sifre)
            server.sendmail(gönderici_mail, alici_mail, e_posta)
            print("E-posta başarılı bir şekilde gönderildi!")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

#schedule kütüphanesi ile her sabah 7 de göndericek bir biçimde ayarlıyoruz.
schedule.every().day.at("07:00").do(e_posta_gonder) #Denemek için saati değiştiriniz.

#Bu şekilde kodu döngüye sokuyoruz ki kod bitmesin.
#Ayrıca her 60 saniyede bir çalışacak biçime sokuyoruz ki işlemcimiz rahatlasın.
while True:
    schedule.run_pending()
    time.sleep(60)