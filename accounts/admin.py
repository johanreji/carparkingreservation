
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse, HttpResponseRedirect


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # change_form_template = "admin/user_change_form.html"

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin', 'vehicle_number', 'mobile_number')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('mobile_number','vehicle_number')}),
        ('Permissions', {'fields': ('admin','staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile_number', 'vehicle_number', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def response_change(self, request, obj):
        if(request.method=="POST"):
            if "admin" in request.POST:
                matching_user = self.get_queryset(request).filter(email=obj.email) 
                obj.staff= True
                obj.admin = True
                obj.save()
                self.message_user(request, "User is now admin")
                return HttpResponseRedirect(".")
        return super().response_change(request, obj)
    min_objects = 1

    def has_delete_permission(self, request, obj=None):
        if(request.method=="POST"):
            queryset = self.model.objects.all()
    
            # If we're running the bulk delete action, estimate the number
            # of objects after we delete the selected items
            selected = request.POST.getlist('_selected_action')
            if selected:
                queryset = queryset.filter(admin=True).exclude(pk__in=selected)
            
            print(queryset.count())
            if queryset.count() < 1:
                message = 'There should be at least 1 admin left.'
                self.message_user(request, message.format(self.min_objects))
                return False

        return super(UserAdmin, self).has_delete_permission(request, obj)    
    def delete_view(self, request, object_id, extra_context=None):
        if(request.method=="POST"):
            queryset = User.objects.filter(admin=True).exclude(pk=object_id)
            if queryset.count() < 1:
                message = 'There should be at least 1 admin left.'
                self.message_user(request, message)
                return HttpResponseRedirect(request.path_info)
        return super(UserAdmin, self).delete_view(request, object_id, extra_context)   
             

    


admin.site.register(User, UserAdmin)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)