import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

from django.http import HttpResponse

from .dynamo import connect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import uuid


@api_view(['GET'])
def patient_id(request):

    if request.method == 'GET':

        last_name = request.GET.get('lastName').lower()
        first_name = request.GET.get('firstName').lower()
        dob = request.GET.get('DOB')
        email = request.GET.get('email').lower()

        dynamodb = connect()
        table = dynamodb.Table('Patients')
        response = table.query(
            IndexName="LastName-index",
            KeyConditionExpression=Key('LastName').eq(last_name)
        )

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


@api_view(['GET'])
def new_intake(request):

    if request.method == 'GET':
        patient_id = request.GET.get('patientId');

        dynamodb = connect()
        table = dynamodb.Table('IntakeForms')

        item = {
            'uuid': str(uuid.uuid4()),
            'PatientId': patient_id
        }

        table.put_item(Item=item)

        return HttpResponse(item['uuid'])


@api_view(['PUT'])
def update_intake(request, id):

    if request.method == 'PUT':

        dynamodb = connect()
        table = dynamodb.Table('IntakeForms')

        data = json.loads(request.body.decode())

        updates = []
        expression_attribute_values = {}

        for key, value in data.items():
            if value != "":
                updates.append(f"{key} = :{key}")
                expression_attribute_values[f":{key}"] = value

        update_expression = "set " + ", ".join(updates)

        response = table.update_item(
            Key={'uuid': id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )

        return HttpResponse()

@api_view(['POST'])
def appointment_request(request):

    if request.method == 'POST':
        print(request)

        data = json.loads(request.body.decode())

        print(data)

        patient_info = data.pop('patientInformation')


        last_name = patient_info.get('lastName').lower()
        first_name = patient_info.get('firstName').lower()
        dob = patient_info.get('DOB')
        email = patient_info.get('email').lower()

        dynamodb = connect()
        table = dynamodb.Table('Patients')

        # Get a list of patients from the database whose last name matches
        response = table.query(
            IndexName="LastName-index",
            KeyConditionExpression=Key('LastName').eq(last_name)
        )

        # Look for this patient in the list of patients returned from the database
        for item in response['Items']:
            if item['LastName'] == last_name and item['FirstName'] == first_name and item['DOB'] == dob and \
                    item['Email'] == email:
                # Found the requested patient
                patient_id = item['uuid']
                break
        else:
            # Did not find the requested patient, so add a new one
            item = {
                'LastName': last_name,
                'uuid': str(uuid.uuid4()),
                'LastNameRepr': patient_info.get('lastName'),
                'FirstName': first_name,
                'FirstNameRepr': patient_info.get('firstName'),
                'DOB': dob,
                'Email': email
            }

            if data.get('MI'):
                item['MI'] = patient_info.get('MI').upper()

            table.put_item(Item=item)

            patient_id = item['uuid']


        table = dynamodb.Table('AppointmentRequests')

        data['uuid'] = str(uuid.uuid4())
        data['PatientId'] = patient_id

        table.put_item(Item=data)

        return HttpResponse()


def staff_form_list(request):

    if request.method == 'GET':
        dynamodb = connect()
        table = dynamodb.Table('IntakeForms')

        response = table.scan()
        print(response)
