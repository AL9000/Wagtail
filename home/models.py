from django.contrib import messages
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, \
    FieldRowPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel


class FormField(AbstractFormField):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='form_fields')


class HomePage(AbstractEmailForm):
    body = RichTextField(blank=True)
    subtitle = models.CharField(blank=True, max_length=50)
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+'
    )
    contact_text = RichTextField(blank=True)
    landing_page_template = "home/home_page.html"

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body', classname="full"),
        ImageChooserPanel('image'),
        InlinePanel('portfolio_items', label="Portfolio items"),
        # form
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('contact_text', classname="full"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('from_address', classname="col6"),
                        FieldPanel('to_address', classname="col6"),
                    ]
                ),
                FieldPanel('subject'),
            ],
            "Email",
        ),
    ]

    def get_landing_page_template(self, request, *args, **kwargs):
        messages.success(request, "Ton message m'a bien été envoyé, merci ;)")
        return self.landing_page_template

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        for name, field in form.fields.items():
            field.widget.attrs.update({'placeholder': field.label})
            css_classes = field.widget.attrs.get('class', '').split()
            css_classes.append('form-control')
            field.widget.attrs.update({'class': ' '.join(css_classes)})
        return form


class PortfolioItem(Orderable):
    page = ParentalKey(
        HomePage, on_delete=models.CASCADE, related_name='portfolio_items'
    )

    title = models.CharField(blank=True, max_length=50)
    description = RichTextField(blank=True)
    project_url = models.URLField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('project_url'),
        ImageChooserPanel('image'),
    ]
