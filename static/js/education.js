(() => {
    const configElement = document.getElementById('education-config');
    if (!configElement) return;
    const config = JSON.parse(configElement.textContent);
    const list = document.getElementById('education-list');
    const search = document.getElementById('education-search');
    const feedback = document.getElementById('education-feedback');
    const stateText = document.getElementById('education-state-text');
    const retry = document.getElementById('education-retry');
    const addForm = document.getElementById('education-form');
    const deleteForm = document.getElementById('education-delete-form');
    let controller;
    let debounceTimer;
    let latestRequest = 0;

    function element(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined) node.textContent = String(text ?? '');
        return node;
    }

    function getCookie(name) {
        const cookie = document.cookie.split('; ').find(value => value.startsWith(`${name}=`));
        return cookie ? decodeURIComponent(cookie.slice(name.length + 1)) : '';
    }

    function safeUrl(value, sameOrigin = false) {
        if (!value) return null;
        try {
            const url = new URL(value, window.location.origin);
            if (!['http:', 'https:'].includes(url.protocol)) return null;
            if (sameOrigin && url.origin !== window.location.origin) return null;
            return url.href;
        } catch {
            return null;
        }
    }

    function toast(message, type = 'error') {
        if (typeof window.showToast === 'function') {
            window.showToast(type === 'success' ? 'Berhasil' : 'Ada kendala', message, type, 5000);
        }
    }

    async function readJson(response) {
        if (!response.headers.get('content-type')?.includes('application/json')) {
            throw new Error('Server tidak mengirim JSON. Periksa sesi login atau coba lagi.');
        }
        return response.json();
    }

    async function post(url, body) {
        const target = safeUrl(url, true);
        if (!target) throw new Error('Alamat aksi tidak valid.');
        const response = await fetch(target, {
            method: 'POST',
            headers: { 'Accept': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            credentials: 'same-origin',
            body,
        });
        const data = await readJson(response);
        return { response, data };
    }

    function setState(message, isError = false) {
        list.hidden = true;
        list.replaceChildren();
        feedback.hidden = false;
        stateText.textContent = message;
        retry.hidden = !isError;
    }

    function setStarButton(button, fields) {
        button.textContent = `${fields.is_starred ? '★ Unstar' : '☆ Star'} (${fields.star_count})`;
        button.setAttribute('aria-pressed', String(fields.is_starred));
    }

    function renderEducation(item) {
        const fields = item.fields;
        const urls = item.urls || {};
        const row = element('li', `timeline-item${fields.end_year == null ? ' is-current' : ''}`);
        const pin = element('div', 'timeline-pin');
        pin.setAttribute('aria-hidden', 'true');
        const card = element('article', 'timeline-card');
        const imageUrl = safeUrl(fields.thumbnail);
        if (imageUrl) {
            const imageWrapper = element('div', 'timeline-card-thumbnail');
            const image = element('img', 'timeline-logo');
            image.src = imageUrl;
            image.alt = `${fields.institution} logo`;
            image.width = 64;
            image.height = 64;
            image.loading = 'lazy';
            imageWrapper.append(image);
            card.append(imageWrapper);
        }
        const content = element('div', 'timeline-card-content');
        const heading = element('div', 'timeline-card-heading');
        const headingText = element('div');
        if (fields.end_year == null) headingText.append(element('span', 'current-label', 'Currently Studying'));
        headingText.append(element('h2', '', fields.title), element('p', 'timeline-institution', fields.institution));
        heading.append(headingText, element('p', 'timeline-period', `${fields.start_year} – ${fields.end_year ?? 'Present'}`));
        const body = element('div', 'timeline-card-body');
        const details = element('div');
        details.append(element('p', 'timeline-major', fields.major));
        const lines = String(fields.description ?? '').split(/\r?\n/).map(line => line.trim()).filter(Boolean);
        if (lines.length) {
            const bullets = element('ul', 'timeline-details');
            lines.forEach(line => bullets.append(element('li', '', line)));
            details.append(bullets);
        }
        body.append(details);
        const actions = element('div', 'education-card-actions');
        const updateUrl = safeUrl(urls.update, true);
        if (updateUrl) {
            const update = element('a', 'button education-update-button', 'Update');
            update.href = updateUrl;
            actions.append(update);
        }
        const deleteUrl = safeUrl(urls.delete, true);
        if (deleteUrl && deleteForm) {
            const remove = element('button', 'button education-delete-button', 'Hapus Pendidikan');
            remove.type = 'button';
            remove.addEventListener('click', () => {
                deleteForm.action = deleteUrl;
                document.getElementById('delete-education-name').textContent = `${fields.title} di ${fields.institution}`;
                document.getElementById('delete-education-modal').showPopover();
            });
            actions.append(remove);
        }
        const starUrl = safeUrl(urls.star, true);
        if (config.isAuthenticated && starUrl) {
            const star = element('button', 'button button-star');
            star.type = 'button';
            setStarButton(star, fields);
            star.addEventListener('click', async () => {
                star.disabled = true;
                try {
                    const { response, data } = await post(starUrl);
                    if (!response.ok) throw new Error(data.message || 'Star gagal diperbarui.');
                    fields.star_count = data.star_count;
                    fields.is_starred = data.is_starred;
                    setStarButton(star, fields);
                    toast(data.message, 'success');
                } catch (error) {
                    toast(error.message);
                } finally {
                    star.disabled = false;
                }
            });
            actions.append(star);
        } else {
            const login = element('a', 'button button-star', `☆ Login to star (${fields.star_count})`);
            login.href = safeUrl(config.loginUrl, true);
            actions.append(login);
        }
        content.append(heading, body, actions);
        card.append(content);
        row.append(pin, card);
        return row;
    }

    async function loadEducations() {
        controller?.abort();
        controller = new AbortController();
        const requestId = ++latestRequest;
        setState('Memuat data pendidikan...');
        list.setAttribute('aria-busy', 'true');
        const url = new URL(config.listUrl, window.location.origin);
        if (search.value.trim()) url.searchParams.set('title', search.value.trim());
        try {
            const response = await fetch(url, {
                headers: { 'Accept': 'application/json' },
                credentials: 'same-origin',
                signal: controller.signal,
                cache: 'no-store',
            });
            const data = await readJson(response);
            if (!response.ok || !Array.isArray(data)) throw new Error('Data pendidikan gagal dimuat.');
            if (requestId !== latestRequest) return;
            if (!data.length) {
                setState(search.value.trim() ? 'No education matches your search.' : 'No education has been added yet.');
                return;
            }
            const fragment = document.createDocumentFragment();
            data.forEach(item => fragment.append(renderEducation(item)));
            list.replaceChildren(fragment);
            list.hidden = false;
            feedback.hidden = true;
        } catch (error) {
            if (error.name === 'AbortError' || requestId !== latestRequest) return;
            setState('Data gagal dimuat. Periksa koneksi, lalu coba lagi.', true);
            toast(error.message);
        } finally {
            if (requestId === latestRequest) list.setAttribute('aria-busy', 'false');
        }
    }

    // Debouncing waits until typing pauses, instead of requesting every keystroke.
    search.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        controller?.abort();
        debounceTimer = setTimeout(loadEducations, 350);
    });
    retry.addEventListener('click', loadEducations);

    // The owner-only modal does not exist for visitors, regular users, or Editors.
    if (addForm) {
        addForm.addEventListener('submit', async event => {
            event.preventDefault();
            const submit = addForm.querySelector('[type="submit"]');
            addForm.querySelectorAll('[data-error-field]').forEach(node => { node.textContent = ''; node.hidden = true; });
            addForm.querySelectorAll('[aria-invalid]').forEach(node => node.removeAttribute('aria-invalid'));
            submit.disabled = true;
            try {
                const { response, data } = await post(config.createUrl, new FormData(addForm));
                if (!response.ok) {
                    const messages = [];
                    Object.entries(data.errors || {}).forEach(([name, errors]) => {
                        const message = errors.map(error => error.message).join(' ');
                        const output = Array.from(addForm.querySelectorAll('[data-error-field]')).find(node => node.dataset.errorField === name);
                        if (output) { output.textContent = message; output.hidden = false; }
                        const field = addForm.elements.namedItem(name);
                        if (field) {
                            field.setAttribute('aria-invalid', 'true');
                            if (output) field.setAttribute('aria-describedby', output.id);
                        }
                        messages.push(message);
                    });
                    throw new Error(messages.join(' ') || data.message || 'Pendidikan gagal ditambahkan.');
                }
                addForm.reset();
                document.getElementById('add-education-modal').hidePopover();
                toast(data.message, 'success');
                // Clear an old search so the newly added record is visible.
                clearTimeout(debounceTimer);
                search.value = '';
                await loadEducations();
            } catch (error) {
                toast(error.message);
            } finally {
                submit.disabled = false;
            }
        });
    }

    if (deleteForm) {
        deleteForm.addEventListener('submit', async event => {
            event.preventDefault();
            const submit = deleteForm.querySelector('[type="submit"]');
            submit.disabled = true;
            try {
                const { response, data } = await post(deleteForm.action, new FormData(deleteForm));
                if (!response.ok) throw new Error(data.message || 'Pendidikan gagal dihapus.');
                document.getElementById('delete-education-modal').hidePopover();
                toast(data.message, 'success');
                await loadEducations();
            } catch (error) {
                toast(error.message);
            } finally {
                submit.disabled = false;
            }
        });
    }
    loadEducations();
})();