USE financement;
DROP TABLE IF EXISTS paiement;
DROP TABLE IF EXISTS echeance;
DROP TABLE IF EXISTS garantie;
DROP TABLE IF EXISTS pret;
DROP TABLE IF EXISTS `client`;
DROP TABLE IF EXISTS conseiller;
DROP TABLE IF EXISTS categorie;

CREATE TABLE IF NOT EXISTS categorie (
	id_categorie INT AUTO_INCREMENT PRIMARY KEY,
	libelle_categorie VARCHAR(50) NOT NULL,
	taux_interet_base DECIMAL(5,4) NOT NULL,
	montant_max DECIMAL(15,2) NOT NUll
)ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS conseiller(
	id_conseiller INT AUTO_INCREMENT PRIMARY KEY,
	nom VARCHAR(50) NOT NULL,
	prenom VARCHAR(50) NOT NULL,
	email VARCHAR(100) NOT NULL
)ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS `client`(
	id_client INT AUTO_INCREMENT PRIMARY KEY,
	nom_client VARCHAR(50) NOT NULL,
	prenom_client VARCHAR(50),
	adresse VARCHAR(150),
	tel VARCHAR(20)
)ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS pret (
	id_pret INT AUTO_INCREMENT PRIMARY KEY,
	capital_pret DECIMAL(15,2) NOT NULL,
	taux_interet DECIMAL(5,4) NOT NULL,
	duree_mois_echeance INT NOT NULL,
	date_deblocage DATE NOT NULL,
	remboursmt_mensl DECIMAL(10,2) NOT NULL,
	id_client INT NOT NULL,
	id_categorie INT NOT NULL,
	id_conseiller INT NOT NULL,
	FOREIGN KEY (id_client) REFERENCES `client`(id_client)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	FOREIGN KEY (id_categorie) REFERENCES categorie(id_categorie)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	FOREIGN KEY (id_conseiller) REFERENCES conseiller(id_conseiller)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
)ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS garantie (
	id_garantie INT AUTO_INCREMENT PRIMARY KEY,
	type_garantie VARCHAR(50) NOT NULL,
	valeur DECIMAL(15,2) NOT NULL,
	id_pret INT NOT NULL,
	FOREIGN KEY (id_pret) REFERENCES pret(id_pret)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS echeance (
	id_pret INT NOT NULL,
	num_echeance INT NOT NULL,
	date_limite DATE NOT NULL,
	montant DECIMAL(10,2) NOT NULL,
	PRIMARY KEY (id_pret, num_echeance),
	FOREIGN KEY (id_pret) REFERENCES pret(id_pret)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS paiement (
	id_paiment INT AUTO_INCREMENT PRIMARY KEY,
	date_paiement DATE NOT NULL,
	montant_recupere DECIMAL(10,2) NOT NULL,
	id_pret INT NOT NULL,
	num_echeance INT NOT NULL,
	FOREIGN KEY (id_pret, num_echeance) REFERENCES echeance(id_pret, num_echeance)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)ENGINE=INNODB;