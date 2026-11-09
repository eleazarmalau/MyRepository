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

    function educationActionUrl(template, id) {
        if (!template) return null;
        return safeUrl(template.replace(
            '00000000-0000-0000-0000-000000000000', encodeURIComponent(id),
        ), true);
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

    function errorMessages(value) {
        if (typeof value === 'string') return [value];
        if (Array.isArray(value)) return value.flatMap(errorMessages);
        if (value && typeof value === 'object') return Object.values(value).flatMap(errorMessages);
        return [];
    }

    function apiErrorMessage(data, fallback) {
        return errorMessages(data).join(' ') || fallback;
    }

    async function writeEducation(url, method, payload) {
        const target = safeUrl(url, true);
        if (!target) throw new Error('Alamat aksi tidak valid.');
        const response = await fetch(target, {
            method,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            credentials: 'same-origin',
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });
        if (response.status === 204) return { response, data: null };
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

    function setStarButton(button, education) {
        button.textContent = `${education.is_starred ? '★ Unstar' : '☆ Star'} (${education.star_count})`;
        button.setAttribute('aria-pressed', String(education.is_starred));
    }

    function renderEducation(education) {
        const row = element('li', `timeline-item${education.end_year == null ? ' is-current' : ''}`);
        const pin = element('div', 'timeline-pin');
        pin.setAttribute('aria-hidden', 'true');
        const card = element('article', 'timeline-card');
        const imageUrl = safeUrl(education.thumbnail);
        if (imageUrl) {
            const imageWrapper = element('div', 'timeline-card-thumbnail');
            const image = element('img', 'timeline-logo');
            image.src = imageUrl;
            image.alt = `${education.institution} logo`;
            image.width = 64;
            image.height = 64;
            image.loading = 'lazy';
            imageWrapper.append(image);
            card.append(imageWrapper);
        }
        const content = element('div', 'timeline-card-content');
        const heading = element('div', 'timeline-card-heading');
        const headingText = element('div');
        if (education.end_year == null) headingText.append(element('span', 'current-label', 'Currently Studying'));
        headingText.append(element('h2', '', education.title), element('p', 'timeline-institution', education.institution));
        heading.append(headingText, element('p', 'timeline-period', `${education.start_year} – ${education.end_year ?? 'Present'}`));
        const body = element('div', 'timeline-card-body');
        const details = element('div');
        details.append(element('p', 'timeline-major', education.major));
        const lines = String(education.description ?? '').split(/\r?\n/).map(line => line.trim()).filter(Boolean);
        if (lines.length) {
            const bullets = element('ul', 'timeline-details');
            lines.forEach(line => bullets.append(element('li', '', line)));
            details.append(bullets);
        }
        body.append(details);
        const actions = element('div', 'education-card-actions');
        const updateUrl = educationActionUrl(config.updateUrlTemplate, education.id);
        if (updateUrl) {
            const update = element('a', 'button education-update-button', 'Update');
            update.href = updateUrl;
            actions.append(update);
        }
        const deleteUrl = educationActionUrl(config.deleteUrlTemplate, education.id);
        if (deleteUrl && deleteForm) {
            const remove = element('button', 'button education-delete-button', 'Hapus Pendidikan');
            remove.type = 'button';
            remove.addEventListener('click', () => {
                deleteForm.action = deleteUrl;
                document.getElementById('delete-education-name').textContent = `${education.title} di ${education.institution}`;
                document.getElementById('delete-education-modal').showPopover();
            });
            actions.append(remove);
        }
        const starUrl = educationActionUrl(config.starUrlTemplate, education.id);
        if (config.isAuthenticated && starUrl) {
            const star = element('button', 'button button-star');
            star.type = 'button';
            setStarButton(star, education);
            star.addEventListener('click', async () => {
                star.disabled = true;
                try {
                    const { response, data } = await writeEducation(starUrl, 'POST');
                    if (!response.ok) throw new Error(apiErrorMessage(data, 'Star gagal diperbarui.'));
                    education.star_count = data.star_count;
                    education.is_starred = data.is_starred;
                    setStarButton(star, education);
                    toast('Star berhasil diperbarui.', 'success');
                } catch (error) {
                    toast(error.message);
                } finally {
                    star.disabled = false;
                }
            });
            actions.append(star);
        } else {
            const login = element('a', 'button button-star', `☆ Login to star (${education.star_count})`);
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
            addForm.querySelectorAll('[aria-invalid]').forEach(node => {
                node.removeAttribute('aria-invalid');
                node.removeAttribute('aria-describedby');
            });
            submit.disabled = true;
            try {
                const formData = new FormData(addForm);
                const payload = Object.fromEntries([
                    'title', 'institution', 'major', 'description', 'thumbnail',
                    'start_year', 'end_year',
                ].map(name => [name, formData.get(name)]));
                // Empty HTML inputs are strings; the API expects null for an ongoing education.
                if (!payload.end_year) payload.end_year = null;
                const { response, data } = await writeEducation(config.createUrl, 'POST', payload);
                if (!response.ok) {
                    Object.entries(data || {}).forEach(([name, errors]) => {
                        const message = errorMessages(errors).join(' ');
                        const errorField = name === 'non_field_errors' ? '__all__' : name;
                        const output = Array.from(addForm.querySelectorAll('[data-error-field]')).find(node => node.dataset.errorField === errorField);
                        if (output) { output.textContent = message; output.hidden = false; }
                        const field = addForm.elements.namedItem(name);
                        if (field) {
                            field.setAttribute('aria-invalid', 'true');
                            if (output) field.setAttribute('aria-describedby', output.id);
                        }
                    });
                    throw new Error(apiErrorMessage(data, 'Pendidikan gagal ditambahkan.'));
                }
                addForm.reset();
                document.getElementById('add-education-modal').hidePopover();
                toast('Pendidikan berhasil ditambahkan!', 'success');
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
                const { response, data } = await writeEducation(deleteForm.action, 'DELETE');
                if (!response.ok) throw new Error(apiErrorMessage(data, 'Pendidikan gagal dihapus.'));
                document.getElementById('delete-education-modal').hidePopover();
                toast('Pendidikan berhasil dihapus!', 'success');
                clearTimeout(debounceTimer);
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
