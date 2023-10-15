document.getElementById('signup').addEventListener('submit', function(event) {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPass').value;

    if (password !== confirmPassword) {
        alert('As senhas são diferentes! Por favor, tente novamente.');
        event.preventDefault();
    } else if (password.length < 6) {
        alert('A Senha é muito curta! A senha deve ter, no mínimo, 6 caracteres.');
        event.preventDefault();
    }
});
