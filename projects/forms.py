from django import forms
from tinymce.widgets import TinyMCE
from .models import Project


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class ProjectsForm(forms.ModelForm):
    prefix = 'projects'
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Project
        fields = ('title', 'overview', 'content', 'thumbnail',
                  'featured', 'previous_post', 'next_post')
