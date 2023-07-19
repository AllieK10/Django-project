from django.db import models


DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)


class Task(models.Model):
    name = models.CharField(max_length=120) #the title of task (test)
    topic = models.CharField(max_length=120) #someting like "Pronunciation of English words"
    # so that we could make each test as big as we want
    number_of_questions = models.IntegerField(blank=True, null=True, editable=True)
    # if test is not finished in time, you cannot go to a new level
    time = models.IntegerField(help_text="duration of the quiz in minutes", blank=True, null=True, editable=True)
    # if you made too many mistakes, you cannot take a harder test
    score_to_pass = models.IntegerField(help_text="required score to pass in %", blank=True, null=True, editable=True)
    # you can choose between three difficulty levels, you can always go back to the easier one, but never to the harder one without passing your current test
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
