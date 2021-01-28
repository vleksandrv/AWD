# AWD
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from pandas.plotting import table


#wczytanie pliku
os.chdir(r"C:\Users\Lenovo\Downloads")
plik="googleplaystore.csv"
data=pd.read_csv(plik)

#usuwanie zduplikowanych wartoci
data = data.drop_duplicates()


### 1. HIPOTEZA: PŁATNE APLIKACJE UZYSKUJĄ WYŻSZE OCENY

#1.1 Sprawdzenie rozkładu częstoci cen aplikacji
#zastępowanie braków danych
data["Price"]=data["Price"].str.replace("$", " ")
data.Price = data.Price.replace('Everyone', np.NaN)
data["Type"]=data["Type"].replace('0', np.NaN)
data.Price= data.Price.str.strip()
data.Price= data.Price.fillna('missing')
data = data.replace('missing', np.NaN)

data['Price'] = data['Price'].astype(float) 
data.info()

Price_czestosci=data.Price.value_counts(dropna=False)

#1.2 koszt najtańszej aplikacji
data_gryplatne= data[data.Type== 'Paid']
print(data_gryplatne.Price.min())

#1.3 koszt najdroższej aplikacji
print(data_gryplatne.Price.max())

#1.3 Obliczenie sredniej ceny w przypadku gier płatnych
data_gryplatne= data[data.Type== 'Paid']
print(round(data_gryplatne.Price.mean()))


#z uwagi na odstające wartosci obliczam medianę

sorted_price = data_gryplatne["Price"].sort_values(ascending=True)
print(sorted_price.median())

#dolny i gorny kwartyl
dolny_kwartyl=sorted_price.quantile(0.25)
gorny_kwartyl=sorted_price.quantile(0.75)

kwartyle = {'Kwartyl': ['Dolny','Górny'],
        'wynik[$]': [dolny_kwartyl,gorny_kwartyl]
        }
df = pd.DataFrame(kwartyle, columns = ['Kwartyl','wynik'])



#Obliczam, jaka jest srednia ocena dla platnych i nieplatnych aplikacji
pytanie2=round(data.groupby("Type")["Rating"].mean(),2)

#Wynik: Płatne aplikacje mają nieznacznie wyższą srednią ocen.



#Wykres kołowy- częstoci płatnych i niepłatnych gier

do_wykresu_kolowego=data.Type.value_counts(dropna=False)
do_wykresu_kolowego = do_wykresu_kolowego.dropna()
do_wykresu_kolowego=do_wykresu_kolowego.iloc[:2]

fig1= plt.figure(1 , figsize=(6 ,6))
colors = ['#c76998', '#00c3ff']
plt.pie([do_wykresu_kolowego.iloc[0],do_wykresu_kolowego.iloc[1]],colors=colors, labels=["Darmowe","Płatne"], autopct='%1.1f%%')
#plt.title('Stosunek aplikacji płatnych do aplikacji darmowych')
plt.show()

fig1.canvas.get_supported_filetypes()
fig1.savefig("kolowy.png")



#wykres pudelkowy- cena aplikacji platnych   

fig,ax=plt.subplots()
ax.boxplot(sorted_price)
plt.ylabel("Cena [$]")
ax.set_yscale('log')
plt.ylim([0,1000])
plt.show()




### 2. HIPOTEZA: Aplikacji z jakich kategorii jest najwięcej i czy pokrywa się to z kategoriami mającymi najwięcej pozytywnych ocen?

ap_categories=data["Category"]
category_czestosci=data.Category.value_counts(dropna=False)
#widzimy, że najwięcej aplikacji posiada kategorię "Family".

#5 najpopularniejszych (najczęstszych) kategorii aplikacji

czestosci_category=data.Category.value_counts()
pop_cat=czestosci_category[:5]

nowa_data=pop_cat.reset_index()
print(nowa_data)

#wykres słupkowy z 5 najczęsciej występującymi kategoriali aplikacji
plt.bar(nowa_data.index, nowa_data.Category, color='green')
plt.xticks(range(len(nowa_data.index)),['FAMILY','GAME','TOOLS','MEDICAL','BUSINESS'])
plt.yticks(range(0,2500,500))
plt.ylabel("Liczba aplikacji w danej kategorii")
plt.show()


#5 najlepiej ocenianych kategorii aplikacji

kategorie_oceny=round(data.groupby("Category")["Rating"].mean(),2)
kategorie_oceny=kategorie_oceny[1:]
sorted_kategorie_oceny=kategorie_oceny.sort_values(ascending=False)

najpop_kategorie=sorted_kategorie_oceny[:5]
najpop_kategorie=najpop_kategorie.reset_index()
print(najpop_kategorie)

#wykres słupkowy z 5 najlepiej ocenianymi kategoriami
#wizualizacja z dwoma zmiennymi- rating i category
plt.bar(najpop_kategorie.index, najpop_kategorie.Rating, color='pink')
plt.xticks(range(len(najpop_kategorie.index)),['EVENTS','EDUCATION','ART AND DESIGN','BOOKS','PERSONALIZATION'])
plt.yticks(range(0,6))
plt.ylabel("Średnia ocena użytkowników")
plt.tick_params(axis="x",rotation=60)
plt.show()



#możemy porównać najlepiej i najgorzej oceniane kategorie wraz z ich cenami
#najlepiej oceniane kategorie
cena_kategorie_oceny=round(data.groupby("Category")["Rating","Price"].mean(),2)
cena_kategorie_oceny=cena_kategorie_oceny[1:]
sorted_cena_kategorie_oceny=cena_kategorie_oceny.sort_values(by="Rating", ascending=False)
#sorted_cena_kategorie_oceny.reset_index(level=0, inplace=True)


#wybrane 5 najlepszych wraz ze srednią ceną
tabela_1=sorted_cena_kategorie_oceny[:5]
tabela_1.reset_index(level=0, inplace=True)



#5 najgorszych wraz ze srednią ceną
sorted_cena_kategorie_oceny_najgorzej=cena_kategorie_oceny.sort_values(by="Rating", ascending=True)

tabela_2=sorted_cena_kategorie_oceny_najgorzej[:5]
tabela_2.reset_index(level=0, inplace=True)



data_events= data[data.Category== 'EVENTS']


#zapisywanie tabel do excela
tabela_1.to_excel('Tabela1.xlsx')
tabela_2.to_excel('Tabela2.xlsx')



