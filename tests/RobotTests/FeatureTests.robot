*** Settings ***
Library    Selenium2Library
Resource    allKeywords.txt
Resource    allVariables.txt

Suite Setup    Run Keywords    Open Browser    ${webSiteURL}    ${browser}
...                     AND    Maximize Browser Window

Suite Teardown    Close Browser

*** Test Cases ***
Login Page
    [Tags]    UIR-03
    [Setup]    Go To Login Page
    Verify Login Form Is Visible
    Verify "Do not Have An Account" Button
    Verify "Forgot Password" Button

    Verify Login As Customer
    Verify Login As Staff
    Verify Login As Admin

    Verify Login With Invalid Username
    Verify Login With Invalid Password
    [Teardown]    Go To Home Page

Register Page
    [Tags]    UIR-04
    [Setup]    Go To Register Page
    Verify Register Form Is Visible
    Verify "Already Have An Account" Button
    [Teardown]    Go To Home Page

# Manage Products Page
#   [Tags]    UIR-05
#   [Setup]    Go To Manage Products Page
#
#   [Teardown]    Go To Home Page
