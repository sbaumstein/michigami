CREATE TABLE football (
    MichiganScore INTEGER NOT NULL,
    OpponentScore INTEGER NOT NULL,
    OpponentName VARCHAR(256) NOT NULL,
    EventType VARCHAR(256) NOT NULL,
    ConferenceGame VARCHAR(256) NOT NULL,
    GameDate DATETIME NOT NULL,
    PRIMARY KEY(GameDate)
);

CREATE TABLE basketball (
    MichiganScore INTEGER NOT NULL,
    OpponentScore INTEGER NOT NULL,
    OpponentName VARCHAR(256) NOT NULL,
    EventType VARCHAR(256) NOT NULL,
    ConferenceGame VARCHAR(256) NOT NULL,
    GameDate DATETIME NOT NULL,
    PRIMARY KEY(GameDate)
);

