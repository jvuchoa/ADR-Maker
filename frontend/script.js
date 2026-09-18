document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const userInput = document.getElementById('user-input');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');
    const outputSection = document.getElementById('output-section');
    const adrResult = document.getElementById('adr-result');
    const copyBtn = document.getElementById('copy-btn');
    const rawMarkdown = document.getElementById('raw-markdown');

    generateBtn.addEventListener('click', async () => {
        const text = userInput.value.trim();
        
        if (!text) {
            showError("Por favor, insira algum texto.");
            return;
        }

        // Reset UI
        hideError();
        outputSection.classList.add('hidden');
        loading.classList.remove('hidden');
        generateBtn.disabled = true;

        try {
            const response = await fetch('/api/generate-adr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_input: text })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Erro desconhecido ao gerar o ADR.");
            }

            // Render Markdown
            rawMarkdown.value = data.markdown_content;
            adrResult.innerHTML = DOMPurify.sanitize(marked.parse(data.markdown_content));
            
            outputSection.classList.remove('hidden');
        } catch (error) {
            showError(error.message);
        } finally {
            loading.classList.add('hidden');
            generateBtn.disabled = false;
        }
    });

    copyBtn.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(rawMarkdown.value);
            const originalText = copyBtn.innerText;
            copyBtn.innerText = "Copiado!";
            setTimeout(() => {
                copyBtn.innerText = originalText;
            }, 2000);
        } catch (err) {
            alert('Falha ao copiar texto.');
        }
    });

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.classList.add('hidden');
    }
});
