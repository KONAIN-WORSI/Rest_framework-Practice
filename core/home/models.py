from django.db import models

    
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    father_name = models.CharField(max_length=100)

class Category(models.Model):
    category_name = models.CharField(max_length=100)

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=100)


class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to='excel')


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description  = models.TextField(blank = True)
    skill = models.JSONField(default=list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company} in {self.location} with skills: {', '.join(self.skill)}"

    