from collections import namedtuple

# API RESPONSE SUCCESS MESSAGES
# Format --> '{{key}}' : MESSAGE('description')
MESSAGE = namedtuple('MESSAGE', ['main_message', 'extra_message'])


NULL_MESSAGE = MESSAGE("", "")



SUCCESS_RESPONSES = {
    'ACCOUNT_CREATED_WITH_MAIL': MESSAGE('your account is created successfully', 'Mail sent to register email for verification'),
    'WELCOME_USER': MESSAGE('Login Successfully', 'Your Account is Logged In'),
    'POST_CREATED': MESSAGE('POST CREATED', 'Your Post Created Successfully'),
}


WARNING_RESPONSES = {
    'ACCOUNT_CREATED_WITHOUT_MAIL': MESSAGE('your account is created successfully', 'Due to Technical Issue mail is not sent for verification we will contact you soon')

}

MODEL_RESPONSES = {
    'FORM': MESSAGE('', '')
}


INFO_RESPONSES = {

}




ERROR_RESPONSES = {
    'INVALID_DATA': MESSAGE('The Login Details is Invalid', 'Some Of The Field Is Invalid'),
    'REQUIRED_DATA': MESSAGE('Invalid Request','Some Of The Field Is Required Or Invalid'),
    'NO_EMAIL_FOUND': MESSAGE('Invalid Email', 'The Email Is Not Register In System'),
    'INVALID_CREDENTIAL': MESSAGE('Invalid Credential', 'Email And Password Is Incorrect'),
    'INACTIVE_ACCOUNT': MESSAGE('Inactive Account', 'The Account Is InActive Please Verify Your Email For Activation'),
    'ACCOUNT_LOCKED': MESSAGE('Account Locked', 'Your Account is Locked For 15 Minute If Your Forget Your Password Click on Reset Password For Login'),
    'INVALID_CREDENTIAL_WITH_LOCK_MES': MESSAGE('Invalid Credential' ,'Email And Password Is Wrong,If Your Login Failed For 3 Time Account Will Be Lock For 15 Minute'),
    'INVALID_FILE': MESSAGE('INVALID_FILE','File Is Invalid Please Upload Valid File'),
    'RETRY': MESSAGE("Retry", 'Something Went Wrong Try After Sometime'),
}
