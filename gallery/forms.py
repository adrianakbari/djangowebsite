from django import forms
from tinymce.widgets import TinyMCE
from .models import Gallery


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class GalleryForm(forms.ModelForm):
    prefix = 'gallery'
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Gallery
        fields = ('title', 'overview', 'content', 'thumbnail',
                  'featured', 'previous_post', 'next_post')
