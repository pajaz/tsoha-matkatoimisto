<h1> Matkatoimisto X </h1>
<h2> Verkkosovelluksen käyttöohje </h2>

<h3> Käyttäjäluokka: Admin </h3>
Admin -käyttäjällä on tällä hetkellä pääsy sivuston jokaiselle (toteutetulle) osa-alueelle. 
<h3> Käyttäjäluokka: User </h3>
Matkatoimiston asiakas, jonka toiminnallisuudet rajoittuvat kohteiden tarkasteluun, varausten tekemiseen, rajoitetusti oman varauksen tietojen muokkaamiseen sekä omien käyttäjätietojen muokkaamiseen.

<h4> Käyttäjän luominen, editointi ja poistaminen </h4>

Admin-käyttäjälle tulisi sovelluksen käynnistysvaiheessa luoda omat tunnukset komentorivin kautta asennusohjeiden mukaan.

Uusi käyttäjä voi luoda itselleen tunnukset sivun oikeassa ylälaidassa olevan painikkeen kautta. 

Admin -käyttäjällä on oikeus luoda tunnuksia muille, sekä antaa näille samat oikeudet kuin itselleen.

Jokainen käyttäjä pystyy tarkastella omia tietojaan "Profiili" -sivun kautta (sivun oikea ylälaita). Saman sivun kautta löytyy myös painike käyttäjätietojen muokkauslomakkeen avaamiseen. (Admin -käyttäjällä  on oikeus muokata myös muiden käyttäjien tietoja)

Profiili-sivulla on myös listattuna kyseisen tunnuksen tekemät varaukset, joiden päivämäärää klikkaamalla pääsee varauksen infosivulle.

Profiili-sivulle on pääsy ainoastaan käyttäjällä itsellään, sekä Admin -käyttäjällä,

<h4>Uusien matkakohteiden ja hotellien lisääminen</h4>

Uusien matkakohteiden ja hotellien lisääminen onnistuu joko navigointipalkista löytyvien pudotusvalikoiden tai 
matkakohteiden/hotellien listaussivuilta löytyvistä painikkeista.

Lisäämiseen käytettävään lomakkeeseen on tähdellä(*) merkitty vaaditut kentät. Loput kentät voi jättää tyhjäksi myöhempää
täyttöä varten, jos näin haluaa. Jokaisessa tekstikentässä on nähtävissä malli kentän täyttämiseen ja virheellisesti täytetty
kenttä aiheuttaa virheviestin kyseisen kentän alapuolelle.

Hotellin lisääminen vaatii aina sen liittämistä johonkin matkakohteeseen.

<h4> Matkakohteiden ja hotellien tietojen editointi </h4>

Matkakohteiden ja hotellien tietojen editointiin pääsee käsiksi kohteiden/hotellien listaussivuilta, josta jokaisen kohteen riviltä löytyy painike "Muokkaa".

Kummallakin sivulla on tarjolla myös haku-lomake. Matkakohteita voi hakea kohdemaan, nimen tai molempien perusteella. Hotellien 
haku toimii samalla tavalla, mutta matkakohteen, nimen tai molempien perusteella.

Muokkaamiseen käytettävä lomake on muutamia sivuilla tapahtuvia otsikko-/tekstimuutoksia lukuunottamatta täysin sama kuin lisäämislomake ja siinä on samat ominaisuudet.

<h4> Matkakohteiden ja hotellien tietojen tarkastelu </h4>

Tällä hetkellä sekä matkakohteiden, että hotellien listaussivuilta pääsee haluamansa matkakohteen tai hotellin nimeä klikkaamalla
katselemaan tarkempia tietoja. Sivuilla on nähtävissä kaikki kyseisen kohteen tietokannasta löytyvät tiedot.

Matkakohteiden sivuilla on tällä hetkellä lisäksi tieto kuinka monta varausta kyseiseen kohteeseen on tehty, sekä matkojen
varaamiseen liittyvää tietoa ja toiminnallisuutta, josta enemmän myöhemmin tässä dokumentissa.

<h4> Varausten tarkastelu, muokkaus ja tekeminen </h4> 

Varausten listaussivuilta löytyy kaikki sovellukseen lisätyt varaukset listattuna varauksen alkupäivämäärän mukaan. Id:stä painamalla aukeaa yksittäisen varauksen infosivu. User -käyttäjälle näkyy samalla sivulla listaus omista varauksista.

Listaussivulla on myös hakutoiminto, jonka avulla voi hakea varauksia kohteen, maksutilanteen ja ajankohdan (mennyt, aktiivinen, tuleva) mukaan.

Varauksen infosivulta löytyy kaikki varaukseen liittyvät tiedot, sekä mahdollisuus muokata matkustajatietoja tai poistaa varau. Kun asiakas on vahvistanut varauksen tiedot, pystyy admin käyttäjä kuittaamaan sivun alaosasta Laskun lähetetyksi, jonka jälkeen painike vaihtuu Lasku maksettu painikkeeksi. 

Normaali käyttäjä pystyy muokkaamaan varauksensa matkustajatietoja tai poistamaan varauksen siihen asti, kun hän on vahvistanut varauksen tiedot. Jos tämän jälkeen tulee tarvetta poistaa tai lisätä matkustajia varauksesta, joutuu asiakas olemaan yhteydessä matkatoimistoon, koska muokkausominaisuus säilyy Admin -käyttäjällä. 



