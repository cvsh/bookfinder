
from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class HomePage(Page):
    description = RichTextField(blank=True)
    book_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="book_img"
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('book_image'),
        MultiFieldPanel(
         [InlinePanel('authors_many', label="name")],
         heading="Authors of the book"
        ),
    ]

    search_fields = Page.search_fields + [
        index.FilterField('authors_many'),
    ]

    def get_context(self, request):
        filter_string = request.GET.get('qf')
        context = super(HomePage, self).get_context(request)
        print(filter_string)
        if filter_string:
            books = HomePage.objects.filter(authors_many__author_name__name=filter_string)
        else:
            books = self.get_children()
        context['books'] = books
        context['filter_query'] = filter_string
        context['authors'] = Author.objects.all()
        return context

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        
class Authors(Orderable):
    page = ParentalKey("home.HomePage", related_name="authors_many")
    author_name = models.ForeignKey(
        "home.Author",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    
    panels = [SnippetChooserPanel("author_name")]
