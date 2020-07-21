from stacker.blueprints.base import Blueprint

from stacker.blueprints.variables.types import (
    CFNString
)

from troposphere import (
    AWS_REGION,
    AWSHelperFn,
    Condition,
    Equals,
    If,
    Output,
    Ref,
    Sub,
    ec2,
    elasticloadbalancingv2 as alb
)

class EC2(Blueprint):
    VARIABLES = {
        'Environment': {
            'type': CFNString,
            'description': 'Name of the environment'
        },
        'Product': {
            'type': CFNString,
            'description': 'Name of the product'
        },
        'ImageId': {
            'type': CFNString,
            'description': 'ID of the AMI to use as the master node'
        },
        'KmsId': {
            'type': CFNString,
            'description': 'The KMS key to encrypt disks'
        },
        'InstanceType': {
            'type': CFNString,
            'description': 'The instance type and size for the master'
        },
        'AlbDns': {
            'type': CFNString,
            'description': 'DNS name for the application load balancer'
        },
        'AlbSecurityGroup': {
            'type': CFNString,
            'description': 'Security Group ID of the Jenkins Load Balancer'
        },
        'InstanceProfile': {
            'type': CFNString,
            'description': 'ARN of the instance profile to assign the master node'
        },
        'ListenerArn': {
            'type': CFNString,
            'description': 'ARN of the listener to which we want listener rule attached'
        },
        'ListenerRulePriority': {
            'type': CFNString,
            'description': 'What priority this rule should have'
        },
        'SubnetId': {
            'type': CFNString,
            'description': 'ID of the subnet this stack should be placed in'
        },
        'VpcId': {
            'type': CFNString,
            'description': 'ID of the VPC this stack should be placed in'
        },
        'JumpServerSecurityGroupId': {
            'type': CFNString,
            'description': 'ID of the security group for the jump server allowed to ssh to this host'
        },
        'UserData': {
            'type': AWSHelperFn,
            'description': 'base64 encoded string of the userdata for the instance',
            'default': Ref('AWS::NoValue')
        }
    }

    def get_tags(self):
        return [
                ec2.Tag('Owner', 'Deploy'),
                ec2.Tag('Name', Sub('${Environment} Deploy Jenkins Master')),
                ec2.Tag('athenahealth:zone', 'ee'),
                ec2.Tag('athenahealth:function', 'dss'),
                ec2.Tag('athenahealth:team', 'DEPLOY'),
                ec2.Tag('athenahealth:environment', If('IsProd', 'Production', Ref('Environment'))),
                ec2.Tag('Deploy Environment', Ref('Environment')),
                ec2.Tag('maid_offhours', 'off')
            ]

    def create_conditions(self):
        t = self.template

        t.add_condition('IsProd', Equals(Ref('Environment'), 'prod'))

    def create_security_groups(self):
        t = self.template

        self.master_sg = t.add_resource(ec2.SecurityGroup(
            'JenkinsMasterSecurityGroup',
            GroupDescription='Security Group for Jenkins Master Node',
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    SourceSecurityGroupId=Ref('AlbSecurityGroup'),
                    FromPort='443',
                    ToPort='443',
                    IpProtocol='tcp'
                ),
                ec2.SecurityGroupRule(
                    SourceSecurityGroupId=Ref('JumpServerSecurityGroupId'),
                    FromPort='22',
                    ToPort='22',
                    IpProtocol='tcp'
                )
            ],
            VpcId=Ref('VpcId'),
            Tags=self.get_tags()
        ))

        self.slave_sg = t.add_resource(ec2.SecurityGroup(
            'JenkinsSlaveSecurityGroup',
            GroupDescription='Security Group for Jenkins Slave Nodes',
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    SourceSecurityGroupId=self.master_sg.Ref(),
                    IpProtocol='-1'
                )
            ],
            VpcId=Ref('VpcId'),
            Tags=self.get_tags()
        ))

    def create_ec2_instances(self):
        t = self.template

        self.master_instance = t.add_resource(ec2.Instance(
            'JenkinsEC2Instance',
            ImageId=Ref('ImageId'),
            IamInstanceProfile=Ref('InstanceProfile'),
            InstanceType=Ref('InstanceType'),
            SubnetId=Ref('SubnetId'),
            UserData=self.get_variables()['UserData'],
            SecurityGroupIds=[self.master_sg.Ref()],
            BlockDeviceMappings=[
                ec2.BlockDeviceMapping(
                    DeviceName='/dev/sda1',
                    Ebs=ec2.EBSBlockDevice(
                        DeleteOnTermination=True,
                        VolumeSize=15,
                        Encrypted=True,
                        KmsKeyId=Ref('KmsId')
                    )
                ),
                ec2.BlockDeviceMapping(
                    DeviceName='/dev/sdg',
                    Ebs=ec2.EBSBlockDevice(
                        DeleteOnTermination=False,
                        VolumeSize=50,
                        Encrypted=True,
                        KmsKeyId=Ref('KmsId')
                    )
                )
            ],
            Tags=self.get_tags(),
        ))

    def create_target_groups(self):
        t = self.template

        self.target_group = t.add_resource(alb.TargetGroup(
            'JenkinsMasterHTTPSTargetGroup',
            TargetType='instance',
            Targets=[
                alb.TargetDescription(
                    Id=self.master_instance.Ref(),
                    Port=443
                )
            ],
            HealthCheckPath='/jenkins/login',
            Port=443,
            Protocol='HTTPS',
            VpcId=Ref('VpcId'),
            Tags=self.get_tags()
        ))

    def create_alb_listener_rules(self):
        t = self.template

        t.add_resource(alb.ListenerRule(
            'JenkinsMasterListenerRule',
            ListenerArn=Ref('ListenerArn'),
            Priority=Ref('ListenerRulePriority'),
            Actions=[
                alb.Action(
                    Type='forward',
                    TargetGroupArn=self.target_group.Ref()
                )
            ],
            Conditions=[
                alb.Condition(
                    Field='host-header',
                    HostHeaderConfig=alb.HostHeaderConfig(
                        Values=[Ref('AlbDns')]
                    )
                ),
                alb.Condition(
                    Field='path-pattern',
                    PathPatternConfig=alb.PathPatternConfig(
                        Values=['/jenkins/*', '/jenkins']
                    )
                )
            ]
        ))

    def create_outputs(self):
        t = self.template

        t.add_output(Output(
            'JenkinsSlaveSecurityGroup',
            Value=self.slave_sg.Ref()
        ))

    def create_template(self):
        self.create_conditions()
        self.create_security_groups()
        self.create_ec2_instances()
        self.create_target_groups()
        self.create_alb_listener_rules()
        self.create_outputs()

    def get_template(self):
        return self.template.to_json()


ec2_obj = EC2("Ec2Instance", context={})
ec2_obj.create_template()
print(ec2_obj.get_template())