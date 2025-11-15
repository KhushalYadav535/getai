import csv
import io
import random
from urllib.parse import urlparse
from urllib.parse import urlunparse

import pandas as pd
import requests
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .models import News, Category, Data, ToolSubmit, Tags, Banner, Research


def get_actual_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-successful status codes
        actual_url = response.url
    except (requests.RequestException, ValueError):
        actual_url = ''
    return actual_url


def remove_query_params(url):
    parsed_url = urlparse(url)
    clean_url = urlunparse(parsed_url._replace(query=''))
    return clean_url


def save_image(image_content, image_path):
    with open(image_path, 'wb') as f:
        f.write(image_content)


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(required=False, label="Please select a file")


class DataAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("upload-csv/", self.upload_csv, name='upload_csv')
        ]
        return my_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']

            reader = csv.DictReader(io.TextIOWrapper(csv_file, encoding='utf-8'))
            for row in reader:
                title = row['Title']
                category_name = row['Category']
                description = row['Description']
                image_url = row['ImageURL']
                link = row['Link']
                click_count = random.randint(999, 5000)

                category, _ = Category.objects.get_or_create(name=category_name)

                actual_url = get_actual_url(link)
                cleaned_url = remove_query_params(actual_url)

                try:
                    # Check if the record already exists in the database
                    existing_data = Data.objects.filter(title=title).first()
                    print(existing_data)
                    if existing_data:
                        # Skip the record if it already exists
                        continue

                    # Download the image from the provided URL
                    response = requests.get(image_url)
                    response.raise_for_status()  # Raise an exception for non-successful status codes

                    # Create the Data object
                    data = Data(
                        title=title,
                        category=category,
                        description=description,
                        webpage=cleaned_url,
                        click_count=click_count
                    )
                    data.save()

                    # Save the image in the Data model
                    image_name = f"{title}.png"
                    image_content = ContentFile(response.content)
                    data.image.save(image_name, image_content)
                    print(data)

                except (requests.RequestException, ValueError, IOError):
                    pass

            self.message_user(request, "CSV file uploaded successfully.")
            return HttpResponseRedirect(reverse('admin:scrap_data_data_changelist'))

        form = CsvUploadForm()
        return render(request, 'admin/upload_csv.html', {'form': form})


class NewsAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-news-csv/', self.upload_csv, name='upload_news_csv'),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            data_objects_without_image = []
            created_count = 0
            skipped_count = 0

            for chunk in pd.read_csv(csv_file, chunksize=1000):
                for _, row in chunk.iterrows():
                    title = row.get('Title', '').strip()
                    description = row.get('Description', '').strip()
                    link = row.get('Link', '').strip()
                    image_url = row.get('ImageURL', '').strip()  # Get image URL from CSV
                    click_count = random.randint(999, 5000)

                    if not title:
                        continue

                    # Check if the record already exists in the database
                    existing_news = News.objects.filter(title=title).first()
                    if existing_news:
                        skipped_count += 1
                        continue

                    # Process URL
                    actual_url = get_actual_url(link) if link else ''
                    cleaned_url = remove_query_params(actual_url) if actual_url else link

                    try:
                        # If image URL is provided, save individually (required for FileField)
                        if image_url:
                            news = News(
                                title=title,
                                description=description,
                                webpage=cleaned_url,
                                click_count=click_count
                            )
                            
                            try:
                                response = requests.get(image_url, timeout=10)
                                response.raise_for_status()
                                
                                # Generate image name
                                image_name = f"{title[:50]}.png"  # Limit filename length
                                # Sanitize filename to remove invalid characters
                                image_name = "".join(c for c in image_name if c.isalnum() or c in (' ', '-', '_', '.')).strip()
                                image_content = ContentFile(response.content)
                                news.image.save(image_name, image_content)
                                created_count += 1
                            except (requests.RequestException, ValueError, IOError) as e:
                                # Save without image if download fails
                                print(f"Failed to download image for {title}: {str(e)}")
                                news.image = None
                                news.save()
                                created_count += 1
                        else:
                            # No image, can use bulk_create for efficiency
                            news = News(
                                title=title,
                                description=description,
                                webpage=cleaned_url,
                                click_count=click_count
                            )
                            data_objects_without_image.append(news)
                            created_count += 1
                        
                    except Exception as e:
                        print(f"Error processing news item {title}: {str(e)}")
                        continue

            # Bulk create items without images
            if data_objects_without_image:
                try:
                    News.objects.bulk_create(data_objects_without_image, ignore_conflicts=True)
                except ValidationError as e:
                    self.message_user(request, f"Error occurred while uploading some items: {str(e)}")

            if created_count > 0 or skipped_count > 0:
                message = f"CSV file processed. {created_count} news items created."
                if skipped_count > 0:
                    message += f" {skipped_count} items skipped (duplicates)."
                self.message_user(request, message)
                return HttpResponseRedirect(reverse('admin:scrap_data_news_changelist'))
            else:
                self.message_user(request, "No new news items to create. All items may already exist.")

        form = CsvUploadForm()
        return render(request, 'admin/upload_csv.html', {'form': form})


class ResearchAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-research-csv/', self.upload_csv, name='upload_research_csv'),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            data_objects = []

            for chunk in pd.read_csv(csv_file, chunksize=1000):
                for _, row in chunk.iterrows():
                    title = row['Title']
                    subject = row['Subject']
                    link = row['Link']
                    click_count = random.randint(999, 5000)

                    data = Research(
                        title=title,
                        subject=subject,
                        webpage=link,
                        click_count=click_count
                    )
                    data_objects.append(data)

            if data_objects:
                try:
                    Research.objects.bulk_create(data_objects)
                    self.message_user(request, "CSV file uploaded successfully.")
                    return HttpResponseRedirect(reverse('admin:scrap_data_research_changelist'))
                except ValidationError:
                    self.message_user(request, "Error occurred while uploading the CSV file.")

        form = CsvUploadForm()
        return render(request, 'admin/upload_csv.html', {'form': form})


admin.site.register(Data, DataAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Research, ResearchAdmin)

admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Banner)
admin.site.register(ToolSubmit)
