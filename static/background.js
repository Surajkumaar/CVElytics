// Create binary code columns in the background
document.addEventListener('DOMContentLoaded', function() {
    createBinaryBackground();
});

function createBinaryBackground() {
    const container = document.body;
    const numColumns = 15; // Number of binary columns to create
    
    for (let i = 0; i < numColumns; i++) {
        const column = document.createElement('div');
        column.className = 'binary-column';
        
        // Random position
        column.style.left = `${Math.random() * 100}%`;
        
        // Random animation duration between 10-30s
        const duration = 10 + Math.random() * 20;
        column.style.animation = `binary-flow ${duration}s linear infinite`;
        
        // Random delay so they don't all start at once
        column.style.animationDelay = `${Math.random() * 10}s`;
        
        // Generate binary content
        column.innerHTML = generateBinaryString();
        
        container.appendChild(column);
    }
}

function generateBinaryString() {
    let result = '';
    const length = 50 + Math.floor(Math.random() * 100); // Random length between 50-150 characters
    
    for (let i = 0; i < length; i++) {
        // Mostly 0s and 1s, but occasionally add a CVE reference
        if (Math.random() < 0.01) {
            result += '<span style="color: rgba(0, 188, 212, 0.3);">CVE</span><br>';
        } else {
            result += Math.round(Math.random()) + '<br>';
        }
    }
    
    return result;
}
