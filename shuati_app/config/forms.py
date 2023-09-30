from django import forms


class LoginRegisterForm(forms.ModelForm):
    pass

# class RegisterForm(forms.ModelForm):
#     # 新增确认密码
#     conform_password = forms.CharField(
#         label="Confirm Password",
#         widget=forms.PasswordInput(
#             render_value=True,  # 密码保存
#         )
#     )
#     pwd = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(
#             render_value=True,  # 密码保存
#         )
#     )
#     code = forms.CharField(label="captcha")
#
#     class Meta:
#         model = User
#         fields = ["username", "email", "password", "conform_password", "code"]
#         widgets = {
#             "password": forms.PasswordInput(render_value=True)
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for name, field in self.fields.items():
#             field.widget.attrs = {
#                 "class": "form-control",
#                 "placeholder": field.label
#             }
