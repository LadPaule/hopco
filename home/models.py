from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField, StreamField
# from wagtail_embed_videos.edit_handlers import EmbedVideoChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

# todo: HomePage
class HomePage(Page):
    # todo: facts and call to action
    beneficiary_number = models.CharField(max_length=255, blank=True, null=True)
    beneficiary_narration = models.CharField(max_length=255, blank=True, null=True)

    donate_title = models.CharField(max_length=255, blank=True, null=True)
    donate_body = models.TextField(blank=True, null=True)

    sponsor_title = models.CharField(max_length=255, blank=True, null=True)
    sponsor_body = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('beneficiary_number', help_text='The number of beneficiaries that have been reached since program start'),
        FieldPanel('beneficiary_narration', help_text='narration'),
        FieldPanel('donate_title'),
        FieldPanel('donate_body'),
        FieldPanel('sponsor_title'),
        FieldPanel('sponsor_body'),
        InlinePanel('carousel_items', label="Carousel items"),
        InlinePanel('causes_items', label="HOPCO causes", max_num=4),
        InlinePanel('involve_items', label="sponsor CTA"),
        InlinePanel('past_events', label="about CTA", max_num=3),
    ]
class HomePageCarouselItem(Orderable):
    page = ParentalKey(HomePage, related_name='carousel_items')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+' )
    title = models.CharField(blank=True, max_length=250)
    body = RichTextField(blank=True)
    read_more= models.CharField(max_length=255, blank=True, null=True)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('body'),
        FieldPanel('read_more'),
    ]
# todo: HomePageCauses
class HomePageCauses(Orderable):
    page = ParentalKey(HomePage, related_name='causes_items')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+' )
    title = models.CharField(blank=True, max_length=250)
    body = RichTextField(blank=True)
    tab_id = models.CharField(max_length=255, blank=True, null=True)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('tab_id'),
        FieldPanel('body'),
    ]

class HomePageInvolve(Orderable):
    page = ParentalKey(HomePage, related_name='involve_items')
    icon_class = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(blank=True, max_length=250)
    body = RichTextField(blank=True)
    panels = [
        FieldPanel('icon_class'),
        FieldPanel('title'),
        FieldPanel('body'),
    ]

class HomePastEvents(Orderable):
    page = ParentalKey(HomePage, related_name='past_events')
    event_title = models.CharField(max_length=255, blank=True, null=True)
    event_body = models.TextField(blank=True, null=True)
    event_image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+' )
    event_date = models.CharField(max_length=255, blank=True, null=True)
    event_location = models.CharField(max_length=255, blank=True, null=True)
    panels = [
        FieldPanel('event_title'),
        ImageChooserPanel('event_image'),
        FieldPanel('event_location'),
        FieldPanel('event_body'),
        FieldPanel('event_date'),
    ]
# todo: ContactPage
class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    thank_you_message = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', help_text="This is the title of the page"),
        FieldPanel('location', help_text="This is the location of the page"),
        FieldPanel('email', help_text="This is the email of the page"),
        FieldPanel('phone', help_text="This is the phone of the page"),
        InlinePanel('form_fields', label="Contact form Sections",
                    help_text="This is the contact page form section"),
        FieldPanel('thank_you_message',
                   help_text="This is the title of the page"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings"),

    ]

class ContactPageFormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')

class EmpoweringPage(Page):
    featured_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+' )
    body_heading = models.CharField(max_length=255, blank=True, null=True)
    body_1 = RichTextField(blank=True, null=True)
    body_2 = RichTextField(blank=True, null=True)
    body_3 = RichTextField(blank=True, null=True)
    body_4 = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [

        ImageChooserPanel('featured_image'),
        FieldPanel('body_heading'),
        FieldPanel('body_1'),
        FieldPanel('body_2'),
        FieldPanel('body_3'),
        FieldPanel('body_4'),
        InlinePanel('faqs', label="FAQs", help_text="Add Frequently Asked Questions about the women and youths empowerment program"),

    ]
class EmpoweringPageFaqs(Orderable):
    page = ParentalKey(EmpoweringPage, related_name='faqs')
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = RichTextField(blank=True, null=True)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

class SkillsPage(Page):
    featured_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+' )
    body_heading = models.CharField(max_length=255, blank=True, null=True)
    body_1 = RichTextField(blank=True, null=True)
    body_2 = RichTextField(blank=True, null=True)
    body_3 = RichTextField(blank=True, null=True)
    body_4 = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('featured_image'),
        FieldPanel('body_heading'),
        FieldPanel('body_1'),
        FieldPanel('body_2'),
        FieldPanel('body_3'),
        FieldPanel('body_4'),
        InlinePanel('faqs', label="FAQs", help_text="Add Frequently Asked Questions about the skills Developemt program"),
    ]
class SkillsPageFaqs(Orderable):
    page = ParentalKey(SkillsPage, related_name='faqs')
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = RichTextField(blank=True, null=True)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]
class TalentPage(Page):
    featured_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+' )
    body_heading = models.CharField(max_length=255, blank=True, null=True)
    body_1 = RichTextField(blank=True, null=True)
    body_2 = RichTextField(blank=True, null=True)
    body_3 = RichTextField(blank=True, null=True)
    body_4 = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('featured_image'),
        FieldPanel('body_heading'),
        FieldPanel('body_1'),
        FieldPanel('body_2'),
        FieldPanel('body_3'),
        FieldPanel('body_4'),
        InlinePanel('faqs', label="FAQs", help_text="Add Frequently Asked Questions about the Talent support & nurturing program"),
    ]
class TalentPageFaqs(Orderable):
    page = ParentalKey(TalentPage, related_name='faqs')
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = RichTextField(blank=True, null=True)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

class RefugesPage(Page):
    featured_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+' )
    body_heading = models.CharField(max_length=255, blank=True, null=True)
    body_1 = RichTextField(blank=True, null=True)
    body_2 = RichTextField(blank=True, null=True)
    body_3 = RichTextField(blank=True, null=True)
    body_4 = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('featured_image'),
        FieldPanel('body_heading' ),
        FieldPanel('body_1' ),
        FieldPanel('body_2' ),
        FieldPanel('body_3' ),
        FieldPanel('body_4' ),

        InlinePanel('faqs', label="FAQs", help_text="Add Frequently Asked Questions about the Refugees response program"),
    ]
class RefugesPageFaqs(Orderable):
    page = ParentalKey(RefugesPage, related_name='faqs')
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = RichTextField(blank=True, null=True)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]
class GivePage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Page"),
        InlinePanel('card_information', label="card Information", help_text="Upload images to the give give card"),
    ]
class GivePageGalleryImage(Orderable):
    page = ParentalKey('GivePage', on_delete=models.CASCADE, related_name='card_information')
    card_image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    card_title= models.CharField(blank=True, max_length=250)
    card_text = models.CharField (blank=True, max_length=2200)
    card_back_side = models.CharField (blank=True, max_length=2200)
    panels = [ ImageChooserPanel('card_image'),
        FieldPanel('card_title'),
        FieldPanel('card_text'),
        FieldPanel('card_back_side'),
    ]

class AboutPage(Page):
    hero_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+' )
    hero_heading = models.CharField(max_length=255, blank=True, null=True)
    hero_text = RichTextField(blank=True, null=True)
    featured_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+' )
    body= RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('hero_heading'),
        FieldPanel('hero_text'),
        ImageChooserPanel('featured_image'),
        FieldPanel('body'),
        InlinePanel('strategics', label="Strategic organisataion", help_text="Add Team strategics here "),
        InlinePanel('team_members', label="Team members", help_text="Add Team members here"),
    ]

class Strategics(Orderable):
    page = ParentalKey(AboutPage, related_name='strategics')
    icon= models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=1000, blank=True, null=True)
    panels = [
        FieldPanel('icon'),
        FieldPanel('title'),
        FieldPanel('value'),
    ]

class TeamMember(Orderable):
    page = ParentalKey(AboutPage, related_name='team_members')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    name = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_handle = models.CharField(max_length=255, blank=True, null=True)
    facebook_handle = models.CharField(max_length=255, blank=True, null=True)
    instagram_handle = models.CharField(max_length=255, blank=True, null=True)
    linkedin_handle = models.CharField(max_length=255, blank=True, null=True)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('name'),
        FieldPanel('job_title'),
        FieldPanel('twitter_handle'),
        FieldPanel('facebook_handle'),
        FieldPanel('instagram_handle'),
        FieldPanel('linkedin_handle'),
    ]
    