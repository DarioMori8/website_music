# Sito di Streaming Musicale Django

Benvenuto nel nostro sito di streaming musicale basato su Django! Questo README fornisce una panoramica delle funzionalità e delle caratteristiche del sito.

## Indice
- [Funzionalità](#funzionalità)
- [Pagina Home](#pagina-home)
- [Dettagli Playlist](#dettagli-playlist)
- [Controlli delle Canzoni](#controlli-delle-canzoni)
- [Canzoni Preferite](#canzoni-preferite)
- [Aggiungere Canzoni alle Playlist](#aggiungere-canzoni-alle-playlist)
- [Suggerimenti](#suggerimenti)
- [Barra di Navigazione](#barra-di-navigazione)
- [Pagina di Ricerca](#pagina-di-ricerca)
- [Profilo Utente](#profilo-utente)
- [Creazione di Playlist](#creazione-di-playlist)
- [Installazione e Configurazione](#installazione-e-configurazione)

## Funzionalità
- Pagina home con un carosello di playlist.
- Visualizzazione dettagliata delle playlist e delle loro canzoni.
- Controlli per riprodurre, riavviare e fermare le canzoni.
- Aggiungere o rimuovere canzoni dai preferiti.
- Aggiungere canzoni a playlist specifiche dell'utente.
- Suggerimenti di canzoni e playlist.
- Funzionalità di ricerca completa.
- Gestione del profilo utente.
- Creazione e gestione di playlist utente.

## Pagina Home
La pagina home include:
- Un carosello di playlist. Cliccando su una playlist si aprono i dettagli.
- Una lista di canzoni con controlli di riproduzione e stop. Facendo doppio clic su play, la canzone si riavvia.
- Un'icona a forma di cuore per aggiungere/rimuovere canzoni dai preferiti.
- Un'icona con il simbolo "+" per aggiungere canzoni alle tue playlist.
- Un pulsante in fondo che apre una pagina con suggerimenti di canzoni e playlist.
Le playlist mostrate sono solo quelle pubbliche e vengano selezionate solo le canzoni e le playlist più ascoltate dai vari utenti. 

## Dettagli Playlist
Cliccando su una playlist nel carosello si apre una visualizzazione dettagliata con tutte le canzoni presenti nella playlist.

## Controlli delle Canzoni
- **Play**: Clicca una volta per riprodurre, doppio clic per riavviare.
- **Stop**: Clicca per fermare la canzone.
- **Preferiti**: Clicca sull'icona a forma di cuore per aggiungere una canzone ai preferiti. Clicca di nuovo per rimuoverla dai preferiti.

## Aggiungere Canzoni alle Playlist
- Clicca sull'icona con il simbolo "+" accanto a una canzone.
- Seleziona la playlist in cui vuoi aggiungere la canzone.

## Suggerimenti
- In fondo alla pagina home, il pulsante apre una pagina con suggerimenti.
- I suggerimenti includono canzoni e playlist che potrebbero piacerti.
- Le funzionalità all0interno della pagina sono simile a quella della pagina home.

## Barra di Navigazione
- **Logo**: Cliccando sul logo si ritorna alla pagina home.
- **Icona Profilo**: 
  - Se non sei loggato, ti porta alla pagina di login/registrazione.
  - Se sei loggato, apre la tua pagina del profilo.
- **Icona di Ricerca**: Apre la pagina di ricerca.

## Pagina di Ricerca
- Cerca tra utenti, canzoni, playlist, artisti o generi.
- Cliccando sui risultati di ricerca si aprono le pagine corrispondenti:
  - **Utente**: Apre il profilo utente con il pulsante segui/non segui e le sue playlist pubbliche.
  - **Artista**: Apre una pagina con le canzoni dell'artista.
  - **Genere**: Apre una pagina con canzoni e playlist di quel genere.
  - **Playlist**: Apre la visualizzazione dettagliata della playlist.
- I filtri possono essere attivati cliccando sui pulsanti sotto la barra di ricerca.

## Profilo Utente
- **Pulsante Modifica (in basso a destra)**: Ti permette di modificare bio, username, immagine, ecc.
- **Pulsanti a Sinistra**:
  - **Preferiti**: Lista delle tue canzoni preferite.
  - **Seguiti**: Lista degli utenti che segui.
  - **Playlist**: Lista delle tue playlist. Clicca per visualizzare i dettagli e per eventaulmente aggiungere nuove playlist.

## Creazione di Playlist
- Naviga al tuo profilo e clicca sul pulsante presnte nella lista delle tua playlist per creare una nuova playlist.
- Inserisci il nome della playlist.
- Facoltativamente, aggiungi canzoni e per impostare la playlist come pubblica si deve spuntare o meno l'ultima voce presente; Se spuntata allora è pubblica.
- Salva la nuova playlist.

## Installazione e Configurazione
1. Clona il repository:
   ```bash
   git clone <repository-url>
2. Installa le dipendenze:
    ```bash
    pip install -r requirements.txt
3. Esegui le migrazioni:
    ```bash
    python manage.py migrate
4. Crea un superuser:
    ```bash
    python manage.py createsuperuser
5. Avvia il server di sviluppo:
    ```bash
    python manage.py runserver