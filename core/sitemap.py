from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        # List the URL names for your static pages
        return ['welcome', 'subscriptions:subscribe', 'users:dashboard', 'products:products_display', 'training:training_display']
    
    def location(self, item):
        return reverse(item)