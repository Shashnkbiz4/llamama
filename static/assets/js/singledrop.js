document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-input');
    const fileName = document.querySelector('.file-name');
    const fileSize = document.querySelector('.file-size');
    const dropZone = document.querySelector('.drop-zone');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileName.textContent = file.name;
            fileSize.textContent = `(${formatFileSize(file.size)})`;
        } else {
            fileName.textContent = '';
            fileSize.textContent = '';
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drop-zone--over');
    });

    ['dragleave', 'dragend'].forEach(type => {
        dropZone.addEventListener(type, () => {
            dropZone.classList.remove('drop-zone--over');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drop-zone--over');
        fileInput.files = e.dataTransfer.files;
        const file = fileInput.files[0];
        fileName.textContent = file.name;
        fileSize.textContent = `(${formatFileSize(file.size)})`;
    });

    function formatFileSize(bytes) {
        const units = ['B', 'KB', 'MB', 'GB', 'TB'];
        let unitIndex = 0;
        let size = bytes;

        while (size >= 1024 && unitIndex < units.length - 1) {
            size /= 1024;
            unitIndex++;
        }

        return `${size.toFixed(2)} ${units[unitIndex]}`;
    }

    document.getElementById('upload-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch("{% url 'upload' %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('pdf-type').textContent = data.pdf_type;
                document.getElementById('client-id').textContent = data.client_id;
                document.getElementById('output-box').style.display = 'block';
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
