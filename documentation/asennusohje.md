<h1> Matkatoimisto X </h1>
<h2> Asennusohje </h2>
Mitenköhän tarkkaan tähän pitää asiaa kirjoittaa?
<h4> Postgresql -komennot ensimmäisen käynnistyksen jälkeen </h4>
Nämä komennot luovat käyttäjäroolit tietokantaan, sekä ensimmäisen adminoikeuksilla toimivan tunnuksen.  

Huom! Syötä komennot tässä järjestyksessä!

INSERT INTO role (name) VALUES ('Admin'), ('User');

(Sijoita allaolevaan haluamasi tiedot omille paikoilleen. Älä koske ykköseen salasanan jälkeen)  

INSERT INTO kayttaja (first_name, last_name, username, email, phone_number, password, admin) 
VALUES ('Etunimi', 'Sukunimi', 'kayttajanimi', 'email<span>@matkatoimisto.x', '0501234567', 'salasana', 1);  


INSERT INTO roles (role_id, kayttaja_id) VALUES (1, 1), (2, 1);
