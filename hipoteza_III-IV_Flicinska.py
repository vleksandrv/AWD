#wczytanie pakietu pandas
import pandas as pd
#wczytanie pakietu numpy
import numpy as np

import os
os.chdir(r'C:\Users\HP\Desktop\Projekt_AIWD')

#wczytujemy plik Excelowy
baza_danych_excel = pd.ExcelFile('googleplaystore.xlsx')
#sprawdzenie nazw arkuszy
print(baza_danych_excel.sheet_names)

#odwołanie się do pierwszego i jedynego arkusza
data = baza_danych_excel.parse('googleplaystore')
#odwołanie się do numeru arkusza pierwszego
data = baza_danych_excel.parse(0)
#wybranie kolumns
data=baza_danych_excel.parse(0,usecols=[0,5,7,8,9])

#zmiana wielkosci liter wszstkich danych
data["App"]= data["App"].str.lower() 
data["Content Rating"]= data["Content Rating"].str.lower() 
data["Genres"]= data["Genres"].str.lower() 

# zmiana nazwy kolumny "price" aby była podana waluta
#usuwanie zduplikowanych danych
data = data.drop_duplicates()
data["App"] = data["App"].drop_duplicates()
#usuwanie braków danych
data = data.dropna()

#usuwanie $ i + z danych installs i price
data["Price"]=data["Price"].str.replace("$", " ")
data["Price"]=data["Price"].str.strip()
data["Installs"]=data["Installs"].str.replace(",", "")
data["Installs"]=data["Installs"].str.replace("+", " ")
data["Installs"]=data["Installs"].str.strip()
#zmiana wartoci "nan" na "0" w kolumnie "Price"
data["Price"]= data["Price"].fillna("0")
data["Installs"]= data["Installs"].fillna("0")

#zmiana zmiennych z kolumn "installs" i "Price" z danych typu object na zmienne numeryczne
data['Price'] = data['Price'].astype(float) 
data['Installs'] = data['Installs'].astype(int) 


data.describe()
print(data)
data.info()
#zapis
data.to_excel('wyczyszczone_dane_excel.xlsx')

#1.1: Utworzenie tabelki

tabele_excel = pd.ExcelFile('wyczyszczone_dane_excel.xlsx')
#1.2: Sprawdzenie nazw arkuszy
print(tabele_excel.sheet_names)

#1.3: Odwołanie się do pierwszego i jedynego arkusza
tabele_tidy = tabele_excel.parse('Sheet1')
#odwołanie się do numeru arkusza pierwszego
tabele_tidy = tabele_excel.parse(0)
tabele_tidy=tabele_excel.parse(0,usecols=[1,2,3])
print(tabele_tidy.info())


#2: Opracowanie kolumn "Price" i "Installs", przygotowanie srednich, median itp.
#2.1: Kolumna "Price":(Średnia, mediana, wartoć max i min)
# "Price" - Średnia cena
tabele_tidy.Price.mean()
print("Średnia cena to:", tabele_tidy.Price.mean(), "$")
# "Price" - dominanta
tabele_tidy.Price.mode()
print("Dominanta:", data.Price.mode(), "$")
# "Price" - mediana:
tabele_tidy.Price.median()
print("Mediana:",data.Price.median())
# "Price" - maximum i minimum wartoć 
tabele_tidy.Price.max()
print("Maksymalna cena:",tabele_tidy.Price.max(), "$")
tabele_tidy.Price.min()
print("Minimalna cena:",tabele_tidy.Price.min(), "$")
# "Price" - unikalne kategoria
tabele_tidy.Price.unique()
print("Wszystkie możliwe ceny", tabele_tidy.Price.unique())

#2.2: Kolumna "Installs"
tabele_tidy.Installs.unique()
print("Wszystkie możliwe ilosci pobrań:", tabele_tidy.Installs.unique())

#2.3: Obliczenie sumy,sredniej, odchylenia, minimum i maximum, kwartyli
print(tabele_tidy.describe())

#2.4: Posortowanie wszystkiech aplikacji po rosnącej cenie i iloci pobrań
tabele_tidy.sort_values(by="Price", ascending=True)
tabele_tidy.sort_values(by= "Installs", ascending=True)
print(tabele_tidy)

#3: Utworzenie tabel dla aplikacji płatnych i bezpłatnych
#Filtrowanie danych - przygotowanie tabeli, która posiada tylko aplikacje płatne, posortowane pod względem rosnącej iloci pobrań i ceny
aplikacje_platne= tabele_tidy[~(tabele_tidy.Price==0)]
aplikacje_platne=aplikacje_platne.sort_values(by=["Installs", "Price"])
aplikacje_platne=aplikacje_platne.reset_index()
aplikacje_platne=aplikacje_platne.drop('index', axis=1)
print(aplikacje_platne)
print(aplikacje_platne.describe())


#3.1: Filtrowanie danych - przygotowanie tabeli, która posiada tylko aplikacje bezpłatne, posortowane pod względem rosnącej iloci pobrań
aplikacje_bezplatne=tabele_tidy[(tabele_tidy.Price==0)]
aplikacje_bezplatne=aplikacje_bezplatne.sort_values("Installs")
aplikacje_bezplatne=aplikacje_bezplatne.reset_index()
aplikacje_bezplatne=aplikacje_bezplatne.drop('index', axis=1)
print(aplikacje_bezplatne)

#3.2: Tabela dla 10 aplikacji bezpłatych, które posiadają najwiecej pobrań:
aplikacje_bezpłatne_top_10=aplikacje_bezplatne.iloc[8875:]
aplikacje_bezpłatne_top_10=aplikacje_bezpłatne_top_10.reset_index()
aplikacje_bezpłatne_top_10=aplikacje_bezpłatne_top_10.drop('index', axis=1)
print(aplikacje_bezpłatne_top_10)
aplikacje_bezpłatne_top_10.to_excel('aplikacje_bezpłatne_top_10.xlsx')


# 4: Tabele odnonie "Genres"i "Content Rating" dla
tabela_rating_genres = pd.ExcelFile('wyczyszczone_dane_excel.xlsx')
#1.2: Sprawdzenie nazw arkuszy
print(tabela_rating_genres.sheet_names)

#4.1 Odwołanie się do pierwszego i jedynego arkusza
tabela_R_G = tabela_rating_genres.parse('Sheet1')
#odwołanie się do numeru arkusza pierwszego
tabela_R_G = tabela_rating_genres.parse(0)
tabela_R_G=tabela_rating_genres.parse(0,usecols=[1,4,5])
print(tabela_R_G.info())
print(tabela_R_G)

#4.2: Filtrowanie - Tabela_R_G, przygotowanie tabeli, która posiada tylko dane dedykowane dla młodzieży (Teen)
tabela_R_G_Teen=tabela_R_G[(tabela_R_G["Content Rating"]=="teen")]
tabela_R_G_Teen.sort_values(by=["Genres","Content Rating"])
tabela_R_G_Teen=tabela_R_G_Teen.reset_index()
tabela_R_G_Teen=tabela_R_G_Teen.drop('index', axis=1)
print(tabela_R_G_Teen)


#6: Wizualizacja danych dla danych "Genres" i "Data rating"
#6.1: Import pakietu do wizualizacji danych
import matplotlib.pyplot as plt
#zliczenie ilosci aplikacji każdego rodzaju dedykowanych dla mlodziezy
tabela_czestosc_kategorii_teen=pd.ExcelFile('Tabela_R_G_Teen.xlsx')
print(tabela_czestosc_kategorii_teen.sheet_names)
czestosc_kategorii_teen= tabela_czestosc_kategorii_teen.parse("Sheet1")
czestosc_kategorii_teen = tabela_czestosc_kategorii_teen.parse(0)
czestosc_kategorii_teen=tabela_R_G_Teen.Genres.value_counts() 
czestosc_kategorii_teen= czestosc_kategorii_teen.reset_index()
print(czestosc_kategorii_teen.info())
print(czestosc_kategorii_teen)

low_czestosc_kategorii_teen=czestosc_kategorii_teen.iloc[36:]
print(low_czestosc_kategorii_teen)
low_czestosc_kategorii_teen.to_excel("10_low_czestosc_kategorii_teen.xlsx")


#6.1: Wykres pięciu kategorii dedykowanych dla "Teen", które posiadają najwięcej pobranych aplikacji
czestosc_kategorii_teen_powyzej_5=czestosc_kategorii_teen.iloc[:10]
print(czestosc_kategorii_teen_powyzej_5)
plt.bar(czestosc_kategorii_teen_powyzej_5["index"], czestosc_kategorii_teen_powyzej_5.Genres, color='black')
plt.xticks(range(len(czestosc_kategorii_teen_powyzej_5.index)), ['action','entertainment',
'social',"personalization","role playing","simulation","casino","strategy","adventure","news & magazines"])
plt.yticks(range(0,160,20))
plt.tick_params(axis='x', rotation=70)
plt.xlabel('Kategorie aplikacji')
plt.ylabel('Ilość aplikacji w kategorii')
plt.show()
plt.savefig('Wykres_podsumowania_zliczonych kategorii.png')


#7: Wizualizacja danych dla danych "Price" i "Installs'
#7.1: Posortowana tabela dla aplikacji płatnych pod względem pobrań:
tabela_posortowane_platne_pobraniami=pd.ExcelFile('aplikacje_platne.xlsx')
print(tabela_posortowane_platne_pobraniami.sheet_names)
posortowane_platne_pobraniami= tabela_posortowane_platne_pobraniami.parse("Sheet1")
posortowane_platne_pobraniami=posortowane_platne_pobraniami.reset_index()
posortowane_platne_pobraniami=posortowane_platne_pobraniami.drop('Unnamed: 0', axis=1)
posortowane_platne_pobraniami=posortowane_platne_pobraniami.drop('index', axis=1)

print(posortowane_platne_pobraniami)
posortowane_platne_pobraniami_top_5=posortowane_platne_pobraniami.iloc[743:]
posortowane_platne_pobraniami_top_5=posortowane_platne_pobraniami_top_5.reset_index()
posortowane_platne_pobraniami_top_5=posortowane_platne_pobraniami_top_5.drop('index', axis=1)
print(posortowane_platne_pobraniami_top_5)
posortowane_platne_pobraniami_top_5.to_excel('posortowane_platne_pobraniami_top_10.xlsx')


#8: Wykres kołowy dla kategorii: ilosc kategorii i ilosc aplikacji w nich
#8.1: Tabela z posortowanymi kategoriami wszystkich aplikacji
tabela_czestosc_kategorii_ogolna=pd.ExcelFile('tabela_R_G.xlsx')
print(tabela_czestosc_kategorii_ogolna.sheet_names)
czestosc_kategorii_ogolna= tabela_czestosc_kategorii_ogolna.parse("Sheet1")
czestosc_kategorii_ogolna = tabela_czestosc_kategorii_ogolna.parse(0)
czestosc_kategorii_ogolna=data.Genres.value_counts() 
czestosc_kategorii_ogolna= czestosc_kategorii_ogolna.reset_index()
print(czestosc_kategorii_ogolna.info())
print(czestosc_kategorii_ogolna)

#8.2: Tabela z 5 najliczniejszymi kategoriami ogólnie
czestosc_kategorii_ogolna_top_5=czestosc_kategorii_ogolna.iloc[:11]
czestosc_kategorii_ogolna_top_5=czestosc_kategorii_ogolna_top_5.reset_index()
czestosc_kategorii_ogolna_top_5=czestosc_kategorii_ogolna_top_5.drop('level_0', axis=1)
print(czestosc_kategorii_ogolna_top_5)
    
#8.3: Tabela z 10 najliczniejszymi kategoriami ogólnie
kategorie_nazwy=czestosc_kategorii_ogolna_top_5["index"]
ilosc_aplikacji_ogolna=czestosc_kategorii_ogolna_top_5.Genres
plt.rcParams.update({'figure.autolayout': True})

fig, ax = plt.subplots()
ax.barh(kategorie_nazwy, ilosc_aplikacji_ogolna)
labels = ax.get_xticklabels()
plt.setp(labels, rotation=60, horizontalalignment='right')
ax.set(xlim=[0, 1000], xlabel='Ilość aplikacji w kategorii', ylabel='Nazwy kategorii aplikacji')
plt.show()
plt.savefig('Wykres_podsumowania_zliczonych kategorii.png')

print(posortowane_platne_pobraniami.describe())

#5:zapisywanie plików
tabela_R_G_Teen.to_excel('Tabela_R_G_Teen.xlsx')
tabela_R_G.to_excel('tabela_R_G.xlsx')
aplikacje_bezplatne.to_excel('aplikacje_bezplatne.xlsx')
aplikacje_platne.to_excel('aplikacje_platne.xlsx')
tabele_tidy.to_excel('Tabele_tidy.xlsx')
data.to_excel('posortowane_aplikacje_paid_free.xlsx')
czestosc_kategorii_teen.to_excel('czestosc_kategorii_teen.xlsx')