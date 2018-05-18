from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
            # Uncomment if you don't want the slug to change every time the name changes
            #if self.id is None:
             #   self.slug = slugify(self.name)
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):  
        return self.name
        
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'pages'

    def __str__(self):     
        return self.title

'''class PageForm(forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data'''