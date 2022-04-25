/* Time Track DB File */

/* Drop existing tables */
DROP TABLE IF EXISTS `Tasks`;
DROP TABLE IF EXISTS `Employees`;
DROP TABLE IF EXISTS `Projects`;
DROP TABLE IF EXISTS `Clients`;

/* Create new tables */

CREATE TABLE `Clients` (
  `clientId` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `clientOrganizationName` varchar(35),
  `clientContactFirstName` varchar(35) NOT NULL,
  `clientContactLastName` varchar(35) NOT NULL,
  `clientContactEmail` varchar(254),
  PRIMARY KEY (`clientID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `Projects` (
  `projectId` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `clientId` int(11) NOT NULL,
  `projectDescription` varchar(140) NOT NULL,
  `projectBillRate` decimal(6,2) NOT NULL,
  PRIMARY KEY (`projectId`),
  FOREIGN KEY (`clientId`)
  REFERENCES Clients (`clientId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `Employees` (
  `eeId` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `eeFirstName` varchar(35) NOT NULL,
  `eeLastName` varchar(35) NOT NULL,
  `eePosition` varchar(35) NOT NULL,
  `eeStatus`  tinyint(1) NOT NULL,
  PRIMARY KEY (`eeId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `Tasks` (
  `taskId` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `projectId` int(11) NOT NULL,
  `taskDescription` varchar(240) NOT NULL,
  `taskTime` decimal(6,2) NOT NULL,
  `eeId` int(11),
  PRIMARY KEY (`taskID`),
  FOREIGN KEY (`projectId`)
  REFERENCES Projects (`projectId`),
  FOREIGN KEY (`eeId`)
  REFERENCES Employees (`eeId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

/* Populate new tables */

/* Clients */

INSERT INTO `Clients` (`clientId`, `clientOrganizationName`, `clientContactFirstName`, `clientContactLastName`,`clientContactEmail`)
VALUES (NULL, 'ACME', 'Rafiki', 'Adams ', 'ra@example.com');

INSERT INTO `Clients` (`clientId`, `clientOrganizationName`, `clientContactFirstName`, `clientContactLastName`,`clientContactEmail`)
VALUES (NULL, 'Bat Enterprises', 'Mufasa', 'Ghosh ', 'mg@example.com');

/* Projects */

INSERT INTO `Projects` (`projectId`, `clientId`, `projectDescription`, `projectBillRate`)
VALUES (NULL, 1, 'Monthly garden maintenence at Adams house.', 55.99);

INSERT INTO `Projects` (`projectId`, `clientId`, `projectDescription`, `projectBillRate`)
VALUES (NULL, 2, 'Periodic tree trimming at Ghosh house.', 55.99);

/* Employees */

INSERT INTO `Employees` (`eeId`, `eeFirstName`, `eeLastName`, `eePosition`, `eeStatus`)
VALUES (NULL, 'Brandi','Bingo','Manager',1);

INSERT INTO `Employees` (`eeId`, `eeFirstName`, `eeLastName`, `eePosition`, `eeStatus`)
VALUES (NULL, 'Shenzi','Filson','Associate',1);

/* Tasks */

INSERT INTO `Tasks` (`taskId`, `projectId`, `taskDescription`, `taskTime`, `eeId`)
VALUES (NULL, 1, 'Pulled weeds all damn day', 3.4, 1);

INSERT INTO `Tasks` (`taskId`, `projectId`, `taskDescription`,`taskTime`, `eeId`)
VALUES (NULL, 2, 'Trimmed 57 trees.', 2.5, 2);
