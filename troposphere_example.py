# from troposphere import Ref, Template
# from troposphere import ec2


# t = Template()
# ec2_instance = ec2.Instance('MyNewInstance', ImageId='ami-1234567890', InstanceType="t2.micro")
# t.add_resource(ec2_instance)
# print(t.to_json())
# print(t.to_yaml())


from troposphere import Base64, FindInMap, GetAtt, Parameter, Output, Ref, Template, ec2, Sub, Equals


template = Template()

keyname_param = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "access to the instance",
    Type="String",
))

template.add_mapping('RegionMap', {
    "us-east-1":      {"AMI": "ami-7f418316"},
    "us-west-1":      {"AMI": "ami-951945d0"},
    "us-west-2":      {"AMI": "ami-16fd7026"},
    "eu-west-1":      {"AMI": "ami-24506250"},
    "sa-east-1":      {"AMI": "ami-3e3be423"},
    "ap-southeast-1": {"AMI": "ami-74dda626"},
    "ap-northeast-1": {"AMI": "ami-dcfa4edd"}
})

template.add_condition('IsProd', Equals(Ref('prod'), 'Production'))

ec2_instance = template.add_resource(ec2.Instance(
    "Ec2Instance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    KeyName=Ref(keyname_param),
    SecurityGroups=["default"],
    UserData=Base64("80")
))

template.add_output([
    Output(
        "InstanceId",
        Description="InstanceId of the newly created EC2 instance",
        Value=Ref(ec2_instance),
    ),
    Output(
        "AZ",
        Description="Availability Zone of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "AvailabilityZone"),
    ),
    Output(
        "PublicIP",
        Description="Public IP address of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PublicIp"),
    ),
    Output(
        "PrivateIP",
        Description="Private IP address of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PrivateIp"),
    ),
    Output(
        "PublicDNS",
        Description="Public DNSName of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PublicDnsName"),
    ),
    Output(
        "PrivateDNS",
        Description="Private DNSName of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PrivateDnsName"),
    ),
])

with open('cfn_template.json', 'w') as f_tem:
    f_tem.write(template.to_json())

print(template.to_json())