from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Company(models.Model):
    """Model to store company information"""
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

class IPO(models.Model):
    """Model to store IPO information"""
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('listed', 'Listed'),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ipos')
    price_band_min = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price_band_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    open_date = models.DateField()
    close_date = models.DateField()
    issue_size = models.DecimalField(max_digits=20, decimal_places=2, help_text="Issue size in rupees")
    issue_type = models.CharField(max_length=100, help_text="e.g., Fresh Issue, OFS, Combination")
    listing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    ipo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    listing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_market_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rhp_document = models.FileField(upload_to='ipo_documents/rhp/', blank=True, null=True, help_text="Red Herring Prospectus")
    drhp_document = models.FileField(upload_to='ipo_documents/drhp/', blank=True, null=True, help_text="Draft Red Herring Prospectus")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.get_status_display()}"

    @property
    def price_band(self):
        """Returns the price band as a formatted string"""
        return f"₹{self.price_band_min} - ₹{self.price_band_max}"
    
    @property
    def listing_gain(self):
        """Calculate listing gain if available"""
        if self.listing_price and self.ipo_price and self.ipo_price > 0:
            gain = ((self.listing_price - self.ipo_price) / self.ipo_price) * 100
            return round(gain, 2)
        return None
    
    @property
    def current_return(self):
        """Calculate current return if available"""
        if self.current_market_price and self.ipo_price and self.ipo_price > 0:
            gain = ((self.current_market_price - self.ipo_price) / self.ipo_price) * 100
            return round(gain, 2)
        return None
    
    class Meta:
        verbose_name = "IPO"
        verbose_name_plural = "IPOs"
        ordering = ['-open_date']

class UserProfile(models.Model):
    """Extended User model for additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_client = models.BooleanField(default=False)
    api_key = models.CharField(max_length=64, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.user.username
