import jenkins
from xml.etree import ElementTree as etree


# Disable job
jenkinsSource = 'http://localhst:8080/'
server = jenkins.Jenkins(jenkinsSource, username = 'kmaran', password = 'pass123')
server.disable_job('watchdog_sample')

# Update Default Values
job_config = server.get_job_config('param_pipeline')
root = etree.fromstring(job_config)
jobs_params = root.find('properties').find('hudson.model.ParametersDefinitionProperty').find('parameterDefinitions')

for job_params in jobs_params:
    if job_params.find('name').text == 'biweekly':
        job_params.find('defaultValue').text = 'false'

updated_xml = etree.tostring(root).decode()
server.reconfig_job('param_pipeline', updated_xml)
# print(updated_xml)

# Build Status
last_build_number = server.get_job_info('sandbox_sample')['lastCompletedBuild']['number']
build_info = server.get_build_info('sandbox_sample', last_build_number)
print("Last Build Number:", last_build_number)
print("Build Status:", build_info['result'])
