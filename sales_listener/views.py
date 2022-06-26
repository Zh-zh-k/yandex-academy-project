import yaml
from datetime import datetime
from openapi_schema_validator import validate, OAS30Validator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Position
from .serializers import PositionSerializer


with open("openapi.yaml", "r") as f :
    openapi_schema = yaml.safe_load(f)
add_schema = openapi_schema["components"]["schemas"]["ShopUnitImportRequest"]
add_schema = openapi_schema["components"]["schemas"]["ShopUnitImport"]
add_schema["properties"]["type"] = openapi_schema["components"]["schemas"]["ShopUnitType"]

def uuids_check(data) :
    uuids = set()
    for elem in data :
        validate(elem, add_schema, OAS30Validator)
        if "id" in elem :
            if elem["id"] in uuids :
                return False
            uuids.add("id")
    return True


@csrf_exempt
def add_data(request) :
    try:
        data = JSONParser().parse(request)
    except:
        return JsonResponse({"code": 400, "message": "Validation Failed"}, status=400)
    if not "items" in data or not "updateDate" in data :
        return JsonResponse({"code": 400, "message": "Validation Failed"}, status=400)
    try:
        res = uuids_check(data["items"])
        if res == False:
            return JsonResponse({"code": 400, "message": "Validation Failed"}, status=400)
    except:
        return JsonResponse({"code": 400, "message": "Validation Failed"}, status=400)
    serializer = PositionSerializer(data=data["items"], many=True, context={"date": data["updateDate"]})
    if serializer.is_valid() :
        serializer.save()
        print(serializer.data)
        return HttpResponse(status=200)
    else :
        print(serializer.errors)
        return JsonResponse({"code": 400, "message": "Validation Failed"}, status=400)


def get_response(elem) :
    serializer = PositionSerializer(elem)
    response = serializer.data
    if elem.type == "CATEGORY" :
        children = []
        cnt = 0
        value = 0
        updateDate = response["date"]
        try:
            elems = Position.objects.filter(parentId=elem.id)
            for curElem in elems :
                curCnt, curResponse = get_response(curElem)
                children.append(curResponse)
                cnt += curCnt
                value += curResponse["price"] * curCnt
                if datetime.fromisoformat(curResponse["date"].replace('Z', '+00:00')) > datetime.fromisoformat(updateDate.replace('Z', '+00:00')) :
                    updateDate = curResponse["date"]

        except:
            pass
        response["children"] = children
        if cnt > 0 :
            response["price"] = int(value / cnt)
        response["date"] = updateDate
    else :
        response["children"] = None
        cnt = 1
    
    return cnt, response


@csrf_exempt
def get_data(request, uuid) :
    if request.method == 'GET' :
        try:
            element = Position.objects.get(id=uuid)
        except Position.DoesNotExist :
            return JsonResponse({"code": 404, "message": "Item not found"}, status=404)
        
        _, response = get_response(element)
        return JsonResponse(response, safe=False)

def delete_tree(elem) :
    try:
        elems = Position.objects.filter(parentId=elem.id)
        for curElem in elems :
            delete_tree(curElem)
            curElem.delete()
    except:
        pass

@csrf_exempt
def delete_data(request, uuid) :
    if request.method == 'DELETE' :
        try:
            element = Position.objects.get(id=uuid)
        except Position.DoesNotExist :
            return JsonResponse({"code": 404, "message": "Item not found"}, status=404)
        
        delete_tree(element)
        element.delete()
        return HttpResponse(status=200)
        

