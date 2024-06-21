

window.addEventListener('beforeunload', function (e) {
    // Esegui il logout solo se l'utente è autenticato
    if (userIsAuthenticated) {
        // Invia una richiesta AJAX per eseguire il logout
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/logout/', true);
        xhr.send();
    }
});
