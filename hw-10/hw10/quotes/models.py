from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    tag = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f"{self.tag}"


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, default=None, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quote}"
