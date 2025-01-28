// Analyse le code saisi par l'utilisateur
async function analyzeCode() {
    const codeInput = document.getElementById('code-input').value;
    const responseOutput = document.getElementById('response-output');

    if (codeInput.trim() === '') {
        responseOutput.textContent = "Veuillez entrer du code pour l'analyser.";
        return;
    }

    responseOutput.textContent = "Analyse en cours...";
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: codeInput })
        });

        const result = await response.json();
        responseOutput.textContent = result.response;
    } catch (error) {
        responseOutput.textContent = "Une erreur s'est produite pendant l'analyse.";
        console.error(error);
    }
}

// Téléverse un fichier pour analyse
async function uploadFile() {
    const fileInput = document.getElementById('file-input');
    const responseOutput = document.getElementById('response-output');

    if (!fileInput.files.length) {
        responseOutput.textContent = "Veuillez choisir un fichier.";
        return;
    }

    responseOutput.textContent = "Téléversement et analyse en cours...";
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        responseOutput.textContent = result.response;
    } catch (error) {
        responseOutput.textContent = "Une erreur s'est produite pendant le téléversement.";
        console.error(error);
    }
}

// Ajoute les événements aux boutons
document.getElementById('analyze-code-btn').addEventListener('click', analyzeCode);
document.getElementById('upload-file-btn').addEventListener('click', uploadFile);
