from django.test import TestCase
from django.utils import timezone
from news_aggregator.workers.serializers import NewsAPISerializer
from news_aggregator.workers.collectors import NewsAPICollector
from news_aggregator.models import Category, Resource, News


class TestNewsAPISerializer(TestCase):

    def setUp(self):
        self.serializer = NewsAPISerializer()
        self.collector = NewsAPICollector()

    def tearDown(self):
        del self.serializer
        del self.collector

    def test_is_get_extract_data(self):
        """ Test is data extracted from the collector's storage """
        self.collector.news_storage.append('data')
        self.serializer.get(self.collector.news_storage)
        self.assertFalse(self.collector.news_storage, "data wasn't extracted")

    # ------------ Test '_have_required_fields' method --------------

    def test_have_required_fields_with_empty_fields(self):
        self.assertFalse(self.serializer._have_required_fields('', '', None))

    def test_have_required_fields_with_valid_fields(self):
        self.assertTrue(self.serializer._have_required_fields('Some data', 'Some data2'))

    # ------------ Test serializers methods --------------

    def test_is_source_created(self):
        url = 'https://docs.djangoproject.com/'
        name = 'Django'
        country = 'us'
        self.serializer._serialize_source(url, name, country)

        source = Resource.objects.get(pk=url)
        self.assertTrue(source, "Source wasn't created")

    def test_is_category_created(self):
        name = 'Django'
        self.serializer._serialize_category(name)

        category = Category.objects.get(name=name)
        self.assertTrue(category, "Category wasn't created")

    def test_is_news_created(self):
        # Create source and category instances for article
        source = Resource.objects.create(
            resource_url='https://docs.djangoproject.com/',
            name='Django',
            country='us'
        )
        category = Category.objects.create(name='django2')

        # Create news article
        self.serializer._serialize_news(
            title='Interesting topic',
            pub_date=timezone.now(),
            news_source=source,
            news_category=category,
            lang='en',
            content='Interesting content'
        )

        article = News.objects.get(pk=1)
        self.assertTrue(article, "Category wasn't created")
