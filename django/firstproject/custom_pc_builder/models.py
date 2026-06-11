from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class CompatibilityRule(models.Model):
    component_type = models.CharField(max_length=50)
    compatible_with_type = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['component_type', 'compatible_with_type']
        verbose_name_plural = 'compatibility rules'

    def __str__(self):
        return f"{self.component_type} compatible with {self.compatible_with_type}"


class SavedBuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_builds')
    name = models.CharField(max_length=200)
    cpu = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds_as_cpu')
    gpu = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds_as_gpu')
    motherboard = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds_as_motherboard')
    ram = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds_as_ram')
    storage = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds_as_storage')
    psu = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds_as_psu')
    cooling = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds_as_cooling')
    case = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds_as_case')
    is_compatible = models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Build: {self.name}"

    @property
    def components(self):
        return {
            'cpu': self.cpu,
            'gpu': self.gpu,
            'motherboard': self.motherboard,
            'ram': self.ram,
            'storage': self.storage,
            'psu': self.psu,
            'cooling': self.cooling,
            'case': self.case,
        }

    def calculate_total(self):
        total = 0
        for comp in self.components.values():
            if comp:
                total += comp.price
        self.total_price = total
        return total

    def check_compatibility(self):
        self.is_compatible = True
        return self.is_compatible
