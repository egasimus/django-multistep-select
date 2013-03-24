from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.widgets import Select, MultiWidget
from django.utils.html import format_html
from django.utils.safestring import mark_safe


SELECT_SCRIPT = """<script type="text/javascript">
(function($) {
	$(document).ready(function() {
		$("#id_synonym_0").change(function(){
			var request_url = "%s".replace('$VALUE$',$(this).val())
			$.getJSON(request_url,function(data){
				$("#id_synonym_1").empty().append('<option value="">Please select a definition:</option>')
				$(data).each(function(){
					var option = '<option value=' + 
						$(this)[0].pk+'>' + 
						$(this)[0].fields.text.substring(0,50) +
						'</option>'
					$("#id_synonym_1").append(option)
				})
			})
		})
	})
})(grp.jQuery);

</script>"""

class TwoStepSelect(MultiWidget):

	def __init__(self, attrs=None, **kwargs):
		self.parent_model = kwargs.get('parent_model')
		self.parent_choices = [('','---')]
		self.parent_choices.extend([(p.pk, p) for p in self.parent_model.objects.all()])

		self.child_model = kwargs.get('child_model')
		self.child_choices = [('','---')] 
		self.child_choices.extend([(p.pk, p) for p in self.child_model.objects.all()])

		self.parent_lookup = kwargs.get('parent_lookup')

		widgets = (
			Select(attrs=attrs,choices=[('','---')]),
			Select(attrs=attrs,choices=[('','---')])
		)
		super(TwoStepSelect, self).__init__(widgets, attrs)

	def value_from_datadict(self, data, files, name):
		return data.get(name+"_1",None)

	def decompress(self, value):
		self.widgets[0].choices = self.parent_choices

		if value:
			try:
				child_instance = self.child_model.objects.get(pk=value)
				self.widgets[1].choices = self.child_choices
				parent_instance = getattr(child_instance,self.parent_lookup)
				return [parent_instance, child_instance]
			except self.child_model.DoesNotExist:
				return [None, None]

		return [None, None]

	def render(self, name, value, attrs=None):
		if self.is_localized:
			for widget in self.widgets:
				widget.is_localized = self.is_localized

		if not isinstance(value, list):
			value = self.decompress(value)

		output = []
		final_attrs = self.build_attrs(attrs)

		id_ = final_attrs.get('id', None)

		widget_ids = []
		for i, widget in enumerate(self.widgets):
			widget_ids.append(id_ + name + '_%s' % i)
			try:
				widget_value = value[i]
			except IndexError:
				widget_value = None
			if id_:
				final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
			output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))

		json_url = reverse(
			'json_list',
			kwargs={
				'app':self.child_model._meta.app_label,
				'model':self.child_model.__name__,
				'lookup':self.parent_lookup,
				'value':"$VALUE$"
			}
		)

		out_script = SELECT_SCRIPT % json_url

		output.append(out_script)

		return mark_safe(self.format_output(output))