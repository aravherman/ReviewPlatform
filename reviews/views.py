from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg, Count
from .models import Shop, Review
from .forms import userreg
# Create your views here.
def index(request):
    shops = Shop.objects.all()
    cat = request.GET.get('category')
    query = request.GET.get('search')
    if query:
        shops = shops.filter(name__icontains=query) 
    if cat and cat!='category':
        shops = shops.filter(category=cat)
    categories = Shop.category_choices

    sort = request.GET.get('sort')
    if sort == 'desc-rating':
        shops = shops.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    elif sort == "desc-review":
        shops = shops.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
    elif sort == "new":
        shops = shops.order_by('-created_at')


    paginator = Paginator(shops, 6)
    pnumber = request.GET.get('page')
    try:
        sh = paginator.page(pnumber)
    except PageNotAnInteger:
        sh = paginator.page(1)
    except EmptyPage:
        sh = paginator.page(paginator.num_pages)
    return render(request, 'reviews/index.html',{'shops':shops, 'categories':categories, 'sh':sh})

# this decorator ensures that only logged-in users can access this view
@login_required(login_url='login')
def shop_det(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    reviews = Review.objects.filter(shop=shop)

    if request.method=="POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        Review.objects.create(
            shop = shop,
            user = request.user ,
            rating = rating,
            comment = comment
        )
        return redirect('shop_detail',shop_id = shop_id)
    return render(request, 'reviews/shop_detail.html',{
        'shop':shop,
        'reviews' : reviews
    })

# def is_admin(user):
#     return user.is_staff
# is_admin,
@login_required(login_url='login')
def add_shop(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to add a shop.")
    if request.method=="POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        category = request.POST.get("category")
        qname = Shop.objects.filter(name__iexact=name)
        qloc = Shop.objects.filter(location__iexact=location)
        if qname.exists() and qloc.exists():
            categories = Shop.category_choices
            return render(request, 'reviews/add_shop.html',{'error':'Shop with this name and location already exists.','categories':categories})
        
        Shop.objects.create(
            name = name,
            location = location,
            category = category,
            added_by = request.user
        )
        return redirect('home')
    else:
        categories = Shop.category_choices
        return render(request, 'reviews/add_shop.html',{'categories':categories})
    
@login_required(login_url='login')
def del_shop(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to delete a shop.")
    if request.method == "POST":
        shop_name = request.POST.get("name")
        shop_location = request.POST.get("location")
        shop_category = request.POST.get("category")
        try:
            shop = Shop.objects.get(name__iexact=shop_name, location__iexact=shop_location, category=shop_category)
            shop.delete()
            return redirect('home')
        except Shop.DoesNotExist:
            categories = Shop.category_choices
            return render(request, 'reviews/del_shop.html',{'error':'No matching shop found. Please check the details and try again.','categories':categories})
    else:
        categories = Shop.category_choices
        return render(request, 'reviews/del_shop.html',{'categories':categories})
    
@login_required(login_url='login')
def upd_shop(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to update a shop.")
    if request.method == "POST":
        old_name = request.POST.get("old_name")
        old_location = request.POST.get("old_location")
        old_category = request.POST.get("old_category")
        new_name = request.POST.get("new_name")
        new_location = request.POST.get("new_location")
        new_category = request.POST.get("new_category")
        shop = Shop.objects.all()
        try:
            shop = Shop.objects.get(name__iexact=old_name, location__iexact=old_location, category=old_category)
            shop.name = new_name
            shop.location = new_location
            shop.category = new_category
            shop.save()
            return redirect('home')
        except Shop.DoesNotExist:
            categories = Shop.category_choices
            return render(request, 'reviews/upd_shop.html',{'error':'No matching shop found. Please check the details and try again.','categories':categories})
    else:
        categories = Shop.category_choices
        return render(request, 'reviews/upd_shop.html',{'categories':categories})
def login_view(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        upass = request.POST.get('password')
        user = authenticate(request, username=uname, password=upass)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            # if next_url:
            #     return redirect(next_url)
            return redirect('home')
        else:
            return render(request, 'reviews/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'reviews/login.html')
    
def logt(request):
    logout(request)
    return redirect('home')

def regt(request):
    if request.method == "POST":
        form = userreg(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            error = form.errors
            return render(request, 'reviews/register.html',{'form':form, 'error':error})
    else:
        form = userreg()
        return render(request, 'reviews/register.html', {'form':form})
    
@login_required
def upvote(request, review_id):
    rev = get_object_or_404(Review, pk=review_id)
    user = request.user
    if user in rev.upvoted_by.all():
        return JsonResponse({'total':rev.total_votes()})
    if user in rev.downvoted_by.all():
        rev.downvoted_by.remove(user)
    rev.upvoted_by.add(user)
    rev.upv+=1
    rev.save()
    return JsonResponse({
        'total':rev.total_votes(),
        'upv': True,
        'dnv': False
        })

@login_required
def downvote(request, review_id):
    rev = get_object_or_404(Review, pk=review_id)
    user = request.user
    if user in rev.downvoted_by.all():
        return JsonResponse({'total':rev.total_votes()})
    if user in rev.upvoted_by.all():
        rev.upvoted_by.remove(user)
    rev.downvoted_by.add(user)
    rev.dnv+=1
    rev.save()
    return JsonResponse({
        'total':rev.total_votes(),
        'dnv': True,
        'upv': False
        })
