# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl import fields
# from django_elasticsearch_dsl.registries import registry

# from news.models import News

# @registry.register_document
# class NewsDocument(Document):
#     title = fields.CompletionField() 
#     # tags = fields.ObjectField(
#     #     properties={
#     #         "title": fields.TextField(),
#     #     }
#     # )
#     # categories = fields.ObjectField(
#     #     properties={
#     #         "title": fields.TextField(),
#     #     }
#     # )
#     class Index:
#         name = "news"
#         settings = {
#             "number_of_shards": 1, 
#             "number_of_replicas": 0
#             }

#     class Django:
#         model = News
#         fields = [
#             "id",
#             "description",
#             "content",
#         ]
