*** Settings ***
Library     class_moshellcommand.py
Library     RequestsLibrary
Library     Collections

*** Variables ***
${base_url}         https://reqres.in/api/users
${page_id}          2
${expectedname}     test
${expectedjob}      team leader


*** Test Cases ***
Test mosehll command1 to show alarm
        ${result}=     class_moshellcommand.Commandexecution        alt
        Should Be Equal As Numbers   ${result}     0

Test moshell command2 to show status of cell
        ${result}=     class_moshellcommand.Commandexecution        st cell
        Should Be Equal As Numbers    ${result}     0

Test SSH close
        ${value}=      class_moshellcommand.Ssh_close
        Should Be Equal As Integers    ${value}    0


Test simulation to run TM500 test case via API call
    &{req_body}=  Create Dictionary    name=test        job=team leader
    ${response}=     POST        ${base_url}     json=${req_body}    expected_status=201
    log      ${response.json()}
    Dictionary Should Contain Key     ${response.json()}     id
    ${name}=    Get From Dictionary     ${response.json()}    name
    Should Be Equal As Strings    ${expectedname}   ${name}
 
    ${job}=    Get From Dictionary     ${response.json()}    job
    Should Be Equal As Strings    ${expectedjob}    ${job}
        