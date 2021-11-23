from django.db import models


class Pet(models.Model):
    """Haustier hat Namen, Alter und Beschreibung

    p = Pet(name='Fiffi', rezeptname="Currywurst")
    p.save()
    """

    ANIMAL_TYPES = (
        ("dog", "Hund"),
        ("cat", "Katze"),
        ("bird", "Vogel"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=15)  # sqlite3 prüft max_length nicht
    age = models.IntegerField()
    description = models.TextField('Beschreibung des Haustiers')
    # color
    # wohnort
    # weight
    # height
    color = models.CharField(max_length=15)
    animal_type = models.CharField(
        max_length=5,
        choices=ANIMAL_TYPES
    )

    def __str__(self):
        return '{}'.format(self.name)
