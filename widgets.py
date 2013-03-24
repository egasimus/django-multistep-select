from django.forms.widgets import Select, MultiWidget
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Q

SELECT_SCRIPT = """<script type="text/javascript">
	
</script>"""

class TwoStepSelect(MultiWidget):

	def __init__(self, attrs=None, **kwargs):
		self.parent_model = kwargs.get('parent_model')
		self.child_model = kwargs.get('child_model')
		self.lookup = kwargs.get('lookup')

		child_choices = [('','---')] 
		child_choices.extend([(p.pk, p) for p in self.child_model.objects.all()])

		widgets = (
			Select(attrs=attrs,choices=[('','---')]),
			Select(attrs=attrs,choices=[('','---')])
		)
		super(TwoStepSelect, self).__init__(widgets, attrs)

	def decompress(self, value):
		print "===============",value

		parent_choices = [('','---')]
		parent_choices.extend([(p.pk, p) for p in self.parent_model.objects.all()])

		self.widgets[0].choices = parent_choices

		if value:
			try:
				child_instance = self.child_model.objects.get(pk=value)
				parent_instance = getattr(child_instance,self.lookup)
			except self.child_model.DoesNotExist:
				return [None, None]

			return [parent_instance, child_instance]
		return [None, None]

	def render(self, *args, **kwargs):
		output = super(TwoStepSelect, self).render(*args, **kwargs)
		output += SELECT_SCRIPT
		return mark_safe(output)