from django.core.management.base import BaseCommand

from service.models import Question


class Command(BaseCommand):

	def handle(self, *args, **options):
		# print("id\")
		for q in Question.objects.all():
			print(" {},'{}'".format(q.pk, q.text.encode('utf8')))
