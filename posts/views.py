from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import CommentForm, PostForm
from .models import Post, PostView, Author
from marketing.models import Signup
from services.models import Service, Contact, Event
from marketing.forms import EmailSignupForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import stripe
from django.contrib import messages


stripe.api_key = settings.STRIPE_API_KEY

def error_404(request, exception):
        context = {}
        return render(request,'blog/404.html', context)

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'blog/search_results.html', context)


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def about(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    

    context = {
        'about_page': 'active',
        'object_list': featured,
        'latest': latest  
    }
    return render(request, 'blog/about.html', context)


def index(request):
    all_events = Event.objects.all()
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    context = {
        'home_page': 'active',
        'all_events': all_events,
        'object_list': featured,
        'latest': latest  
    }
    return render(request, 'blog/index.html', context)

def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post_list = Post.objects.get_queryset().order_by('id')
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    form = EmailSignupForm()
    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

        
    try:
        paginated_queryset = paginator.page(page)
    
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)

    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'blog_page': 'active',
        'form': form,
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count
    }
    return render(request, 'blog/blog.html', context)

def post(request, id):
    category_count = get_category_count()
    post = get_object_or_404(Post, id=id)
    most_recent = Post.objects.order_by('-timestamp')[0:3]

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.id
            }))

    context = {
        'form': form,
        'category_count': category_count,
        'post': post,
        'most_recent': most_recent
    }
    return render(request, 'blog/post.html', context)

def services(request):
    all_services = Service.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post_list = Post.objects.all()

    context = {
        'services_page': 'active',
        'most_recent': most_recent,
        'all_services': all_services
    }

    return render(request, 'blog/services.html', context)


def serviceDetails(request, id):
    details = get_object_or_404(Service, id=id)
    all_services = Service.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'all_services': all_services,
        'most_recent': most_recent,
        'details': details
    }
    return render(request, 'blog/single_service.html', context)


def contact_us(request):
    context = {
        'contact_page': 'active',
    }
    return render(request, 'blog/contact_us.html', context)


def thankyou(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

        consumer_info = Contact(name=name, email=email, subject=subject, message=message)
        consumer_info.save()

        send_mail(consumer_info.subject + ', from: ' + consumer_info.name + ", " + consumer_info.email, consumer_info.message,
              settings.EMAIL_HOST_USER, ['k.deep5643@gmail.com'], fail_silently=False)
    return render(request, 'blog/thankyou.html', {})


def events(request):
    all_events = Event.objects.all()
    context = {
        'events_page': 'active',
        "all_events": all_events
    }
    return render(request, 'blog/events.html', context)

@user_passes_test(lambda u: u.is_superuser)
def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/post_create.html", context)

@user_passes_test(lambda u: u.is_superuser)
def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/post_create.html", context)


@user_passes_test(lambda u: u.is_superuser)
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))


@login_required()
def donation(request):
    context = {}
    return render(request, 'blog/donation.html', context)


@login_required()
def charge(request):
    amount = int(request.POST['amount'])
    if request.method == "POST":
        print('Data:', request.POST)

        customer = stripe.Customer.create(
            email = request.POST['email'],
            name = request.POST['name'],
            source = request.POST['stripeToken'],
        )

        charge = stripe.Charge.create(
            customer = customer,
            amount = amount*100,
            currency="nzd",
            description = "Donation",
            
        )

        messages.success(request, f'Thank you for your donations!')
        return redirect('index')
