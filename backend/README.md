# Overview
This project enables us to maintain a backend project for testing purposes within a parent directory. The goal is to deploy it as a subdirectory, rather than deploying the entire parent folder.

# Instructions
1) Clone this project into your local machine
2) To set up this project in VSCode, open the terminal and execute the following commands:
    2.1) For creating the virtual environment:
    ``` python -m venv venv ```
    2.2) For activating the virtual environment:
    ``` .\venv\Scripts\activate ```
    2.3) For installing the required packages:
    ``` pip install -r requirements.txt ```
    2.4) To run your project:
    ``` uvicorn app:app --reload ```
3) To view it in your browser, copy ans paste this:
    ``` http://127.0.0.1:8000  ``` or this ``` http://127.0.0.1:8000/usersInit  ```
*Note:* 
    Make sure your backend project is running to see a list of user in your frondend
