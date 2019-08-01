from django import template

register = template.Library()

# ImageType'a göre verilen ideanın fotoğrafının urli
@register.filter(name='cast_image_type')
def cast_image_type(SelectedIdea, Phototype):

    current_image = SelectedIdea.photo_set.all().filter(ImageType=Phototype).first()
    if current_image is None:
        return "static/default_idea.jpg"
    return current_image.Image.url

@register.filter(name='get_like_count')
def get_like_count(SelectedIdea):
    return SelectedIdea.likes_list.all().count()


register.filter('get_like_count', get_like_count)
register.filter('cast_image_type', cast_image_type)
