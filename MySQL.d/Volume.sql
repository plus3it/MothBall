CREATE TABLE `Volume` (
   `AccountId` VARCHAR(12) NOT NULL,
   `instanceId` VARCHAR(19) NOT NULL,
   `attachmentSet` VARCHAR(10) NOT NULL,
   `availabilityZone` VARCHAR(12) NOT NULL,
   `createTime` DATETIME DEFAULT NULL,
   `encrypted` BOOL DEFAULT 0,
   `iops` SMALLINT DEFAULT NULL,
   `kmsKeyId` VARCHAR(12) DEFAULT NULL,
   `size` SMALLINT NOT NULL,
   `snapshotId` VARCHAR(13) DEFAULT NULL,
   `status` VARCHAR(9) DEFAULT NULL,
   `tagSet` JSON DEFAULT NULL,
   `volumeId` VARCHAR(12) NOT NULL,
   `volumeType` VARCHAR(8) NOT NULL DEFAULT 'gp2',
   PRIMARY KEY (`volumeId`)
);
