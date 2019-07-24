from django import template

register = template.Library()

# ImageType'a göre verilen ideanın fotoğrafının urli
@register.filter(name='cast_image_type')
def cast_image_type(SelectedIdea, type):
    return SelectedIdea.photo_set.all().filter(ImageType=1).first().Image.url


register.filter('cast_image_type', cast_image_type)
