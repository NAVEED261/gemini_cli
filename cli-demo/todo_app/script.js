const taskInput = document.getElementById('task-input');
const addTaskBtn = document.getElementById('add-task-btn');
const taskList = document.getElementById('task-list');

let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function renderTasks() {
    taskList.innerHTML = '';
    tasks.forEach((task, index) => {
        const listItem = document.createElement('li');
        listItem.classList.add('task-item');
        if (task.completed) {
            listItem.classList.add('completed');
        }

        listItem.innerHTML = `
            <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} data-index="${index}">
            <span class="task-text">${task.text}</span>
            <div class="task-actions">
                <button class="edit-btn" data-index="${index}"><i class="fas fa-edit"></i></button>
                <button class="delete-btn" data-index="${index}"><i class="fas fa-trash"></i></button>
            </div>
        `;
        taskList.appendChild(listItem);
    });
}

function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText !== '') {
        tasks.push({ text: taskText, completed: false });
        taskInput.value = '';
        saveTasks();
        renderTasks();
    }
}

function toggleComplete(event) {
    if (event.target.classList.contains('task-checkbox')) {
        const index = event.target.dataset.index;
        tasks[index].completed = !tasks[index].completed;
        saveTasks();
        renderTasks();
    }
}

function deleteTask(event) {
    if (event.target.closest('.delete-btn')) {
        const index = event.target.closest('.delete-btn').dataset.index;
        tasks.splice(index, 1);
        saveTasks();
        renderTasks();
    }
}

function editTask(event) {
    if (event.target.closest('.edit-btn')) {
        const index = event.target.closest('.edit-btn').dataset.index;
        const currentTaskText = tasks[index].text;
        
        const listItem = event.target.closest('.task-item');
        const taskTextSpan = listItem.querySelector('.task-text');
        const taskActionsDiv = listItem.querySelector('.task-actions');

        // Replace span with input field
        const editInput = document.createElement('input');
        editInput.type = 'text';
        editInput.value = currentTaskText;
        editInput.classList.add('edit-input');
        taskTextSpan.replaceWith(editInput);

        // Change buttons to save/cancel
        taskActionsDiv.innerHTML = `
            <button class="save-edit-btn" data-index="${index}"><i class="fas fa-save"></i></button>
            <button class="cancel-edit-btn" data-index="${index}"><i class="fas fa-times"></i></button>
        `;

        editInput.focus();

        // Event listeners for save/cancel
        listItem.querySelector('.save-edit-btn').addEventListener('click', (e) => {
            const newText = editInput.value.trim();
            if (newText !== '') {
                tasks[index].text = newText;
                saveTasks();
            }
            renderTasks(); // Re-render to revert to display mode
        });

        listItem.querySelector('.cancel-edit-btn').addEventListener('click', () => {
            renderTasks(); // Re-render to revert to display mode without saving
        });

        editInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const newText = editInput.value.trim();
                if (newText !== '') {
                    tasks[index].text = newText;
                    saveTasks();
                }
                renderTasks();
            }
        });
    }
}

addTaskBtn.addEventListener('click', addTask);
taskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTask();
    }
});
taskList.addEventListener('change', toggleComplete);
taskList.addEventListener('click', deleteTask);
taskList.addEventListener('click', editTask);

renderTasks();
