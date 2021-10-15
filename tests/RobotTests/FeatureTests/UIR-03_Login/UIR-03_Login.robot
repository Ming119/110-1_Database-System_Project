*** Settings ***
Library    Selenium2Library
Resource    ../../Keywords/common.txt
Resource    ../../Keywords/flash.txt
Resource    ../UIR-04_Register/UIR-04_Register.txt
Resource    ./UIR-03_Login.txt


Suite Setup    Run Keywords    Open Browser    ${webSiteURL}    ${browser}
...                     AND    Maximize Browser Window
...                     AND    Go to Login Page

Suite Teardown    Close Browser

*** Test Cases ***
Verify Login As Customer
    Login Page::Wait Until Login Form Is Visible
    Login Page::Login As    ${customer}
    Flash::Wait Until Flash Message With Category Is Visible    Login successful!    success
    Common::Wait Until Navbar Contains    Home    Products    Shopping Cart    ${customer}[username]    Logout
    [Teardown]    Run Keywords    Logout
    ...                    AND    Go to Login Page

Verify Login As Staff
    Login Page::Wait Until Login Form Is Visible
    Login Page::Login As    ${staff}
    Flash::Wait Until Flash Message With Category Is Visible    Login successful!    success
    Common::Wait Until Navbar Contains    Home    Products    Orders    Promotions    ${staff}[username]    Logout
    [Teardown]    Run Keywords    Logout
    ...                    AND    Go to Login Page

Verify Login As Admin
    Login Page::Wait Until Login Form Is Visible
    Login Page::Login As    ${admin}
    Flash::Wait Until Flash Message With Category Is Visible    Login successful!    success
    Common::Wait Until Navbar Contains    Home    Products    Manage Users    ${admin}[username]    Logout
    [Teardown]    Run Keywords    Logout
    ...                    AND    Go to Login Page

Verify Do not Have An Account Button
    Login Page::Wait Until Login Form Is Visible
    Login Page::Click Do Not Have An Account Button
    Register Page::Wait Until Register Form Is Visible
    [Teardown]    Go to Login Page

# Verify Forgot Password Button
#     Login Page::Wait Until Login Form Is Visible
#     Login Page::Click Forfot Password Button
#     Forgot Password Page::Wait Until Forgot Password Form Is Visible
#     [Teardown]    Go to Login Page
