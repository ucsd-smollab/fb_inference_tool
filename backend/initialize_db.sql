DROP DATABASE IF EXISTS privacy_db;
CREATE DATABASE privacy_db;

USE privacy_db;

CREATE TABLE participant_profile (
	participant_url VARCHAR(500) NOT NULL,
	name VARCHAR(1000) NOT NULL,
	prof_pic_url VARCHAR(1000) NOT NULL,
	perc_comp_total FLOAT(4, 3) UNSIGNED NOT NULL,
	perc_comp_inf FLOAT(4, 3) UNSIGNED NOT NULL,
	religion VARCHAR(1000) ,
	politics VARCHAR(1000),
    num_friends_scraped SMALLINT DEFAULT 0,
    PRIMARY KEY(participant_url)
);

CREATE TABLE friend_profiles (
	friend_url VARCHAR(500) NOT NULL,
	name VARCHAR(1000) NOT NULL,
	prof_pic_url VARCHAR(1000) NOT NULL,
    mutual_count SMALLINT NOT NULL,
	perc_comp_total FLOAT(4, 3) UNSIGNED NOT NULL,
	perc_comp_inf FLOAT(4, 3) UNSIGNED NOT NULL,
	religion VARCHAR(1000) ,
	politics VARCHAR(1000),
    PRIMARY KEY(friend_url)
);

CREATE TABLE mutual_friends (
	friend_url VARCHAR(200) NOT NULL,
    mutual_url VARCHAR(200) NOT NULL,
    PRIMARY KEY(friend_url, mutual_url)
);

CREATE TABLE work (
	friend_url VARCHAR(200) NOT NULL,
    workplace VARCHAR(400) NOT NULL,
    PRIMARY KEY(friend_url, workplace)
);

CREATE TABLE college (
	friend_url VARCHAR(200) NOT NULL,
    college_name VARCHAR(400) NOT NULL,
    PRIMARY KEY(friend_url, college_name)
);

CREATE TABLE high_school (
	friend_url VARCHAR(200) NOT NULL,
    hs_name VARCHAR(400) NOT NULL,
    PRIMARY KEY(friend_url, hs_name)
);

CREATE TABLE places_lived (
	friend_url VARCHAR(200) NOT NULL,
    location VARCHAR(400) NOT NULL,
    PRIMARY KEY(friend_url, location)
);

CREATE TABLE friend_inf (
	friend_url VARCHAR(200) NOT NULL,
    work_inf VARCHAR(1000),
    college_inf VARCHAR(1000),
    high_school_inf VARCHAR(1000),
    places_lived_inf VARCHAR(1000),
	religion_inf VARCHAR(1000),
	politic_inf VARCHAR(1000),
    PRIMARY KEY(friend_url)
);

CREATE TABLE work_inf (
	friend_url VARCHAR(200) NOT NULL,
    workplace VARCHAR(400) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, workplace)
);

CREATE TABLE college_inf (
	friend_url VARCHAR(200) NOT NULL,
    college_name VARCHAR(400) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, college_name)
);

CREATE TABLE high_school_inf (
	friend_url VARCHAR(200) NOT NULL,
    hs_name VARCHAR(400) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, hs_name)
);

CREATE TABLE places_lived_inf (
	friend_url VARCHAR(200) NOT NULL,
    location VARCHAR(400) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, location)
);

CREATE TABLE religion_inf (
	friend_url VARCHAR(200) NOT NULL,
    religious_belief VARCHAR(400) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, religious_belief)
);

CREATE TABLE politics_inf (
	friend_url VARCHAR(200) NOT NULL,
    political_view VARCHAR(400) NOT NULL,
    mutual_count SMALLINT DEFAULT '0' NOT NULL,
    PRIMARY KEY(friend_url, political_view)
);

CREATE TABLE attribute_count (
	attribute VARCHAR(400) NOT NULL,
    category VARCHAR(400) NOT NULL,
    mutual_count SMALLINT NOT NULL DEFAULT 0,
    inf_count SMALLINT NOT NULL DEFAULT 0,
    PRIMARY KEY(attribute, category)
);

CREATE TABLE mutual_count (
    friend_url VARCHAR(200) NOT NULL,
		attribute VARCHAR(400) NOT NULL,
    category VARCHAR(400) NOT NULL,
    mutual_count SMALLINT NOT NULL DEFAULT 0,
    PRIMARY KEY(friend_url, category, attribute)
);

CREATE TABLE stop_scraping (
		stop TINYINT(1),
    PRIMARY KEY(stop)
);
