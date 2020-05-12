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
