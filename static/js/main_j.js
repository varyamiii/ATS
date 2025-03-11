// Обработка загрузки файлов
const fileInput = document.getElementById('resume-upload');
const uploadedFilesList = document.getElementById('uploaded-files-list');

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    uploadedFilesList.innerHTML = ''; // Очистить список

    for (const file of files) {
        const listItem = document.createElement('li');
        listItem.textContent = file.name;
        uploadedFilesList.appendChild(listItem);
    }
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