# -------------------   Django imports ------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils.dateparse import parse_datetime, parse_date

from django.conf import settings
# -------------------   DRF imports ------------------------
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
# -------------------   API app imports ------------------------
import api.models as api_models 
import api.serializers as api_serializers
import api.permissions as api_permissions
import api.APIViews as api_APIViews
# -------------------   Other imports ------------------------
from datetime import datetime, date, timedelta
import json
import random
import string
import requests
import copy

##################################################################################
#                                     Deploy Test                                #
##################################################################################

def time(request):
    return JsonResponse({"utcnow": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S:%f')}, status=status.HTTP_200_OK)
    # resp = HttpResponse()
    # resp["Access-Control-Allow-Origin"] = "*"
    # resp["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # resp["Access-Control-Max-Age"] = "1000"
    # resp["Access-Control-Allow-Headers"] = "*"
    # if request.method == 'OPTIONS':
    #     return resp
    # else:
    #     resp.write('{\'utcnow\':\'%s\'}' % datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S:%f'))
    #     return resp


##################################################################################
#                            Classsheet all features                             #
##################################################################################

class StudentClassSheetList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsStudent, api_permissions.IsClassMember, )

    def get_queryset(self):
        user_id = self.request.user_object.id
        queryset = api_models.User.objects.filter(id = user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        # context = dict(target_list = 'score', class_id = class_id)
        context = dict(target_list = 'all', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)


class TeacherClassSheetList(generics.ListAPIView):
    
    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def get_serializer_class(self):
        method = self.request.method.lower()
        if method == 'post':
            return api_serializers.QuizScoreSerializers
        return api_serializers.ClassSheetSerializer

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.user_object.id
        class_id = self.kwargs['class_id']
        # context = dict(target_list = 'score', class_id = class_id, teacher_id = user_id)
        context = dict(target_list = 'all', class_id = class_id, teacher_id = user_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class ManagerClassSheetList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        # context = dict(target_list = 'score', class_id = class_id)
        context = dict(target_list = 'all', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

##################################################################################
#                                     Quiz                                       #
##################################################################################

class TeacherQuizList(generics.ListCreateAPIView):

    queryset = api_models.Quizzes.objects.all()
    serializer_class = api_serializers.QuizSerializer
    permission_classes = (api_permissions.IsTeacher, )

    def filter_queryset(self,queryset):
        user_id = self.request.user_object.id
        queryset = self.queryset.filter(teacher_id=user_id)
        if 'quiz_type' in self.request.query_params:
            qt = self.request.query_params['quiz_type']
            if qt == api_models.Quizzes.EXAM:
                queryset = queryset.filter(quiz_type=api_models.Quizzes.EXAM)
            else:
                queryset = queryset.filter(quiz_type=api_models.Quizzes.QUIZ)
        return queryset

    def post(self, request, *args, **kwargs):
        request.data['teacher_id'] = request.user_object.id
        return super().post(request, *args, **kwargs)

class TeacherQuizDetail(generics.RetrieveUpdateAPIView, api_APIViews.DestroyAPIView):

    http_method_names = ('delete' , 'put', 'get', )
    queryset = api_models.Quizzes.objects.all()
    serializer_class = api_serializers.QuizSerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsQuizeOwner,)

    def put(self, request, *args, **kwargs):
        request.data['teacher_id'] = request.user_object.id
        return super().put(request, *args, **kwargs)


class StudentQuizDetail(generics.RetrieveAPIView):

    http_method_names = ('get')
    # queryset = api_models.QuizScore.objects.all()
    serializer_class = api_serializers.QuizSerializer
    permission_classes = (api_permissions.IsStudent,)

    def get_object(self):
        lookup_url_kwargs = ['meeting', 'quiz']
        for lookup_url_kwarg in lookup_url_kwargs:
            assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )
        quiz_id = self.kwargs['quiz']
        meeting_id = self.kwargs['meeting']
        quiz = api_models.Quizzes.objects.get(id=quiz_id)
        user_id = self.request.user_object.id
        if quiz.quiz_type == api_models.Quizzes.QUIZ:
            quiz_scores = api_models.QuizScore.objects.filter(quiz=quiz_id, class_meeting=meeting_id, student= user_id, score=None)
        else:
            quiz_scores = api_models.NewExamScore.objects.filter(quiz=quiz_id, exam_meeting=meeting_id, student= user_id, score=None)
        if len(quiz_scores) == 0:
            return Response({'msg': _('Could not find a score record for this quiz')}, status=status.HTTP_404_NOT_FOUND)
        if len(quiz_scores)>1:
            quiz_scores = sorted(quiz_scores, key=lambda x:x.created_at, reverse=True)
        quiz_score = quiz_scores[0]

        # if quiz.quiz_type == api_models.Quizzes.QUIZ:
        #     queryset = api_models.QuizScore.objects.all()
        #     filter_kwargs = {'class_meeting': meeting_id, 'quiz': quiz_id}
        # else:
        #     queryset = api_models.NewExamScore.objects.all()
        #     filter_kwargs = {'exam_meeting': meeting_id, 'quiz': quiz_id}
        # # queryset = self.filter_queryset(self.get_queryset())
        # # filter_kwargs = self.kwargs
        # obj = get_object_or_404(queryset, **filter_kwargs, student = self.request.user_object.id)
        self.check_object_permissions(self.request, quiz_score)
        return quiz
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        quiz_text = json.loads(instance.quiz_text)
        for index, question in enumerate(quiz_text):
            question.pop('true', None)
            quiz_text[index] = question
        instance.quiz_text = quiz_text
        serializer = self.get_serializer(instance)
        res = serializer.data
        res['quiz_text'] = json.dumps(instance.quiz_text)
        return Response(res)

##################################################################################
#                                     QuizScore                                  #
##################################################################################


class TeacherCreateQuizeStudentsList(generics.CreateAPIView):

    permission_classes = (api_permissions.IsTeacher, api_permissions.IsClassMeetingOwner, )
    # serializer_class = api_serializers.BriefUserSerializer
    # queryset = api_models.ClassMeeting.objects.all()
    # lookup_field = 'id'
    # lookup_url_kwarg = 'class_meeting'

    def get_quiz_object(self):
        queryset = api_models.Quizzes.objects.all()
        lookup_url_kwarg = 'quiz'
        permission = api_permissions.IsQuizeOwner()
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'id': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        if not permission.has_object_permission(self.request, self, obj):
            self.permission_denied(
                self.request, message=getattr(permission, 'message', None)
            )
        return obj

    def create(self, request, *args, **kwargs):
        quiz = self.get_quiz_object()
        if quiz.quiz_type == api_models.Quizzes.QUIZ:
            class_meeting_id = self.kwargs['meeting']
            class_meeting = api_models.ClassMeeting.objects.get(id=class_meeting_id)
            # class_meeting_students_id = class_meeting.students.values_list('id', flat=True)
            # class_meeting_students_ids = api_models.ClassMeetingStudents.objects.filter(class_meeting=class_meeting.id).values_list('students', flat=True)
            class_id = class_meeting.class_id.id
            class_meeting_students_ids = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students', flat=True)
            # quiz.students.add(*class_meeting_students_id, through_defaults=dict(class_meeting=class_meeting))
            for class_meeting_students_id in class_meeting_students_ids:
                student = api_models.User.objects.get(id=class_meeting_students_id)
                quiz_score = api_models.QuizScore()
                quiz_score.class_meeting = class_meeting
                quiz_score.quiz = quiz
                quiz_score.student = student
                quiz_score.save()
        else: # api_models.Quizzes.EXAM
            exam_meeting_id = self.kwargs['meeting']
            exam_meeting = api_models.NewExamMeeting.objects.get(id=exam_meeting_id)
            class_id = exam_meeting.exam.class_id.id
            exam_meeting_students_ids = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students', flat=True)
            # exam_meeting.students.add(*exam_meeting_students_id, through_defaults=dict(quiz=quiz))
            for exam_meeting_students_id in exam_meeting_students_ids:
                student = api_models.User.objects.get(id=exam_meeting_students_id)
                exam_score = api_models.NewExamScore()
                exam_score.exam_meeting = exam_meeting
                exam_score.quiz = quiz
                exam_score.student = student
                exam_score.save()
        return Response(status=status.HTTP_201_CREATED)


class StudentQuizScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsStudent, api_permissions.IsClassMember, )

    def get_queryset(self):
        user_id = self.request.user_object.id
        queryset = api_models.User.objects.filter(id = user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'score', class_id = class_id)
        # context = dict(target_list = 'all', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)


class StudentQuizScoreUpdate(generics.UpdateAPIView):

    permission_classes = (api_permissions.IsStudent, api_permissions.hasThisQuizeInMeeting, )

    def patch(self, request, *args, **kwargs):
        user_id = request.user_object.id
        meeting_id = kwargs['meeting']
        quiz_id = kwargs['quiz']
        quiz = api_models.Quizzes.objects.get(id=quiz_id)
        quiz_text = json.loads(quiz.quiz_text)
        question_count = len(quiz_text)
        grade_count = 0
        for question,resp in request.data.items():
            question_id = int(question)
            if question_id >= len(quiz_text):
                continue
            true_resp = quiz_text[question_id]['true']
            if resp == true_resp:
                grade_count += 1
        grade = 20.0*grade_count/float(question_count)
        if quiz.quiz_type == api_models.Quizzes.QUIZ:
            quiz_scores = api_models.QuizScore.objects.filter(quiz=quiz_id, class_meeting=meeting_id, student= user_id, score=None)
        else:
            quiz_scores = api_models.NewExamScore.objects.filter(quiz=quiz_id, exam_meeting=meeting_id, student= user_id, score=None)
        if len(quiz_scores) == 0:
            return Response({'msg': _('Could not find a record for this quiz')}, status=status.HTTP_404_NOT_FOUND)
        if len(quiz_scores)>1:
            quiz_scores = sorted(quiz_scores, key=lambda x:x.created_at, reverse=True)
        quiz_score = quiz_scores[0]
        quiz_score.score = grade
        quiz_score.submitted_choices = json.dumps(request.data)
        quiz_score.score_text = '%d / %d' % (grade_count, question_count)
        quiz_score.save()
        return Response({'msg': _('Score submitted successfully %.2f' % grade)}, status=status.HTTP_200_OK)


class TeacherQuizScoreList(generics.ListAPIView):

    
    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def get_serializer_class(self):
        method = self.request.method.lower()
        if method == 'post':
            return api_serializers.QuizScoreSerializers
        return api_serializers.ClassSheetSerializer

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.user_object.id
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'score', class_id = class_id, teacher_id = user_id)
        # context = dict(target_list = 'all', class_id = class_id, teacher_id = user_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class ManagerQuizScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'score', class_id = class_id)
        # context = dict(target_list = 'all', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)


def AlternateManagerQuizScoreList(request,class_id):
    class_student_ids = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students', flat=True)
    res = []
    for student_id in class_student_ids:
        student = api_models.User.objects.get(id=student_id)
        student_res = {}
        student_res['student_id'] = student_id
        student_res['first_name'] = student.first_name
        student_res['last_name'] = student.last_name
        meeting_info = []
        meeting_ids = api_models.ClassMeetingStudents.objects.filter(students=student_id, class_meeting__class_id = class_id).values_list('class_meeting', flat=True)
        for meeting_id in meeting_ids:
            meeting_res = {}
            meeting = api_models.ClassMeeting.objects.get(id=meeting_id)
            meeting_res['date'] = meeting.date
            meeting_res['teacher_id'] = meeting.teacher_id
            meeting_res['lesson_name'] = meeting.lesson_name
            meeting_res['slot_order'] = meeting.section_id.section_order
            scores_set = api_models.QuizScore.objects.filter(student=student_id, class_meeting=meeting_id)
            if len(scores_set) == 0:
                meeting_res['target_list'] = []
            else:
                scores = list(scores_set.values_list('score', flat=True))
                meeting_res['target_list'] = scores
            meeting_info.append(meeting_res)
        student_res['meetings'] = meeting_info
        res.append(student_res)
    return JsonResponse(res, safe=False, status=status.HTTP_200_OK)


##################################################################################
#                                     Exam                                       #
##################################################################################


class ManagerExamList(generics.ListCreateAPIView):
    
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )
    queryset = api_models.NewExam.objects.all()
    serializer_class = api_serializers.ExamSerializer


class ManagerExamDetails(generics.RetrieveUpdateAPIView, api_APIViews.DestroyAPIView):

    http_method_names = ('delete' , 'put', 'get', )
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )
    queryset = api_models.NewExam.objects.all()
    serializer_class = api_serializers.ExamSerializer


class TeacherExamList(generics.ListAPIView):
    permission_classes = (api_permissions.IsTeacher, )
    queryset = api_models.NewExam.objects.all()
    serializer_class = api_serializers.ExamWithTokenSerializer

    def filter_queryset(self,queryset):
        user_id = self.request.user_object.id
        class_lesson_ids = api_models.Section.objects.filter(teacher_id = user_id).values_list('class_id', 'selected_lesson')
        class_ids, lesson_ids = set(), set()
        for class_id, lesson_id in class_lesson_ids:
            class_ids.add(class_id)
            lesson_ids.add(lesson_id)
        queryset = self.queryset.filter(class_id__in=class_ids, lesson_id__in=lesson_ids)
        return queryset


class ParentExamList(generics.ListAPIView):
    permission_classes = (api_permissions.IsParent, )
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.user_object.id
        children = api_models.ParentChild.objects.filter(parent=user_id).values_list('child',flat=True)
        res = []
        for child_id in children:
            child = api_models.User.objects.get(id=child_id)
            class_ids = api_models.ClassroomStudents.objects.filter(students = child).values_list('classroom')
            queryset = api_models.NewExam.objects.filter(class_id__in=class_ids)
            for exam in queryset:
                exam_res = {}
                exam_res['student_id'] = child_id
                exam_res['student_fullname'] = child.full_name
                exam_res['id'] = exam.id
                exam_res['class_id'] = exam.class_id.id
                exam_res['class_name'] = exam.class_id.name
                exam_res['lesson_id'] = exam.lesson_id.id
                exam_res['lesson_name'] = exam.lesson_id.name
                # exam_res['level'] = {'id': exam.class_id.level, 'title': settings.LEVEL_MAP.get(exam.class_id.level, None)}
                # exam_res['field'] = {'id': exam.class_id.field, 'title': settings.FIELD_MAP.get(exam.class_id.field, None)}
                # exam_res['degree'] = {'id': exam.class_id.degree, 'title': settings.DEGREE_MAP.get(exam.class_id.degree, None)}
                exam_res['level'] = exam.class_id.level
                exam_res['field'] = exam.class_id.field
                exam_res['degree'] = exam.class_id.degree
                exam_res['date'] = exam.date
                exam_res['time'] = exam.time
                exam_res['duration'] = exam.duration
                exam_res['class_type'] = exam.class_type
                exam_res['done'] = exam.done
                teacher_ids = api_models.Section.objects.filter(selected_lesson=exam.lesson_id.id,class_id=exam.class_id.id).values_list('teacher_id',flat=True)
                teacher_names = [user.full_name for user in api_models.User.objects.filter(id__in=teacher_ids)]
                exam_res['teacher_name'] = ', '.join(list(teacher_names))
                res.append(exam_res)
        return JsonResponse(res, safe=False, status=status.HTTP_200_OK)

class StudentExamList(generics.ListAPIView):
    permission_classes = (api_permissions.IsStudent, )
    queryset = api_models.NewExam.objects.all()
    serializer_class = api_serializers.ExamWithTokenSerializer

    def filter_queryset(self,queryset):
        user_id = self.request.user_object.id
        class_ids = api_models.ClassroomStudents.objects.filter(students = user_id).values_list('classroom')
        queryset = self.queryset.filter(class_id__in=class_ids)
        return queryset


class ExamMeetingEnd(generics.UpdateAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin|api_permissions.IsTeacher, api_permissions.CanCreateExamMeeting, )

    def put(self, request, *args, **kwargs):
        exam_meeting = api_models.NewExamMeeting.objects.get(id=self.kwargs['exam_meeting_id'])
        exam_meeting.done = True
        exam_meeting.save()
        exam = exam_meeting.exam
        exam.done = True
        exam.save()
        return Response({'msg': _('exam ended successfully')}, status=status.HTTP_200_OK)


def ExpandedExamMeetingList(exam_meeting, teacher):
    classroom = api_models.Classroom.objects.get(id=exam_meeting.exam.class_id.id)
    student_ids = api_models.ClassroomStudents.objects.filter(classroom=classroom.id).values_list('students',flat=True)
    res = {"totalCount": 1, "count": 1, "status": 200}
    body = {"id": exam_meeting.id, "date": exam_meeting.created_at, "degree": {"id": classroom.degree}, "level": {"id": classroom.level}, "field": {"id": classroom.field}}
    body["token"] = exam_meeting.token
    body["class_id"] = classroom.id
    body["class_name"] = classroom.name
    body["school_id"] = classroom.school_id
    body["lesson_name"] = exam_meeting.exam.lesson_id.name
    teacher_serializer = api_serializers.UserSerializer(teacher)
    teacher_json = teacher_serializer.data
    teacher_json["my_classes_id"] = list(set(api_models.Section.objects.filter(teacher_id=teacher.id).values_list('class_id',flat=True)))
    teacher_json["gender"] = {"id": teacher_json["gender"]}
    students_json = []
    for student_id in student_ids:
        student = api_models.User.objects.get(id=student_id)
        student_serializer = api_serializers.UserSerializer(student)
        student_json = student_serializer.data
        student_json["my_classes_id"] = list(set(api_models.ClassroomStudents.objects.filter(students=student_id).values_list('classroom',flat=True)))
        student_json["degree"] = {"id": student_json["degree"]}
        student_json["level"] = {"id": student_json["level"]}
        student_json["field"] = {"id": student_json["field"]}
        student_json["gender"] = {"id": student_json["gender"]}
        students_json.append(student_json)
    body["teacher"] = teacher_json
    body["students"] = students_json
    res["body"] = body
    return Response(res)


class ExamMeetingList(generics.ListCreateAPIView):
    
    # permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin|api_permissions.IsTeacher, api_permissions.CanCreateExamMeeting, )
    permission_classes = (api_permissions.IsTeacher, api_permissions.CanCreateExamMeeting, )
    queryset = api_models.NewExamMeeting.objects.all()
    serializer_class = api_serializers.ExamMeetingSerializer

    def generate_random_string(self, length):
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def post(self, request, *args, **kwargs):
        request.data['token'] = self.generate_random_string(20)
        resp = super().post(request, *args, **kwargs)
        exam_meeting = api_models.NewExamMeeting.objects.get(id=resp.data['id'])
        teacher = api_models.User.objects.get(id=self.request.user_object.id)
        return ExpandedExamMeetingList(exam_meeting, teacher)

    def filter_queryset(self,queryset):
        # if 'MANAGER' in self.request.user_object.base_roles or 'ADMIN' in self.request.user_object.base_roles:
        #     return self.queryset
        user_id = self.request.user_object.id
        class_lesson_ids = api_models.Section.objects.filter(teacher_id = user_id).values_list('class_id', 'selected_lesson')
        class_ids, lesson_ids = set(), set()
        for class_id, lesson_id in class_lesson_ids:
            class_ids.add(class_id)
            lesson_ids.add(lesson_id)
        exam_ids = api_models.NewExam.objects.filter(class_id__in=class_ids, lesson_id__in=lesson_ids).values_list('id',flat=True)
        queryset = self.queryset.filter(exam_id__in=exam_ids)
        return queryset

class TeacherExamMeetingByTokenList(generics.ListAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin|api_permissions.IsTeacher, )
    queryset = api_models.NewExamMeeting.objects.all()
    serializer_class = api_serializers.ExamMeetingSerializer

    def list(self, request, *args, **kwargs):
        token = self.kwargs['token']
        filter_params = dict(token=token)
        exam_meeting = get_object_or_404(self.queryset, **filter_params)
        teacher = api_models.User.objects.get(id=self.request.user_object.id)
        return ExpandedExamMeetingList(exam_meeting, teacher)


class StudentExamMeetingByTokenList(generics.ListAPIView):

    permission_classes = (api_permissions.IsStudent, )
    queryset = api_models.NewExamMeeting.objects.all()
    serializer_class = api_serializers.ExamMeetingSerializer

    def list(self, request, *args, **kwargs):
        token = self.kwargs['token']
        filter_params = dict(token=token)
        exam_meeting = get_object_or_404(self.queryset, **filter_params)
        classroom = api_models.Classroom.objects.get(id=exam_meeting.exam.class_id.id)
        teacher_ids = api_models.Section.objects.filter(selected_lesson=exam_meeting.exam.lesson_id.id, class_id=classroom.id).values_list('teacher_id',flat=True)
        teacher = api_models.User.objects.get(id=teacher_ids[0])
        return ExpandedExamMeetingList(exam_meeting, teacher)


class ParentExamScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ExamSheetSerializer
    permission_classes = (api_permissions.IsParent, api_permissions.HasChildInClass, )

    def get_queryset(self):
        user_id = self.request.user_object.id
        children = api_models.ParentChild.objects.filter(parent=user_id).values_list('child',flat=True)
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students',flat=True)
        student_ids = set(class_students_queryset).intersection(set(children))
        queryset = api_models.User.objects.filter(id__in = student_ids)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(class_id = class_id)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class StudentExamScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ExamSheetSerializer
    permission_classes = (api_permissions.IsStudent, api_permissions.IsClassMember, )

    def get_queryset(self):
        user_id = self.request.user_object.id
        queryset = api_models.User.objects.filter(id = user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(class_id = class_id)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class TeacherExamScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ExamSheetSerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.user_object.id
        class_id = self.kwargs['class_id']
        context = dict(class_id = class_id, teacher_id = user_id)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class ManagerExamScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ExamSheetSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(class_id = class_id)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)


##################################################################################
#                                     Presence                                   #
##################################################################################


class TeacherPresenceAbsenceClassMeetingList(generics.ListAPIView):

    serializer_class = api_serializers.PresenceAbsencePerMeetingSerializer
    queryset = api_models.PresenceAbsence.objects.all()
    permission_classes = (api_permissions.IsTeacher, )

    def get_queryset(self):
        class_meeting_id = self.kwargs['class_meeting_id']
        queryset = api_models.PresenceAbsence.objects.filter(class_meeting=class_meeting_id)
        return queryset

##################################################################################
#                                     Presence                                   #
##################################################################################

class TeacherCreatePresenceAbsenceSheet(generics.CreateAPIView):

    queryset = api_models.ClassMeeting.objects.all()
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsClassMeetingOwner, )
    serializer_class = api_serializers.BriefUserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'class_meeting_id'

    def create(self, request, *args, **kwargs):
        class_meeting = self.get_object()
        class_students = class_meeting.class_id.students
        class_student_ids = class_students.values_list('id', flat=True)
        class_meeting.students.set(class_student_ids, through_defaults=dict(status='A'))
        serializer = self.get_serializer(class_students, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TeacherSubmitEntrancePresence(generics.UpdateAPIView):

    http_method_names = ('patch', )
    queryset = api_models.ClassMeeting.objects.all()
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsClassMeetingOwner,)

    lookup_field = 'id'
    lookup_url_kwarg = 'class_meeting_id'

    def patch(self, request, *args, **kwargs):
        class_meeting = self.get_object()
        student_id = self.kwargs['student_id']
        filter_params = dict(class_meeting=class_meeting.id, student=student_id)
        presence_absence_queryset = api_models.PresenceAbsence.objects.all()
        presence_absence_student = get_object_or_404(presence_absence_queryset, **filter_params)
        if presence_absence_student.status == api_models.PresenceAbsence.ABSENT:
            presence_absence_student.status=api_models.PresenceAbsence.ENTRANCE
            presence_absence_student.save()
        return Response({'msg': _('enrance submitted successfully')}, status=status.HTTP_200_OK)


class TeacherSubmitVerifiedPresence(generics.UpdateAPIView):
    
    http_method_names = ('patch', )
    queryset = api_models.ClassMeeting.objects.all()
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsClassMeetingOwner,)

    lookup_field = 'id'
    lookup_url_kwarg = 'class_meeting_id'

    def patch(self, request, *args, **kwargs):
        class_meeting = self.get_object()
        student_id = self.kwargs['student_id']
        filter_params = dict(class_meeting=class_meeting.id, student=student_id)
        presence_absence_queryset = api_models.PresenceAbsence.objects.all()
        presence_absence_student = get_object_or_404(presence_absence_queryset, **filter_params)
        student_status = request.data.get('status','V')
        if student_status == 'V':
            presence_absence_student.status=api_models.PresenceAbsence.VERIFIED
        else: # 'U'
            presence_absence_student.status=api_models.PresenceAbsence.END_SET_ABSENT
        presence_absence_student.save()
        return Response({'msg': _('verification submitted successfully')}, status=status.HTTP_200_OK)


class TeacherSubmitVerifiedPresenceList(generics.UpdateAPIView):
    
    http_method_names = ('patch', )
    queryset = api_models.ClassMeeting.objects.all()
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsClassMeetingOwner,)

    lookup_field = 'id'
    lookup_url_kwarg = 'class_meeting_id'

    def patch(self, request, *args, **kwargs):
        class_meeting = self.get_object()
        presence_absence_queryset = api_models.PresenceAbsence.objects.all()
        for data in request.data:
            if 'student_id' not in data:
                continue
            student_id = data['student_id']
            filter_params = dict(class_meeting=class_meeting.id, student=student_id)
            if presence_absence_queryset.filter(class_meeting=class_meeting.id, student=student_id).exists():
                presence_absence_student = get_object_or_404(presence_absence_queryset, **filter_params)
                student_status = data.get('status','V')
                if student_status == 'V':
                    presence_absence_student.status=api_models.PresenceAbsence.VERIFIED
                else: # 'U'
                    presence_absence_student.status=api_models.PresenceAbsence.END_SET_ABSENT
                presence_absence_student.save()
        return Response({'msg': _('verification submitted successfully')}, status=status.HTTP_200_OK)



class StudentPresenceAbsenceList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsStudent, api_permissions.IsClassMember, )

    def get_queryset(self):
        user_id = self.request.user_object.id
        queryset = api_models.User.objects.filter(id = user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'presence', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class TeacherPresenceAbsenceList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.user_object.id
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'presence', class_id = class_id, teacher_id = user_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class ManagerPresenceAbsenceList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'presence', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)


##################################################################################
#                              Per Day Disciplinary                              #
##################################################################################


class TeacherSubmitDisciplinaryPerDay(generics.CreateAPIView):
    
    queryset = api_models.DisciplinaryPerDay.objects.all()
    serializer_class = api_serializers.DisciplinarySerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def post(self, request, *args, **kwargs):
        request.data['teacher_id'] = self.request.user_object.id
        request.data['class_id'] = self.kwargs['class_id']
        return super().post(request, *args, **kwargs)


class TeacherSubmitDisciplinaryPerDayDetails(generics.UpdateAPIView, api_APIViews.DestroyAPIView):
    
    queryset = api_models.DisciplinaryPerDay.objects.all()
    serializer_class = api_serializers.DisciplinarySerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsNoteOwner, )

    def put(self, request, *args, **kwargs):
        request.data['teacher_id'] = self.request.user_object.id
        request.data['class_id'] = self.kwargs['class_id']
        if 'has_disciplinary' not in request.data or not request.data['has_disciplinary']:
            request.data['disciplinary'] = ""
        return super().put(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        request.data['teacher_id'] = self.request.user_object.id
        request.data['class_id'] = self.kwargs['class_id']
        return super().destroy(request, *args, **kwargs)


##################################################################################
#                             Per Day Meeting Score                              #
##################################################################################


class TeacherSubmitMeetingScorePerDay(generics.CreateAPIView):
    
    queryset = api_models.MeetingScorePerDay.objects.all()
    serializer_class = api_serializers.MeetingScoreSerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def post(self, request, *args, **kwargs):
        request.data['teacher_id'] = self.request.user_object.id
        request.data['class_id'] = self.kwargs['class_id']
        if 'score' not in request.data or request.data['score'] == '':
            return JsonResponse({}, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().post(request, *args, **kwargs)


class TeacherSubmitMeetingScorePerDayDetails(generics.UpdateAPIView, api_APIViews.DestroyAPIView):
    
    queryset = api_models.MeetingScorePerDay.objects.all()
    serializer_class = api_serializers.MeetingScoreSerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsNoteOwner, )

    def put(self, request, *args, **kwargs):
        request.data['teacher_id'] = self.request.user_object.id
        request.data['class_id'] = self.kwargs['class_id']
        if 'score' not in request.data or request.data['score'] == '':
            return JsonResponse({}, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().put(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        request.data['teacher_id'] = self.request.user_object.id
        request.data['class_id'] = self.kwargs['class_id']
        return super().destroy(request, *args, **kwargs)


##################################################################################
#                               Per Day class sheet                              #
##################################################################################


def PerDayClassSheet(student_ids, alldates, meeting_scores, disciplinary_notes, quiz_scores, teacher_user=None):
    res = []
    for student_id in student_ids:
        student = api_models.User.objects.get(id=student_id)
        student_res = {}
        student_res['student_id'] = student_id
        student_res['first_name'] = student.first_name
        student_res['last_name'] = student.last_name
        student_meeting_scores = {}
        for ms in meeting_scores.filter(student_id=student_id):
            d = ms.date
            if teacher_user != None and ms.teacher_id.id != teacher_user:
                continue
            if d not in student_meeting_scores:
                student_meeting_scores[d] = []
            student_meeting_scores[d].append({'id': ms.id, 'lesson_id': ms.lesson_id.id, 'lesson': ms.lesson_id.name, 'teacher_name': ms.teacher_id.full_name, 'score': ms.score})
        student_disciplinary_notes = {}
        for dn in disciplinary_notes.filter(student_id=student_id):
            d = dn.date
            if teacher_user != None and dn.teacher_id.id != teacher_user:
                continue
            if d not in student_disciplinary_notes:
                student_disciplinary_notes[d] = []
            student_disciplinary_notes[d].append({'id': dn.id, 'lesson_id': dn.lesson_id.id, 'lesson': dn.lesson_id.name, 'teacher_name': dn.teacher_id.full_name, 'has_disciplinary': dn.has_disciplinary, 'disciplinary': dn.disciplinary})
        student_quiz_scores = {}
        for qs in quiz_scores.filter(student=student_id):
            d = qs.class_meeting.date.date()
            if teacher_user != None and qs.quiz.teacher_id.id != teacher_user:
                continue
            if d not in student_quiz_scores:
                student_quiz_scores[d] = []
            student_quiz_scores[d].append({'lesson_id': qs.quiz.lesson_id.id, 'lesson': qs.quiz.lesson_id.name, 'teacher_name': qs.quiz.teacher_id.full_name, 'quiz_title': qs.quiz.quiz_title, 'score': qs.score})
        # dates = set(student_meeting_scores.keys()).union(set(student_disciplinary_notes.keys())).union(set(student_quiz_scores.keys()))
        date_info = {}
        # for d in dates:
        for d in alldates:
            date_res = {}
            date_res['meeting_scores'] = student_meeting_scores.get(d,[])
            date_res['disciplinary_notes'] = student_disciplinary_notes.get(d,[])
            date_res['quiz_scores'] = student_quiz_scores.get(d,[])
            date_info[d.strftime('%Y-%m-%d')] = date_res
        student_res['meetings'] = date_info
        res.append(student_res)
    return JsonResponse(res, safe=False, status=status.HTTP_200_OK)


class ParentPerDayClassSheetList(generics.ListAPIView):

    permission_classes = (api_permissions.IsParent, api_permissions.HasChildInClass, )

    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        meeting_scores = api_models.MeetingScorePerDay.objects.filter(class_id=class_id)
        disciplinary_notes = api_models.DisciplinaryPerDay.objects.filter(class_id=class_id)
        quiz_scores = api_models.QuizScore.objects.filter(class_meeting__class_id=class_id)
        user_id = request.user_object.id
        children = api_models.ParentChild.objects.filter(parent=user_id).values_list('child',flat=True)
        student_ids = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students',flat=True)
        student_ids = set(student_ids).intersection(set(children))
        alldates = set([cm.date.date() for cm in api_models.ClassMeeting.objects.filter(class_id=class_id)])
        return PerDayClassSheet(student_ids, alldates, meeting_scores, disciplinary_notes, quiz_scores)


class StudentPerDayClassSheetList(generics.ListAPIView):

    permission_classes = (api_permissions.IsStudent, api_permissions.IsClassMember, )

    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        meeting_scores = api_models.MeetingScorePerDay.objects.filter(class_id=class_id)
        # meeting_scores_student_ids = set(meeting_scores.values_list('student_id',flat=True))
        disciplinary_notes = api_models.DisciplinaryPerDay.objects.filter(class_id=class_id)
        # disciplinary_notes_student_ids = set(disciplinary_notes.values_list('student_id',flat=True))
        quiz_scores = api_models.QuizScore.objects.filter(class_meeting__class_id=class_id)
        # quiz_scores_student_ids = set(quiz_scores.values_list('student_id',flat=True))
        # student_ids = meeting_scores_student_ids.union(disciplinary_notes_student_ids).union(quiz_scores_student_ids)
        student_ids = [self.request.user_object.id]
        alldates = set([cm.date.date() for cm in api_models.ClassMeeting.objects.filter(class_id=class_id)])
        return PerDayClassSheet(student_ids, alldates, meeting_scores, disciplinary_notes, quiz_scores)


class TeacherPerDayClassSheetList(generics.ListAPIView):

    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        teacher_id = self.request.user_object.id
        meeting_scores = api_models.MeetingScorePerDay.objects.filter(teacher_id=teacher_id, class_id=class_id)
        # meeting_scores_student_ids = set(meeting_scores.values_list('student_id',flat=True))
        disciplinary_notes = api_models.DisciplinaryPerDay.objects.filter(teacher_id=teacher_id, class_id=class_id)
        # disciplinary_notes_student_ids = set(disciplinary_notes.values_list('student_id',flat=True))
        quiz_scores = api_models.QuizScore.objects.filter(quiz__teacher_id=teacher_id, class_meeting__class_id=class_id)
        # quiz_scores_student_ids = set(quiz_scores.values_list('student_id',flat=True))
        # student_ids = meeting_scores_student_ids.union(disciplinary_notes_student_ids).union(quiz_scores_student_ids)
        student_ids = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students',flat=True)
        alldates = set([cm.date.date() for cm in api_models.ClassMeeting.objects.filter(teacher_id=teacher_id, class_id=class_id)])
        return PerDayClassSheet(student_ids, alldates, meeting_scores, disciplinary_notes, quiz_scores, teacher_id)
        

class ManagerPerDayClassSheetList(generics.ListAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        meeting_scores = api_models.MeetingScorePerDay.objects.filter(class_id=class_id)
        # meeting_scores_student_ids = set(meeting_scores.values_list('student_id',flat=True))
        disciplinary_notes = api_models.DisciplinaryPerDay.objects.filter(class_id=class_id)
        # disciplinary_notes_student_ids = set(disciplinary_notes.values_list('student_id',flat=True))
        quiz_scores = api_models.QuizScore.objects.filter(class_meeting__class_id=class_id)
        # quiz_scores_student_ids = set(quiz_scores.values_list('student_id',flat=True))
        # student_ids = meeting_scores_student_ids.union(disciplinary_notes_student_ids).union(quiz_scores_student_ids)
        student_ids = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students',flat=True)
        alldates = set([cm.date.date() for cm in api_models.ClassMeeting.objects.filter(class_id=class_id)])
        return PerDayClassSheet(student_ids, alldates, meeting_scores, disciplinary_notes, quiz_scores)


##################################################################################
#                          Per Day Presence Absence                              #
##################################################################################


def SummarizePresenceAbsence(date_statuses):
    date_statuses.sort(key=lambda x:x[0],reverse=True)
    if date_statuses[0][1] == api_models.PresenceAbsence.VERIFIED:
        return api_models.PresenceAbsence.VERIFIED
    if date_statuses[0][1] == api_models.PresenceAbsence.END_SET_ABSENT:
        return api_models.PresenceAbsence.END_SET_ABSENT
    for temp_status in date_statuses:
        if temp_status[1] == api_models.PresenceAbsence.ENTRANCE:
            return api_models.PresenceAbsence.ENTRANCE
    return api_models.PresenceAbsence.ABSENT

def PerDayPresenceAbsence(class_id, student_ids, alldates, teacher_user=None):
    res = []
    for student_id in student_ids:
        student = api_models.User.objects.get(id=student_id)
        student_res = {}
        student_res['id'] = student_id
        student_res['first_name'] = student.first_name
        student_res['last_name'] = student.last_name
        presence_absences = api_models.PresenceAbsence.objects.filter(student=student_id, class_meeting__class_id=class_id)
        per_day_presence_absences = {}
        all_teachers = set([])
        for pa in presence_absences:
            dt = pa.class_meeting.date
            d  = dt.date()
            slot = pa.class_meeting.section_id.section_order
            pa_status = pa.status
            if teacher_user != None and teacher_user != pa.class_meeting.teacher_id:
                continue
            if d not in per_day_presence_absences:
                per_day_presence_absences[d] = {}
            if slot not in per_day_presence_absences[d]:
                per_day_presence_absences[d][slot] = []
            per_day_presence_absences[d][slot].append((dt,pa_status,pa.class_meeting.lesson_name,pa.class_meeting.teacher_id,pa.class_meeting.id))
        for d in per_day_presence_absences:
            for slot in per_day_presence_absences[d]:
                (dt,pa_status,lesson_name,teacher_id,class_meeting_id) = per_day_presence_absences[d][slot][0]
                new_pa_status = SummarizePresenceAbsence(per_day_presence_absences[d][slot])
                per_day_presence_absences[d][slot] = (new_pa_status, lesson_name, teacher_id, class_meeting_id)
                all_teachers.add(teacher_id)
        teacher2name = {}
        for teacher_id in all_teachers:
            teacher = api_models.User.objects.get(id=teacher_id)
            teacher2name[teacher_id] = teacher.full_name
        date_info = []
        # for d in dates:
        for d in alldates:
            if d in per_day_presence_absences:
                for slot in per_day_presence_absences[d]:
                    (pa_status, lesson_name, teacher_id, class_meeting_id) = per_day_presence_absences[d][slot]
                    slot_data = {}
                    slot_data['id'] = class_meeting_id
                    slot_data['teacher_id'] = teacher_id
                    slot_data['teacher_name'] = teacher2name[teacher_id]
                    slot_data['lesson_name'] = lesson_name
                    slot_data['slot_order'] = slot+1
                    slot_data['target_list'] = [{'status':pa_status}]
                    cur_data = {}
                    cur_data['date'] = d.strftime('%Y-%m-%d')
                    cur_data['slots'] = slot_data
                    date_info.append(cur_data)
        student_res['meetings'] = date_info
        res.append(student_res)
    return JsonResponse(res, safe=False, status=status.HTTP_200_OK)


class ParentPerDayPresenceAbsenceList(generics.ListAPIView):

    permission_classes = (api_permissions.IsParent, api_permissions.HasChildInClass, )

    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        classroom = api_models.Classroom.objects.get(id=class_id)
        user_id = request.user_object.id
        children = api_models.ParentChild.objects.filter(parent=user_id).values_list('child',flat=True)
        student_ids = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students',flat=True)
        student_ids = set(student_ids).intersection(set(children))
        alldates = set([cm.date.date() for cm in api_models.ClassMeeting.objects.filter(class_id=class_id)])
        return PerDayPresenceAbsence(classroom, student_ids, alldates)


class StudentPerDayPresenceAbsenceList(generics.ListAPIView):

    permission_classes = (api_permissions.IsStudent, api_permissions.IsClassMember, )

    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        classroom = api_models.Classroom.objects.get(id=class_id)
        student_ids = [self.request.user_object.id]
        alldates = set([cm.date.date() for cm in api_models.ClassMeeting.objects.filter(class_id=class_id)])
        return PerDayPresenceAbsence(classroom, student_ids, alldates)


class TeacherPerDayPresenceAbsenceList(generics.ListAPIView):

    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        classroom = api_models.Classroom.objects.get(id=class_id)
        teacher_id = self.request.user_object.id
        student_ids = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students',flat=True)
        alldates = set([cm.date.date() for cm in api_models.ClassMeeting.objects.filter(teacher_id=teacher_id, class_id=class_id)])
        return PerDayPresenceAbsence(classroom, student_ids, alldates, teacher_id)
        

class ManagerPerDayPresenceAbsenceList(generics.ListAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        classroom = api_models.Classroom.objects.get(id=class_id)
        student_ids = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students',flat=True)
        alldates = set([cm.date.date() for cm in api_models.ClassMeeting.objects.filter(class_id=class_id)])
        return PerDayPresenceAbsence(classroom, student_ids, alldates)

##################################################################################
#                                 Meeting Score                                  #
##################################################################################


class TeacherSubmitMeetingScore(generics.UpdateAPIView):
    
    http_method_names = ('patch', )
    queryset = api_models.ClassMeeting.objects.all()
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsClassMeetingOwner,)

    lookup_field = 'id'
    lookup_url_kwarg = 'class_meeting_id'

    def patch(self, request, *args, **kwargs):
        class_meeting = self.get_object()
        student_id = self.kwargs['student_id']
        filter_params = dict(class_meeting=class_meeting.id, student=student_id)
        presence_absence_queryset = api_models.PresenceAbsence.objects.all()
        presence_absence_student = get_object_or_404(presence_absence_queryset, **filter_params)
        student_score = request.data['meeting_score']
        presence_absence_student.meeting_score = student_score
        presence_absence_student.save()
        return Response({'msg': _('meeting score submitted successfully')}, status=status.HTTP_200_OK)


class StudentMeetingScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsStudent, api_permissions.IsClassMember, )

    def get_queryset(self):
        user_id = self.request.user_object.id
        queryset = api_models.User.objects.filter(id = user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'meeting_score', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class TeacherMeetingScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.user_object.id
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'meeting_score', class_id = class_id, teacher_id = user_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class ManagerMeetingScoreList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'meeting_score', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)


##################################################################################
#                              Disciplinary Note                                 #
##################################################################################


class TeacherSubmitDisciplinaryNote(generics.UpdateAPIView):
    
    http_method_names = ('patch', )
    queryset = api_models.ClassMeeting.objects.all()
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsClassMeetingOwner,)

    lookup_field = 'id'
    lookup_url_kwarg = 'class_meeting_id'

    def patch(self, request, *args, **kwargs):
        class_meeting = self.get_object()
        student_id = self.kwargs['student_id']
        filter_params = dict(class_meeting=class_meeting.id, student=student_id)
        presence_absence_queryset = api_models.PresenceAbsence.objects.all()
        presence_absence_student = get_object_or_404(presence_absence_queryset, **filter_params)
        has_disciplinary = request.data.get('has_disciplinary',False)
        if has_disciplinary:
            student_note = request.data.get('disciplinary',"")
            presence_absence_student.disciplinary = student_note
            presence_absence_student.has_disciplinary = True
        else:
            presence_absence_student.disciplinary = ""
            presence_absence_student.has_disciplinary = False
        presence_absence_student.save()
        return Response({'msg': _('disciplinary note submitted successfully')}, status=status.HTTP_200_OK)


class StudentDisciplinaryNoteList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsStudent, api_permissions.IsClassMember, )

    def get_queryset(self):
        user_id = self.request.user_object.id
        queryset = api_models.User.objects.filter(id = user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'disciplinary', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class TeacherDisciplinaryNoteList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsTeacher, api_permissions.HasAnySectionInClass, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.user_object.id
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'disciplinary', class_id = class_id, teacher_id = user_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)

class ManagerDisciplinaryNoteList(generics.ListAPIView):

    serializer_class = api_serializers.ClassSheetSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        class_students_queryset = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students')
        queryset = api_models.User.objects.filter(id__in = class_students_queryset)
        return queryset
    
    def list(self, request, *args, **kwargs):
        class_id = self.kwargs['class_id']
        context = dict(target_list = 'disciplinary', class_id = class_id)
        from_date = parse_datetime(self.request.query_params.get('from_date', ''))
        to_date = parse_datetime(self.request.query_params.get('to_date', ''))
        if from_date:
            context['from_date'] = from_date
        if to_date:  
            context['to_date'] = to_date
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context = context)
        return Response(serializer.data)


##################################################################################
#                                     Homework                                   #
##################################################################################


class TeacherHomeworkList(generics.ListCreateAPIView):
    
    permission_classes = (api_permissions.IsTeacher, api_permissions.CanCreateHomework, )
    queryset = api_models.NewHomework.objects.all()
    serializer_class = api_serializers.HomeworkSerializer

    def filter_queryset(self,queryset):
        user_id = self.request.user_object.id
        class_lesson_ids = api_models.Section.objects.filter(teacher_id = user_id).values_list('class_id', 'selected_lesson')
        class_ids, lesson_ids = set(), set()
        for class_id, lesson_id in class_lesson_ids:
            class_ids.add(class_id)
            lesson_ids.add(lesson_id)
        queryset = self.queryset.filter(class_id__in=class_ids, lesson_id__in=lesson_ids)
        return queryset
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        homework_id = response.data['id']
        class_id = response.data['class_id']
        class_students_ids = api_models.ClassroomStudents.objects.filter(classroom = class_id).values_list('students', flat=True)
        self.queryset.get(id=homework_id).responses.set(class_students_ids)
        return response

class TeacherHomeworkDetails(generics.RetrieveUpdateAPIView, api_APIViews.DestroyAPIView):

    http_method_names = ('delete' , 'put', 'get', )
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsHomeworkOwner, )
    queryset = api_models.NewHomework.objects.all()
    serializer_class = api_serializers.HomeworkSerializer
    unallowed_update_fields = ('class_id', 'lesson_id', )
    def put(self, request, *args, **kwargs):
        for field in self.unallowed_update_fields:
            request.data.pop(field, None)
        return super().put(request, *args, **kwargs)


class StudentHomeworkResponseUpload(generics.UpdateAPIView):

    http_method_names = ('patch', )
    permission_classes = (api_permissions.IsStudent, api_permissions.IsHomeworkResponseOwner, )
    queryset = api_models.NewHomeworkResponse.objects.all()
    serializer_class = api_serializers.HomeworkResponseSerializer

    def patch(self, request, *args, **kwargs):
        file_name = request.data.get('file', None)
        request.data.clear()
        request.data['file'] = file_name
        request.data['submitdate'] = datetime.now()
        request.data['done'] = True
        return super().patch(request, *args, **kwargs)

class StudentHomeworkResponseList(generics.ListAPIView):

    permission_classes = (api_permissions.IsStudent, )
    queryset = api_models.NewHomeworkResponse.objects.all()
    serializer_class = api_serializers.HomeworkResponseSerializer

    def filter_queryset(self,queryset):
        user_id = self.request.user_object.id
        class_id = self.kwargs['class_id']
        class_homeworks = api_models.NewHomework.objects.filter(class_id = class_id).values_list('id', flat=True)
        queryset = self.queryset.filter(student_id = user_id, homework_id__in=class_homeworks)
        return queryset


class TeacherHomeworkResponseList(generics.ListAPIView):

    permission_classes = (api_permissions.IsTeacher, )
    queryset = api_models.NewHomeworkResponse.objects.all()
    serializer_class = api_serializers.HomeworkResponseSerializer

    def filter_queryset(self,queryset):
        user_id = self.request.user_object.id
        class_id = self.kwargs['class_id']
        lesson_ids = api_models.Section.objects.filter(class_id = class_id, teacher_id = user_id).values_list('selected_lesson', flat=True).distinct()
        class_homeworks = api_models.NewHomework.objects.filter(class_id = class_id, lesson_id__in=lesson_ids).values_list('id', flat=True)
        queryset = self.queryset.filter(homework_id__in=class_homeworks)
        return queryset

class ManagerHomeworkResponseList(generics.ListAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )
    queryset = api_models.NewHomeworkResponse.objects.all()
    serializer_class = api_serializers.HomeworkResponseSerializerWithoudFile

    def filter_queryset(self,queryset):
        class_id = self.kwargs['class_id']
        class_homeworks = api_models.NewHomework.objects.filter(class_id = class_id).values_list('id', flat=True)
        queryset = self.queryset.filter(homework_id__in=class_homeworks)
        return queryset


##################################################################################
#                              Teacher Availability                              #
##################################################################################


class ManagerTeacherAvailabilityList(generics.ListCreateAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )
    queryset = api_models.TeacherAvailability.objects.all()
    serializer_class = api_serializers.TeacherAvailabilitySerializer

    def filter_queryset(self,queryset):
        teacher_id = self.kwargs['teacher_id']
        queryset = self.queryset.filter(teacher_id = teacher_id)
        return queryset
    
    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            for data in request.data:
                data['teacher_id'] = self.kwargs['teacher_id']
        else:
            request.data['teacher_id'] = self.kwargs['teacher_id']
        return super().post(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        if isinstance(self.request.data, list):
            return super().get_serializer(*args, many=True, **kwargs)
        return super().get_serializer(*args, **kwargs)



class ManagerTeacherAvailabilityDetails(generics.UpdateAPIView, generics.DestroyAPIView):

    http_method_names = ('delete', 'patch', )
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )
    queryset = api_models.TeacherAvailability.objects.all()
    serializer_class = api_serializers.TeacherAvailabilitySerializer
    unallowed_update_fields = ('teacher_id', 'verified', )

    def patch(self, request, *args, **kwargs):
        for field in self.unallowed_update_fields:
            request.data.pop(field, None)
        return super().patch(request, *args, **kwargs)

class ManagerTeacherReservedSectionsList(generics.ListAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )
    queryset = api_models.Section.objects.all()
    serializer_class = api_serializers.TeacherReservedSectionsSerializer

    def filter_queryset(self,queryset):
        teacher_id = self.kwargs['teacher_id']
        queryset = self.queryset.filter(teacher_id = teacher_id)
        return queryset


class TeacherTeacherAvailabilityList(generics.ListAPIView):

    permission_classes = (api_permissions.IsTeacher, )
    queryset = api_models.TeacherAvailability.objects.all()
    serializer_class = api_serializers.TeacherAvailabilitySerializer

    def filter_queryset(self,queryset):
        user_id = self.request.user_object.id
        queryset = self.queryset.filter(teacher_id = user_id)
        return queryset


class TeacherTeacherAvailabilityToggleStatus(generics.UpdateAPIView):

    http_method_names = ('patch', )
    permission_classes = (api_permissions.IsTeacher, api_permissions.IsTeacherAvailabilityOwner, )
    queryset = api_models.TeacherAvailability.objects.all()
    serializer_class = api_serializers.TeacherAvailabilitySerializer

    def patch(self, request, *args, **kwargs):
        TeacherAvailability_section = self.get_object()
        TeacherAvailability_section.verified = not TeacherAvailability_section.verified
        TeacherAvailability_section.save()
        return Response({'msg': _('Status of availability section was updated successfully')}, status=status.HTTP_200_OK)


class TeacherTeacherReservedSectionsList(generics.ListAPIView):

    permission_classes = (api_permissions.IsTeacher, )
    queryset = api_models.Section.objects.all()
    serializer_class = api_serializers.TeacherReservedSectionsSerializer

    def filter_queryset(self,queryset):
        user_id = self.request.user_object.id
        queryset = self.queryset.filter(teacher_id = user_id)
        return queryset


##################################################################################
#                                  Teacher Lessons                               #
##################################################################################


class ManagerTeacherLessonsList(generics.ListCreateAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )
    queryset = api_models.TeacherLessons.objects.all()
    serializer_class = api_serializers.TeacherLessonsSerializer

    def filter_queryset(self, queryset):
        teacher_id = self.request.query_params.get('teacher_id')
        lesson_id = self.request.query_params.get('lesson_id')
        if teacher_id:
            queryset = self.queryset.filter(teacher_id = teacher_id)
        if lesson_id:
            queryset = self.queryset.filter(lesson_id = lesson_id)

        day_of_week = self.request.query_params.get('day_of_week')
        start_time = parse_datetime(self.request.query_params.get('start_time', ''))
        end_time = parse_datetime(self.request.query_params.get('end_time', ''))

        if start_time and end_time and day_of_week:
            available_teachers_queryset = api_models.TeacherAvailability.objects.all()
            have_section_teachers_queryset = api_models.Section.objects.all()
            available_teachers_ids = set(available_teachers_queryset.filter(day_of_week=day_of_week, start_time__lte = start_time, end_time__gte = end_time).values_list('teacher_id',flat=True).distinct())
            section_start_time_check = Q(start_time__gte = start_time) & Q(start_time__lt = end_time)
            query_start_time_check = Q(start_time__lte = start_time) & Q(end_time__gt = start_time)
            #end_time_check = Q(end_time__gt = start_time) & Q(end_time__lte = end_time)
            have_section_teachers_ids = set(have_section_teachers_queryset.filter(Q(day_of_week = day_of_week), Q(section_start_time_check | query_start_time_check)).values_list('teacher_id', flat=True).distinct())
            teachers = available_teachers_ids.difference(have_section_teachers_ids)
            queryset = self.queryset.filter(teacher_id__in=teachers)

        return queryset
    
    def get_serializer(self, *args, **kwargs):
        if isinstance(self.request.data, list):
            return super().get_serializer(*args, many=True, **kwargs)
        return super().get_serializer(*args, **kwargs)


class ManagerTeacherLessonsDelete(api_APIViews.DestroyAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )
    queryset = api_models.TeacherLessons.objects.all()
    serializer_class = api_serializers.TeacherLessonsSerializer


##################################################################################
#                               Schedule wrapped                                 #
##################################################################################

class ParentScheduleList(generics.ListAPIView):

    permission_classes = (api_permissions.IsParent, )

    def list(self, request, *args, **kwargs):
        resp = requests.get('%s/api/schedules' % settings.JAVA_BASE, verify=False, headers={'Authorization': request.headers['Authorization']})
        resp_json = resp.json()
        if resp.status_code == 200 and 'body' in resp_json:
            user_id = self.request.user_object.id
            children = api_models.ParentChild.objects.filter(parent=user_id).values_list('child',flat=True)
            body = resp_json['body']
            for i in range(len(body)):
                for j in range(len(body[i]['sections'])):
                    del(body[i]['sections'][j]['token'])
            resp_json['body'] = []
            resp_json['count'] = 0
            resp_json['totalCount'] = 0
            for child_id in children:
                child = api_models.User.objects.get(id=child_id)
                child_resp = {'id': child_id, 'full_name': child.full_name, 'degree': {'id': child.degree, 'title': settings.DEGREE_MAP.get(child.degree, None)}, 'level': {'id': child.level, 'title': settings.LEVEL_MAP.get(child.level, None)}, 'field': {'id': child.field, 'title': settings.FIELD_MAP.get(child.field, None)}}
                classroom_ids = api_models.ClassroomStudents.objects.filter(students=child_id).values_list('classroom',flat=True)
                for b in body:
                    if b['id'] in classroom_ids:
                        b_copy = copy.copy(b)
                        b_copy['student_info'] = child_resp
                        resp_json['body'].append(b_copy)
            resp_json['count'] = len(resp_json['body'])
            resp_json['totalCount'] = len(resp_json['body'])
        return JsonResponse(resp_json)


##################################################################################
#                                Classroom Views                                 #
##################################################################################

class ParentClassroomList(generics.ListAPIView):

    permission_classes = (api_permissions.IsParent, )

    def list(self, request, *args, **kwargs):
        resp = requests.get('%s/api/classrooms' % settings.JAVA_BASE, verify=False, headers={'Authorization': request.headers['Authorization']})
        resp_json = resp.json()
        if resp.status_code == 200 and 'body' in resp_json:
            user_id = self.request.user_object.id
            children = api_models.ParentChild.objects.filter(parent=user_id).values_list('child',flat=True)
            classroom_ids = api_models.ClassroomStudents.objects.filter(students__in=children).values_list('classroom',flat=True)
            for i in reversed(range(len(resp_json['body']))):
                if resp_json['body'][i]['id'] not in classroom_ids:
                    resp_json['body'].pop(i)
                    resp_json['count'] -= 1
                    resp_json['totalCount'] -= 1
        return JsonResponse(resp_json)

class StudentClassroomList(generics.ListAPIView):

    permission_classes = (api_permissions.IsStudent, )

    def list(self, request, *args, **kwargs):
        resp = requests.get('%s/api/classrooms' % settings.JAVA_BASE, verify=False, headers={'Authorization': request.headers['Authorization']})
        resp_json = resp.json()
        if resp.status_code == 200 and 'body' in resp_json:
            user_id = self.request.user_object.id
            classroom_ids = api_models.ClassroomStudents.objects.filter(students=user_id).values_list('classroom',flat=True)
            for i in reversed(range(len(resp_json['body']))):
                if resp_json['body'][i]['id'] not in classroom_ids:
                    resp_json['body'].pop(i)
                    resp_json['count'] -= 1
                    resp_json['totalCount'] -= 1
        return JsonResponse(resp_json)

class TeacherClassroomList(generics.ListAPIView):

    permission_classes = (api_permissions.IsTeacher, )

    def list(self, request, *args, **kwargs):
        resp = requests.get('%s/api/classrooms' % settings.JAVA_BASE, verify=False, headers={'Authorization': request.headers['Authorization']})
        resp_json = resp.json()
        if resp.status_code == 200 and 'body' in resp_json:
            user_id = self.request.user_object.id
            classroom_ids = api_models.Section.objects.filter(teacher_id=user_id).values_list('class_id',flat=True)
            for i in reversed(range(len(resp_json['body']))):
                if resp_json['body'][i]['id'] not in classroom_ids:
                    resp_json['body'].pop(i)
                    resp_json['count'] -= 1
                    resp_json['totalCount'] -= 1
        return JsonResponse(resp_json)

class ManagerClassroomList(generics.ListAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def list(self, request, *args, **kwargs):
        resp = requests.get('%s/api/classrooms' % settings.JAVA_BASE, verify=False, headers={'Authorization': request.headers['Authorization']})
        resp_json = resp.json()
        return JsonResponse(resp_json)


##################################################################################
#                        Teacher Lessons from section                            #
##################################################################################

class TeacherLessonsFromSection(generics.ListAPIView):

    serializer_class = api_serializers.LessonsFromSectionSerializer
    queryset = api_models.Lesson.objects.all()
    permission_classes = (api_permissions.IsTeacher, )

    def get_queryset(self):
        teacher_id = self.request.user_object.id
        if 'day_of_week' in self.request.query_params and 'class_id' in self.request.query_params:
            day_of_week = self.request.query_params['day_of_week']
            class_id = self.request.query_params['class_id']
            teacher_lessons = api_models.Section.objects.filter(teacher_id=teacher_id, day_of_week=day_of_week, class_id=class_id).values_list('selected_lesson',flat=True)
        else:
            teacher_lessons = api_models.Section.objects.filter(teacher_id=teacher_id).values_list('selected_lesson',flat=True)
        queryset = self.queryset.filter(id__in=teacher_lessons)
        return queryset


##################################################################################
#                               Parent Child views                               #
##################################################################################


class ManagerParentChildCreate(generics.CreateAPIView):

    queryset = api_models.ParentChild.objects.all()
    serializer_class = api_serializers.ParentChildSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, api_permissions.IsValidParentChildPair, )

    def create(self, request, *args, **kwargs):
        data = request.data
        parent_id = data['parent']
        new_data = []
        for child_id in data['children']:
            if api_models.ParentChild.objects.filter(parent=parent_id, child=child_id).exists():
                continue
            new_data.append({'parent': parent_id, 'child': child_id})
        serializer = self.get_serializer(data=new_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        data = request.data
        parent_id = data['parent']
        current_children = set(api_models.ParentChild.objects.filter(parent=parent_id).values_list('child', flat=True))
        new_children = set(data['children'])
        children_to_rem = current_children - new_children
        children_to_add = new_children - current_children
        for child_id in children_to_rem:
            pc = api_models.ParentChild.objects.get(parent=parent_id, child=child_id)
            pc.delete()
        new_data = []
        for child_id in children_to_add:
            new_data.append({'parent': parent_id, 'child': child_id})
        serializer = self.get_serializer(data=new_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        queryset = api_models.ParentChild.objects.filter(parent=parent_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ManagerParentChildList(generics.ListAPIView):

    queryset = api_models.ParentChild.objects.all()
    serializer_class = api_serializers.ParentChildSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def get_queryset(self):
        parent_id = self.kwargs['parent_id']
        queryset = self.queryset.filter(parent_id=parent_id)
        return queryset


# class ManagerParentChildDetail(api_APIViews.DestroyAPIView):

#     queryset = api_models.ParentChild.objects.all()
#     serializer_class = api_serializers.ParentChildSerializer
#     permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )


class ParentParentChildList(generics.ListAPIView):

    queryset = api_models.ParentChild.objects.all()
    serializer_class = api_serializers.ParentChildSerializer
    permission_classes = (api_permissions.IsParent, )

    def get_queryset(self):
        parent_id = self.request.user_object.id
        queryset = self.queryset.filter(parent_id=parent_id)
        return queryset


##################################################################################
#                               Parent Dashboards                                #
##################################################################################


class ParentDashboardsList(generics.ListAPIView):

    queryset = api_models.ClassroomStudents.objects.all()
    serializer_class = api_serializers.ParentDashboardsSerializer
    permission_classes = (api_permissions.IsParent, )

    def get_queryset(self):
        parent_id = self.request.user_object.id
        children = api_models.ParentChild.objects.filter(parent_id=parent_id).values_list('child_id',flat=True)
        queryset = self.queryset.filter(students__in=children)
        return queryset


##################################################################################
#                                  Lessons update                                #
##################################################################################


class ManagerLessonsUpdate(generics.UpdateAPIView):

    http_method_names = ('put', )
    queryset = api_models.Lesson.objects.all()
    serializer_class = api_serializers.LessonSerializer
    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def put(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data['lessons'], many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # for data in request.data['lessons']:
        #     lesson_id = data['id']
        #     state = data['state']
        #     lesson = api_models.Lesson.objects.get(id=lesson_id)
        #     lesson.state = state
        #     lesson.save()
        
        resp = requests.get('%s/api/lessons' % settings.JAVA_BASE, verify=False, headers={'Authorization': request.headers['Authorization']})
        resp_json = resp.json()
        return JsonResponse(resp_json)


##################################################################################
#                            Students Classmeetings                              #
##################################################################################


class StudentSchedulesList(generics.ListAPIView):

    permission_classes = (api_permissions.IsStudent, )

    def list(self, request, *args, **kwargs):
        resp = requests.get('%s/api/schedules/my' % settings.JAVA_BASE, verify=False, headers={'Authorization': request.headers['Authorization']})
        resp_json = resp.json()
        if resp.status_code == 200 and 'body' in resp_json:
            user_id = self.request.user_object.id
            classroom_ids = api_models.ClassroomStudents.objects.filter(students=user_id).values_list('classroom',flat=True)
            for i in reversed(range(len(resp_json['body']))):
                if resp_json['body'][i]['class_id'] not in classroom_ids:
                    resp_json['body'].pop(i)
                    resp_json['count'] -= 1
                    resp_json['totalCount'] -= 1
        return JsonResponse(resp_json)


##################################################################################
#                            Students Classmeetings                              #
##################################################################################

def get_usage():
    res = {'used': 0, 'total': 0}
    if api_models.DiskUsage.objects.all().exists():
        used = [sv.disk_usage for sv in api_models.SavedVideos.objects.all()]
        total = api_models.DiskUsage.objects.all()
        res['used'] = sum(used)
        res['total'] = total[0].max_disk_usage
    return res

class DiskUsageList(generics.ListCreateAPIView):
    
    http_method_names = ('post', 'get' )

    def list(self, request, *args, **kwargs):
        res = get_usage()
        return JsonResponse(res)
    
    def post(self, request, *args, **kwargs):
        if not api_models.DiskUsage.objects.all().exists():
            total = api_models.DiskUsage()
        else:
            total = api_models.DiskUsage.objects.all()
            total = total[0]
        total.max_disk_usage = request.data['max_disk_usage']
        total.save()
        res = get_usage()
        return JsonResponse(res)

class CanRecordVideo(generics.ListAPIView):
    
    http_method_names = ('get', )
    permission_classes = (api_permissions.IsTeacher, )

    def list(self, request, *args, **kwargs):
        res = get_usage()
        if res['used'] < res['total']:
            return JsonResponse({'can_record': True})
        return JsonResponse({'can_record': False})

class SavedVideosCreate(generics.ListCreateAPIView):
    
    http_method_names = ('post', )

    def post(self, request, *args, **kwargs):
        if not api_models.DiskUsage.objects.all().exists():
            return JsonResponse({'status': status.HTTP_403_FORBIDDEN})
        class_meeting = api_models.ClassMeeting.objects.get(id=request.data['class_meeting'])
        sv = api_models.SavedVideos()
        sv.location = request.data['location']
        sv.disk_usage = request.data['disk_usage']
        sv.class_meeting = class_meeting
        sv.save()
        return JsonResponse({'status': status.HTTP_200_OK})


def PerDayVideos(meeting_ids, is_admin=False):
    res = []
    for id in meeting_ids:
        try:
            if not api_models.SavedVideos.objects.filter(class_meeting=id).exists():
                continue
            videos = api_models.SavedVideos.objects.filter(class_meeting=id)
            meeting = api_models.ClassMeeting.objects.get(id=id)
            d = meeting.date.date()
            class_name = meeting.class_name
            lesson_name = meeting.lesson_name
            teacher_id = meeting.teacher_id
            teacher = api_models.User.objects.get(id=teacher_id)
            teacher_name = teacher.full_name
            for v in videos:
                v_res = {}
                v_res['date'] = d
                v_res['location'] = v.location
                v_res['disk_usage'] = v.disk_usage
                v_res['class_name'] = class_name
                v_res['lesson_name'] = lesson_name
                v_res['teacher_name'] = teacher_name
                res.append(v_res)
        except:
            continue
    fin_res = {}
    fin_res['videos'] = res
    if is_admin:
        fin_res['usage'] = get_usage()
    return JsonResponse(fin_res, safe=False, status=status.HTTP_200_OK)

class ParentPerDayVideosList(generics.ListAPIView):

    permission_classes = (api_permissions.IsParent, )

    def list(self, request, *args, **kwargs):
        user_id = request.user_object.id
        children = set(api_models.ParentChild.objects.filter(parent=user_id).values_list('child',flat=True))
        class_ids = set(api_models.ClassroomStudents.objects.filter(students__in=children).values_list('classroom',flat=True))
        meeting_ids = set(api_models.ClassMeeting.objects.filter(class_id__in=class_ids).values_list('id',flat=True))
        return PerDayVideos(meeting_ids)


class StudentPerDayVideosList(generics.ListAPIView):

    permission_classes = (api_permissions.IsStudent, )

    def list(self, request, *args, **kwargs):
        user_id = request.user_object.id
        class_ids = set(api_models.ClassroomStudents.objects.filter(students=user_id).values_list('classroom',flat=True))
        meeting_ids = set(api_models.ClassMeeting.objects.filter(class_id__in=class_ids).values_list('id',flat=True))
        return PerDayVideos(meeting_ids)


class TeacherPerDayVideosList(generics.ListAPIView):

    permission_classes = (api_permissions.IsTeacher, )

    def list(self, request, *args, **kwargs):
        user_id = request.user_object.id
        meeting_ids = set(api_models.ClassMeeting.objects.filter(teacher_id=user_id).values_list('id',flat=True))
        return PerDayVideos(meeting_ids)


class ManagerPerDayVideosList(generics.ListAPIView):

    permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    def list(self, request, *args, **kwargs):
        meeting_ids = set(api_models.ClassMeeting.objects.all().values_list('id',flat=True))
        return PerDayVideos(meeting_ids, is_admin=True)


# ##################################################################################
# #                                     Reports                                    #
# ##################################################################################

def ChartReportPerDayPresenceAbsence(from_date, to_date):
    res = {}
    all_pa = api_models.PresenceAbsence.objects.filter(class_meeting__date__gte=from_date, class_meeting__date__lte=to_date)
    for pa in all_pa:
        if pa.status != api_models.PresenceAbsence.VERIFIED:
            continue
        d = pa.class_meeting.date.date()
        students = res.get(d,set([]))
        students.add(pa.student)
        res[d] = students
    delta = to_date - from_date
    final_res = {'plot_type': 'column', 'title': 'آمار حضور و غیاب در مدرسه', 'dates': [], 'data': [{'name': 'حضور و غیاب', 'data': []}]}
    for i in range(delta.days + 1):
        day = from_date + timedelta(days=i)
        c = len(res.get(day,set([])))
        final_res['dates'].append(day.strftime('%Y-%m-%d'))
        final_res['data'][0]['data'].append(c)
    return final_res

class ManagerPresenceAbsenceReport(generics.ListAPIView):

    # permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    template_name = 'api/admin_school_presence-absence.html'

    def list(self, request, *args, **kwargs):
        from_date = parse_date(self.request.query_params['from_date'])
        to_date = parse_date(self.request.query_params['to_date'])
        report = ChartReportPerDayPresenceAbsence(from_date=from_date, to_date=to_date)
        return render(request, self.template_name, {'report': report})

def ChartReportPerDayPresenceAbsencePerClass(from_date, to_date, class_id):
    cur_class = api_models.Classroom.objects.get(id=class_id)
    res = {}
    section_orders = set([])
    all_pa = api_models.PresenceAbsence.objects.filter(class_meeting__date__gte=from_date, class_meeting__date__lte=to_date, class_meeting__class_id=class_id)
    for pa in all_pa:
        if pa.status != api_models.PresenceAbsence.VERIFIED:
            continue
        d = pa.class_meeting.date.date()
        s = pa.class_meeting.section_id.section_order
        section_orders.add(s)
        students = res.get((d,s),set([]))
        students.add(pa.student)
        res[(d,s)] = students
    section_orders = list(section_orders)
    section_orders.sort()
    delta = to_date - from_date

    final_res = {'plot_type': 'column', 'title': 'آمار حضور و غیاب، %s' % cur_class.name, 'dates': []}
    if len(section_orders): 
        final_res['data'] = [{'name': 'جلسه %d' % (s+1), 'data': []} for s in range(max(section_orders)+1)]
    else:
        final_res['data'] = []
    for i in range(delta.days + 1):
        day = from_date + timedelta(days=i)
        final_res['dates'].append(day.strftime('%Y-%m-%d'))
        for s in section_orders:
            c = len(res.get((day,s),set([])))
            final_res['data'][s]['data'].append(c)
    return final_res


class ManagerPresenceAbsencePerClassReport(generics.ListAPIView):

    # permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    template_name = 'api/admin_school_presence-absence.html'

    def list(self, request, *args, **kwargs):
        from_date = parse_date(self.request.query_params['from_date'])
        to_date = parse_date(self.request.query_params['to_date'])
        class_id = self.request.query_params['class_id']
        report = ChartReportPerDayPresenceAbsencePerClass(from_date=from_date, to_date=to_date, class_id=class_id)
        return render(request, self.template_name, {'report': report})


def ChartReportPerDayScorePerClass(from_date, to_date, class_id, lesson_id):
    cur_class = api_models.Classroom.objects.get(id=class_id)
    lesson = api_models.Lesson.objects.get(id=lesson_id)
    res = {}
    all_students = api_models.ClassroomStudents.objects.filter(classroom=class_id).values_list('students',flat=True)
    all_students = list(set(all_students))

    all_scores = api_models.MeetingScorePerDay.objects.filter(date__gte=from_date, date__lte=to_date, class_id=class_id, lesson_id=lesson_id)
    for score_object in all_scores:
        d = score_object.date
        s = score_object.score
        st = score_object.student_id.id
        scores = res.get((d,st),[])
        scores.append(s)
        res[(d,st)] = scores
    delta = to_date - from_date
    final_res = {'plot_type': 'line', 'title': 'نمرات درس %s درس کلاس %s' % (lesson.name, cur_class.name), 'dates': []}
    if len(all_students):
        final_res['data'] = []
        for student_id in all_students:
            user = api_models.User.objects.get(id=student_id)
            final_res['data'].append({'name': user.full_name, 'data': []})
    else:
        final_res['data'] = []
    for i in range(delta.days + 1):
        day = from_date + timedelta(days=i)
        final_res['dates'].append(day.strftime('%Y-%m-%d'))
        for i in range(len(all_students)):
            st = all_students[i]
            scores = res.get((day,st),[])
            if not len(scores):
                final_res['data'][i]['data'].append('null')
            else:
                score = sum(scores)/float(len(scores))
                final_res['data'][i]['data'].append(score)
    return final_res

class ManagerScorePerClassReport(generics.ListAPIView):

    # permission_classes = (api_permissions.IsManager|api_permissions.IsAdmin, )

    template_name = 'api/admin_school_score.html'

    def list(self, request, *args, **kwargs):
        from_date = parse_date(self.request.query_params['from_date'])
        to_date = parse_date(self.request.query_params['to_date'])
        class_id = self.request.query_params['class_id']
        lesson_id = self.request.query_params['lesson_id']
        report = ChartReportPerDayScorePerClass(from_date=from_date, to_date=to_date, class_id=class_id, lesson_id=lesson_id)
        return render(request, self.template_name, {'report': report})
