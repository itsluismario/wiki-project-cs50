import markdown2
import random
import re
from django.shortcuts import render, redirect, HttpResponse

from . import util

pagelist = util.list_entries()

# default page


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
