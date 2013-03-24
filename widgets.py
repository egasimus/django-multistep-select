from django.forms.widgets import Select, MultiWidget
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Q

SELECT_SCRIPT = """<script type="text/javascript">
	
</script>"""

class TwoStepSelect(MultiWidget):

	def __init__(self, parent_model, child_model, lookup, attrs=None, **kwargs):
		parent_choices = [(p.pk, p) for p in parent_model.objects.all()]
		child_choices = [(p.pk, p) for p in child_model.objects.all()]
		widgets = (
			Select(attrs=attrs,choices=parent_choices),
			Select(attrs=attrs,choices=child_choices)
		)
		super(TwoStepSelect, self).__init__(widgets, attrs)

	def decompress(self, value):
		print "===============",value
		if value:
			try:
				child_instance = child_model.objects.get(pk=value)
				parent_instance = getattr(child_instance,lookup)
			except child_model.DoesNotExist:
				return [None, None]

			return [parent_instance, child_instance]
		return [None, None]

	def render(self, *args, **kwargs):
		output = super(TwoStepSelect, self).render(*args, **kwargs)
		output += SELECT_SCRIPT
		return mark_safe(output)