const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const fileInput = document.getElementById('file-input');
const fileNameDisplay = document.getElementById('file-name');
const uploadArea = document.getElementById('upload-area');
const textInput = document.getElementById('email-text');
const loadingOverlay = document.getElementById('loading-overlay');
const resultsSection = document.getElementById('results-section');
const categoryBadge = document.getElementById('category-badge');
const responseContent = document.getElementById('response-content');

let currentFile = null;

// Tab Switching
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.target).classList.add('active');
    });
});

// File Handling
fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

function handleFile(file) {
    if (!file) return;
    currentFile = file;
    fileNameDisplay.textContent = `Arquivo selecionado: ${file.name}`;
    uploadBtn.disabled = false;
}

// Text Handling
textInput.addEventListener('input', () => {
    textBtn.disabled = textInput.value.trim().length === 0;
});

// API Calls
uploadBtn.addEventListener('click', () => submitData({ file: currentFile }));
textBtn.addEventListener('click', () => submitData({ text: textInput.value }));

async function submitData(data) {
    setLoading(true);

    try {
        const formData = new FormData();
        if (data.file) {
            formData.append('file', data.file);
        } else {
            formData.append('text', data.text);
        }

        const response = await fetch('/api/classify', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro ao processar');
        }

        const result = await response.json();
        afficherResults(result);

    } catch (error) {
        alert('Erro: ' + error.message);
    } finally {
        setLoading(false);
    }
}

function afficherResults(result) {
    const isProd = result.category.toLowerCase().includes('produtivo') && !result.category.toLowerCase().includes('improdutivo');

    categoryBadge.className = 'badge ' + (isProd ? 'produtivo' : 'improdutivo');
    categoryBadge.textContent = isProd ? 'Produtivo' : 'Improdutivo';

    // Display original email
    const emailOriginal = document.getElementById('email-original');
    emailOriginal.textContent = result.raw_text_preview || result.email_original || 'Texto não disponível';

    // Display response
    responseContent.textContent = result.reply;

    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function setLoading(active) {
    if (active) {
        loadingOverlay.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
    }
}

function resetApp() {
    resultsSection.classList.add('hidden');
    textInput.value = '';
    fileInput.value = '';
    fileNameDisplay.textContent = '';
    currentFile = null;
    uploadBtn.disabled = true;
    textBtn.disabled = true;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function copyResponse() {
    try {
        await navigator.clipboard.writeText(responseContent.textContent);
        const originalText = document.querySelector('.secondary-btn').textContent;
        // Optionally show feedback
    } catch (err) {
        console.error('Failed to copy', err);
    }
}
