import json
from django.conf import settings
# from django.contrib.postgres.fields import JSONField
from django.db import models

JSONTextField = models.TextField


# See
# https://developers.google.com/maps/documentation/javascript/reference?hl=en#LatLngBoundsLiteral


class LatLngBounds(models.Model):
    east = models.FloatField()
    north = models.FloatField()
    south = models.FloatField()
    west = models.FloatField()


class MapArea(models.Model):
    title = models.CharField(max_length=100, blank=True)
    display_area = models.ForeignKey(LatLngBounds, related_name='+')
    # This data should be obviously moved to a storage suitable
    # for blobs. Keeping in here to ease deployment. Migration is
    # an exercise for the happy future developer.
    # The data stored is image in PNG or JPEG format.
    contour_map_image = models.BinaryField(null=True)
    # Which part of the Earth the rectangular stored
    # in contour_map_image represents.
    contour_map_reference = models.ForeignKey(LatLngBounds, related_name='+', null=True)


class Question(models.Model):
    map_area = models.ForeignKey(MapArea)
    max_duration = models.DurationField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    # See "JSON Objects per Question Type" for more details.
    type = models.TextField()
    statement_data = JSONTextField()
    reference_data = JSONTextField()


class QuestionSet(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    max_duration = models.DurationField()
    question_ids = JSONTextField(default=json.dumps(None))

    def get_questions(self):
        questions = []
        for question_id in json.loads(self.question_ids):
            questions.append(Question.objects.get(id=question_id))
        return questions


class AnswerSet(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    question_set = models.ForeignKey(QuestionSet, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)


class Answer(models.Model):
    answer_set = models.ForeignKey(AnswerSet, db_index=True)
    question_set = models.ForeignKey(QuestionSet, null=True)
    question = models.ForeignKey(Question, null=True)
    answer_data = JSONTextField(default=json.dumps(None))
    scoring_data = JSONTextField(default=json.dumps(None))  # May be recalculated
    duration = models.DurationField()
    submission_time = models.DateTimeField()
