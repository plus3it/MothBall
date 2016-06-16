import json
import logging

from mothball.db.models.base import EBS, EIP, SecurityGroup, Instances
from mothball.managers.base import AWSServiceManager


class EBSManager(AWSServiceManager):

    def __init__(self, ec2_session, db_session):
        super(EBSManager, self).__init__(ec2_session, db_session)

    def create_record(self, account_id, instance_id, instance):

        devices = self.ec2_session.Instance(instance).block_device_mappings

        for dev in devices:
            new_ebs = EBS()
            new_ebs.AcountId = account_id
            new_ebs.instanceId = instance_id
            new_ebs.attachmentSet = dev['DeviceName']

            volume = self.ec2_session.Volume(new_ebs.volumeId)
            new_ebs.volumeId = volume.volume_id
            new_ebs.size = volume.size
            new_ebs.volumeType = volume.volume_type
            new_ebs.iops = volume.iops
            new_ebs.availabilityZone = volume.availability_zone
            new_ebs.tagSet = json.dumps(volume.tags)
            new_ebs.createTime = volume.created_time
            new_ebs.encrypted = volume.encrypted
            new_ebs.kmsKeyId = volume.kms_key_id
            new_ebs.snapshotId = volume.snapshot_id
            new_ebs.status = volume.state

            self.db_session.update(new_ebs)


class EIPManager(AWSServiceManager):

    def __init__(self, ec2_session, db_session):
        super(EIPManager, self).__init__(ec2_session, db_session)

    def create_record(self, account_id, instance_id, instance):

        interfaces = self.ec2_session.Instance(instance).network_interfaces_attribute

        for interface in interfaces:
            new_eip = EIP()
            new_eip.AccountId = account_id
            new_eip.instanceId = instance_id

            nid = self.ec2_session.NetworkInterface(interface['NetworkInterfaceId'])
            new_eip.association = nid.association
            new_eip.assocAttr = nid.association_attribute
            new_eip.attachment = nid.attachment
            new_eip.description = nid.description
            new_eip.groups = nid.groups
            new_eip.interfaceId = nid.id
            new_eip.type = nid.interface_type
            new_eip.MACaddress = nid.mac_address
            new_eip.owner = nid.owner_id
            new_eip.privateIP = nid.private_ip_address
            new_eip.privateIPs = nid.private_ip_addresses
            new_eip.requester = nid.requester_id
            new_eip.managed = nid.requester_managed
            new_eip.SrcDstChk = nid.source_dest_check
            new_eip.status = nid.status
            new_eip.subnetId = nid.subnet_id
            new_eip.tagSet = nid.tag_set
            new_eip.vpcId = nid.vpc_id

            self.db_session.update(new_eip)

class SecurityGroupManager(AWSServiceManager):

    def __init__(self, ec2_session, db_session):
        super(SecurityGroupManager, self).__init__(ec2_session, db_session)

    def create_record(self, account_id, instance_id, instance):

        sgs = self.ec2_session.Instance(instance).security_groups

        for sg in sgs:
            new_sg = SecurityGroup()

            secgroup = self.ec2_session.SecurityGroup(sg['GroupId'])
            new_sg.sgId = sg.GroupId
            new_sg.AccountId = account_id
            new_sg.instanceId = instance_id
            new_sg.description = secgroup.description
            new_sg.name = secgroup.group_name
            new_sg.ingressRules = secgroup.ip_permissions
            new_sg.egressRules = secgroup.ip_permissions_egress
            new_sg.vpcId = secgroup.vpc_id
            new_sg.tagSet = secgroup.tags

            self.db_session.update(new_sg)


class Instance(AWSServiceManager):

    def __init__(self, ec2_session, db_session):
        super(Instance, self).__init__(ec2_session, db_session)

    def create_record(self, account_id, instance_id, instance):

        new_inst = Instances()

        new_inst.AccountId = account_id
        new_inst.instanceId = instance_id
        new_inst.AvailabilityZone = None

        self.db_session.update(new_inst)
