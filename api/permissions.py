from rest_framework import permissions
import api.models as api_models

##################################################################################
#                             Base Role permissions                              #
##################################################################################

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'STUDENT' in request.user_object.base_roles 

class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):     
        return 'PARENT' in request.user_object.base_roles 

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):     
        return 'TEACHER' in request.user_object.base_roles 

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):     
        return 'MANAGER' in request.user_object.base_roles 
        
class IsHeadMaster(permissions.BasePermission):
    def has_permission(self, request, view):     
        return 'HEADMASTER' in request.user_object.base_roles 

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):     
        return 'ADMIN' in request.user_object.base_roles 

##################################################################################
#                                 Other permissions                              #
##################################################################################

class IsValidParentChildPair(permissions.BasePermission):
    def has_permission(self, request, view):
        parent_id = request.data.get('parent',None)
        parent = api_models.User.objects.get(id=parent_id)
        parent_role = api_models.Role.objects.get(id=parent.role)
        if parent_role.name != 'PARENT':
            return False
        children_ids = request.data.get('children',None)
        for child_id in children_ids:
            child = api_models.User.objects.get(id=child_id)
            child_role = api_models.Role.objects.get(id=child.role)
            if child_role.name != 'STUDENT':
                return False
        return True

class CanCreateHomework(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            user_id = request.user_object.id
            class_id = request.data.get('class_id',None)
            lesson_id = request.data.get('lesson_id',None)
            return api_models.Section.objects.filter(class_id = class_id, selected_lesson = lesson_id, teacher_id = user_id).exists()
        return True

class IsHomeworkResponseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student_id.id == request.user_object.id

class IsHomeworkOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user_object.id
        return api_models.Section.objects.filter(class_id = obj.class_id.id, selected_lesson = obj.lesson_id.id, teacher_id = user_id).exists()

class IsQuizeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.teacher_id.id == request.user_object.id
        
# class hasThisQuize(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.student.id == request.user_object.id

class IsClassMeetingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.teacher_id == request.user_object.id

class IsNoteOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.teacher_id.id == request.user_object.id

class HasAnySectionInClass(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user_object.id
        class_id = view.kwargs['class_id']
        return api_models.Section.objects.filter(class_id = class_id, teacher_id = user_id).exists()

class CanCreateExamMeeting(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if 'MANAGER' in request.user_object.base_roles or 'ADMIN' in request.user_object.base_roles:
                return True
            user_id = request.user_object.id
            exam_id = request.data.get('exam',None)
            exam = api_models.NewExam.objects.get(id=exam_id)
            class_id = exam.class_id.id
            lesson_id = exam.lesson_id.id
            return api_models.Section.objects.filter(class_id = class_id, selected_lesson = lesson_id, teacher_id = user_id).exists()
        return True

class hasThisQuizeInMeeting(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user_object.id
        meeting = view.kwargs['meeting']
        quiz_id = view.kwargs['quiz']
        quiz = api_models.Quizzes.objects.get(id=quiz_id)
        if quiz.quiz_type == api_models.Quizzes.QUIZ:
            return api_models.QuizScore.objects.filter(quiz=quiz_id, class_meeting=meeting, student=user_id).exists()
        else:
            return api_models.NewExamScore.objects.filter(quiz=quiz_id, exam_meeting=meeting, student=user_id).exists()

class HasChildInClass(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user_object.id
        children = api_models.ParentChild.objects.filter(parent=user_id).values_list('child',flat=True)
        class_id = view.kwargs['class_id']
        return api_models.ClassroomStudents.objects.filter(classroom = class_id, students__in = children).exists()

class IsClassMember(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user_object.id
        class_id = view.kwargs['class_id']
        return api_models.ClassroomStudents.objects.filter(classroom = class_id, students = user_id).exists()
    
class IsTeacherAvailabilityOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.teacher_id.id == request.user_object.id
