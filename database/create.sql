CREATE TABLE users (username CHAR[8] NOT NULL PRIMARY KEY, 
                    password_hash TEXT,
                    security_level INT CHECK(3 >= security_level >= 1),
                    one_time_id ,
                    ip_address );

INSERT INTO TABLE users VALUES ("Pedro", "this_should_be_a_hash", 3, "another_hash", "127.0.0.1:3000");