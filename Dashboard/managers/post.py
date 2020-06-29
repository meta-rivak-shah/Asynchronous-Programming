from django.contrib.auth.models import BaseUserManager


class PostManager(BaseUserManager):
    def create_post(self, data):
        obj = self.model(
            post_text= data.cleaned_data.get( 'post_text', ''),
            post_type= data.cleaned_data.get( 'post_type', ''),
        )
        return obj


    def create_form_request(self,verified_data, file, user):
        post_obj = self.create_post(verified_data)
        if file:
            post_obj.post_image = file
        post_obj.created_by = user
        post_obj.user = user
        post_obj.save(using=self._db)
        return post_obj

