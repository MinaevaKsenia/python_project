BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
"id" 		    INTEGER PRIMARY KEY AUTOINCREMENT,
"first_name"    TEXT    NOT NULL,
"last_name" 	TEXT    NOT NULL,
"email" 		TEXT    NOT NULL UNIQUE,
"password"   	TEXT    NOT NULL
);
COMMIT;





