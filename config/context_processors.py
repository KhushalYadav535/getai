from scrap_data.models import Data, News, Research, Category


def get_global_context(request):
    context = {}

    data_count = Data.objects.all().count()
    news_count = News.objects.all().count()
    research_count = Research.objects.all().count()
    categories = Category.objects.all()

    if data_count:
        context.update({"data_count": data_count})
    if news_count:
        context.update({"news_count": news_count})
    if research_count:
        context.update({"research_count": research_count})
    if categories:
        context.update({"categories": categories})

    return context
