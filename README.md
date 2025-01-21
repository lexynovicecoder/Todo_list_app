# Task Management Project (To-Do List App)

This project is a simple task management application built to help users organize their tasks effectively.

## Setup Instructions

Follow these steps to set up the project:

### 1. Install virtualenv

If you haven't already installed `virtualenv`, you can do so using pip:

```bash
pip install virtualenv
```

### 2. Create Virtual Environment

Create a Python virtual environment for the project:

```bash
python -m venv .venv
```

For Python 3:

```bash
python3 -m venv .venv
```

### 3. Activate Virtual Environment

Activate the virtual environment based on your operating system:

For Unix/Linux/MacOS:

```bash
source .venv/bin/activate
```

For Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Configure Environment Variables

Create a copy of `.env.example` and name it `.env`. Modify `.env` to set your environment variables.

### 5. Initialize Database

Create the SQLite database file `database/database.db`:

```bash
touch database/database.db
```

### 6. Run the Code

Run the application using the following command:

```bash
python3 main.py
```

### 7. View API Documentation
Go to this URL
```
localhost:8000/docs
```




## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. You can also open issues for bugs or feature requests.

## License

This project is licensed under the [MIT License](LICENSE).
