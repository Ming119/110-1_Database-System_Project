*** Settings ***
Library    Selenium2Library
Resource    allKeywords.txt

Suite Setup    Run Keywords    Open Browser    ${webSiteURL}    ${browser}
...                     AND    Maximize Browser Window

Suite Teardown    Close Browser

*** Test Cases ***
Login Page
    [Tags]    UIR-03
    [Setup]    Go To Login Page
    Verify Login As Customer
    Verify Login As Staff
    Verify Login As Admin
    Verify Do not Have An Account Button
    Verify Forgot Password Button

Register Page
    [Tags]    UIR-04
    [Setup]    Go To Register Page
    Verify Already Have An Account Button
