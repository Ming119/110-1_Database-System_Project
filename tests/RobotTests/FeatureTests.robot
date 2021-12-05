*** Settings ***
Library    Selenium2Library
Resource    allKeywords.txt
Resource    allVariables.txt

Suite Setup    Run Keywords    Open Browser    ${webSiteURL}    ${browser}
...                     AND    Maximize Browser Window

Suite Teardown    Close Browser

*** Test Cases ***
Index Page
    [Tags]    index
    [Setup]    Go To Home Page
    Verify Index Page Is Visible
    [Teardown]    Go To Home Page

Login Page
    [Tags]    UIR-03    login
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
    [Tags]    UIR-04    register
    [Setup]    Go To Register Page
    Verify Register Form Is Visible
    Verify "Already Have An Account" Button

    # Verify Register With Invalid
    [Teardown]    Go To Home Page

Forgot Password Page
    [Tags]    forgot_password
    [Setup]    Run Keywords    Go To Login Page
    ...                 AND    Click Element    ${forgotPasswordButton}
    Verify Forgot Password Form Is Visible
    Verify Forgot Password
    [Teardown]    Go To Home Page

Manage Products Page
  [Tags]    UIR-05    manage_product
  [Setup]    Run Keywords    Go To Login Page
  ...                 AND    Login As   username=staff    password=staff
  ...                 AND    Go To Manage Products Page
  Verify Manage Product Page Is Visible
  [Teardown]    Go To Home Page
