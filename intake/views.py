from django.shortcuts import render
from django.http import HttpResponse
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from .dynamo import connect

import uuid

def patient_id(request):

    if request.method == 'GET':

        last_name = request.GET.get('lastName').lower()
        first_name = request.GET.get('firstName').lower()
        dob = request.GET.get('dob')
        email = request.GET.get('email').lower()


        dynamodb = connect()
        table = dynamodb.Table('Patients')
        response = table.query(KeyConditionExpression=Key('LastName').eq(last_name))

        print(response)


        for item in response['Items']:
            if item['LastName'] == last_name and item['FirstName'] == first_name and item['DOB'] == dob and \
                    item['Email'] == email:
                return HttpResponse(item['uuid'])

        item = {
            'LastName': last_name,
            'uuid': str(uuid.uuid4()),
            'LastNameRepr': request.GET.get('lastName'),
            'FirstName': first_name,
            'FirstNameRepr': request.GET.get('firstName'),
            'DOB': dob,
            'Email': email
        }

        if request.GET.get('MI'):
            item['MI'] = request.GET.get('MI').upper()

        table.put_item(Item=item)

        return HttpResponse(item['uuid'])

