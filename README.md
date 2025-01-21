# webapp_template

## Description

A brief description of your web application.

## Installation

### Backend

1. Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Set up environment variables:
    - `SUPABASE_URL`: The URL of your Supabase project.
    - `SUPABASE_KEY`: The anonymous key for your Supabase project.
    - `SECRET_KEY`: The secret key for your Supabase project.
    - `DATABASE_URL`: The URL of your supabase database.
4. Start the backend server:
    ```bash
    docker compose up --build
    ```

### Frontend

1. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Set up environment variables:
    - `NEXT_PUBLIC_SUPABASE_URL`: The URL of your Supabase project.
    - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: The anonymous key for your Supabase project.

4. Start the frontend development server:
    ```bash
    npm run dev
    ```

## Usage

Instructions on how to use the application.

## Contributing

Guidelines for contributing to the project.

## License

[Specify the license under which the project is distributed.]