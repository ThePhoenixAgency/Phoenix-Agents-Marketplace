---
name: django-patterns
description: DRF, ORM optimization, signals, middleware
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Django Patterns
## DRF Serializer
```python
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']
```
## ORM Optimization
```python
# [INTERDIT] N+1
for user in User.objects.all():
    print(user.profile.bio)  # query par user
# [OK] select_related (FK, OneToOne)
users = User.objects.select_related('profile').all()
# [OK] prefetch_related (ManyToMany, reverse FK)
users = User.objects.prefetch_related('orders').all()
```
## Signals
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```
