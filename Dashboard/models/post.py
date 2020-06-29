from django.db import models
from CommonApp.base import IdWrapper, CustomModel, DeletableWrapper
from CommonApp import constants
from Dashboard.Validations import postValidations
from Dashboard.managers import PostManager



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/'.format(instance.id, filename )


class PostModel(IdWrapper, CustomModel, DeletableWrapper):

    post_image = models.FileField(upload_to=user_directory_path, null=True, blank=True )
    post_text = models.CharField(max_length=1028, null=True, blank=True)
    post_type = models.CharField(max_length=128, null=True, blank=True, choices=constants.POST_TYPE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('CustomUser.CustomUserModel', related_name='%(class)s_updated_by',
                                   on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('CustomUser.CustomUserModel', related_name='%(class)s_id',
                             on_delete=models.CASCADE, null=True, blank=True)
    objects = PostManager()
    validations = postValidations()

    def __str__(self):
        return str(self.id)+str(self.post_type)

    def update_post(self,verified_data):
        pass

    def delete_post(self):
        pass
