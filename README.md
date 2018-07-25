# Fabdeploy

[![N|Solid](http://docs.fabfile.org/en/1.14/_static/logo.png)](http://docs.fabfile.org/en/1.14/index.html)

CLI deployment tool built on top of fabric

## Installing 

```
    pip install -r requirement-fabric.txt
```

## Getting Started

1. Copy fabric-config.example.yaml and rename it ot fabric-config.yml
    ```
        cp fabric-config-example.yml fabric-config.yml
    ```

- Add the host the appropiate configuration
    ``` YAML
        outdev:  # hostname id
            name: 'outdev-combo01'                                          # SSH hostname
            user: 'USERNAME'                                                # SSH username
            api_url: 'https://outdev-kb.acustream.com/knowledgebase/api'    # URL to the api for building frontend 
            path: '/usr/local/kb'                                           # Path for project
            log_path: '/var/log/kb'                                         # Path for log
            branch: 'DEFAULT_BRANCH_TO_DEPLOY'                              # DEFAULT_BRANCH_TO_DEPLOY
            tomcat_user: 'tomcat'                                           # tomcat user
    ```
    > You may add as many host as required with distinct hostname id
- Test the connection
    ``` sh
    fab server:[hostname id] test
    ```
    Example

    ``` sh
    fab server:outdev test
    ```

    
    This should output
     
    ```
    Connection on outdev-combo01: SUCCESS 
    ```
    Which means you have succesfully configured fabdeploy
     
 - To view the task list
    ``` sh
    fab --list
    ```
    This lists out all the task you can perform 
    > Let try view the log from outdev
    
 - View log   
   ``` sh
    fab server:outdev log
    ```
    This lists out all the log file, you can type in the log filename to monitor.

## Running a Task

For HOSTNAME_ID = outdev
1. Deployment

    ``` sh
    fab server:outdev deploy:lf-dev 
    ```
2. Test Connection

    ``` sh
    fab server:outdev test
    ```
3. Reboot
    ``` sh
    fab server:outdev reboot 
    ```
4. Status: Check which branch is deployed
    ``` sh
    fab server:outdev status 
    ```

5. View log:
   ``` sh
    fab server:outdev log:[FILENAME]
    ```
    OR if you don't provide the FILENAME is will print out all the log files 

## Other Features

1. Adding notifications
    ```YAML
        slack: # notification id 
            enable: true  
            message_key: 'text'
            header: ':robot_face:'
            default_msg: '{"text":"default_msg"}'
            endpoint: 'https://hooks.slack.com/services/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'  # ENDPOINT FOR SLACK
    ```
    - enable : enable notification
    - message_key : key in the default_msg  JSON where custom message can be passed 
    - header: header for all the notification
    - endpoint: URL endpoint of the service

## TODO Features
 - Validation for config

