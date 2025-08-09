// Todo App JavaScript - Day 2 Enhanced Version

class TodoApp {
    constructor() {
        this.apiBaseUrl = window.location.origin;
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkHealth();
        this.loadTodos();
        
        // Auto-refresh health status every 30 seconds
        setInterval(() => this.checkHealth(), 30000);
    }

    bindEvents() {
        // Form submission
        document.getElementById('todo-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTodo();
        });

        // Enter key in input
        document.getElementById('task-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.addTodo();
            }
        });
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            const healthElement = document.getElementById('health-status');
            
            if (response.ok && data.status === 'healthy') {
                healthElement.innerHTML = `
                    <span class="status-indicator status-healthy"></span>
                    <span class="text-success">API Healthy</span>
                `;
            } else {
                healthElement.innerHTML = `
                    <span class="status-indicator status-unhealthy"></span>
                    <span class="text-danger">API Unhealthy</span>
                `;
            }
        } catch (error) {
            document.getElementById('health-status').innerHTML = `
                <span class="status-indicator status-unhealthy"></span>
                <span class="text-danger">API Offline</span>
            `;
        }
    }

    async loadTodos() {
        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/todos/list`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const todos = await response.json();
            this.renderTodos(todos);
            this.updateTodoCount(todos.length);
            
        } catch (error) {
            console.error('Error loading todos:', error);
            this.showToast('Error loading todos. Please try again.', 'error');
            this.renderTodos([]);
        } finally {
            this.showLoading(false);
        }
    }

    async addTodo() {
        const taskInput = document.getElementById('task-input');
        const task = taskInput.value.trim();
        
        if (!task) {
            this.showToast('Please enter a task!', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/todos/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ task: task })
            });

            const data = await response.json();

            if (response.ok) {
                taskInput.value = '';
                this.showToast('Todo added successfully!', 'success');
                this.loadTodos(); // Refresh the list
            } else {
                this.showToast(data.error || 'Error adding todo', 'error');
            }
        } catch (error) {
            console.error('Error adding todo:', error);
            this.showToast('Network error. Please try again.', 'error');
        }
    }

    async deleteTodo(todoId) {
        if (!confirm('Are you sure you want to delete this todo?')) {
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/todos/${todoId}`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (response.ok) {
                this.showToast('Todo deleted successfully!', 'success');
                this.loadTodos(); // Refresh the list
            } else {
                this.showToast(data.error || 'Error deleting todo', 'error');
            }
        } catch (error) {
            console.error('Error deleting todo:', error);
            this.showToast('Network error. Please try again.', 'error');
        }
    }

    renderTodos(todos) {
        const container = document.getElementById('todos-container');
        const emptyState = document.getElementById('empty-state');
        
        if (todos.length === 0) {
            container.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';
        
        container.innerHTML = todos.map(todo => `
            <div class="todo-item fade-in" data-todo-id="${todo.id}">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-2">
                            <i class="fas fa-circle text-primary me-2" style="font-size: 8px;"></i>
                            <span class="fw-bold">Task #${todo.id}</span>
                            <span class="badge bg-secondary ms-2">Active</span>
                        </div>
                        <p class="mb-1 text-dark">${this.escapeHtml(todo.task)}</p>
                        <small class="text-muted">
                            <i class="fas fa-calendar-alt me-1"></i>
                            Added recently
                        </small>
                    </div>
                    <div class="ms-3">
                        <button class="btn btn-outline-primary btn-sm me-2" 
                                onclick="todoApp.editTodo(${todo.id})" 
                                title="Edit Todo">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-danger btn-sm" 
                                onclick="todoApp.deleteTodo(${todo.id})" 
                                title="Delete Todo">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    editTodo(todoId) {
        const todoElement = document.querySelector(`[data-todo-id="${todoId}"]`);
        const taskText = todoElement.querySelector('p').textContent;
        
        // For now, just show an alert. In a real app, you'd implement inline editing
        const newTask = prompt('Edit todo:', taskText);
        if (newTask && newTask.trim() && newTask !== taskText) {
            this.showToast('Edit functionality coming soon!', 'info');
        }
    }

    updateTodoCount(count) {
        document.getElementById('total-count').textContent = count;
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        const container = document.getElementById('todos-container');
        
        if (show) {
            loading.style.display = 'block';
            container.style.opacity = '0.5';
        } else {
            loading.style.display = 'none';
            container.style.opacity = '1';
        }
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');
        const toastHeader = toast.querySelector('.toast-header');
        
        // Update toast styling based on type
        toast.className = 'toast';
        toastHeader.className = 'toast-header';
        
        switch (type) {
            case 'success':
                toastHeader.classList.add('bg-success', 'text-white');
                toastHeader.querySelector('i').className = 'fas fa-check-circle text-white me-2';
                break;
            case 'error':
                toastHeader.classList.add('bg-danger', 'text-white');
                toastHeader.querySelector('i').className = 'fas fa-exclamation-triangle text-white me-2';
                break;
            case 'warning':
                toastHeader.classList.add('bg-warning', 'text-dark');
                toastHeader.querySelector('i').className = 'fas fa-exclamation-circle text-dark me-2';
                break;
            default:
                toastHeader.querySelector('i').className = 'fas fa-info-circle text-primary me-2';
        }
        
        toastMessage.textContent = message;
        
        // Show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global functions for onclick handlers
let todoApp;

function loadTodos() {
    todoApp.loadTodos();
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    todoApp = new TodoApp();
});
