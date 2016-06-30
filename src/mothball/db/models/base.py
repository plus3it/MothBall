from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, Boolean
#from sqlalchemy.dialects import postgresql, mysql
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.mysql import JSON


Base = declarative_base()

class Instances(Base):
    """
    Model for Instances Database Table
    """
    __tablename__ = 'Instances'


    id = Column(Integer, primary_key=True, autoincrement=True)
    AccountId = Column(String(12), nullable=False)
    instanceId = Column(String(19), unique= True, nullable=False)
    AvailabilityZone = Column(String(20), nullable=False)

    def __repr__(self):
        """
        Returns all of the attribute data currently set on the model.
        """
        return "<Account(AccountId='{0}', instanceId='{1}', AvailabilityZone='{2}', " \
               "id='{4}'".format(self.AccountId,
                                 self.instanceId,
                                 self.AvailabilityZone,
                                 self.id)


class EBS(Base):
    """
    Model for EBS Database Table
    """
    __tablename__ = 'EBS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AccountId = Column(String(12), nullable=False)
    instanceId = Column(String(19), nullable=False)
    attachmentSet = Column(String(10), nullable=False)
    availabilityZone = Column(String(12), nullable=False)
    createTime = Column(DateTime, nullable=True)
    encrypted = Column(Boolean, default=False, nullable=False)
    iops = Column(Integer)
    kmsKeyId = Column(String(12))
    size = Column(Integer, nullable=False)
    snapshotId = Column(String(22))
    status = Column(String(9))
    tagSet = Column(JSON)
    volumeId = Column(String(12), primary_key=True, nullable=False)
    volumeType = Column(String(8), nullable=False, default='gp2')

    def __repr__(self):
        """
        Returns all of the attribute data currently set on the model.
        """
        return "<EBS(AccountID='{0}', instanceId='{1}', attachmentSet='{2}', availablityZone='{3}'," \
               "createTime='{4}', encrypted='{5}', iops='{6}', kmsKeyId='{7}', size='{8}', snapshotId='{9}', " \
               "status='{10}', tagSet='{11}', volumeId='{12}', volumeType='{13}'".format(self.AccountId,
                                                                                         self.instanceId,
                                                                                         self.attachmentSet,
                                                                                         self.availabilityZone,
                                                                                         self.createTime,
                                                                                         self.encrypted,
                                                                                         self.iops,
                                                                                         self.kmsKeyId,
                                                                                         self.size,
                                                                                         self.snapshotId,
                                                                                         self.status,
                                                                                         self.tagSet,
                                                                                         self.volumeId,
                                                                                         self.volumeType
                                                                                         )


class EIP(Base):
    """
    Model for EIP Database Table
    """
    __tablename__ = 'EIP'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AccountId = Column(String(12), nullable=False)
    instanceId = Column(String(19), nullable=False)
    interfaceId = Column(String(20), nullable=False)
    association = Column(JSON)
    assocAttr = Column(JSON)
    attachment = Column(JSON)
    description = Column(String(255), nullable=False)
    groups = Column(JSON)
    type = Column(String(20))
    MACaddress = Column(String(17), nullable=False)
    owner = Column(String(12), nullable=False)
    privateIP = Column(String(15))
    privateIPs = Column(JSON)
    requester = Column(String(24))
    managed = Column(Boolean, nullable=False)
    SrcDstChk = Column(Boolean, nullable=False)
    status = Column(String(9), nullable=False)
    subnetId = Column(String(24), nullable=False)
    tagSet = Column(JSON)
    vpcId = Column(String(21), nullable=False)

    def __repr__(self):
        """
        Returns all of the attribute data currently set on the model.
        """
        return "<EIP(AccountID='{0}', Id='{1}', instanceId='{2}', interfaceId='{3}'," \
               "association='{4}', assocAttr='{5}', attachment='{6}', description='{7}', " \
               "groups='{8}', type='{9}', MACaddress='{10}', owner='{11}', " \
               "privateIP='{12}', privateIPs='{13}', requester='{14}', managed='{15}', " \
               "SrcDstChk='{16}', status='{17}', subnetId='{18}', tagSet='{19}', " \
               "vpcId='{20}'".format(self.AccountId,
                                     self.id,
                                     self.instanceId,
                                     self.interfaceId,
                                     self.association,
                                     self.assocAttr,
                                     self.attachment,
                                     self.description,
                                     self.groups,
                                     self.type,
                                     self.MACaddress,
                                     self.owner,
                                     self.privateIP,
                                     self.privateIPs,
                                     self.requester,
                                     self.managed,
                                     self.SrcDstChk,
                                     self.status,
                                     self.subnetId,
                                     self.tagSet,
                                     self.vpcId
                                     )


class SecurityGroup(Base):
    """
    Model for SecurityGroup Database Table
    """
    __tablename__ = 'SecurityGroup'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AccountId = Column(String(12), nullable=False)
    instanceId = Column(String(19), nullable=False)
    sgId = Column(String(20), nullable=False)
    description = Column(String(255))
    name = Column(String(100))
    vpcId = Column(String(21), nullable=False)
    ingressRules = Column(JSON)
    egressRules = Column(JSON)
    tagSet = Column(JSON)

    def __repr__(self):
        """
        Returns all of the attribute data currently set on the model.
        """
        return "<SecurityGroup(AccountID='{0}', instanceId='{1}', sgId='{2}', description='{3}', name='{4}'" \
               "vpcId='{5}' ingressRules='{6} egressRules='{7} id='{8} ".format(self.AccountId,
                                                                                self.instanceId,
                                                                                self.sgId,
                                                                                self.description,
                                                                                self.name,
                                                                                self.vpcId,
                                                                                self.ingressRules,
                                                                                self.egressRules,
                                                                                self.id
                                                                                )



























