from django.contrib import admin


from home.models import Doctor_Detail, Patient_Detail, Appointment, Doctor_Profile


class Patient_DetailAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'adhar', 'phone')
    search_fields=('first_name','adhar','phone')
admin.site.register(Patient_Detail, Patient_DetailAdmin)
admin.site.register(Doctor_Detail)
admin.site.register(Doctor_Profile)
admin.site.register(Appointment)