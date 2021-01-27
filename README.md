# AWD
import pandas as pd
import os
#import numpy as np
import matplotlib.pyplot as plt

#otwieranie danych w formie .csv
os.getcwd()
os.listdir() 
os.chdir(r"C:\Users\zuzan\Downloads")

#przypisanie sciezki do zmiennej
plik = "googleplaystore.csv"
data = pd.read_csv(plik)

#usunięcie M z kolumny Size oraz , i + z kolumny Installs oraz . z Reviews
data["Size"]=data["Size"].str.replace("M", " ")
data["Installs"]=data["Installs"].str.replace("+", " ")
data["Installs"]=data["Installs"].str.replace(",", "")

#zmiana tekstu na brak danych w kolumnie Size (ze względu na opcję "Varies with device")
data['Size'] = pd.to_numeric(data['Size'], errors='coerce')

#usunięcie braków danych
data = data.dropna()

#usunięcie zduplikowanych danych
data = data.drop_duplicates()

#nazwy kolumn
data.columns= ['App','Category','Rating','Reviews','Size','Installs','Type','Price','Content Rating','Genres','Last Updated','Current ver','Android ver']

#usuwanie kolumn, których nie potrzebuję do analizy
#del data['Type']
#del data['Price']
#del data['Content Rating']
del data['Genres']
del data['Last Updated']
del data['Current ver']
del data['Android ver']

#installs i reviews traktowane jako numeryczna
data['Installs'] = data['Installs'].astype(int) 
data['Reviews'] = data['Reviews'].astype(int) 
 
#1 pytanie - Które aplikacje mają najlepsze oceny - małe (1-33Mb), srednie(34-67Mb), czy duze (68-100Mb)
#tworzenie podgrup kategorii Size
#Małe aplikacje
male_aplikacje=data[data.Size<=33]
#male_aplikacje_warunek = data[male_gry]

#Srednie aplikacje - najpierw usuwam wyniki mniejsze od 34, 
#potem usuwam wyniki większe od 68
srednie_aplikacje_prawie=data[data.Size >= 34]
srednie_aplikacje=srednie_aplikacje_prawie[data.Size <= 68]

#Duze gry
duze_aplikacje=data[data.Size>=68]
#duze_aplikacje_warunek = data[duze_aplikacje]

#sredni rating dla malych, srednich i duzych gier
"%.2f"%male_aplikacje.Rating.mean()
"%.2f"%srednie_aplikacje.Rating.mean()
"%.2f"%duze_aplikacje.Rating.mean()
"%.2f"%data.Rating.mean()

#przypisuję srednim zmienne
srednia_male="%.2f"%male_aplikacje.Rating.mean()
srednia_srednie="%.2f"%srednie_aplikacje.Rating.mean()
srednia_duze="%.2f"%duze_aplikacje.Rating.mean()
srednia_wszystko = "%.2f"%data.Rating.mean()
#tworzę tabelkę z użyciem srednich
#jest to odpowiedz na pytanie zadane wyzej - roznica jest bardzo niewielka,
#jednak sredni rating jest wyzszy dla srednich gier niz malych, i wyzszy 
#dla duzych apliiacji niz srednich i malych.
Wielkosc_aplikacji_a_jej_oceny=pd.DataFrame([srednia_male,srednia_srednie,srednia_duze,srednia_wszystko],
['Małe aplikacje', 'Średnie aplikacje', 'Duże aplikacje','Wszystkie aplikacje'], ['Srednia ocena'])

#ile jest zmiennych w poszczególnych wielkosciach
ilosc_male= len(male_aplikacje.index)
#5360
ilosc_srednie= len(srednie_aplikacje.index)
#1303
ilosc_duze= len(duze_aplikacje.index) 
#514

#tabelka - porównanie ilosci malych, srednich i duzych aplikacji
ilosc_wszystko = [['Małe aplikacje', ilosc_male, srednia_male], ['Srednie aplikacje', ilosc_srednie, srednia_srednie], ['Duże aplikacje', ilosc_duze, srednia_duze]]
ilosc_wszystko_df = pd.DataFrame(ilosc_wszystko, columns = ['Wielkosć aplikacji','Ilosć aplikacji', 'Sredni rating'])

#wykres - rating a wilekosc aplikacji
#x = ['Małe aplikacje', 'Srednie aplikacje', 'Duze aplikacje']
#y = ['4.16', '4.20', '4.29']
#plt.plot(x,y)
#plt.ylabel('Sredni rating')
#plt.xlabel('Wielkosc aplikacji')
#plt.show()

#wykres do pytania - histogram wielkosci aplikacji i ratingu
size_rating=data[data.Size>=1]
del size_rating['Category']
del size_rating['App']
del size_rating['Reviews']
del size_rating['Installs']
del size_rating['Type']
del size_rating['Price']
del size_rating['Content Rating']

#size_rating.hist(column='Rating')
#size_rating.hist(column='Size')



#___________________________________________________________________


#2 pytanie - Jakie kategorie mają najwięcej reviews?
#badam częstoci kategorii
czestosci= data.Category.value_counts() 
czestosci = czestosci.reset_index()

#skupiam się na 10 największych kategoriach 
czestosci = czestosci.head(11)
czestosci = czestosci.drop(czestosci.index[1])

# przyporządkowuję kategorie do ilosci reviews
ilosc_reviews = data.groupby('Category')['Reviews'].mean()
category_reviews = ilosc_reviews.reset_index()

#print(category_reviews)

#usuniecie game 
#category_reviews = category_reviews.drop(category_reviews.index[14])

#sortuję kategorie, żeby móc zostawić tylko największe 
category_reviews_sort = category_reviews.sort_values('Reviews', ascending=False)
#skupiam się na 10 największych kategoriach 


#segreguję iloscią reviews, żeby sprawdzić, czy największe kategorie mają najwiecej reviews
ilosc_reviews_czestosci = [183922, 185987, 32553.2, 4668.57, 40327.8, 137361, 220393, 321600, 24981.9, 198866]
czestosci["Reviews"] = ilosc_reviews_czestosci

#Zestawienie 10 kateogorii z największą iloscia reviews
category_reviews_sort = category_reviews_sort.head(10)
plt.bar(category_reviews_sort.Category, category_reviews_sort.Reviews)
plt.tick_params(axis='x',rotation=70)
plt.xlabel('Kategoria')
plt.ylabel('Recenzje')
plt.show()

#Zestawienie 10 największych kategorii i iloci ich reviews
czestosci = czestosci.rename(columns={'Category': 'Ilosć aplikacji w kategorii'})
czestosci = czestosci.rename(columns={'index': 'Category'})
plt.bar(czestosci.Category, czestosci.Reviews)
plt.xlabel('Kategoria')
plt.ylabel('Recenzje')
plt.tick_params(axis='x',rotation=70)
plt.show
