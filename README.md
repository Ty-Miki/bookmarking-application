# Command Line Bookmarking Application

The application is built using python. It is developed on to of three layers, database layer, command layer and presentation layer.

### The Database Layer

- This layer is concerned with read, write, update and delete database operation and uses sqlite3 as a database.
- Every operation is done using native python syntax for app integrity.

### The Command Layer

* This layer is the main logic behind the app and is the layer that connects the database layer to the presentation layer.
* This is the motor behind the functioning of the app and it is also developed using native python syntax.


### The Presentation Layer

* This layer is concerned with UI and uses the command line to make things simpler.
* All logic to prompt users for input and for displaying output is done in this layer and it is also developed using native python syntax.


This App design promotes advanced OOP python programming concepts like  **Separation of concerns** , **Data Abstraction & Encapsulation** and other core concepts.

If a developer wants to change the presentation layer, like creating a GUI interface or A Web Interface, It can be done with out affecting the app logic or the database and the same goes for command layer and database layer.


#### Third party Libraries used

- requests==2.31.0


#### Application Options

| Option                  | Command | Description                                                                |
| :---------------------- | :------ | :------------------------------------------------------------------------- |
| Add a bookmark          | A       | Adding a new bookmark to the database.                                     |
| List bookmarks by date  | B       | Retrieve saved bookmarks ordered chronologically.                          |
| List bookmarks by title | T       | Retrieve saved bookmarks ordered alphabetically.                           |
| Delete a bookmark       | D       | Delete a saved bookmark from the database.                                 |
| Import GitHub stars     | G       | Import bookmarks from a GitHub account and save<br />them to the database. |
| Update a bookmark       | U       | Update a saved bookmark.                                                   |
| Quit                    | Q       | Quit the app.                                                              |


I am open for further clarifications and Invitations to collaboration.

contact me at my [personal email.](ethioadvance@gmail.com)
