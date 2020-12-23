BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
"id" 		    INTEGER PRIMARY KEY AUTOINCREMENT,
"first_name"    TEXT    NOT NULL,
"last_name" 	TEXT    NOT NULL,
"email" 		TEXT    NOT NULL UNIQUE,
"password"   	TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	CONSTRAINT "PK_Categories_Id" PRIMARY KEY("id" AUTOINCREMENT),
	CONSTRAINT "FK_Categories_User_id" FOREIGN KEY("user_id") REFERENCES users("id")
);


COMMIT;





