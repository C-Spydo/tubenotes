# StockyAI API
AI Chatbot demonstrating the use of Retrieval-Augmented Generation (RAG)

## How to start
run `(https://github.com/C-Spydo/stockyai.git)` in the directory to be used

## Install dependencies
Install dependencies using `pip install -r requirements.txt`, preferably in a virtual enviroment

## Handling Migrations
To initialize migrations (if repo doesn't already contain a migrations folder)
`flask db init`

To run a migration after updating a table
`flask db migrate -m 'your migration message'`

To update your database after downloading an updated migrations folder or running a migration
`flask db upgrade`

To rollback changes to your database after upgrading it
`flask db downgrade`

## Run Flask App (Development Mode)
run `flask run` in the terminal of your project directory 


