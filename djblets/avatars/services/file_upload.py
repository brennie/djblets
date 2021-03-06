"""An avatar service for providing uploaded images."""

from __future__ import unicode_literals

from hashlib import md5

from django.core.exceptions import ValidationError
from django.core.files.storage import DefaultStorage
from django.forms import forms
from django.utils.translation import ugettext_lazy as _

from djblets.avatars.forms import AvatarServiceConfigForm
from djblets.avatars.services.base import AvatarService


class FileUploadAvatarForm(AvatarServiceConfigForm):
    """The UploadAvatarService configuration form."""

    avatar_service_id = 'file-upload'

    js_view_class = 'Djblets.Avatars.FileUploadSettingsFormView'
    template_name = 'avatars/services/file_upload_form.html'

    avatar_upload = forms.FileField(label=_('File'), required=True)

    MAX_FILE_SIZE = 1 * 1024 * 1024
    is_multipart = True

    def clean_file(self):
        """Ensure the uploaded file is an image of an appropriate size.

        Returns:
            django.core.files.UploadedFile:
            The uploaded file, if it is valid.

        Raises:
            django.core.exceptions.ValidationError:
                Raised if the file is too large or the incorrect MIME type.
        """
        f = self.cleaned_data['avatar_upload']

        if f.size > self.MAX_FILE_SIZE:
            raise ValidationError(_('The file is too large.'))

        content_type = f.content_type.split('/')[0]

        if content_type != 'image':
            raise ValidationError(_('Only images are supported.'))

        return f

    def save(self):
        """Save the file and return the configuration.

        Returns:
            dict:
            The avatar service configuration.
        """
        storage = DefaultStorage()

        file_path = self.cleaned_data['avatar_upload'].name
        file_path = storage.get_valid_name(file_path)
        file_data = self.cleaned_data['avatar_upload'].read()

        with storage.open(file_path, 'wb') as f:
            f.write(file_data)

        file_hash = md5()
        file_hash.update(file_data)

        return {
            'absolute_url': storage.url(file_path),
            'file_path': file_path,
            'file_hash': file_hash.hexdigest(),
        }


class FileUploadService(AvatarService):
    """An avatar service for uploaded images."""

    avatar_service_id = 'file-upload'
    name = _('File Upload')

    config_form_class = FileUploadAvatarForm

    def get_avatar_urls_uncached(self, user, size):
        """Return the avatar URLs for the requested user.

        Args:
            user (django.contrib.auth.models.User):
                The user whose avatar URLs are to be fetched.

            size (int):
                The size (in pixels) the avatar is to be rendered at.

        Returns
            dict:
            A dictionary containing the URLs of the user's avatars at normal-
            and high-DPI.
        """
        settings_manager = self._settings_manager_class(user)
        configuration = \
            settings_manager.configuration_for(self.avatar_service_id)

        if not configuration:
            return {}

        return {
            '1x': configuration['absolute_url'],
        }

    def cleanup(self, user):
        """Clean up the uploaded file.

        This will delete the uploaded file from the storage.

        Args:
            user (django.contrib.auth.models.User):
                The user.
        """
        settings_manager = self._settings_manager_class(user)
        configuration = settings_manager.configuration_for(
            self.avatar_service_id)

        del configuration['file_hash']
        settings_manager.save()

        storage = DefaultStorage()
        storage.delete(configuration['file_path'])

    def get_etag_data(self, user):
        """Return the ETag data for the user's avatar.

        Args:
            user (django.contrib.auth.models.User):
                The user.

        Returns:
            list of unicode:
            The uniquely identifying information for the user's avatar.
        """
        settings_manager = self._settings_manager_class(user)
        configuration = \
            settings_manager.configuration_for(self.avatar_service_id)

        file_hash = configuration.get('file_hash')

        if not file_hash:
            storage = DefaultStorage()
            file_hash = md5()

            with storage.open(configuration['file_path'], 'rb') as f:
                file_hash = file_hash.update(f.read())

            configuration['file_hash'] = file_hash.hexdigest()
            settings_manager.save()

        return [self.avatar_service_id, file_hash]
