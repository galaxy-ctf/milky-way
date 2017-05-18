from django.contrib import admin
from .models import Assessment, Result, Iteration, Course

class AssessmentAdmin(admin.ModelAdmin):
    queryset = Assessment.objects.all()
    list_display = ('start_date', 'description', 'end_date', 'iteration', 'title', 'id',)

class ResultAdmin(admin.ModelAdmin):
    queryset = Result.objects.all()
    list_display = ('submitted', 'assessment', 'id', 'score', 'user',)

class IterationAdmin(admin.ModelAdmin):
    queryset = Iteration.objects.all()
    list_display = ('start_date', 'description', 'end_date', 'course', 'id',)

class CourseAdmin(admin.ModelAdmin):
    queryset = Course.objects.all()
    list_display = ('name', 'description', 'id',)

admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Iteration, IterationAdmin)
admin.site.register(Course, CourseAdmin)
