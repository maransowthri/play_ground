import jenkins

jenkinsSource = 'http://localhost:8080/'
server = jenkins.Jenkins(jenkinsSource, username = 'kmaran', password = 'pass123')
# myJob = server.get_job("param_pipeline")
server.disable_job('param_pipeline')
# new = myConfig.replace('<string>clean</string>', '<string>string bean</string>')
# myJob.update_config(new)