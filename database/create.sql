DROP TABLE IF EXISTS users;

CREATE TABLE users (username CHAR[8] NOT NULL PRIMARY KEY, 
                    password_hash TEXT NOT NULL,
                    security_level INT CHECK(3 >= security_level >= 1) NOT NULL,
                    one_time_id TEXT NOT NULL,
                    ip_address TEXT,
                    public_key TEXT,
                    token TEXT,
                    symmetric_key TEXT,
                    symmetric_key_iv TEXT,
                    challenge TEXT,
                    challenge_timeout DATE
            );

INSERT INTO users VALUES ("Pedro", "this_should_be_a_hash", 3, "another_hash", "127.0.0.1:3000", null, null, null, null, null, null);
INSERT INTO users VALUES ("Raul", "123", 3, "111", "127.0.0.1:3000", null, null, null, null, null, null);
