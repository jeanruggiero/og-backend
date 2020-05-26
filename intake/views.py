import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

from django.http import HttpResponse

from .dynamo import connect

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


import uuid


@api_view(['GET'])
@permission_classes([AllowAny])
def patient_id(request):

    if request.method == 'GET':

        last_name = request.GET.get('lastName').lower()
        first_name = request.GET.get('firstName').lower()
        dob = request.GET.get('dob')
        email = request.GET.get('email').lower()

        dynamodb = connect()
        table = dynamodb.Table('Patients')
        response = table.query(
            IndexName="lastName-index",
            KeyConditionExpression=Key('lastName').eq(last_name)
        )

        for item in response['Items']:
            if item['lastName'] == last_name and item['firstName'] == first_name and item['dob'] == dob and \
                    item['email'] == email:
                return HttpResponse(item['uuid'])

        item = {
            'lastName': last_name,
            'uuid': str(uuid.uuid4()),
            'lastNameRepr': request.GET.get('lastName'),
            'firstName': first_name,
            'firstNameRepr': request.GET.get('firstName'),
            'dob': dob,
            'email': email
        }

        if request.GET.get('mi'):
            item['mi'] = request.GET.get('mi').upper()

        table.put_item(Item=item)

        return HttpResponse(item['uuid'])


@api_view(['GET'])
@permission_classes([AllowAny])
def new_intake(request):

    if request.method == 'GET':
        patient_id = request.GET.get('patientId')

        dynamodb = connect()
        table = dynamodb.Table('IntakeForms')

        item = {
            'uuid': str(uuid.uuid4()),
            'patientId': patient_id
        }

        table.put_item(Item=item)

        return HttpResponse(item['uuid'])


@api_view(['PUT'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def appointment_request(request):

    if request.method == 'POST':
        print(request)

        data = json.loads(request.body.decode())

        print(data)

        patient_info = data.pop('patientInformation')

        last_name = patient_info.get('lastName').lower()
        first_name = patient_info.get('firstName').lower()
        dob = patient_info.get('dob')
        email = patient_info.get('email').lower()

        dynamodb = connect()
        table = dynamodb.Table('Patients')

        # Get a list of patients from the database whose last name matches
        response = table.query(
            IndexName="lastName-index",
            KeyConditionExpression=Key('lastName').eq(last_name)
        )

        # Look for this patient in the list of patients returned from the database
        for item in response['Items']:
            if item['lastName'] == last_name and item['firstName'] == first_name and item['dob'] == dob and \
                    item['email'] == email:
                # Found the requested patient
                patient_id = item['uuid']
                break
        else:
            # Did not find the requested patient, so add a new one
            item = {
                'lastName': last_name,
                'uuid': str(uuid.uuid4()),
                'lastNameRepr': patient_info.get('lastName'),
                'firstName': first_name,
                'firstNameRepr': patient_info.get('firstName'),
                'dob': dob,
                'email': email
            }

            if data.get('mi'):
                item['mi'] = patient_info.get('mi').upper()

            table.put_item(Item=item)

            patient_id = item['uuid']


        table = dynamodb.Table('AppointmentRequests')

        data['uuid'] = str(uuid.uuid4())
        data['patientId'] = patient_id

        table.put_item(Item=data)

        return HttpResponse()




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def form_list(request):

    if request.method == 'GET':
        dynamodb = connect()
        form_table = dynamodb.Table('IntakeForms')

        response = form_table.scan(
            FilterExpression=Attr('dateSubmitted').exists(),
            ProjectionExpression="#id, patientId, dateSubmitted, formProcessed",
            ExpressionAttributeNames={'#id': 'uuid'}
        )

        forms = response['Items']
        forms.sort(key=(lambda form: form['dateSubmitted']), reverse=True)

        patient_table = dynamodb.Table('Patients')

        for form in forms:
            try:
                response = patient_table.get_item(
                    Key={
                        'uuid': form['patientId']
                    }
                )

                patient = response['Item']
                form['lastNameRepr'] = patient['lastNameRepr']
                form['firstNameRepr'] = patient['firstNameRepr']
            except KeyError:
                continue

        return HttpResponse(json.dumps(forms))


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def form_detail(request, id):

    if request.method == 'GET':
        dynamodb = connect()

        form_table = dynamodb.Table('IntakeForms')
        response = form_table.get_item(Key={'uuid': id})
        form = response['Item']

        patient_table = dynamodb.Table('Patients')
        response = patient_table.get_item(Key={'uuid': form['patientId']})
        patient = response['Item']

        form['patient'] = patient

        return HttpResponse(json.dumps(form))


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def appointment_request_list(request):

    if request.method == 'GET':
        dynamodb = connect()
        appointment_request_table = dynamodb.Table('AppointmentRequests')
        response = appointment_request_table.scan(
            FilterExpression=Attr('dateSubmitted').exists(),
            ProjectionExpression="#id, patientId, dateSubmitted, requestProcessed",
            ExpressionAttributeNames={'#id': 'uuid'}
        )

        appointment_requests = response['Items']
        appointment_requests.sort(key=(lambda form: form['dateSubmitted']), reverse=True)

        patient_table = dynamodb.Table('Patients')

        for appointment_request in appointment_requests:
            try:
                response = patient_table.get_item(
                    Key={
                        'uuid': appointment_request['patientId']
                    }
                )

                patient = response['Item']
                appointment_request['lastNameRepr'] = patient['lastNameRepr']
                appointment_request['firstNameRepr'] = patient['firstNameRepr']
            except KeyError:
                continue

        return HttpResponse(json.dumps(appointment_requests))


@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def appointment_request_detail(request, id):

    dynamodb = connect()
    table = dynamodb.Table('AppointmentRequests')

    if request.method == 'GET':

        response = table.get_item(Key={'uuid': id})
        appointment_request = response['Item']

        patient_table = dynamodb.Table('Patients')
        response = patient_table.get_item(Key={'uuid': appointment_request['patientId']})
        patient = response['Item']

        appointment_request['patient'] = patient

        return HttpResponse(json.dumps(appointment_request))

    if request.method == 'PUT':

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