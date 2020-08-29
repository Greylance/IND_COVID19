import json
import pandas as pd
import matplotlib.pyplot as plt
#df = pd.read_json("https://data.covid19.go.id/public/api/update.json")
with open(r'D:\Myproject\pycode\data_analysis_covid19_indonesia\cov19-060820.json') as f:
    data_json = json.loads(f.read())
fig,ax=plt.subplots(1,1,figsize=(12,6))
#print(data_json["update"])
df=pd.DataFrame(data_json)
#Dict data penambahan kasus COVID19
penambahan = df["update"].iloc[5]

#Dict data total kasus COVID19
total = df["update"].iloc[7]

#Dict data harian kasus COVID19
harian = df["update"].iloc[6]

#Ubah dict data harian menjadi dataframe
dataharian = pd.DataFrame.from_dict(harian)
print(dataharian.columns)#Cetak daftar kolom
dataharian = dataharian[["key_as_string","jumlah_meninggal", "jumlah_sembuh", "jumlah_positif", "jumlah_dirawat","jumlah_meninggal_kum", "jumlah_sembuh_kum", "jumlah_positif_kum", "jumlah_dirawat_kum"]]

#Data n hari terakhir
n = 157
dataharian_n = dataharian.iloc[157-n:157]
#Note: jumlah_meninggal + jumlah_sembuh + jumlah_dirawat = jumlah_positif
#Ada tiga kemungkinan yang dapat terjadi pada orang yang positif: sembuh, belum sembuh(dirawat), meninggal
#print(dataharian_n)

#Mengubah tipe data dict values menjadi list
def valueformat(df_col):
    n=0
    for i in df_col:
        df_col.iloc[n] = list(df_col.iloc[n].values())[0]
        n+=1
    return df_col
dataharian_n["jumlah_meninggal"] = valueformat(dataharian_n["jumlah_meninggal"])
dataharian_n["jumlah_sembuh"] = valueformat(dataharian_n["jumlah_sembuh"])
dataharian_n["jumlah_positif"] = valueformat(dataharian_n["jumlah_positif"])
dataharian_n["jumlah_dirawat"] = valueformat(dataharian_n["jumlah_dirawat"])
dataharian_n["jumlah_meninggal_kum"] = valueformat(dataharian_n["jumlah_meninggal_kum"])
dataharian_n["jumlah_sembuh_kum"] = valueformat(dataharian_n["jumlah_sembuh_kum"])
dataharian_n["jumlah_positif_kum"] = valueformat(dataharian_n["jumlah_positif_kum"])
dataharian_n["jumlah_dirawat_kum"] = valueformat(dataharian_n["jumlah_dirawat_kum"])

#Mengganti format tanggal 
n=0
for i in dataharian_n["key_as_string"]:
    dataharian_n["key_as_string"].iloc[n] = dataharian_n["key_as_string"].iloc[n].replace("T00:00:00.000Z","")
    dataharian_n["key_as_string"].iloc[n] = dataharian_n["key_as_string"].iloc[n].replace("-","/")
    #print(dataharian_n["jumlah_dirawat"].iloc[n])
    n+=1
dataharian_n = dataharian_n.rename(columns={"key_as_string": "Tanggal"})
dataharian_n['Tanggal'] = pd.to_datetime(dataharian_n['Tanggal'], format='%Y/%m/%d')

#Grafik garis jumlah penambahan
plot1 = plt.plot(dataharian_n['Tanggal'], dataharian_n['jumlah_meninggal'], color = 'r',label = 'Jumlah Meninggal')
plot2 = plt.plot(dataharian_n['Tanggal'], dataharian_n['jumlah_sembuh'], color = 'b',label = 'Jumlah Sembuh')
plot3 = plt.plot(dataharian_n['Tanggal'], dataharian_n['jumlah_positif'], color = 'm',label = 'Jumlah Positif')
plot4 = plt.plot(dataharian_n['Tanggal'], dataharian_n['jumlah_dirawat'], color = 'y',label = 'Jumlah Dirawat')
print("Tingkat positif tertinggi: {}".format(dataharian_n['jumlah_positif'].max()))
print("Di tanggal: ")
print(dataharian_n['Tanggal'].loc[dataharian_n['jumlah_positif']==dataharian_n['jumlah_positif'].max()])
#plt.annotate("Jumlah penambahan\n positif tertinggi\n%.4f"%highest,(200,200),(200,200),ha="lef t",color='m')
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Kasus")
plt.title("Grafik Laju Penambahan Kasus COVID-19 2 Maret 2020 - 5 Agustus 2020")
plt.legend()
plt.show()

#Grafik garis jumlah kumulatif
plot1 = plt.plot(dataharian_n['Tanggal'], dataharian_n['jumlah_meninggal_kum'], color = 'r',label = 'Jumlah Meninggal')
plot2 = plt.plot(dataharian_n['Tanggal'], dataharian_n['jumlah_sembuh_kum'], color = 'b',label = 'Jumlah Sembuh')
plot3 = plt.plot(dataharian_n['Tanggal'], dataharian_n['jumlah_positif_kum'], color = 'm',label = 'Jumlah Positif')
plot4 = plt.plot(dataharian_n['Tanggal'], dataharian_n['jumlah_dirawat_kum'], color = 'y',label = 'Jumlah Dirawat')
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Kasus")
plt.title("Grafik Kasus COVID-19 Kumulatif 2 Maret 2020 - 5 Agustus 2020")
plt.legend()
plt.show()
