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
    display_area = models.ForeignKey(LatLngBounds, related_name='+')
    # This data should be obviously moved to a storage suitable
    # for blobs. Keeping in here to ease deployment. Migration is
    # an exercise for the happy future developer.
    # The data stored is image in PNG or JPEG format.
    contour_map_image = models.BinaryField()
    # Which part of the Earth the rectangular stored
    # in contour_map_image represents.
    contour_map_reference = models.ForeignKey(LatLngBounds, related_name='+')


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


class QuestionSetMember(models.Model):
    question_set = models.ForeignKey(QuestionSet, db_index=True)
    question = models.ForeignKey(Question)
    index = models.IntegerField()

    class Meta:
        ordering = ['index']


class AnswerSet(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    question_set = models.ForeignKey(QuestionSet)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)


class Answer(models.Model):
    answer_set = models.ForeignKey(AnswerSet, db_index=True)
    question_set_member = models.ForeignKey(QuestionSetMember)
    answer_data = JSONTextField()
    scoring_data = JSONTextField() # May be recalculated
    duration = models.DurationField()
    submission_time = models.DateTimeField()
