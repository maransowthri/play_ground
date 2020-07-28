import os
import jenkins
import requests


jenkins_url="https://deploy.aws.athenahealth.com/jenkins/"
os.environ.setdefault("PYTHONHTTPSVERIFY", "0")
server = jenkins.Jenkins(jenkins_url, username='kmaran',password='11f921cf40dfc75223bc0f5ded5889a98e')
# user = server.get_whoami()
# version = server.get_version()
# print('Hello %s from Jenkins %s' % (user['fullName'], version))
job_instance = server.get_job_info('Watchdog')
print(job_instance)
# latestBuild=job_instance.get_last_build()
# print("Status of the job %s is %s"%(job_instance,latestBuild.get_status()))
# print(os.getenv('PYTHONHTTPSVERIFY', '1'))