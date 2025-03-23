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

// Обработчик выпадающих списков
document.querySelectorAll('.dropbtn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const menu = this.parentElement.querySelector('.dropdown-content');
        menu.classList.toggle('show');

        // Закрытие при клике вне
        document.addEventListener('click', (e) => {
            if (!menu.contains(e.target) && !btn.contains(e.target)) {
                menu.classList.remove('show');
            }
        });
    });
});

// Обработчик формы
filterForm.addEventListener('submit', (event) => {
    event.preventDefault();

    // Сбор данных из кастомных списков
    const getChecked = (name) => {
        return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`))
                   .map(checkbox => checkbox.value);
    };

    const filters = {
        position: document.getElementById('position').value,
        employment_type: document.getElementById('employment_type').value,
        work_format: getChecked('work_format'),
        education: getChecked('education'),
        experience: document.getElementById('experience').value,
        skills: getChecked('skills'),
        english_level: getChecked('english_level'),
        special_requirements: document.getElementById('special_requirements').value
    };

    console.log('Фильтры:', filters);
    // Здесь добавьте отправку на сервер
});

// Сброс формы
document.getElementById('reset-filters').addEventListener('click', () => {
    document.querySelectorAll('.dropdown-content input').forEach(input => {
        input.checked = false;
    });
    document.querySelectorAll('.dropbtn').forEach(btn => {
        btn.textContent = 'Выберите';
    });
});