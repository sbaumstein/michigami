CREATE TABLE football (
    MichiganScore INTEGER NOT NULL,
    OpponentScore INTEGER NOT NULL,
    OpponentName VARCHAR(256) NOT NULL,
    EventType VARCHAR(256) NOT NULL,
    ConferenceGame VARCHAR(256) NOT NULL,
    PRIMARY KEY(MichiganScore, OpponentScore)
);

CREATE TABLE basketball (
    MichiganScore INTEGER NOT NULL,
    OpponentScore INTEGER NOT NULL,
    OpponentName VARCHAR(256) NOT NULL,
    EventType VARCHAR(256) NOT NULL,
    ConferenceGame VARCHAR(256) NOT NULL,
    PRIMARY KEY(MichiganScore, OpponentScore)
);

