*** Settings ***
Library     class_moshellcommand.py
Library     RequestsLibrary
Library     Collections

*** Variables ***
${base_uri}         http://127.0.0.1:5099/rtc/v2
${json_String}      {"FILE_PATH": "C:\\TMA_Sript\\NSA - B7-N2.xml","ITERATION_COUNT": 1,"ACTION_ON_EVENT": 2,"TESTS_SELECTION_BY_NAME": ["1UE-Attach"]}
${test_uri}              ${base_uri}/tmas/0001/campaigns/actions/schedule

*** Test Cases ***
Test mosehll command1 to show alarm
        ${result}=     class_moshellcommand.Commandexecution        alt
        Log To Console    \nMoshell command execution result code is : ${result} 
        Should Be Equal As Numbers   ${result}     0

Test moshell command2 to show status of cell
        ${result}=     class_moshellcommand.Commandexecution        st cell
        Log To Console    \nMoshell command execution result code is : ${result} 
        Should Be Equal As Numbers    ${result}     0

Test SSH close
        ${value}=      class_moshellcommand.Ssh_close
        Should Be Equal As Integers    ${value}    0

Test 1UE_Attach to run TM500 test case via API call
    # &{req_body}=  Create Dictionary    name=test        job=team leader
    # ${response}=     POST        ${base_url}     json=${req_body}    expected_status=201
    # log      ${response.json()}
    # Dictionary Should Contain Key     ${response.json()}     id
    # ${name}=    Get From Dictionary     ${response.json()}    name
    # Should Be Equal As Strings    ${expectedname}   ${name}
 
    # ${job}=    Get From Dictionary     ${response.json()}    job
    # Should Be Equal As Strings    ${expectedjob}    ${job}
        ${response}=    POST    ${test_uri}    ${json_String}
        Log To Console    ${response}
        
      