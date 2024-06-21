

window.addEventListener('beforeunload', function (e) {
    if (userIsAuthenticated) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/logout/', true);
        xhr.send();
    }
});
