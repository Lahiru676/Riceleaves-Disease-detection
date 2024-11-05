const dropArea = document.getElementById('drop-area');
const resultDiv = document.getElementById('result');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop area when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('hover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('hover'), false);
});

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);

async function handleDrop(e) {
    const file = e.dataTransfer.files[0];
    if (!file || !file.type.startsWith('image/')) {
        resultDiv.textContent = 'Please drop a valid image file.';
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            // Access and display the 'class' and 'confidence' from the 'prediction' object
            if (result && result.prediction) {
                const predictedClass = result.prediction.class;
                const confidence = (result.prediction.confidence * 100).toFixed(2);  // Convert to percentage
                resultDiv.textContent = `Prediction: ${predictedClass} (Confidence: ${confidence}%)`;
            } else {
                resultDiv.textContent = 'Error: No prediction received.';
                console.error("Prediction field is missing in response:", result);
            }
        } else {
            resultDiv.textContent = 'Error: Unable to get prediction.';
            console.error("Server responded with an error:", response.status, response.statusText);
        }
    } catch (error) {
        resultDiv.textContent = 'Error: Network or server issue.';
        console.error("Network or server error:", error);
    }
}
