// const fileInput = document.getElementById('fileInput');
// const fileList = document.getElementById('fileList');
// const uploadButton = document.getElementById('uploadButton');
// let filesArray = [];

// fileInput.addEventListener('change', function(event) {
//     const files = event.target.files;
//     fileList.innerHTML = '';
//     filesArray = Array.from(files);
//     uploadButton.disabled = filesArray.length === 0;

//     filesArray.forEach(file => {
//         const fileItem = document.createElement('div');
//         fileItem.className = 'file-item';

//         const fileName = document.createElement('span');
//         fileName.className = 'file-name';
//         fileName.textContent = file.name;

//         const progress = document.createElement('div');
//         progress.className = 'progress';

//         const progressBar = document.createElement('div');
//         progressBar.className = 'progress-bar';

//         progress.appendChild(progressBar);
//         fileItem.appendChild(fileName);
//         fileItem.appendChild(progress);
//         fileList.appendChild(fileItem);

//         simulateProgress(progressBar);
//     });
// });

// function simulateProgress(progressBar) {
//     let progress = 0;
//     const interval = setInterval(() => {
//         progress += 10;
//         progressBar.style.width = progress + '%';
//         if (progress >= 100) {
//             clearInterval(interval);
//         }
//     }, 100);
// }

// uploadButton.addEventListener('click', function() {
//     uploadButton.disabled = true;
//     const formData = new FormData();
//     filesArray.forEach(file => {
//         formData.append('files[]', file);
//     });

//     const xhr = new XMLHttpRequest();
//     xhr.open('POST', '/upload'); // Replace with your server-side upload URL

//     xhr.onload = function() {
//         if (xhr.status === 200) {
//             alert('Files uploaded successfully!');
//         } else {
//             alert('Error uploading files.');
//         }
//         uploadButton.disabled = false;
//     };

//     xhr.send(formData);
// });

const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const uploadButton = document.getElementById('uploadButton');
let filesArray = [];

fileInput.addEventListener('change', function(event) {
    const files = event.target.files;
    fileList.innerHTML = '';
    filesArray = Array.from(files);
    uploadButton.disabled = filesArray.length === 0;

    filesArray.forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';

        const fileName = document.createElement('span');
        fileName.className = 'file-name';
        fileName.textContent = file.name;

        const progress = document.createElement('div');
        progress.className = 'progress';

        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';

        progress.appendChild(progressBar);
        fileItem.appendChild(fileName);
        fileItem.appendChild(progress);
        fileList.appendChild(fileItem);

        simulateProgress(progressBar);
    });
});

function simulateProgress(progressBar) {
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = progress + '%';
        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 100);
}

uploadButton.addEventListener('click', function() {
    uploadButton.disabled = true;
    const formData = new FormData();
    filesArray.forEach(file => {
        formData.append('files[]', file);
    });

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/dashboard/multi-upload/'); // Endpoint URL

    xhr.onload = function() {
        if (xhr.status === 200) {
            alert('Files uploaded successfully!');
            const response = JSON.parse(xhr.responseText);
            console.log(response.file_paths);
        } else {
            alert('Error uploading files.');
        }
        uploadButton.disabled = false;
    };

    xhr.send(formData);
});
