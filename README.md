# Remote Control Simulator V2

A Python-based TV remote control simulator integrated with MySQL.

This project is the second version of my Remote Control Simulator, focused on database integration, persistent history, and basic data analysis.

## Features

- Turn the TV on and off
- Change channels
- Increase and decrease volume
- Load channels from MySQL
- Store user actions in MySQL
- View operation history
- View channel statistics
- Handle database connection errors
- Use environment variables for database credentials

## Technologies

- Python
- MySQL
- mysql-connector-python
- python-dotenv
- Rich
- SQL

## Project Structure

python-remote-control-simulator-v2/
├── database.py
├── main.py
├── remote_control.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
└── .env

## Database

The project uses two main tables.

### channels

Stores the available TV channels.

| Column | Description |
|---|---|
| id | Channel identifier |
| channel_number | Channel number |
| name | Channel name |
| category | Channel category |
| country | Channel country |
| language | Channel language |

### history

Stores actions performed during the simulator's execution.

| Column | Description |
|---|---|
| id | History identifier |
| channel_id | Related channel |
| action | Action performed |
| created_at | Date and time of the action |

## Features in Detail

### Remote Control

The simulator allows the user to:

- Turn the TV on and off
- Change to the next channel
- Change to the previous channel
- Increase the volume
- Decrease the volume

### Database Integration

Channels are loaded directly from MySQL instead of being hardcoded in the Python application.

User actions are also stored in the history table.

### History

The user can view the latest recorded actions using the H command.

### Statistics

The user can view channel usage statistics and general activity using the S command.

## Installation

Install the required dependencies:

pip install -r requirements.txt

Create a .env file in the project root with the following variables:

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=remote_control

Make sure the .env file is included in .gitignore and is never committed to GitHub.

## Usage

Run the application with:

python main.py

### Controls

@  Power
>  Next channel
<  Previous channel
+  Increase volume
-  Decrease volume
H  Show history
S  Show statistics
0  Exit

## Project Structure Details

### main.py

Controls the main application flow and user interaction.

### remote_control.py

Contains the RemoteControl class and the core behavior of the simulator.

### database.py

Handles communication between Python and MySQL, including database queries and history registration.

### requirements.txt

Contains the Python dependencies required to run the project.

### .env

Stores local database configuration and credentials.

## Version History

### V1

The first version focused on the basic remote control simulation using Python and object-oriented programming.

The simulator allowed the user to:

- Turn the TV on and off
- Change channels
- Increase and decrease volume

### V2

The second version introduced database integration and a more structured application.

New features include:

- MySQL integration
- Database-driven channels
- Persistent action history
- SQL queries for statistics
- Database error handling
- Environment variables
- Improved project structure
- Requirements management

## Future Version

A future V3 may introduce API integration and additional external services.

## Author

Rodolpho Netto
