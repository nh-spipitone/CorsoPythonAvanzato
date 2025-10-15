CREATE TABLE IF NOT EXISTS studente (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome        VARCHAR(32) NOT NULL,
    cognome     VARCHAR(32) NOT NULL,
    eta         INT,
    email       VARCHAR(64)
);


CREATE TABLE IF NOT EXISTS dipartimento (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome        VARCHAR(255) NOT NULL,
    via         VARCHAR(255) NOT NULL
);
