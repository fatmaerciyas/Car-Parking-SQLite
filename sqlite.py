import sqlite3
from datetime import datetime
import time


class customer():
    def __init__(self,ad,soyad,plaka,giriş_saati):
        self.ad = ad
        self.soyad = soyad
        self.plaka = plaka
        self.giriş_saati = giriş_saati


    def __str__(self):

        return "Ad :{}\nSoyad:{}\nGiriş saati:{}\n".format(self.ad,self.soyad,self.giriş_saati)

class car_park():

    def __init__(self):

        self.connecting() # her bir araba için sql veritabanıyla bağlantı oluşturacak foksiyon

    def connecting(self): #tablo oluştur
        self.con = sqlite3.connect("car_park.db") #tabloya bağlan
        self.cursor = self.con.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS cars (Name TEXT,Surname TEXT,Plaque ,Check_in_time timestamp)")
        #zamana şu anki zamanı gir plakaya bir veri tipi atamadım çünkü integer str karışık olacak
        self.con.commit()

    def disconnect(self):#bağlantıyı kes
        self.con.close()

    def show_records(self): #tüm kayıtları göster
        self.cursor.execute("Select * From cars")
        #tüm araba bilgilerini al
        list1 = self.cursor.fetchall()
        #bunları bir listeye ata listede eleman yoksa araba yoktur
        if(len(list1) == 0):
            return "Otoparkta araba bulunmuyor"
        else:
            for i in list1:
                print(i)
            return None


    def show_customer(self,ad,soyad): #aranan müşteriyi göster

        self.cursor.execute("Select *From cars where Name = ? ",(ad,)) #demet olarak algılaması için addan sonra virgül koydum
        list2= self.cursor.fetchall()
        if (len(list2) == 0):
            print("Öyle bir müşteri kaydı bulunmuyor")
            return "Öyle bir müşteri kaydı bulunmuyor"

        else:

            print("...Müşteri kaydı...\n")

            for i in list2:
                if (i[0] == ad and i[1] == soyad):
                    print(i)
                    print("\n")
                    return i

    def car_add(self,ad,soyad,plaka):  #ekle


        self.cursor.execute("INSERT INTO cars  VALUES(?,?,?,?)",(ad,soyad,plaka,datetime.now()))

        self.con.commit()

    def delete_record(self,plaka):#sil
        kararlılık = input("{} plakalı araç silinecektir.Emin misiniz? 'E' ya da 'H' basınız ".format(plaka))
        if kararlılık == "E":
            self.cursor.execute("Delete From cars where Plaque = ?", (plaka,))
            self.con.commit()
            print("Kayıt siliniyor...")
            time.sleep(1)
            print("Kayıt başarıyla silindi.")




    def update(self,ad,soyad,plaka): #güncelle
        while True:
            if(self.show_customer(ad,soyad) == "Otoparkta araba bulunmuyor"):
                break


            bilgi = input("""Müşterinin hangi bilgisini güncellemek istiyorsunuz
                   1.Ad Soyad
                   2.Plaka
                   Başka güncelleme yapamazsınız.Müşterinin tarih bilgisi sisteme giriş yaptırıldığı andan itibaren başlar""")

            if(bilgi == "1"):
                new_name = input("Yeni adı giriniz:")
                new_surname = input("Yeni soyadı giriniz:")
                self.cursor.execute("Update cars set Name = ? where Name = ?", (new_name, ad))
                self.cursor.execute("Update cars set Surname = ? where Surname = ?", (new_surname, soyad))
                self.con.commit()
                time.sleep(2)
                print("Müşteri bilgileri başarıyla güncellendi")
                break


            elif(bilgi == "2"):
                new_plaque = input("Yeni plakayı giriniz:")
                self.cursor.execute("Update cars set Plaque = ? where Plaque = ?", (new_plaque,plaka))
                self.con.commit()
                print("Müşteri bilgileri başarıyla güncellendi")
                break

            else:

                print("Lütfen geçerli bir işlem giriniz")

    def search_plaque(self,plaka):
        self.cursor.execute("Select * From cars where Plaque = ?",(plaka,))
        list4 = self.cursor.fetchall()
        print(list4)
        login = list4[0][3]
        return login


    def log_out(self,plaka):
        one_hour_fee = 30 # bir saatlik otopark ücreti 10 tl olsun
        one_minute_fee = 0.5
        login = self.search_plaque(plaka)
        login.split(" ")
        login = list(login)
        end = datetime.now()
        end = str(end)
        end = list(end)
        list1 = list(login[11:19])
        list2 = list(end[11:19])
        a= " "
        b= " "

        for i in list1:
            if( i == ":" ):

                continue
            a += str(i)

        for i in list2:
            if(i == ":"):

                continue
            b += str(i)

        if(int(a) > int(b)):
            hour = int(a) - int(b)

        elif(int(a) < int(b)):
            hour = int(b) - int(a)

        #print(hour) yaptığında kaç saat kaldığını gösteriyor
        hour = str(hour)
        hour = list(hour)


        price = (int(hour[0]) * one_hour_fee) + (int(hour [1]) * one_minute_fee)

        print( "Ödemeniz gereken tutar {} TL".format(price))

        self.delete_record(plaka)
        time.sleep(1)
        print("Müşteri çıkışı yapıldı...")



print("""
Otoparkımıza Hoşgeldiniz

İşlemler;

1.Otopark durumu göster

2.Müşteri ara

3.Kayıt Ekle

4.Kayıt sil

5.Kayıt Güncelle

6.Araba Çıkışı ve Ücret Hesapla

Çıkmak için "q" ya basınız""")

car_park1 = car_park()

while True:
    seçim = input("\nİşleminizi giriniz:")
    if(seçim == "q"):
        print("İşlem sonlandırıldı.")
        break

    elif(seçim == "1"):
        car_park1.show_records()

    elif (seçim == "2"):
        ad = input("Aranacak müşterinin adını giriniz:")
        soyad = input("Soyadını giriniz:")
        car_park1.show_customer(ad,soyad)


    elif (seçim == "3"):
        ad = input("Eklenecek müşterinin adını giriniz:")
        soyad = input("Soyadını giriniz:")
        plaka = input("Plakayı giriniz:")
        car_park1.car_add(ad,soyad,plaka)
        print("\nMüşteri ekleniyor...")
        time.sleep(2)
        print("Müşteri eklendi.")


    elif (seçim == "4"):
        plaka = input("Silinecek arabanın plakasını giriniz:")

        car_park1.delete_record(plaka)


    elif (seçim == "5"):
        ad = input("Bilgileri güncellenecek müşterinin adını giriniz:")
        soyad = input("Soyadını giriniz:")
        plaka = input("Plakayı giriniz:")
        car_park1.update(ad,soyad,plaka)

    elif (seçim == "6"):
        plaka = input("Otopark ücretini öğrenmek istediğiniz arabanın plakasını giriniz:")
        car_park1.log_out(plaka)

    else:
        print("Lütfen geçerli bir işlem giriniz.")

