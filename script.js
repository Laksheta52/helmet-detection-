// API Configuration
const API_URL = 'http://localhost:5000';

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const resetBtn = document.getElementById('resetBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const resultsSection = document.getElementById('resultsSection');
const annotatedImage = document.getElementById('annotatedImage');
const detectionsGrid = document.getElementById('detectionsGrid');
const resultsStats = document.getElementById('resultsStats');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const statusBadge = document.getElementById('statusBadge');

let selectedFile = null;

// Check API Health
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            statusBadge.classList.remove('offline');
            statusBadge.innerHTML = '<span class="status-dot"></span><span>Connected</span>';
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        statusBadge.classList.add('offline');
        statusBadge.innerHTML = '<span class="status-dot"></span><span>Offline</span>';
        console.error('API health check failed:', error);
    }
}

// Initialize
checkAPIHealth();
setInterval(checkAPIHealth, 30000); // Check every 30 seconds

// File Upload Handlers
browseBtn.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('click', (e) => {
    if (e.target !== browseBtn) {
        fileInput.click();
    }
});

fileInput.addEventListener('change', handleFileSelect);

// Drag and Drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file (JPG, PNG, WEBP)');
        return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size too large. Please select an image under 10MB');
        return;
    }

    selectedFile = file;
    displayPreview(file);
}

function displayPreview(file) {
    const reader = new FileReader();

    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewSection.style.display = 'block';
        resultsSection.style.display = 'none';

        // Smooth scroll to preview
        setTimeout(() => {
            previewSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    };

    reader.readAsDataURL(file);
}

// Reset Handler
resetBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
    uploadArea.scrollIntoView({ behavior: 'smooth' });
});

// Analyze Handler
analyzeBtn.addEventListener('click', analyzeImage);

async function analyzeImage() {
    if (!selectedFile) {
        showError('No image selected');
        return;
    }

    // Show loading
    loadingOverlay.style.display = 'flex';

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('image', selectedFile);

        // Send to API
        const response = await fetch(`${API_URL}/detect`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Detection failed');
        }

    } catch (error) {
        console.error('Analysis error:', error);
        showError(`Analysis failed: ${error.message}. Make sure the backend server is running.`);
    } finally {
        loadingOverlay.style.display = 'none';
    }
}

function displayResults(data) {
    // Display annotated image
    annotatedImage.src = data.annotated_image;

    // Display stats
    const helmetRelated = data.detections.filter(d => d.helmet_related).length;
    const licensePlates = data.detections.filter(d => d.license_plate).length;

    resultsStats.innerHTML = `
        <div class="stat-item">
            <div class="stat-value">${data.total_detections}</div>
            <div class="stat-label">Total Detections</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${helmetRelated}</div>
            <div class="stat-label">Helmet Related</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${licensePlates}</div>
            <div class="stat-label">License Plates</div>
        </div>
    `;

    // Display individual detections
    detectionsGrid.innerHTML = '';

    if (data.detections.length === 0) {
        detectionsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h3>No objects detected</h3>
                <p style="color: var(--text-muted);">Try uploading a different image</p>
            </div>
        `;
    } else {
        data.detections.forEach((detection, index) => {
            const card = createDetectionCard(detection, index);
            detectionsGrid.appendChild(card);
        });
    }

    // Show results section
    resultsSection.style.display = 'block';

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function createDetectionCard(detection, index) {
    const card = document.createElement('div');
    card.className = 'detection-card';
    card.style.animationDelay = `${index * 0.1}s`;

    const bbox = detection.bbox;
    const bboxText = `[${bbox[0]}, ${bbox[1]}, ${bbox[2]}, ${bbox[3]}]`;

    let cardHTML = `
        <div class="detection-header">
            <div class="detection-class">${getClassEmoji(detection.class)} ${detection.class}</div>
            <div class="detection-confidence">${detection.confidence}%</div>
        </div>
        <div class="detection-details">
            <div class="detail-row">
                <span class="detail-label">Bounding Box</span>
                <span class="detail-value" style="font-size: 0.75rem;">${bboxText}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Type</span>
                <span class="detail-value">${detection.helmet_related ? 'Helmet Related ⚠️' : 'Vehicle 🚗'}</span>
            </div>
    `;

    if (detection.license_plate) {
        cardHTML += `
            </div>
            <div class="license-plate">
                <div class="license-plate-label">📋 License Plate Detected</div>
                <div class="license-plate-text">${detection.license_plate}</div>
            </div>
        `;
    } else {
        cardHTML += '</div>';
    }

    card.innerHTML = cardHTML;
    return card;
}

function getClassEmoji(className) {
    const emojiMap = {
        'person': '🚶',
        'motorcycle': '🏍️',
        'bicycle': '🚲',
        'car': '🚗',
        'truck': '🚚',
        'bus': '🚌',
        'traffic light': '🚦',
        'stop sign': '🛑'
    };
    return emojiMap[className] || '📦';
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(hideError, 5000);
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Escape to reset
    if (e.key === 'Escape') {
        if (resultsSection.style.display === 'block') {
            resetBtn.click();
        }
    }

    // Enter to analyze (if preview is shown)
    if (e.key === 'Enter' && previewSection.style.display === 'block') {
        analyzeBtn.click();
    }
});

// Add animation class to detection cards
const style = document.createElement('style');
style.textContent = `
    .detection-card {
        animation: cardSlideIn 0.5s ease forwards;
        opacity: 0;
    }
    
    @keyframes cardSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
