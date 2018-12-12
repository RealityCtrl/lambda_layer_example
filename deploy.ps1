Compress-Archive -Path C:\Users\david\git\sqs_helper_layer\sqs_helper.py -DestinationPath C:\tmp\code.zip
Import-Module AWSPowerShell
Write-S3Object -BucketName lambda-deployment-realityctrl-sndbx -File C:\tmp\code.zip
$content = [IO.File]::ReadAllText("C:\Users\david\git\sqs_helper_layer\layer.yaml")
$JSONFile = ConvertFrom-Json "$(get-content $(Join-Path C:\Users\david\git\sqs_helper_layer "deploy_params.json"))"
New-CFNStack -StackName mysqshelperlayerstack -TemplateBody $content -Parameter $JSONFile