CREATE TABLE `SecurityGroup` (
   `AccountId` VARCHAR(12) NOT NULL,
   `sgId` VARCHAR(20) NOT NULL,
   `sgName` VARCHAR(100) DEFAULT NULL,
   `vpcAssn` VARCHAR(21) NOT NULL,
   `ingressRules` JSON DEFAULT NULL,
   `egressRules` JSON DEFAULT NULL,
   UNIQUE KEY (`sgId`)
)
