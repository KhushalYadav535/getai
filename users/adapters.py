from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        # Set is_verify=True for users logging in via Google
        if sociallogin.account.provider == 'google':
            user.is_verify = True
            user.auth_provider = "google"
            user.save()

        return user
