from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewsSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"
    def items(self):
        return ['home','about','contact','privacypolicy','searching','freetrail','ordercontinue','ordersuccessfull','freetrialcheck','registationform','loginsuccess','dashboard','termsandconditions','CancellationRefundPolicy','studentregistation','LearnMoreaboutrqt', 'courses']
    def location(self, item):
        return reverse(item)