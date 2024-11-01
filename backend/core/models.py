from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.timezone import now

class Category(models.Model):
    name= models.CharField(_("name"), max_length=50,)
    description= models.TextField(_("description"),)
    category_parent= models.ForeignKey("Category", verbose_name=_("category parent"), on_delete=models.CASCADE,)
    created_at= models.DateTimeField(_("created at"), auto_now_add= True, auto_created= True,)
    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return str(self.name)


class Company(models.Model):
    name= models.CharField(_("name"), max_length=50,)
    logo= models.ImageField(_("logo"), upload_to="media/company/logo/",)
    description= models.TextField(_("description"),)
    created_at= models.DateTimeField(_("created at"), auto_now_add= True, auto_created= True,)
    

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return str(self.name)
    

class Product(models.Model):
    name= models.CharField(_("name"), max_length=50)
    version= models.CharField(_("version"), max_length=50)
    description= models.TextField(_("description"))

    category= models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.CASCADE)
    company= models.ForeignKey(Company, verbose_name=_("campany"), on_delete=models.CASCADE)

    cost= models.DecimalField(_("cost"), max_digits=5, decimal_places=2)
    price= models.DecimalField(_("price"), max_digits=5, decimal_places=2)

    status= models.BooleanField(_("status (active/non-active)"))

    source= models.CharField(_("source campany"), max_length=50)
    source_id= models.CharField(_("source id"), max_length=50)

    created_by= models.ForeignKey(User, verbose_name=_("created by"), on_delete=models.CASCADE)
    created_at= models.DateTimeField(_("created at"), auto_now_add= True, auto_created= True,)
    

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return str(self.name)
    
    def average_rating(self):
        """Calculate average rating from all reviews."""
        reviews = self.reviews.all()  # Reverse relationship from Review model
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0



class Image(models.Model):
    product= models.ForeignKey(Product, verbose_name=_("user id"), on_delete=models.CASCADE)
    img= models.ImageField(_("photo"), upload_to="media/product/",)
    
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return str(self.product)
    
class Variation(models.Model):
    product= models.ForeignKey(Product, verbose_name=_("user id"), on_delete=models.CASCADE)
    variation_type= models.CharField(_("variation type"), max_length=50)
    variation_value= models.TextField(_("variation value"))
    
    class Meta:
        verbose_name = _("variation")
        verbose_name_plural = _("variations")

    def __str__(self):
        return str(self.product)

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=1)  # 1 to 5 rating
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'Review by {self.user_id} for {self.product}'