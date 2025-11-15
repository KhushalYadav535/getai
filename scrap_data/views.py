import csv
import os
import time
import uuid

from PIL import Image, ImageDraw, ImageFont, ImageOps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .models import Data, Category, Banner, Favourite, Tags, ToolSubmit, News, Research


def scrape_data(request):
    driver = webdriver.Chrome()

    # Open the website
    driver.get("https://gpte.ai/")

    # Scroll to the bottom of the page to load more content
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find all elements
    title_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'post-card-title')))
    category_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'post-card-primary-tag')))
    description_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'post-card-excerpt')))
    image_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'post-card-image')))
    link_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'post-card-image-link')))

    # Extract the data
    titles = [title_element.text for title_element in title_elements]
    categories = [category_element.text for category_element in category_elements]
    descriptions = [description_element.text for description_element in description_elements]
    image_urls = [image_element.get_attribute("src") for image_element in image_elements]
    links = [link_element.get_attribute("href") for link_element in link_elements]

    scraped_data = zip(titles, categories, descriptions, image_urls, links)
    csv_rows = [['Title', 'Category', 'Description', 'Image URL', 'Link']] + list(scraped_data)

    # Save the CSV file to a specific location on the server
    with open('scraped_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_rows)
        
    driver.quit()  # Close the web browser after scraping is done.

    # Prepare the response with the CSV file as an attachment
    with open('scraped_data.csv', 'rb') as csv_file:
        response = HttpResponse(csv_file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=scraped_data.csv'

    return response


class ScrapeGoogleNewsView(View):
    def scrape_google_news(self, query):
        url = f"https://www.google.com/search?q={query}&tbm=nws"

        driver = webdriver.Chrome()
        driver.get(url)

        scraped_data = []

        while True:
            # Allow time for the page to load
            time.sleep(2)

            titles = driver.find_elements(By.CSS_SELECTOR, ".n0jPhd.ynAwRc.MBeuO.nDgy9d")
            title_texts = [title.text for title in titles]

            links = driver.find_elements(By.CSS_SELECTOR, "a.WlydOe")
            link_urls = [link.get_attribute("href") for link in links]

            descriptions = driver.find_elements(By.CSS_SELECTOR, ".GI74Re.nDgy9d")
            description_texts = [desc.text for desc in descriptions]

            scraped_data.extend(list(zip(title_texts, link_urls, description_texts)))

            try:
                next_button = driver.find_element(By.ID, "pnnext")
                next_url = next_button.get_attribute("href")
            except NoSuchElementException:
                break

            if not next_url:
                break

            # Check if a CAPTCHA page is encountered
            if "www.google.com/sorry" in next_url:
                print("CAPTCHA challenge encountered. Stopping scraping.")
                break

            driver.get(next_url)

        driver.quit()

        return scraped_data

    def save_to_csv(self, data):
        with open("scraped_data.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Title", "Link", "Description"])

            for row in data:
                writer.writerow(row)

    def get(self, request):
        search_query = "latest+ai+news+june+2023"  # Replace with your dynamic query

        scraped_data = self.scrape_google_news(search_query)
        self.save_to_csv(scraped_data)

        return HttpResponse("Scraping completed and data saved to CSV.")


# class DataListView(VerificationRequiredMixin, ListView):
class DataListView(ListView):
    model = Data
    template_name = 'home.html'
    context_object_name = 'data'
    paginate_by = 40

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        category_filter = self.request.GET.get('category')
        search_query = self.request.GET.get('search')
        tag_filter = self.request.GET.get('tag')

        if category_filter and category_filter != 'all':
            queryset = queryset.filter(category__name=category_filter)

        if search_query:
            if category_filter and category_filter != 'all':
                queryset = queryset.filter(title__icontains=search_query)
            else:
                queryset = queryset.filter(title__icontains=search_query, category__isnull=False)

        if tag_filter:
            queryset = queryset.filter(tag__id=tag_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        banner = Banner.objects.first()
        tags = Tags.objects.all()
        category_filter = self.request.GET.get('category', 'all')
        search_query = self.request.GET.get('search', '')

        # Get the user's bookmarks
        if self.request.user.is_authenticated:
            favourite = Favourite.objects.get_or_create(user=self.request.user)[0]
            user_bookmarks = favourite.data.all()
        else:
            user_bookmarks = []

        context['categories'] = categories
        context['banner'] = banner
        context['selected_category'] = category_filter
        context['search_query'] = search_query
        context['tags'] = tags
        context['data_count'] = Data.objects.count()
        context['news_count'] = News.objects.count()
        context['research_count'] = Research.objects.count()
        context['user_bookmarks'] = user_bookmarks

        return context

    def get(self, request, *args, **kwargs):
        if 'search' in request.GET and not request.GET['search']:
            # Clear all filters and load all data
            return redirect('data_list')

        return super().get(request, *args, **kwargs)


class NewsListView(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 40

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at', '-id')

        # Retrieve the search query from the GET parameters
        search_query = self.request.GET.get('search')

        if search_query:
            # Filter the queryset based on the search query
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the search query back to the template
        context['search_query'] = self.request.GET.get('search')
        context['news_count'] = News.objects.count()

        return context


class ResearchListView(ListView):
    model = Research
    template_name = 'research.html'
    context_object_name = 'data'
    paginate_by = 40

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')

        # Retrieve the search query from the GET parameters
        search_query = self.request.GET.get('search')

        if search_query:
            # Filter the queryset based on the search query
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(subject__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the search query back to the template
        context['search_query'] = self.request.GET.get('search')
        context['research_count'] = Research.objects.count()

        return context


@login_required(login_url='login')
def add_bookmark(request, item_id):
    if request.method == 'POST':
        user = request.user
        if not request.user.is_verify:
            messages.error(request,
                           'You have not verified your email address. Please check your email and verify your account.')
            return redirect('send_verification_email')
        item = Data.objects.get(pk=item_id)

        favourite, created = Favourite.objects.get_or_create(user=user)

        if item in favourite.data.all():
            favourite.data.remove(item)
        else:
            favourite.data.add(item)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='login')
def bookmark_view(request):
    favourite = Favourite.objects.get(user=request.user)
    items = favourite.data.all()
    context = {'items': items}
    return render(request, 'favourite.html', context)


def submit_tool(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        tool_name = request.POST.get('tool_name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        interested = request.POST.get('interested') == 'on'

        category = Category.objects.get(id=category_id)

        tool_submit = ToolSubmit(
            full_name=full_name,
            tool_name=tool_name,
            email=email,
            website=website,
            category=category,
            description=description,
            interested=interested
        )
        tool_submit.save()

        return redirect('data_list')  # Redirect to a success page after submission

    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'submit.html', context)


class ProfilePictureSerializer(serializers.Serializer):
    profile_image = serializers.ImageField()
    name = serializers.CharField()
    designation = serializers.CharField()
    region_or_branch = serializers.CharField()


class ProfilePictureView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ProfilePictureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Extract validated data
        profile_image = validated_data['profile_image']
        name = validated_data['name']
        designation = validated_data['designation']
        region_or_branch = validated_data['region_or_branch']

        # Generate a unique filename for the output image
        unique_filename = f"profile_{uuid.uuid4().hex}.jpg"
        user_directory = os.path.join(settings.MEDIA_ROOT, 'e-card')
        os.makedirs(user_directory, exist_ok=True)
        output_image_path = os.path.join(user_directory, unique_filename)

        # Base image path
        base_image_path = os.path.join(settings.STATIC_ROOT, 'input_image.jpg')

        try:
            # Load the base image
            base_image_pil = Image.open(base_image_path)

            # Resize the profile image to fit within the half-circle section
            circle_size = (552, 552)
            profile_image_pil = Image.open(profile_image)
            profile_image_pil = ImageOps.fit(profile_image_pil, circle_size, method=Image.LANCZOS)

            # Create a mask for the half-circle section
            mask = Image.new("L", circle_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, circle_size[0], circle_size[1]), fill=255)

            # Apply the mask to the profile image
            profile_image_pil.putalpha(mask)

            # Choose a position to place the profile image on the base image
            profile_position = (-92, 245)

            # Paste the profile image onto the base image
            base_image_pil.paste(profile_image_pil, profile_position, profile_image_pil)

            # Define the text properties
            text_position = (26, 845)
            text_color = (0, 0, 0)
            font_size_name = 24
            font_size_others = 16

            font_name = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Montserrat-Bold.ttf'),
                                           font_size_name)
            font_others = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Montserrat-Bold.ttf'),
                                             font_size_others)

            # Create a drawing context
            draw = ImageDraw.Draw(base_image_pil)

            # Draw the text on the image
            draw.text(text_position, name, font=font_name, fill=text_color)
            draw.text((text_position[0], text_position[1] + 26), designation, font=font_others, fill=text_color)
            draw.text((text_position[0], text_position[1] + 46), region_or_branch, font=font_others, fill=text_color)

            # Convert the image to RGB mode before saving as JPEG
            base_image_pil = base_image_pil.convert("RGB")

            # Save the modified image with compression
            base_image_pil.save(output_image_path, optimize=True, quality=80)

            # Generate the complete image URL
            image_url = request.build_absolute_uri(settings.MEDIA_URL + 'e-card' + '/' + unique_filename)

            return Response({'image_url': image_url})

        except Exception as e:
            return Response({'error': str(e)}, status=400)


class StoryMakerView(TemplateView):
    template_name = 'health-care-chat-bot.html'


class TribeView(TemplateView):
    template_name = 'tribe.html'
