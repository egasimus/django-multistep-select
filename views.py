from django.http import HttpResponse
from django.core import serializers
from django.contrib.contenttypes.models import ContentType

def json_list(request,app,model,lookup,value):
	content = ContentType(app_label=app,model=model)
	contentclass = content.model_class()
	lookup_dict = { lookup:value }
	queryset = contentclass.objects.filter(**lookup_dict)

	return HttpResponse(serializers.serialize('json',queryset), mimetype='application/json')