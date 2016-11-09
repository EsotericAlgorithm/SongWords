CREATE TABLE songs(id INTEGER PRIMARY KEY ASC, 
				   title TEXT, 
				   artist TEXT,
				   metro TEXT UNIQUE,
				   youtube TEXT UNIQUE);
