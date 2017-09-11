--Wirte by Shitao Tang, Yehan Xiao

USE db_SUCS;
CREATE TABLE image_info
(
    token VARCHAR(100),
    time INTEGER,
    longitude DOUBLE,
    latitude DOUBLE,
    url VARCHAR(200),
    PRIMARY KEY(token,time,url)
);

CREATE TABLE account
(
    username VARCHAR(20),
    password_md5 VARCHAR(100)
);

CREATE TABLE images
(
    image_md5 VARCHAR(100)
);

INSERT INTO account VALUES ("root","871ce144069ea0816545f52f09cd135d1182262c3b235808fa5a3281");