# eForm-Auth-Broker

[![Build Status](https://dev.azure.com/SUMSC/eForm/_apis/build/status/SUMSC.eForm-Auth-Broker?branchName=master)](https://dev.azure.com/SUMSC/eForm/_build/latest?definitionId=2&branchName=master)

JWT Issuer of SUMSC eForm service

## Usage

POST Request
```
id: "学号"
token: md5("密码")
```

Response
```
201
status: True/False
data: JWT/Authentication error
```
