from django.shortcuts import render
from googletrans import Translator
# Create your views here.
def index(request):
    if request.method == "POST":
        text = request.POST.get("trans")
        translator = Translator()
        trans = translator.translate(text, src='en', dest='ko')
        print("English to Japanese: ", trans.text)
        context={
            'text': trans.text
        }

        return render(request, "libr/index.html", context)
    return render(request, "libr/index.html")