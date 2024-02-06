document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display default categories with improved error handling
    fetch('/default_categories')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok, status: ${response.status}`);
        }
        return response.json();
    })
    .then(categories => {
        const container = document.getElementById('categoriesContainer');
        Object.entries(categories).forEach(([categoryName, details]) => {
            container.insertAdjacentHTML('beforeend', `
                <div class="fileTypeGroup">
                    <label>Category Name:</label>
                    <input type="text" name="categoryName" value="${categoryName}" required>
                    <label>Extensions (comma-separated):</label>
                    <input type="text" name="extensions" value="${details.extensions.join(',')}" required>
                    <label>Target Directory:</label>
                    <input type="text" name="targetDir" value="${details.target_dir}" required><br><br>
                </div>
            `);
        });
    })
    .catch(error => {
        console.error('Error loading default categories:', error);
        const feedbackArea = document.getElementById('feedbackArea');
        feedbackArea.innerHTML += `<p>Error loading default categories: ${error.message}</p>`;
    });

    document.getElementById('directoryForm').onsubmit = function(e) {
        e.preventDefault();
        const directoryPath = document.getElementById('directoryPath').value;
    
        fetch('/get_extensions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({directoryPath: directoryPath}),
        })
        .then(response => response.json())
        .then(data => {
            if(data.extensions) {
                const list = data.extensions.map(ext => `<li>${ext}</li>`).join('');
                document.getElementById('extensionsList').innerHTML = `<ul>${list}</ul>`;
            } else if(data.error) {
                document.getElementById('extensionsList').textContent = 'Error: ' + data.error;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('extensionsList').textContent = 'Error fetching extensions';
        });
    };
    

    // Add event listener for dynamically adding new category fields
    document.getElementById('addCategoryButton').addEventListener('click', function() {
        const container = document.getElementById('categoriesContainer');
        container.insertAdjacentHTML('beforeend', `
            <div class="fileTypeGroup">
                <label>Category Name:</label>
                <input type="text" name="categoryName" required>
                <label>Extensions (comma-separated):</label>
                <input type="text" name="extensions" required>
                <label>Target Directory:</label>
                <input type="text" name="targetDir" required><br><br>
            </div>
        `);
    });

    // Handle form submission with existing logic
    document.getElementById('cleanerForm').onsubmit = async function(e) {
        e.preventDefault();
        
        const downloadsPath = document.getElementById('downloadsPath').value;
        
        const categories = Array.from(document.querySelectorAll('.fileTypeGroup')).map(group => {
            const categoryName = group.querySelector('input[name="categoryName"]').value;
            const extensions = group.querySelector('input[name="extensions"]').value.split(',').map(ext => ext.trim());
            const targetDir = group.querySelector('input[name="targetDir"]').value;
            return { categoryName, extensions, targetDir };
        });

        const data = { downloadsPath, categories };

        fetch('/sort', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok, status: ${response.status}`);
            }
            return response.json();
        })
        .then(files => {
            const feedbackArea = document.getElementById('feedbackArea');
            feedbackArea.innerHTML = '<h2>Processed Files</h2>';
            files.forEach(file => {
                feedbackArea.innerHTML += `<p>${file.original_name} moved to ${file.destination_folder}</p>`;
            });
        })
        .catch(error => {
            console.error('Error:', error);
            const feedbackArea = document.getElementById('feedbackArea');
            feedbackArea.innerHTML += `<p>Error processing files: ${error.message}</p>`;
        });
    };
});
