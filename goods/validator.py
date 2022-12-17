from rest_framework.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

MEGABYTE_LIMIT = 1
REQUIRED_WIDTH = 1
REQUIRED_HEIGHT = 1

def logo_validator(image):
    filesize = image.size
    print("filesize",filesize)

    width, height = get_image_dimensions(image)
    print("filesize",width, height)
    if width != REQUIRED_WIDTH or height != REQUIRED_HEIGHT:
        print("여기 왔어요")

        raise ValidationError(f"You need to upload an image with {REQUIRED_WIDTH}x{REQUIRED_HEIGHT} dimensions")

    if filesize > MEGABYTE_LIMIT * 1 * 1:
        print("여기 왔어요")
        raise ValidationError(f"Max file size is {MEGABYTE_LIMIT}MB")
# class OrganisationDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Organisation
#         fields = ('id', 'name', 'slug', 'logo',)

#     slug = serializers.ReadOnlyField()
#     logo = ImageField(validators=[logo_validator])
# 