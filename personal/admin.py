from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.urls import path

import pandas as pd

from .models import Profile
from .forms import ExcelUploadForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "user_name",
        "user_last",
        "user_school",
        "user_phone",
    )
    search_fields = (
        "user__username",
        "user_name",
        "user_last",
        "user_school",
        "user_phone",
    )
    change_list_template = "admin/profile_changelist.html"
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-users/",
                self.admin_site.admin_view(self.upload_users),
                name="upload-users",
            ),]
        return custom_urls + urls

    def upload_users(self, request):
        if request.method == "POST":
            form = ExcelUploadForm(
                request.POST,
                request.FILES
            )
            if form.is_valid():
                excel_file = request.FILES["excel_file"]
                try:
                    df = pd.read_excel(excel_file)
                    created_count = 0
                    for _, row in df.iterrows():
                        username = str(row["username"]).strip()
                        if User.objects.filter(
                            username=username
                        ).exists():
                            continue
                        user = User.objects.create(
                            username=username,
                            password=make_password(
                                str(row["password"])
                            ),
                            first_name=str(row["first_name"]),
                            last_name=str(row["last_name"]),
                        )
                        Profile.objects.create(
                            user=user,
                            user_name=row["first_name"],
                            user_last=row["last_name"],
                            user_school=row["school"],
                            user_phone=row["phone"],
                        )
                        created_count += 1
                    messages.success(
                        request,
                        f"{created_count} users imported successfully."
                    )
                    return redirect("../")
                except Exception as e:
                    messages.error(
                        request,
                        f"Import failed: {e}"
                    )
        else:
            form = ExcelUploadForm()
        context = {
            **self.admin_site.each_context(request),
            "title": "Upload Users",
            "form": form,
        }
        return render(
            request,
            "admin/upload_users.html",
            context,
        )