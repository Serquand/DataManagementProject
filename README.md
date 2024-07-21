# Log Collection System

## About

The objective of this program is to retieve log data and analyse it to detect anomalies
It uses an Isolation Forest model to determine if the conncetion attempt is normal or an anomaly, stores the treated data in a NoSQL database and provides a report showing the interacions between the different IP addresses that made the connection attemps.

## Installation

Follow these steps to set up the project locally.

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.x
- MongoDB
- Git

### Step 1: Install Python

1. **Download Python**:
   - Go to the [official Python website](https://www.python.org/downloads/) and download the latest version of Python.

2. **Install Python**:
   - **Windows**: Run the downloaded executable file and follow the instructions. Make sure to check the box that says "Add Python to PATH".
   - **Mac**: Use the downloaded installer or install via Homebrew:
     ```sh
     brew install python
     ```
   - **Linux**: Use your package manager, for example:
     ```sh
     sudo apt update
     sudo apt install python3
     ```

3. **Verify Installation**:
   ```sh
   python --version

### Step 2: Install MongoDB

1. **Download MongoDB**:
   - Go to the [official MongoDB website](https://www.mongodb.com/try/download/community) and download the latest version of Python.

2. **Install Python**:
   - **Windows**: Run the downloaded executable file and follow the instructions.

   - **Mac**: Use the downloaded installer or install via Homebrew:
     ```sh
     brew install mongodb-atlas
     atlas setup
     ```
   - **Linux**: Follow the instructions for your distribution on the MongoDB installation page.
     

3. **Verify Installation**:
   ```sh
   mongo --version

4.  **Run MongoDB**
    - **Windows and Mac**
         ```sh
         mongod

    - **Linux**
         ```sh
         sudo systemctl start mongod

### Step 3: Install Git

1. **Install Git**:

   - **Windows**: Download and install Git from the [official website](https://git-scm.com/download/win).

   - **Mac**: Install via Homebrew:
     ```sh
     brew install git
     ```

   - **Linux**:
     ```sh
     sudo apt update
     sudo apt install git
     ```  

2. **Navigate to your Git repositories folder**
    ```sh
    cd path_to_folder/folder_name/

3. **Clone the Repository:**:
   ```sh
   git clone https://github.com/Serquand/DataManagementProject.git

### Step 3: Create the MongoDB collection

#### Using the MongoDB Shell

1. **Start the MongoDB shell**: Open your terminal or command prompt and start the MongoDB shell by typing:

    ```sh
    mongo
    ```

2. **Create or switch to a database**:

    ```sh
    use DataManagement-Project
    ```

3. **Create a collection**:

    ```sh
    db.createCollection("BeforeTreatment")
    ```

#### Using MongoDB Compass (GUI Client)

1. **Open MongoDB Compass**

2. **Connect to your MongoDB server**: Enter your connection string or connect to `localhost` if you are running MongoDB locally.

3. **Create a new database**:
   - Click on the "Create Database" button.
   - Enter the name "DataManagement-Project" in the "Database Name" field.
   - Enter the name "BeforeTreatment" in the "Collection Name" field.
   - Click "Create Database".

## Running the program

1. **Add the csv file to MongoDB**

    ```sh
    mongoimport --db DataManagement-Project --collection BeforeTreatment --type csv --headerline --file path_to_git_repository/dataset/Test_data.csv
    ```

2. **Analyse the Data**: Run the app.py file

    1. Open your terminal and navigate to the git repository
    ```sh
    cd path_to_git_repository/DataManagementProject/
    ```
    2. Run the app.py file
    ```sh
    python app.py
    ```
    This will create a new collection in your MongoDb database called "AfterTreatment" that will have the processed data.

3. **Get the reports**: Run the queries.py file

    1. Open your terminal and navigate to the git repository
    ```sh
    cd path_to_git_repository/DataManagementProject/
    ```
    2. Run the app.py file
    ```sh
    python queries.py
    ```
    This will provide you a dettailed report of the interactions beween the IP adresses that make and recieve the connection attempts
