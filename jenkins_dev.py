import os
import jenkins
from xml.etree import ElementTree as etree


jenkins_url="https://deploy-dev.aws.athenahealth.com/jenkins/"
os.environ.setdefault("PYTHONHTTPSVERIFY", "0")
server = jenkins.Jenkins(jenkins_url, username='kmaran', password='111bb4bae9b874f4a38d1cdb95ef81031d')

# Update Default Values
job_config = server.get_job_config('job_sample')
root = etree.fromstring(job_config)
jobs_params = root.find('properties').find('hudson.model.ParametersDefinitionProperty').find('parameterDefinitions')

for job_params in jobs_params:
    if job_params.find('name').text == 'executed_user':
        job_params.find('defaultValue').text = 'jenkins'

updated_xml = etree.tostring(root).decode()
server.reconfig_job('job_sample', updated_xml)

# Build Status
last_build_number = server.get_job_info('job_sample')['lastCompletedBuild']['number']
build_info = server.get_build_info('job_sample', last_build_number)
print("Last Build Number:", last_build_number)
print("Build Status:", build_info['result'])


# Disable job
server.disable_job('job_sample')
