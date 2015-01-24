from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

# Create your views here.
from comments.forms import CommentForm
from comments.models import Comment



from .models import Video, Category


@login_required
def video_detail(request, cat_slug, vid_slug):
	obj = Video.objects.get(slug=vid_slug)
	comments = obj.comment_set.all()
	for c in comments:
		c.get_children()
	try:
		cat = Category.objects.get(slug=cat_slug)
	except:
		raise Http404
	try:
		obj = Video.objects.get(slug=vid_slug)
		comments = obj.comment_set.all()
		comment_form = CommentForm(request.POST or None)
		if comment_form.is_valid():
			parent_id = request.POST.get('parent_id')
			parent_comment = None
			if parent_id is not None:
				try:
					parent_comment = Comment.objects.get(id=parent_id)
				except:
					parent_comment = None

			comment_text = comment_form.cleaned_data['comment']
			new_comment = Comment.objects.create_comment(
				user=request.user, 
				path=request.get_full_path(), 
				text=comment_text,
				video = obj,
				parent=parent_comment
				)
			'''
			+**** add comment thread and show that thread with a message
			'''

			return HttpResponseRedirect(obj.get_absolute_url())
		return render(request, "videos/video_detail.html", {"obj": obj, "comments":comments, "comment_form": comment_form})
	except:
		raise Http404



def category_list(request):
	queryset = Category.objects.all()
	context = {
		"queryset": queryset,
	}
	return render(request, "videos/category_list.html", context)



@login_required
def category_detail(request, cat_slug):
	try:
		obj = Category.objects.get(slug=cat_slug)
		queryset = obj.video_set.all()
		return render(request, "videos/video_list.html", {"obj": obj, "queryset": queryset})
	except:
		raise Http404



# def video_edit(request):

# 	return render(request, "videos/video_single.html", {})


# def video_create(request):

# 	return render(request, "videos/video_single.html", {})
