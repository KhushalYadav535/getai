from django.shortcuts import redirect

class VerificationRequiredMixin:
    def get_verification_redirect(self):
        return redirect('email_verify')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_verify:
            return super().dispatch(request, *args, **kwargs)
        elif not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.get_verification_redirect()
