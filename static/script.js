document.addEventListener('DOMContentLoaded', () => {
    const idDisplay = document.getElementById('idDisplay');
    
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initDataUnsafe) {
        const userData = window.Telegram.WebApp.initDataUnsafe.user;
        if (userData && userData.id) {
            idDisplay.textContent = userData.id;
            console.log("ID de Telegram obtenido:", userData.id);
            enviarIdAServidor(userData.id, userData);
        } else {
            idDisplay.textContent = "ID no encontrado.";
            console.error("No se pudo obtener el ID del usuario.");
        }
    } else {
        idDisplay.textContent = "Error: No estás en Telegram WebApp.";
        console.error("La aplicación no se está ejecutando en Telegram WebApp.");
    }

    function enviarIdAServidor(id, userInfo) {
        fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                telegram_id: id,
                user_info: userInfo
            })
        })
        .then(res => res.json())
        .then(data => {
            console.log("✅ Respuesta del servidor:", data.status);
        })
        .catch(err => {
            console.error("❌ Error al enviar el ID:", err);
        });
    }
});
