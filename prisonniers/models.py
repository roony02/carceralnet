from django.db import models

class Prisonnier(models.Model):

    numero_prisonnier = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100)

    nom_pere = models.CharField(max_length=100, null=True, blank=True)
    nom_mere = models.CharField(max_length=100, null=True, blank=True)

    nationalite = models.CharField(max_length=100, null=True, blank=True)

    etat_civil = models.CharField(
        max_length=20,
        choices=[
            ('Celibataire', 'Celibataire'),
            ('Marie', 'Marie'),
            ('Divorce', 'Divorce'),
            ('Veuf', 'Veuf')
        ],
        null=True,
        blank=True
    )

    age = models.IntegerField(null=True, blank=True)

    photo = models.ImageField(
        upload_to='photos/',
        null=True,
        blank=True
    
    )

    plaignant = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    temoin = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    alarme_active = models.BooleanField(default=True)

    cellule = models.CharField(max_length=20)
    motif = models.TextField()

    date_entree = models.DateField()
    date_sortie = models.DateField()

    statut = models.CharField(
        max_length=20,
        choices=[
            ('encours', 'En cours'),
            ('liberable', 'Libérable'),
            ('libere', 'Libéré')
        ]
    )

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
        
    