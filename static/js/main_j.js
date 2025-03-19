const fileInput = document.getElementById('resume-upload');
const uploadedFilesList = document.getElementById('uploaded-files-list');
const progressBar = document.getElementById('progress-bar');

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    if (files.length === 0) return;

    // Проверка расширений файлов
    const allowedExtensions = /(\.pdf)$/i;
    let hasInvalidFile = false;
    for (const file of files) {
        if (!allowedExtensions.exec(file.name)) {
            alert(`Файл "${file.name}" не является PDF.`);
            hasInvalidFile = true;
            fileInput.value = '';
            break;
        }
    }

    if (hasInvalidFile) return;

    // Отображение выбранных файлов
    uploadedFilesList.innerHTML = '';
    for (const file of files) {
        const listItem = document.createElement('li');
        listItem.textContent = `⮹ ${file.name}`;
        uploadedFilesList.appendChild(listItem);
    }

    // Настройка FormData
    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }

    // Настройка XMLHttpRequest
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);

    // Прогресс загрузки
    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            const percent = (e.loaded / e.total * 100).toFixed(0);
            progressBar.style.width = `${percent}%`;
            progressBar.textContent = `${percent}%`;
        }
    };

    // Обработка ответа
    xhr.onload = () => {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            progressBar.style.backgroundColor = '#4CAF50';

            // Отображение результатов
            response.results.forEach(result => {
                const listItem = document.createElement('li');
                listItem.textContent = `${result.filename}: ${result.message}`;
                listItem.style.color = result.status === 'success' ? 'green' : 'red';
                uploadedFilesList.appendChild(listItem);
            });

            setTimeout(() => {
                progressBar.style.width = '0%';
                progressBar.textContent = '';
                progressBar.style.backgroundColor = '#007bff';
                alert('Загрузка завершена!');
            }, 2000);
        } else {
            progressBar.style.backgroundColor = '#ff0000';
            alert('Ошибка загрузки!');
        }
    };

    xhr.send(formData);
});

// Обработка формы фильтров
const filterForm = document.getElementById('filter-form');
const resultsList = document.getElementById('results-list');

filterForm.addEventListener('submit', (event) => {
    event.preventDefault();

    // Пример данных для демонстрации
    const results = [
        { name: 'Резюме 1', status: 'success', message: 'Соответствует фильтрам' },
        { name: 'Резюме 2', status: 'error', message: 'Не соответствует (низкий опыт работы)' },
        { name: 'Резюме 3', status: 'success', message: 'Соответствует фильтрам' },
    ];

    resultsList.innerHTML = ''; // Очистить список

    results.forEach(result => {
        const listItem = document.createElement('li');
        listItem.textContent = `${result.name}: ${result.message}`;
        listItem.className = result.status;
        resultsList.appendChild(listItem);
    });
});