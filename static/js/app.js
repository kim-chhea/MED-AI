// Tab switching
function switchTab(tabName) {
    // Hide all tab panes
    const panes = document.querySelectorAll('.tab-pane');
    panes.forEach(pane => pane.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked button
    event.target.closest('.tab-button').classList.add('active');
}

// Side Effects Analysis
function analyzeSideEffects() {
    const drugName = document.getElementById('drugName').value.trim();

    if (!drugName) {
        showError('sideEffectsError', 'Please enter a drug name');
        return;
    }

    hideAllResults('sideEffects');
    showLoading('sideEffectsLoading');

    fetch('/api/side-effects', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ drug_name: drugName })
    })
        .then(response => response.json())
        .then(data => {
            hideLoading('sideEffectsLoading');
            if (data.result) {
                showResult('sideEffectsResult', data.result);
            } else if (data.error) {
                showError('sideEffectsError', data.error);
            }
        })
        .catch(error => {
            hideLoading('sideEffectsLoading');
            showError('sideEffectsError', `Error: ${error.message}`);
        });
}

// Drug Interactions
function addDrugInput() {
    const container = document.getElementById('drugInputs');
    const row = document.createElement('div');
    row.className = 'drug-input-row';
    row.innerHTML = `
        <input 
            type="text" 
            placeholder="Drug ${container.children.length + 1}"
            class="input-field drug-input"
        >
        <button onclick="removeDrugInput(this)" class="btn btn-secondary">−</button>
    `;
    container.appendChild(row);
}

function removeDrugInput(button) {
    const container = document.getElementById('drugInputs');
    if (container.children.length > 2) {
        button.closest('.drug-input-row').remove();
    }
}

function checkInteractions() {
    const inputs = document.querySelectorAll('.drug-input');
    const drugs = Array.from(inputs)
        .map(input => input.value.trim())
        .filter(val => val.length > 0);

    if (drugs.length < 2) {
        showError('interactionsError', 'Please enter at least 2 drugs');
        return;
    }

    hideAllResults('interactions');
    showLoading('interactionsLoading');

    fetch('/api/interactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ drug_list: drugs })
    })
        .then(response => response.json())
        .then(data => {
            hideLoading('interactionsLoading');
            if (data.result) {
                showResult('interactionsResult', data.result);
            } else if (data.error) {
                showError('interactionsError', data.error);
            }
        })
        .catch(error => {
            hideLoading('interactionsLoading');
            showError('interactionsError', `Error: ${error.message}`);
        });
}

// Image Analysis
function previewImage() {
    const fileInput = document.getElementById('drugImage');
    const preview = document.getElementById('imagePreview');
    const img = document.getElementById('previewImg');

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
            img.src = e.target.result;
            preview.classList.remove('hidden');
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
}

function clearImage() {
    document.getElementById('drugImage').value = '';
    document.getElementById('imagePreview').classList.add('hidden');
}

function analyzeImage() {
    const fileInput = document.getElementById('drugImage');

    if (!fileInput.files || !fileInput.files[0]) {
        showError('imageError', 'Please select an image file');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    hideAllResults('image');
    showLoading('imageLoading');

    fetch('/api/analyze-image', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            hideLoading('imageLoading');
            if (data.result) {
                showResult('imageResult', data.result);
            } else if (data.error) {
                showError('imageError', data.error);
            }
        })
        .catch(error => {
            hideLoading('imageLoading');
            showError('imageError', `Error: ${error.message}`);
        });
}

// Utility Functions
function showLoading(elementId) {
    document.getElementById(elementId).classList.remove('hidden');
}

function hideLoading(elementId) {
    document.getElementById(elementId).classList.add('hidden');
}

function showResult(elementId, result) {
    const container = document.getElementById(elementId);
    container.querySelector('.result-content').textContent = result;
    container.classList.remove('hidden');
}

function showError(elementId, error) {
    const container = document.getElementById(elementId);
    container.textContent = error;
    container.classList.remove('hidden');
}

function hideAllResults(prefix) {
    const resultId = `${prefix}Result`;
    const errorId = `${prefix}Error`;

    const result = document.getElementById(resultId);
    const error = document.getElementById(errorId);

    if (result) result.classList.add('hidden');
    if (error) error.classList.add('hidden');
}

// Drag and drop for file upload
document.addEventListener('DOMContentLoaded', () => {
    const fileLabel = document.querySelector('.file-label');
    const fileInput = document.getElementById('drugImage');

    if (fileLabel) {
        fileLabel.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileLabel.style.borderColor = 'var(--primary-color)';
            fileLabel.style.background = 'rgba(37, 99, 235, 0.1)';
        });

        fileLabel.addEventListener('dragleave', () => {
            fileLabel.style.borderColor = 'var(--border-color)';
            fileLabel.style.background = 'transparent';
        });

        fileLabel.addEventListener('drop', (e) => {
            e.preventDefault();
            fileLabel.style.borderColor = 'var(--border-color)';
            fileLabel.style.background = 'transparent';

            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                fileInput.files = e.dataTransfer.files;
                previewImage();
            }
        });
    }
});

// Allow Enter key to submit
document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const activeTab = document.querySelector('.tab-pane.active').id;

        if (activeTab === 'side-effects') {
            analyzeSideEffects();
        } else if (activeTab === 'interactions') {
            checkInteractions();
        }
    }
});
