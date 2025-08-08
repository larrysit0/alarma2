document.addEventListener('DOMContentLoaded', () => {
    const getIdBtn = document.getElementById('getIdBtn');
    const idDisplay = document.getElementById('idDisplay');
    
    // Obtener datos del usuario a través de la WebApp de Telegram
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initDataUnsafe) {
        const userData = window.Telegram.WebApp.initDataUnsafe.user;
        if (userData && userData.id) {
            idDisplay.textContent = userData.id;
            // Opcional: mostrar la info del usuario en la consola
            console.log("ID de Telegram obtenido:", userData.id);
            console.log("Datos de usuario:", userData);

            // ➡️ Envía el ID y la información de usuario al servidor
            enviarIdAServidor(userData.id, userData);

        } else {
            idDisplay.textContent = "ID no encontrado.";
            console.error("No se pudo obtener el ID del usuario.");
        }
    } else {
        idDisplay.textContent = "Error: no estás en Telegram WebApp.";
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
