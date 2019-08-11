from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from hardware.models import BlogPost

# Create your models here.

User = settings.AUTH_USER_MODEL


# session just represents the row of cart
class session(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer')
    name = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    votes = models.PositiveIntegerField(default=1)
    rate = models.PositiveIntegerField(default=10)

    def price(self):
        return self.votes * self.rate

    def __str__(self):
        return str(self.user) + "-" + str(self.name)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField(default=0, )

    @receiver(post_save, sender=session)
    def create_cart(sender, instance, created, **kwargs):
        if created:
            Cart.objects.get_or_create(user=instance.user)

    @receiver(post_save, sender=session)
    def update_cart(sender, instance, **kwargs):
        sessions = session.objects.filter(user=instance.user)
        items = 0
        for ses in sessions:
            items += ses.votes
        instance.user.cart.count = items
        instance.user.cart.save()

    @receiver(post_delete, sender=session)
    def delete_cart(sender, instance, **kwargs):
        if not session.objects.filter(user=instance.user):
            instance.user.cart.delete()


        else:
            sessions = session.objects.filter(user=instance.user)
            items = 0
            for ses in sessions:
                items += ses.votes
                instance.user.cart.count = items
                instance.user.cart.save()