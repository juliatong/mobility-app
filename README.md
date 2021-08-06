# Mobility-App

## Setup

1. Install dependencies

  ```
  pipenv shell
  pip install -r requirements.txt
  cp env.sample .env
  ```

2. Update the environment variables in `.env` to match your development environment.

3. Create a new MySQL DB and the tables by executing the SQL statements in `db/setup.sql` in MySQL Workbench.

## Running the app

```
flask run
```

Access the site at <http://localhost:5000>.

## Screen Shot

![Screenshot](./screenshot.png)