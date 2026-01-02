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
                // Check if result contains error with suggestions
                if (data.result.error) {
                    showError('sideEffectsError', data.result);
                } else {
                    showResult('sideEffectsResult', data.result);
                }
            } else if (data.error) {
                showError('sideEffectsError', data.error);
            }
        })
        .catch(error => {
            hideLoading('sideEffectsLoading');
            showError('sideEffectsError', `Error: ${error.message}`);
        });
}

// Drug Interactions with Tags
let drugTags = [];

function handleDrugTagInput(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const input = document.getElementById('drugInteractionInput');
        const drugName = input.value.trim();
        
        if (drugName && !drugTags.includes(drugName)) {
            drugTags.push(drugName);
            renderDrugTags();
            input.value = '';
        }
    }
}

function renderDrugTags() {
    const container = document.getElementById('drugTags');
    container.innerHTML = '';
    
    drugTags.forEach((drug, index) => {
        const tag = document.createElement('div');
        tag.className = 'drug-tag';
        tag.innerHTML = `
            <span class="tag-text">${drug}</span>
            <button class="remove-tag" onclick="removeDrugTag(${index})">✕</button>
        `;
        container.appendChild(tag);
    });
}

function removeDrugTag(index) {
    drugTags.splice(index, 1);
    renderDrugTags();
}

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
    // Use drugTags array instead of input fields
    if (drugTags.length < 2) {
        showError('interactionsError', 'Please add at least 2 drugs');
        return;
    }

    hideAllResults('interactions');
    showLoading('interactionsLoading');

    fetch('/api/interactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ drug_list: drugTags })
    })
        .then(response => response.json())
        .then(data => {
            hideLoading('interactionsLoading');
            if (data.result) {
                // Check if result contains error with suggestions
                if (data.result.error) {
                    showError('interactionsError', data.result);
                } else {
                    showResult('interactionsResult', data.result);
                }
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
    const dropZone = document.getElementById('dropZone');

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
            img.src = e.target.result;
            preview.classList.remove('hidden');
            dropZone.style.display = 'none';
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
}

function clearImage() {
    const fileInput = document.getElementById('drugImage');
    const preview = document.getElementById('imagePreview');
    const img = document.getElementById('previewImg');
    const dropZone = document.getElementById('dropZone');
    
    // Clear the image file input
    fileInput.value = '';
    // Clear the image source
    img.src = '';
    // Hide the preview
    preview.classList.add('hidden');
    // Show the upload zone again
    dropZone.style.display = 'block';
    // Clear any results
    hideAllResults('image');
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
    const contentDiv = container.querySelector('.result-content');
    
    // Handle ML model response format
    if (typeof result === 'object') {
        if (result.error) {
            showError(elementId.replace('Result', 'Error'), result.error);
            return;
        }
        
        // Format side effects result
        if (result.side_effects) {
            let html = `<h3>💊 ${result.drug}</h3>`;
            html += `<p><strong>Total Side Effects:</strong> ${result.count}</p>`;
            
            // Show common effects
            if (result.common_effects && result.common_effects.length > 0) {
                html += '<div class="effects-section" style="margin: 15px 0; padding: 15px; background: #e8f5e9; border-radius: 8px; border-left: 4px solid #4caf50;">';
                html += '<h4 style="margin-top: 0; color: #2e7d32;">✓ Common Side Effects (' + result.common_count + ')</h4>';
                html += '<ul class="side-effects-list">';
                result.common_effects.forEach(effect => {
                    html += `<li>• ${effect}</li>`;
                });
                html += '</ul>';
                html += '</div>';
            }
            
            // Show serious effects
            if (result.serious_effects && result.serious_effects.length > 0) {
                html += '<div class="effects-section" style="margin: 15px 0; padding: 15px; background: #ffebee; border-radius: 8px; border-left: 4px solid #f44336;">';
                html += '<h4 style="margin-top: 0; color: #c62828;">⚠️ Serious Side Effects (' + result.serious_count + ')</h4>';
                html += '<ul class="side-effects-list">';
                result.serious_effects.forEach(effect => {
                    html += `<li>• ${effect}</li>`;
                });
                html += '</ul>';
                html += '</div>';
            }
            
            contentDiv.innerHTML = html;
        }
        // Format interaction result
        else if (result.interaction_risk) {
            const riskIcon = result.interaction_risk === 'Dangerous' ? '🔴' : 
                           result.interaction_risk === 'Moderate' ? '🟡' : '🟢';
            let html = `<h3>${riskIcon} Drug Interaction Analysis</h3>`;
            html += `<p style="font-size: 18px;"><strong>${result.drugA}</strong> + <strong>${result.drugB}</strong></p>`;
            html += `<p class="risk-level risk-${result.interaction_risk.toLowerCase()}" style="font-size: 20px; padding: 15px; border-radius: 8px; font-weight: bold; text-align: center;">Risk Level: ${result.interaction_risk}</p>`;
            html += `<p><strong>Confidence:</strong> ${result.confidence}</p>`;
            
            // Show detailed explanation in a highlighted box
            html += '<div style="margin: 20px 0; padding: 20px; background: #f5f5f5; border-radius: 8px; border-left: 4px solid #2196F3;">';
            html += '<h4 style="margin-top: 0; color: #1976D2;">📋 What Happens When Taking Both Drugs Together:</h4>';
            html += `<p class="description" style="line-height: 1.8; color: #333;">${result.description}</p>`;
            html += '</div>';
            
            if (result.warning) {
                html += '<p class="warning-text" style="background: #f44336; color: white; padding: 15px; border-radius: 8px; font-weight: bold;">⚠️ WARNING: High risk interaction detected! Consult healthcare provider immediately.</p>';
            }
            contentDiv.innerHTML = html;
        }
        // Format image analysis result
        else if (result.extracted_text || result.detected_drugs !== undefined) {
            let html = '<h3>📸 Image Analysis Results</h3>';
            
            // Check if no drugs were detected
            if (result.detected_drugs && result.detected_drugs.length === 0) {
                html += `<div style="background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 15px 0;">`;
                html += `<p style="font-size: 18px; margin: 0 0 10px 0;"><strong>⚠️ ${result.message || 'No drug names detected'}</strong></p>`;
                if (result.suggestion) {
                    html += `<p style="color: #666; margin: 5px 0;">${result.suggestion}</p>`;
                }
                html += `</div>`;
                
                // Still show extracted text
                if (result.extracted_text) {
                    html += '<div class="extracted-text" style="margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 4px;">';
                    html += '<strong>📄 Extracted Text:</strong><br>';
                    html += `<pre style="white-space: pre-wrap; font-size: 12px; margin: 5px 0;">${result.extracted_text}</pre>`;
                    html += '</div>';
                }
                
                contentDiv.innerHTML = html;
                container.classList.remove('hidden');
                return;
            }
            
            // Show risk warning if dangerous interaction detected
            if (result.risk_warning) {
                html += `<div class="warning-text" style="background: #ff4444; color: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    ${result.risk_warning}
                </div>`;
            }
            
            // Show summary
            if (result.summary) {
                html += `<p class="summary" style="font-size: 16px; margin: 15px 0;"><strong>${result.summary}</strong></p>`;
            }
            
            // Show detected drugs with their side effects
            if (result.drug_analyses && result.drug_analyses.length > 0) {
                html += '<div class="drug-analyses" style="margin: 20px 0;">';
                
                result.drug_analyses.forEach((drugAnalysis, index) => {
                    html += `<div class="drug-card" style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #007bff;">`;
                    html += `<h4 style="margin-top: 0; color: #007bff;">💊 ${drugAnalysis.drug}</h4>`;
                    
                    if (drugAnalysis.status === 'success' && drugAnalysis.side_effects) {
                        html += `<p><strong>Total Side Effects:</strong> ${drugAnalysis.count}</p>`;
                        
                        // Show common effects
                        if (drugAnalysis.common_effects && drugAnalysis.common_effects.length > 0) {
                            html += '<div style="margin: 10px 0; padding: 10px; background: #e8f5e9; border-radius: 6px; border-left: 3px solid #4caf50;">';
                            html += '<p style="margin: 0 0 8px 0; font-weight: bold; color: #2e7d32;">✓ Common Effects (' + drugAnalysis.common_count + '):</p>';
                            html += '<ul style="margin: 5px 0; padding-left: 20px;">';
                            drugAnalysis.common_effects.forEach(effect => {
                                html += `<li style="margin: 3px 0;">${effect}</li>`;
                            });
                            html += '</ul></div>';
                        }
                        
                        // Show serious effects
                        if (drugAnalysis.serious_effects && drugAnalysis.serious_effects.length > 0) {
                            html += '<div style="margin: 10px 0; padding: 10px; background: #ffebee; border-radius: 6px; border-left: 3px solid #f44336;">';
                            html += '<p style="margin: 0 0 8px 0; font-weight: bold; color: #c62828;">⚠️ Serious Effects (' + drugAnalysis.serious_count + '):</p>';
                            html += '<ul style="margin: 5px 0; padding-left: 20px;">';
                            drugAnalysis.serious_effects.forEach(effect => {
                                html += `<li style="margin: 3px 0;">${effect}</li>`;
                            });
                            html += '</ul></div>';
                        }
                    } else if (drugAnalysis.message) {
                        html += `<p style="color: #666;">${drugAnalysis.message}</p>`;
                    }
                    
                    html += '</div>';
                });
                
                html += '</div>';
            }
            
            // Show interaction check results
            if (result.interaction_check) {
                html += '<div class="interaction-section" style="margin: 20px 0; padding: 20px; background: #fff8e1; border-radius: 8px; border-left: 4px solid #ffc107;">';
                html += '<h4 style="margin-top: 0;">⚠️ Drug Interaction Check</h4>';
                
                if (Array.isArray(result.interaction_check)) {
                    result.interaction_check.forEach(interaction => {
                        const riskColor = interaction.risk === 'Dangerous' ? '#dc3545' : 
                                        interaction.risk === 'Moderate' ? '#ffc107' : '#28a745';
                        html += `<div style="margin: 15px 0; padding: 15px; background: white; border-left: 4px solid ${riskColor}; border-radius: 4px;">`;
                        html += `<p style="font-size: 16px; margin: 5px 0;"><strong>${interaction.drugA}</strong> + <strong>${interaction.drugB}</strong></p>`;
                        html += `<p style="color: ${riskColor}; font-weight: bold; font-size: 18px; margin: 10px 0;">Risk: ${interaction.risk}</p>`;
                        if (interaction.description) {
                            html += `<div style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 4px;">`;
                            html += `<p style="margin: 0; line-height: 1.6; color: #333;">${interaction.description}</p>`;
                            html += '</div>';
                        }
                        html += '</div>';
                    });
                } else if (result.interaction_check.interaction_risk) {
                    const riskColor = result.interaction_check.interaction_risk === 'Dangerous' ? '#dc3545' : 
                                    result.interaction_check.interaction_risk === 'Moderate' ? '#ffc107' : '#28a745';
                    html += `<p style="color: ${riskColor}; font-weight: bold; font-size: 18px;">Risk Level: ${result.interaction_check.interaction_risk}</p>`;
                    if (result.interaction_check.description) {
                        html += `<div style="margin-top: 15px; padding: 15px; background: white; border-radius: 4px;">`;
                        html += `<p style="margin: 0; line-height: 1.6; color: #333;">${result.interaction_check.description}</p>`;
                        html += '</div>';
                    }
                }
                
                html += '</div>';
            }
            
            // Show extracted text at the bottom
            if (result.extracted_text) {
                html += '<div class="extracted-text" style="margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 4px;">';
                html += '<strong>📄 Raw Extracted Text:</strong><br>';
                html += `<pre style="white-space: pre-wrap; font-size: 12px; margin: 5px 0;">${result.extracted_text}</pre>`;
                html += '</div>';
            }
            
            contentDiv.innerHTML = html;
        }
        else {
            contentDiv.textContent = JSON.stringify(result, null, 2);
        }
    } else {
        contentDiv.textContent = result;
    }
    
    container.classList.remove('hidden');
}

// Global variable to track wrong drugs for replacement
let wrongDrugs = {};

function showError(elementId, error) {
    const container = document.getElementById(elementId);
    
    // Handle object errors with suggestions
    if (typeof error === 'object') {
        let html = `<div class="error-message">❌ ${error.error || error.message || 'An error occurred'}</div>`;
        
        if (error.did_you_mean) {
            html += '<div class="suggestion-box">';
            html += '<p><strong>💡 Did you mean:</strong></p>';
            
            if (Array.isArray(error.did_you_mean)) {
                html += '<ul class="suggestion-list">';
                error.did_you_mean.forEach(suggestion => {
                    html += `<li class="suggestion-item" onclick="useSuggestion('${suggestion}')">${suggestion}</li>`;
                });
                html += '</ul>';
            } else {
                // Track wrong drugs for replacement
                wrongDrugs = {};
                html += '<ul class="suggestion-list">';
                for (const [drug, suggestions] of Object.entries(error.did_you_mean)) {
                    wrongDrugs[drug] = true; // Mark this drug as wrong
                    suggestions.forEach(suggestion => {
                        html += `<li class="suggestion-item" onclick="useSuggestion('${suggestion}', '${drug}')">${suggestion}</li>`;
                    });
                }
                html += '</ul>';
            }
            html += '</div>';
        } else if (error.suggestion) {
            html += `<p class="hint-text">${error.suggestion}</p>`;
        }
        
        container.innerHTML = html;
    } else {
        container.innerHTML = `<div class="error-message">❌ ${error}</div>`;
    }
    
    container.classList.remove('hidden');
}

function useSuggestion(drugName, wrongDrug) {
    const activeTab = document.querySelector('.tab-pane.active').id;
    
    if (activeTab === 'side-effects') {
        document.getElementById('drugName').value = drugName;
        analyzeSideEffects();
    } else if (activeTab === 'interactions') {
        // If we know which drug was wrong, replace it
        if (wrongDrug) {
            const index = drugTags.findIndex(d => d.toLowerCase() === wrongDrug.toLowerCase());
            if (index !== -1) {
                // Replace the wrong drug with the correct suggestion
                drugTags[index] = drugName;
                renderDrugTags();
                // Automatically recheck after replacement
                setTimeout(checkInteractions, 300);
            }
        } else {
            // Fallback: just add the drug if we don't know which one to replace
            const input = document.getElementById('drugInteractionInput');
            input.value = drugName;
            handleDrugTagInput({key: 'Enter', preventDefault: () => {}});
        }
    }
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
    // Check API status on load
    checkAPIStatus();
    
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('drugImage');

    if (dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('drag-over');
            });
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;

            if (files && files[0]) {
                fileInput.files = files;
                previewImage();
            }
        });
    }
});

// Check API Status
function checkAPIStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            const banner = document.getElementById('apiStatusBanner');
            const bannerContent = banner.querySelector('.banner-text');
            
            if (data.mode === 'ml_local' && data.operational) {
                // System is working - show success banner
                banner.className = 'api-status-banner success';
                banner.querySelector('.banner-icon').textContent = '✅';
                bannerContent.innerHTML = `
                    <strong>System Ready</strong>
                    <p>All features are operational</p>
                `;
                banner.style.display = 'block';
            } else if (data.mode === 'ml_local' && !data.operational) {
                // System not ready
                banner.className = 'api-status-banner warning';
                banner.querySelector('.banner-icon').textContent = '⚠️';
                bannerContent.innerHTML = `
                    <strong>System Not Ready</strong>
                    <p>${data.message || 'Please run: python src/train_models.py'}</p>
                `;
                banner.style.display = 'block';
            } else {
                banner.style.display = 'none';
            }
        })
        .catch(error => {
            console.log('Could not check status:', error);
            const banner = document.getElementById('apiStatusBanner');
            banner.style.display = 'none';
        });
}

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
// ============================================
// DATASET MANAGEMENT FEATURES
// ============================================

// State to track uploaded datasets
let uploadedDatasets = {
    side_effects: null,
    interactions: null
};

// Toggle between built-in and custom dataset mode
function toggleDatasetMode() {
    const toggle = document.getElementById('datasetToggle');
    const customSection = document.getElementById('customDatasetSection');
    const builtinInfo = document.getElementById('builtinDatasetInfo');
    
    console.log('=== Toggle Dataset Mode ===');
    console.log('Toggle checked:', toggle.checked);
    console.log('Custom section element:', !!customSection);
    console.log('Built-in info element:', !!builtinInfo);
    
    const mode = toggle.checked ? 'custom' : 'builtin';
    
    // Call API to switch dataset mode on the backend
    fetch('/api/switch-dataset-mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mode: mode })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('✓ Backend switched to', mode, 'mode');
        } else {
            console.error('✗ Failed to switch mode:', data.error);
        }
    })
    .catch(error => {
        console.error('✗ Error switching mode:', error);
    });
    
    if (toggle.checked) {
        // Switch to custom dataset mode
        console.log('→ Switching to CUSTOM dataset mode');
        if (customSection) {
            customSection.classList.remove('hidden');
            console.log('✓ Custom section shown');
        }
        if (builtinInfo) {
            builtinInfo.classList.add('hidden');
            console.log('✓ Built-in info hidden');
        }
        showToast('📊 Switched to Custom Dataset mode', 'info');
    } else {
        // Switch to built-in dataset mode
        console.log('→ Switching to BUILT-IN dataset mode');
        if (customSection) {
            customSection.classList.add('hidden');
            console.log('✓ Custom section hidden');
        }
        if (builtinInfo) {
            builtinInfo.classList.remove('hidden');
            console.log('✓ Built-in info shown');
        }
        
        // Reset custom dataset state
        uploadedDatasets = {
            side_effects: null,
            interactions: null
        };
        
        // Reset file inputs
        const sideEffectsInput = document.getElementById('sideEffectsDataset');
        const interactionsInput = document.getElementById('interactionsDataset');
        const sideEffectsFileName = document.getElementById('sideEffectsFileName');
        const interactionsFileName = document.getElementById('interactionsFileName');
        const sideEffectsStatus = document.getElementById('sideEffectsUploadStatus');
        const interactionsStatus = document.getElementById('interactionsUploadStatus');
        const trainStatus = document.getElementById('trainStatus');
        const trainButton = document.getElementById('trainButton');
        
        if (sideEffectsInput) sideEffectsInput.value = '';
        if (interactionsInput) interactionsInput.value = '';
        if (sideEffectsFileName) sideEffectsFileName.textContent = 'Choose CSV File';
        if (interactionsFileName) interactionsFileName.textContent = 'Choose CSV File';
        if (sideEffectsStatus) sideEffectsStatus.innerHTML = '';
        if (interactionsStatus) interactionsStatus.innerHTML = '';
        if (trainStatus) trainStatus.innerHTML = '';
        if (trainButton) trainButton.disabled = true;
        
        console.log('✓ Custom dataset state reset');
        showToast('📊 Switched to Built-in Dataset mode - predictions will use original models', 'success');
    }
    console.log('=== Toggle Complete ===');
}

// Download CSV template
function downloadTemplate(type) {
    const url = `/api/download-template?type=${type}`;
    
    // Use fetch to download the file properly
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Template not found');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${type}_template.csv`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            
            showToast(`📥 Downloaded ${type} template successfully!`, 'success');
        })
        .catch(error => {
            console.error('Download error:', error);
            showToast(`❌ Failed to download template: ${error.message}`, 'error');
        });
}

// Handle dataset file upload
function handleDatasetUpload(type) {
    const inputId = type === 'side_effects' ? 'sideEffectsDataset' : 'interactionsDataset';
    const fileNameId = type === 'side_effects' ? 'sideEffectsFileName' : 'interactionsFileName';
    const statusId = type === 'side_effects' ? 'sideEffectsUploadStatus' : 'interactionsUploadStatus';
    
    const input = document.getElementById(inputId);
    const file = input.files[0];
    
    console.log(`handleDatasetUpload called for ${type}`, file);
    
    if (!file) {
        console.log('No file selected');
        return;
    }
    
    // Validate file type
    if (!file.name.endsWith('.csv')) {
        showToast('❌ Please upload a CSV file', 'error');
        input.value = '';
        return;
    }
    
    // Update file name display
    const fileNameElement = document.getElementById(fileNameId);
    if (fileNameElement) {
        fileNameElement.textContent = file.name.length > 20 ? 
            file.name.substring(0, 17) + '...' : file.name;
        console.log('File name updated:', file.name);
    }
    
    // Show upload status
    const statusElement = document.getElementById(statusId);
    statusElement.innerHTML = '<div class="status-uploading">📤 Uploading...</div>';
    
    // Create FormData and upload
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);
    
    fetch('/api/upload-dataset', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadedDatasets[type] = data.filename;
            statusElement.innerHTML = `
                <div class="status-success">
                    ✓ Uploaded successfully
                    <span class="status-detail">${data.records} records</span>
                </div>
            `;
            
            // Check if both datasets are uploaded
            checkTrainButtonState();
            
            showToast(`✅ ${type} dataset uploaded successfully!`, 'success');
        } else {
            statusElement.innerHTML = `
                <div class="status-error">
                    ✕ ${data.error}
                </div>
            `;
            uploadedDatasets[type] = null;
            input.value = '';
            fileNameElement.textContent = 'Choose CSV File';
            
            showToast(`❌ Upload failed: ${data.error}`, 'error');
        }
    })
    .catch(error => {
        statusElement.innerHTML = `
            <div class="status-error">
                ✕ Upload failed
            </div>
        `;
        uploadedDatasets[type] = null;
        input.value = '';
        fileNameElement.textContent = 'Choose CSV File';
        
        showToast('❌ Upload failed. Please try again.', 'error');
        console.error('Upload error:', error);
    });
}

// Check if both datasets are uploaded to enable train button
function checkTrainButtonState() {
    const trainButton = document.getElementById('trainButton');
    
    if (uploadedDatasets.side_effects && uploadedDatasets.interactions) {
        trainButton.disabled = false;
        trainButton.classList.add('pulse');
    } else {
        trainButton.disabled = true;
        trainButton.classList.remove('pulse');
    }
}

// Train models with custom datasets
function trainCustomModels() {
    const trainButton = document.getElementById('trainButton');
    const trainStatus = document.getElementById('trainStatus');
    const trainLoading = document.getElementById('trainLoading');
    
    // Disable button and show loading
    trainButton.disabled = true;
    trainStatus.classList.add('hidden');
    trainLoading.classList.remove('hidden');
    
    fetch('/api/retrain-models', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            side_effects_file: uploadedDatasets.side_effects,
            interactions_file: uploadedDatasets.interactions
        })
    })
    .then(response => response.json())
    .then(data => {
        trainLoading.classList.add('hidden');
        trainStatus.classList.remove('hidden');
        
        if (data.success) {
            trainStatus.innerHTML = `
                <div class="status-success-large">
                    <div class="success-icon">🎉</div>
                    <div class="success-content">
                        <h4>Training Completed Successfully!</h4>
                        <div class="metrics">
                            <div class="metric">
                                <span class="metric-label">Side Effects Accuracy:</span>
                                <span class="metric-value">${data.side_effects_accuracy}</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Interactions Accuracy:</span>
                                <span class="metric-value">${data.interactions_accuracy}</span>
                            </div>
                        </div>
                        <p class="success-note">Your custom models are now active and ready to use!</p>
                    </div>
                </div>
            `;
            
            // Update system status
            checkAPIStatus();
            
            showToast('🎉 Models trained successfully!', 'success');
        } else {
            trainStatus.innerHTML = `
                <div class="status-error-large">
                    <div class="error-icon">❌</div>
                    <div class="error-content">
                        <h4>Training Failed</h4>
                        <p>${data.error}</p>
                    </div>
                </div>
            `;
            trainButton.disabled = false;
            
            showToast(`❌ Training failed: ${data.error}`, 'error');
        }
    })
    .catch(error => {
        trainLoading.classList.add('hidden');
        trainStatus.classList.remove('hidden');
        trainStatus.innerHTML = `
            <div class="status-error-large">
                <div class="error-icon">❌</div>
                <div class="error-content">
                    <h4>Training Error</h4>
                    <p>An unexpected error occurred. Please try again.</p>
                </div>
            </div>
        `;
        trainButton.disabled = false;
        
        showToast('❌ Training error. Please try again.', 'error');
        console.error('Training error:', error);
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    // Remove existing toast if any
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.textContent = message;
    
    // Add to body
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Initialize file input click handlers when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== Initializing file input handlers ===');
    
    // Setup click handlers for file upload labels
    const sideEffectsLabel = document.querySelector('label[for="sideEffectsDataset"]');
    const interactionsLabel = document.querySelector('label[for="interactionsDataset"]');
    const sideEffectsInput = document.getElementById('sideEffectsDataset');
    const interactionsInput = document.getElementById('interactionsDataset');
    
    console.log('Side effects label found:', !!sideEffectsLabel);
    console.log('Side effects input found:', !!sideEffectsInput);
    console.log('Interactions label found:', !!interactionsLabel);
    console.log('Interactions input found:', !!interactionsInput);
    
    if (sideEffectsLabel && sideEffectsInput) {
        sideEffectsLabel.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('✓ Side effects label clicked - triggering file input');
            sideEffectsInput.click();
        });
        console.log('✓ Side effects click handler attached');
    } else {
        console.error('✗ Could not attach side effects handler');
    }
    
    if (interactionsLabel && interactionsInput) {
        interactionsLabel.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('✓ Interactions label clicked - triggering file input');
            interactionsInput.click();
        });
        console.log('✓ Interactions click handler attached');
    } else {
        console.error('✗ Could not attach interactions handler');
    }
    
    // Setup change handlers for file inputs
    if (sideEffectsInput) {
        sideEffectsInput.addEventListener('change', function(e) {
            console.log('✓ Side effects file selected:', e.target.files);
            if (e.target.files.length > 0) {
                console.log('File details:', {
                    name: e.target.files[0].name,
                    size: e.target.files[0].size,
                    type: e.target.files[0].type
                });
            }
            handleDatasetUpload('side_effects');
        });
        console.log('✓ Side effects change handler attached');
    }
    
    if (interactionsInput) {
        interactionsInput.addEventListener('change', function(e) {
            console.log('✓ Interactions file selected:', e.target.files);
            if (e.target.files.length > 0) {
                console.log('File details:', {
                    name: e.target.files[0].name,
                    size: e.target.files[0].size,
                    type: e.target.files[0].type
                });
            }
            handleDatasetUpload('interactions');
        });
        console.log('✓ Interactions change handler attached');
    }
    
    console.log('=== File input handlers initialized ===');
});