from django.shortcuts import redirect

#for user permission 
def unauthenticated_user(view_func):
  def wrapper_func(request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('home')
    else:
      return view_func(request, *args, **kwargs)

  return wrapper_func
