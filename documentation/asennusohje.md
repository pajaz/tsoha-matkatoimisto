<h1> Matkatoimisto X </h1>
<h2> Asennusohje </h2>

<h4> Let's get started (Local/Heroku) </h4>

* Lataa kopio projektista, joko komennolla 
```git clone git@github.com:pajaz/tsoha-matkatoimisto.git ```
 tai lataamalla pakattu versio tämän repositorion etusivulta.
* Navigoi itsesi terminaalissa projektin juurikansioon, jonka tulisi olla /tsoha-matkatoimisto, ellet ole antanut sille uutta nimeä.
* Syötä seuraavat komennot terminaalissa:  
```
$ python -m venv venv  
$ source venv/bin/activate  
$ pip install -r requirements.txt  
```
Nyt olet luonut projektille virtuaaliympäristön ja ladannut tarvittavat riippuvuudet. 
Sovellus toimii nyt periaatteessa paikallisesti juurikansiossa annetulla komennolla  
```
$ python3 run.py
```
Jos kiinnostus oli vain paikalliseen pyörittämiseen, voit siirtyä kohtaan  
"SQL-komennot ensimmäisen käynnistyksen jälkeen". Muussa tapauksessa jatketaan sovelluksen siirtämiseen Herokuun.

Olethan luonut Heroku -tunnukset ja asentanut tarvittavat Heroku-työvälineet (Heroku CLI).
Jos et, tutustu asiaan [Tästä](https://devcenter.heroku.com/articles/heroku-cli)  

* Luo sovellukselle paikka Herokuun komennolla
```
$ heroku create tsoha-matkatoimisto  (kyseinen nimi tietysti tällä hetkellä käytössä, eli keksi omasi)
```
* Lisää paikalliseen versionhallintaan tieto Herokusta
```
$ git remote add heroku htts://git.heroku.com/tahan-se-keksimasi-nimi.git
```
* Lähetetään sovellus Herokuun
```
$ git add .
$ git commit -m "Kiva eka commit viesti"
$ git push heroku master
```
Nyt voit siirtyä hyvin mielin ottamaan Herokun tarjoaman PostgreSQL -tietokannan käyttöön.


<h4> Postgresql(ja sqlite3) -komennot ensimmäisen käynnistyksen jälkeen </h4>
Nämä komennot luovat käyttäjäroolit tietokantaan, sekä ensimmäisen adminoikeuksilla toimivan tunnuksen.  

Huom! Syötä komennot tässä järjestyksessä!
```
INSERT INTO role (name) VALUES ('Admin'), ('User');  
```
(Sijoita allaolevaan haluamasi tiedot omille paikoilleen. Älä koske ykköseen salasanan jälkeen!)  
```
INSERT INTO kayttaja (first_name, last_name, username, email, phone_number, password, admin) 
VALUES ('Etunimi', 'Sukunimi', 'admin', 'email<span>@matkatoimisto.x', '0501234567', 'salasana', 1);  
INSERT INTO roles (role_id, kayttaja_id) VALUES (1, 1), (2, 1);
```
