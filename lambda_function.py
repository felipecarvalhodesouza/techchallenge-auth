import boto3
import json
from botocore.exceptions import ClientError

client = boto3.client('cognito-idp', region_name='us-east-1')

def lambda_handler(event, context):
    
    request_body = event

    if request_body['operation'] == 'register':

        try:
            print("Registering new user")
            create_user_params = {
                'UserPoolId': 'us-east-1_pGFsCFVuS',
                'Username': request_body['email'],
                'UserAttributes': [
                    {'Name': 'email', 'Value': request_body['email']},
                    {'Name': 'email_verified', 'Value': 'true'}
                ]
            }

            response = client.admin_create_user(**create_user_params)
            print("User created successfully: ", response)

            set_password_params = {
                'UserPoolId': 'us-east-1_pGFsCFVuS',
                'Username': request_body['email'],
                'Password': request_body['password'],
                'Permanent': True
            }

            client.admin_set_user_password(**set_password_params)
            print("Password set successfully")

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'User created and confirmed successfully', 'user': str(response['User'])})
            }
        except ClientError as e:
            print(f"User creation error: {e.response['Error']['Message']}")
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Failed to create user'})
            }

    else: 
        try:
            username = request_body['email']
            password = request_body['password']
			
            user_pool_id = 'us-east-1_pGFsCFVuS'
            client_id = '3mmedbc37gunvdc708k2s6nsiu'

            response = client.initiate_auth(
				AuthFlow='USER_PASSWORD_AUTH',
				AuthParameters={
					'USERNAME': username,
					'PASSWORD': password
				},
				ClientId=client_id
			)

            return {
				'statusCode': 200,
				'headers': {
					'Access-Control-Allow-Origin': '*'
				},
                'body': json.dumps({
                    'accessToken': response['AuthenticationResult']['AccessToken'],
                    'idToken': response['AuthenticationResult']['IdToken'],
                    'refreshToken': response['AuthenticationResult']['RefreshToken']
                })
			}
        except Exception as e:
            return {
				'statusCode': 403,
				'headers': {
					'Access-Control-Allow-Origin': '*'
				},
				'body': json.dumps(str(e))
			}
