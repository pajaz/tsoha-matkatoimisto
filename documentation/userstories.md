<h1> Matkatoimisto X verkkosovellus - User stories </h1>

Tässä tiedostossa listataan, sekä sovelluksen asiakkaan, että hallinnoijan tarvitsemia ominaisuuksia. Esitetyn ominaisuuden perään listattuna toiminnon suorittava SQL-kysely.

<h2> Asiakas </h2>

* Haluan mahdollisuuden helposti hakea mahdollisia matkakohteita kohdemaan perusteella.(done)
```
SELECT * FROM Matkakohde WHERE country="Haettu maa"
```
* Varaus olisi hyvä pystyä tekemään suoraan sivujen kautta, koska puhelin/email ym. ovat turhan hitaita ja vaivalloisia keinoja.(done) 

* Olisi kätevää, jos verkkosivuille voisi luoda oman tunnuksen jonka kautta omia varauksia olisi mahdollista tarkastella ja muokata.(done) 

Tunnuksen luominen:  
INSERT INTO User (first_name, last_name, username, email, phone_number, password)   
VALUES ("string", "string", "string", "string", "string", "string");  
INSERT INTO roles (role_id, kayttaja_id) VALUES (2, User.id);  
Omien varausten haku:  
SELECT Varaus.id, Varaus.start_date, Varaus.end_date, Matkakohde.name FROM Varaus  
INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id  
WHERE Varaus.user_id = "oma id" ORDER BY Varaus.start_date;  

* Tahtoisin pelkkien lentojen lisäksi varata samaa kautta myös majoituksen matkakohteesta.(done)

* Majoituksista olisi hyvä tietää mahdollisimman paljon (sijainti, tähtiluokitus, palvelut yms), jottei varausta tarvitse tehdä täysin sokkona. Tietysti sama pätee myös matkakohteisiin eli kattava kohteen esittely olisi tarpeellinen.(done) 

Hotellin tietojen haku esittelysivulle:  
SELECT * FROM Hotelli WHERE Hotelli.id = "halutun hotellin id";  
Matkakohteen tietojen haku esittelysivulle:  
SELECT * FROM Matkakohde WHERE Matkakohde.id = "halutun matkakohteen id;  


<h2> Admin </h2>

* Haluan, että pystyn lisäämään, poistamaan ja muokkaamaan sivuilla näytettäviä matkakohteita ja hotelleja.(done)

Laitan esimerkin komennoista hotellin lisäämiseksi:
INSERT INTO Hotelli (name, address, phone_number, email, small_rooms, large_rooms, destination_id, price_small, price_large, star_rating, introduction) VALUES ("string, "string", "string", "string", int, int, int, int, int, int);  
Tietojen muokkaus:   
Update Hotelli SET sarake="jotain", sarake2="jotain muuta" WHERE {{ tähän ehtoja }}

* Tahdon tarkastella asiakkaiden tekemien varausten tietoja. Varauksen tietojen pitäisi sisältää ainakin matkakohde ja mahdollinen majoitus, kaikki varaukseen kuuluvat matkustajat henkilötietoineen, matkustusajat, hinta, maksutilanne(done)

Varaussivun tietojen hakukysely (yksi esimerkki):  
SELECT Matkakohde.name as Matkakohde_nimi, Kayttaja.username as user, Hotelli.name as Hotel  
FROM Matkakohde, Kayttaja, Hotelli WHERE Matkakohde.id = Varaus.dest_id  
AND Kayttaja.id = Varaus.user_id AND Hotelli.id = Varaus.hotel_id AND Varaus.id = 1;  
Palauttaa varauksen numero 1 tietoja

* Haluan mahdollisuuden lisätä varauksia tietokantaan. Tämä olisi kätevää, jos asiakas tekee varauksen esimerkiksi puhelimitse. Varausten poistaminen sivuilta kuuluu tietysti myös toiveisiini(done)

Poistetaan varaus id:llä 1:
DELETE FROM Varaus WHERE Varaus.id = 1;

* Toivottavasti valmiissa sovelluksessa on ominaisuus erilaisten yhteenvetokyselyiden tekemiselle. Onko minun mahdollista saada esimerkiksi selville tietyssä matkakohteessa tai maassa tällä hetkellä olevien matkustajien määrä, tai vaikkapa jokaisen heidän yhteystietonsa?(done(ish)) 

En ehtinyt (muistanut) tehdä suoraa kyselyä ihmismäärille eri kohteissa. Kuitenkin hakutoiminto löytyy, jolla saa listattua kaikki varaukset kohteen mukaan. Haussa myös yhtenä vaihtoehtona tällä hetkellä aktiiviset varaukset. 

Tämä listaa kaikki varaukset kohteessa nro 1.  
SELECT Varaus.id, Matkakohde.name as Matkakohde FROM Varaus INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id WHERE Varaus.dest_id = 1 AND Varaus.start_date < "tänään" AND Varaus.end_date > "tänään" AND handled=1;

Ja tässä itseasiassa kaikkien matkustajien määrä kohteessa 1 tällä hetkellä:  
SELECT sum(Varaus.passengers), Matkakohde.name as Matkakohde FROM Varaus 
INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id 
WHERE Varaus.dest_id = Matkakohde.id AND Varaus.start_date < "2018-08-31" AND Varaus.end_date > "2018-08-31" 
AND handled=1 AND Matkakohde.id = 1;



