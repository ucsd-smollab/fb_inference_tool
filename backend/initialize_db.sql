DROP DATABASE IF EXISTS privacy_db;
CREATE DATABASE privacy_db;

USE privacy_db;

CREATE TABLE participant_profile (
	participant_url VARCHAR(50) NOT NULL,
	name VARCHAR(50) NOT NULL,
	prof_pic_url VARCHAR(400) NOT NULL,
	perc_comp_total FLOAT(4, 3) UNSIGNED NOT NULL,
	perc_comp_inf FLOAT(4, 3) UNSIGNED NOT NULL,
	religion VARCHAR(50) ,
	politics VARCHAR(50),
    num_friends_scraped SMALLINT DEFAULT 0,
    PRIMARY KEY(participant_url)
);

CREATE TABLE friend_profiles (
	friend_url VARCHAR(50) NOT NULL,
	name VARCHAR(50) NOT NULL,
	prof_pic_url VARCHAR(400) NOT NULL,
    mutual_count SMALLINT NOT NULL,
	perc_comp_total FLOAT(4, 3) UNSIGNED NOT NULL,
	perc_comp_inf FLOAT(4, 3) UNSIGNED NOT NULL,
	religion VARCHAR(50) ,
	politics VARCHAR(50),
    PRIMARY KEY(friend_url)
);

CREATE TABLE mutual_friends (
	friend_url VARCHAR(50) NOT NULL,
    mutual_url VARCHAR(50) NOT NULL,
    PRIMARY KEY(friend_url, mutual_url)
);

CREATE TABLE work (
	friend_url VARCHAR(50) NOT NULL,
    workplace VARCHAR(100) NOT NULL,
    PRIMARY KEY(friend_url, workplace)
);

CREATE TABLE college (
	friend_url VARCHAR(50) NOT NULL,
    college_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(friend_url, college_name)
);

CREATE TABLE high_school (
	friend_url VARCHAR(50) NOT NULL,
    hs_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(friend_url, hs_name)
);

CREATE TABLE places_lived (
	friend_url VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    PRIMARY KEY(friend_url, location)
);

CREATE TABLE friend_inf (
	friend_url VARCHAR(50) NOT NULL,
    work_inf VARCHAR(50),
    college_inf VARCHAR(50),
    high_school_inf VARCHAR(50),
    places_lived_inf VARCHAR(50),
	religion_inf VARCHAR(50),
	politic_inf VARCHAR(50),
    PRIMARY KEY(friend_url)
);

CREATE TABLE work_inf (
	friend_url VARCHAR(50) NOT NULL,
    workplace VARCHAR(100) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, workplace)
);

CREATE TABLE college_inf (
	friend_url VARCHAR(50) NOT NULL,
    college_name VARCHAR(100) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, college_name)
);

CREATE TABLE high_school_inf (
	friend_url VARCHAR(50) NOT NULL,
    hs_name VARCHAR(100) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, hs_name)
);

CREATE TABLE places_lived_inf (
	friend_url VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, location)
);

CREATE TABLE religion_inf (
	friend_url VARCHAR(50) NOT NULL,
    religious_belief VARCHAR(100) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, religious_belief)
);

CREATE TABLE politics_inf (
	friend_url VARCHAR(50) NOT NULL,
    political_view VARCHAR(100) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, political_view)
);

CREATE TABLE attribute_count (
	attribute VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    mutual_count SMALLINT NOT NULL DEFAULT 0,
    inf_count SMALLINT NOT NULL DEFAULT 0,
    PRIMARY KEY(attribute, category)
);

CREATE TABLE mutual_count (
    friend_url VARCHAR(50) NOT NULL,
	attribute VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    mutual_count SMALLINT NOT NULL DEFAULT 0,
    PRIMARY KEY(friend_url, category, attribute)
);