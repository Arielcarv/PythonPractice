# Studybud

A community for programming students. The original project was built with Django traditional **Function-based Views**. I used this Guided project posted on [Traversy Media Youtube channel](https://www.youtube.com/watch?v=PtQiiknWUcI) to study and practice more the **Class-based Views** approach. the original project code is at [Code](https://github.com/divanov11/StudyBud/).

Visit the finished application at (Somewhere)


## Setup
1. Create a virtual environment and activate it.

    ```bash
      python3 -m venv venv
      source venv/bin/activate
    ```
      OR with pyenv
    ```bash  
      pyenv virtualenv 3.11.2 studybud
      pyenv activate studybud
    ```

2. Inside project folder, install requirements.
    ```bash
      pip install -r requirements.txt
    ```

3. Run the migrations.
    ```bash
      python manage.py migrate
    ```
   
4. Run the server.
    ```bash
      python manage.py runserver
    ```