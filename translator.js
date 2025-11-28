document.getElementById('translateBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('fileInput');
    const languageSelect = document.getElementById('languageSelect');
    const status = document.getElementById('statusMessage');
    status.textContent = '';

    if (!fileInput.files.length) {
        status.style.color = 'red';
        status.textContent = 'Please select a .txt file.';
        return;
    }
    if (!languageSelect.value) {
        status.style.color = 'red';
        status.textContent = 'Please select a language.';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('language', languageSelect.value);

    status.style.color = 'black';
    status.textContent = 'Translating...';

    try {
        const resp = await fetch('/translate', {
            method: 'POST',
            body: formData
        });

        if (!resp.ok) {
            const err = await resp.json().catch(() => ({error: 'Unknown error'}));
            status.style.color = 'red';
            status.textContent = 'Error: ' + err.error;
            return;
        }

        const blob = await resp.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'translated.txt';
        a.click();
        window.URL.revokeObjectURL(url);

        status.style.color = 'green';
        status.textContent = 'Translation complete!';
    } catch (error) {
        status.style.color = 'red';
        status.textContent = 'Error: ' + error;
    }
});
