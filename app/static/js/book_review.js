document.addEventListener('DOMContentLoaded', async function() {
    const grid = document.getElementById('books-review-grid');
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    // Obtener el tipo de lista desde la URL
    const pathParts = window.location.pathname.split('/');
    const lista = decodeURIComponent(pathParts[pathParts.length - 1]);
    // Mapear nombre de lista a filtro
    let filtro = () => true;
    if (lista === 'por leer') filtro = i => i.status === 'to-read';
    if (lista === 'leyendo actualmente') filtro = i => i.status === 'reading';
    if (lista === 'leídos recientemente') filtro = i => i.status === 'completed';
    if (lista === 'favoritos') filtro = i => i.is_favorite === true;
    // 1. Obtener todas las interacciones del usuario
    const resp = await fetch('/interactions/', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    if (!resp.ok) return;
    const interacciones = await resp.json();
    // 2. Filtrar según la lista
    const librosFiltrados = interacciones.filter(filtro);
    grid.innerHTML = '';
    for (const inter of librosFiltrados) {
        const bookResp = await fetch(`/books/${inter.book_id}`);
        if (!bookResp.ok) continue;
        const html = await bookResp.text();
        const temp = document.createElement('div');
        temp.innerHTML = html;
        // Extraer portada, título, autor, y el primer género
        const img = temp.querySelector('.book-cover img, .book-cover-large img');
        const titulo = temp.querySelector('h1, h3');
        const autor = temp.querySelector('h3, .book-author');
        const generoPrincipal = temp.querySelector('.book-genres span');
        // Renderizar tarjeta
        const card = document.createElement('div');
        card.className = 'book-card-review';
        card.innerHTML = `
            <div class="book-cover">
                <img src="${img ? img.src : '/static/img/default_cover.webp'}" alt="Portada de ${titulo ? titulo.textContent : ''}">
            </div>
            <div class="book-title" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px;">${titulo ? titulo.textContent : ''}</div>
            <div class="book-author">${autor ? autor.textContent : ''}</div>
            <div class="book-tags">
                ${generoPrincipal ? `<span>${generoPrincipal.textContent}</span>` : ''}
            </div>
            <div class="book-actions">
                <div class="book-actions-row">
                    <button class="favorite-btn${inter.is_favorite ? '' : ' inactive'}" title="Favorito">
                        <i class="ri-heart${inter.is_favorite ? '-fill' : '-line'}"></i>
                    </button>
                    <button class="delete-interaction-btn" title="Eliminar">
                        <i class="ri-close-line"></i>
                    </button>
                </div>
                <div class="book-actions-row2">
                    <div class="dropdown" style="position: relative;">
                        <button class="review-btn">Lista <i class="ri-arrow-down-s-line"></i></button>
                        <div class="dropdown-menu" style="display: none; position: absolute; left: 0; top: 110%; width: 180px; background: #fff; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); z-index: 10; overflow: hidden;">
                            <a href="#" class="dropdown-item" data-status="to-read" style="display: flex; align-items: center; gap: 0.7em; padding: 0.8em 1.2em; color: #29436d; text-decoration: none; font-size: 0.95em;"><i class="ri-bookmark-line" style="font-size: 1.1em;"></i> Por leer</a>
                            <a href="#" class="dropdown-item" data-status="reading" style="display: flex; align-items: center; gap: 0.7em; padding: 0.8em 1.2em; color: #29436d; text-decoration: none; font-size: 0.95em;"><i class="ri-book-open-line" style="font-size: 1.1em;"></i> Leyendo</a>
                            <a href="#" class="dropdown-item" data-status="completed" style="display: flex; align-items: center; gap: 0.7em; padding: 0.8em 1.2em; color: #29436d; text-decoration: none; font-size: 0.95em;"><i class="ri-checkbox-circle-line" style="font-size: 1.1em;"></i> Leído</a>
                        </div>
                    </div>
                    <a href="/books/${inter.book_id}/rate" class="review-btn review-link-btn">Reseñar</a>
                </div>
            </div>
        `;
        grid.appendChild(card);
        // Dropdown funcionalidad
        setTimeout(() => {
            const dropdown = card.querySelector('.dropdown');
            const btn = dropdown.querySelector('button.review-btn');
            const menu = dropdown.querySelector('.dropdown-menu');
            // Mostrar el estado actual en el botón
            if (inter.status) {
                let estadoTxt = '';
                if (inter.status === 'to-read') estadoTxt = 'Por leer';
                if (inter.status === 'reading') estadoTxt = 'Leyendo';
                if (inter.status === 'completed') estadoTxt = 'Leído';
                btn.innerHTML = estadoTxt + ' <i class="ri-arrow-down-s-line"></i>';
            }
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
            });
            document.addEventListener('click', function(e) {
                if (!dropdown.contains(e.target)) menu.style.display = 'none';
            });
            // Métodos de interacción con las listas
            menu.querySelectorAll('.dropdown-item').forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const status = item.getAttribute('data-status');
                    if (!status) return;
                    const method = inter ? 'PATCH' : 'POST';
                    const url = inter ? `/interactions/${inter.book_id}` : '/interactions/';
                    const body = inter ? { status: status } : { book_id: inter.book_id, status: status };
                    fetch(url, {
                        method,
                        headers: {
                            'Authorization': 'Bearer ' + token,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(body)
                    })
                    .then(async r => {
                        if (!r.ok) {
                            alert('Error al actualizar la lista');
                            return null;
                        }
                        return r.json();
                    })
                    .then(data => {
                        if (data) {
                            // Actualizar el texto del botón con el nuevo estado
                            let estadoTxt = '';
                            if (data.status === 'to-read') estadoTxt = 'Por leer';
                            if (data.status === 'reading') estadoTxt = 'Leyendo';
                            if (data.status === 'completed') estadoTxt = 'Leído';
                            btn.innerHTML = estadoTxt + ' <i class="ri-arrow-down-s-line"></i>';
                            item.closest('.dropdown-menu').style.display = 'none';
                        }
                    });
                });
            });
            // Favorito (corazón)
            const favBtn = card.querySelector('.favorite-btn');
            favBtn.addEventListener('click', function(e) {
                e.preventDefault();
                fetch(`/interactions/${inter.book_id}`, {
                    method: 'PATCH',
                    headers: {
                        'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ is_favorite: !inter.is_favorite })
                })
                .then(async r => {
                    if (!r.ok) {
                        window.alert('Error al actualizar favorito');
                        return null;
                    }
                    return r.json();
                })
                .then(data => {
                    if (data) {
                        inter.is_favorite = data.is_favorite;
                        favBtn.classList.toggle('inactive', !data.is_favorite);
                        favBtn.querySelector('i').className = 'ri-heart' + (data.is_favorite ? '-fill' : '-line');
                    }
                });
            });
            // Eliminar interacción (botón x)
            const delBtn = card.querySelector('.delete-interaction-btn');
            delBtn.addEventListener('click', function(e) {
                e.preventDefault();
                if (window.confirm('¿Quieres eliminarlo? Perderás la calificación y reseñas realizadas')) {
                    fetch(`/interactions/${inter.book_id}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': 'Bearer ' + token }
                    })
                    .then(async r => {
                        if (!r.ok) {
                            window.alert('Error al eliminar la relación');
                            return;
                        }
                        card.remove();
                    });
                }
            });
        }, 0);
    }
    // Set dynamic title
    const titleMap = {
        'por leer': 'Por leer',
        'leyendo actualmente': 'Leyendo actualmente',
        'leídos recientemente': 'Leídos recientemente',
        'favoritos': 'Favoritos'
    };
    document.getElementById('review-list-title').textContent = titleMap[lista] || 'Libros';
});