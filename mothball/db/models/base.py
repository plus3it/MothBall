from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy.dialects.mysql import JSON


Base = declarative_base()


class EBS(Base):

    __tablename__ = 'EBS'

    AccountId = Column(String(12), nullable=False)
    instanceId = Column(String(19), nullable=False)
    attachmentSet = Column(String(10), nullable=False)
    availabilityZone = Column(String(12), nullable=False)
    createTime = Column(DateTime, nullable=True)
    encrypted = Column(Boolean, nullable=False)
    iops = Column(Integer, default='NULL')
    kmsKeyId = Column(String(12), default='NULL')
    size = Column(Integer, nullable=False)
    snapshotId = Column(String(13), default='Null')
    status = Column(String(9), default='NULL')
    # tagSet = Column(JSON, default='NULL')
    tagSet = Column(String, default='NULL')
    volumeId = Column(String(12), primary_key=True, nullable=False)
    volumeType = Column(String(8), nullable=False, default='gp2')

    def __repr__(self):
        return "<EBS(AccountID='{0}', instanceId='{1}', attachmentSet='{2}', availablityZone='{3}'," \
               "createTime='{4}', encrypted='{5}', iops='{6}', kmsKeyId='{7}', size='{8}', snapshotId='{9}', " \
               "status='{10}', tagSet='{11}', volumeId='{12}', volumeType='{13}'".format(self.AccountId,
                                                                                         self.instanceId,
                                                                                         self.attachmentSet,
                                                                                         self.availabilityZone,
                                                                                         self.createTime,
                                                                                         self.encypted,
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

    __tablename__ = 'EIP'

    AccountId = Column(String(12), nullable=False)
    instanceId = Column(String(19), nullable=False)
    MACaddress_orig = Column(String(17), default='NULL')
    MACaddress_new = Column(String(17), default='NULL')
    ifaceId_orig = Column(String(21), nullable=False, unique=True)
    ifaceId_new = Column(String(21), default='NULL', unique=True)
    privateDNS_orig = Column(String(255), default='NULL')
    privateDNS_new = Column(String(255), default='NULL')
    privateIP_orig = Column(String(15), default='NULL')
    privateIP_new = Column(String(15), default='NULL')
    publicDNS_orig = Column(String(255), default='NULL')
    publicDNS_new = Column(String(255), default='NULL')
    publicIP_orig = Column(String(15), default='NULL')
    publicIP_new = Column(String(15), default='NULL')
    SrcDstChk = Column(Boolean, default=False)
    SubnetId_orig = Column(String(24), nullable=False)
    SubnetId_new = Column(String(24), default='NULL')
    VpcId_orig = Column(String(21), nullable=False)
    VpcId_new = Column(String(21), default='NULL')

    def __repr__(self):
        return "<EIP(AccountID='{0}', instanceId='{1}', MACaddress_orig='{2}', MACaddress_new='{3}'," \
               "ifaceId_orig='{4}', ifaceId_new='{5}', privateDNS_orig='{6}', privateDNS_new='{7}', " \
               "privateIP_orig='{8}', privateIP_new='{9}', publicDNS_orig='{10}', publicDNS_new='{11}', " \
               "publicIP_orig='{12}', publicIP_new='{13}', SrcDstChk='{14}', SubnetId_orig='{15}', " \
               "SubnetId_new='{16}', VpcId_orig='{17}', VpcId_new='{18}'".format(self.AccountId,
                                                                                 self.instanceId,
                                                                                 self.MACaddress_orig,
                                                                                 self.MACaddress_new,
                                                                                 self.ifaceId_orig,
                                                                                 self.ifaceId_new,
                                                                                 self.privateDNS_orig,
                                                                                 self.privateDNS_new,
                                                                                 self.privateIP_orig,
                                                                                 self.privateIP_new,
                                                                                 self.publicDNS_orig,
                                                                                 self.publicDNS_new,
                                                                                 self.publicIP_orig,
                                                                                 self.publicIP_new,
                                                                                 self.SrcDstChk,
                                                                                 self.SubnetId_orig,
                                                                                 self.SubnetId_new,
                                                                                 self.VpcId_orig,
                                                                                 self.VpcId_new
                                                                                 )


class Instance(Base):
    pass


class SecurityGroup(Base):

    __tablename__ = 'SecurityGroup'

    AccountId = Column(String(12), nullable=False)
    sgId = Column(String(20), nullable=False, unique=True)
    sgName = Column(String(100), default='NULL')
    vpcAssn = Column(String(21), nullable=False)
    # ingressRules = Column(JSON, default='NULL')
    # egressRules = Column(JSON,default='NULL')
    ingressRules = Column(String, default='NULL')
    egressRules = Column(String, default='NULL')

    def __repr__(self):
        return "<SecurityGroup(AccountID='{0}', sgId='{1}', sgName='{2}', vpcAssn='{3}', ingressRules='{4}'" \
               "egressRules='{5}'".format(self.AccountId,
                                          self.sgId,
                                          self.sgName,
                                          self.vpcAssn,
                                          self.ingressRules,
                                          self.egressRules
                                          )



























