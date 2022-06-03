from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import RichTextField, StreamField
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from django.contrib.auth.models import User
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtail.search import index
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet


# todo: add events landing page
class EventsLisitingPage(Page):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # TODO: Handling Pagination
        all_events_pages = EventPage.objects.live(
        ).public().order_by('-last_published_at')

        # @TODO: paginate change integer to 8 per page
        paginator = Paginator(all_events_pages, 8)
        page = request.GET.get('page')
        try:
            events_pages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            events_pages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            events_pages = paginator.page(paginator.num_pages)
        context["events_pages"] = events_pages

        return context

# todo: single event page


class EventPage(Page):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    event_date = models.DateField(blank=True, null=True)
    event_venue = models.CharField(max_length=255, blank=True, null=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        ImageChooserPanel('featured_image'),
        FieldPanel('event_date'),
		FieldPanel('event_venue'),
        FieldPanel('body', classname="full"),
    ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        siblings = Page.objects.sibling_of(self, inclusive=False).public().order_by('-last_published_at')
        context['siblings'] = siblings
        return context

    search_fields = Page.search_fields + [
        index.SearchField('title', partial_match=True, boost=10),
        index.SearchField('event_date', partial_match=True),
        index.SearchField('event_venue', partial_match=True),
    ]

    @route(r"^search/$")
    def search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)
        self.event_pages = self.get_event_pages(
        ).objects.live().autocomplete("name", search_query)
        if search_query:
            self.event_pages = self.event_pages.search(search_query)
        return self.render(request)
