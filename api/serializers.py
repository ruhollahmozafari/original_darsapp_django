from rest_framework import serializers
from django.core import serializers as django_serializers
from django.db.models import BigIntegerField, Case, Value, When

from django.conf import settings

import api.models as api_models

##################################################################################
#                             user serializers                                   #
##################################################################################

class BriefUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.User
        fields = ('id', 'first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.User
        fields = '__all__'


##################################################################################
#                             Quize serializers                                  #
##################################################################################


class QuizSerializer(serializers.ModelSerializer):

    created_at_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = api_models.Quizzes
        fields = ['id', 'teacher_id', 'quiz_title', 'quiz_type', 'quiz_text', 'duration', 'lesson_id', 'created_at_timestamp']
    
    def get_created_at_timestamp(self, obj):
        return obj.created_at.timestamp()

class QuizScoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = api_models.QuizScore
        fields = ('id','quiz','student','class_meeting','score', )


##################################################################################
#                             Exam serializers                                   #
##################################################################################


class ExamSerializer(serializers.ModelSerializer):

    lesson_name = serializers.ReadOnlyField(source='lesson_id.name')
    class_name = serializers.ReadOnlyField(source='class_id.name')
    level = serializers.ReadOnlyField(source='class_id.level')
    field = serializers.ReadOnlyField(source='class_id.field')
    degree = serializers.ReadOnlyField(source='class_id.degree')
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = api_models.NewExam
        fields = ['id', 'class_id', 'class_name', 'lesson_id', 'lesson_name', 'level', 'field', 'degree', 'teacher_name', 'date', 'time', 'duration', 'class_type', 'done']
    
    def get_teacher_name(self,obj):
        teacher_ids = api_models.Section.objects.filter(selected_lesson=obj.lesson_id.id,class_id=obj.class_id.id).values_list('teacher_id',flat=True)
        teacher_names = [user.full_name for user in api_models.User.objects.filter(id__in=teacher_ids)]
        return ', '.join(list(teacher_names))

class ExamWithTokenSerializer(ExamSerializer):

    token = serializers.SerializerMethodField()

    class Meta(ExamSerializer.Meta):
        fields = ExamSerializer.Meta.fields + ['token', ]
    
    def get_token(self, obj):
        exam_meetings = api_models.NewExamMeeting.objects.filter(exam=obj, done=False)
        if len(exam_meetings) == 0:
            return None
        else:
            return exam_meetings[0].token

class ExamMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.NewExamMeeting
        fields = ['id','exam','token', 'done']


# class ExamMeetingStudentsSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = api_models.NewExamMeetingStudents
#         fields = ['id','exam_meeting','students']



##################################################################################
#                         Homework serializers                                   #
##################################################################################

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.NewHomework
        fields = ('id','class_id','lesson_id','description','file','deadline', )


class HomeworkResponseSerializerWithoudFile(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student_id.full_name')
    lesson_name = serializers.ReadOnlyField(source='homework_id.lesson_id.name')
    class_name = serializers.ReadOnlyField(source='homework_id.class_id.name')
    class Meta:
        model = api_models.NewHomeworkResponse
        fields = ('id', 'homework_id', 'student', 'done', 'submitdate', 'lesson_name', 'class_name', )

class HomeworkResponseSerializer(HomeworkResponseSerializerWithoudFile):
    class Meta(HomeworkResponseSerializerWithoudFile.Meta):
        fields = HomeworkResponseSerializerWithoudFile.Meta.fields + ('file', )

##################################################################################
#              general srializer for score and presence absence                  #
##################################################################################


class SlotsSerializer(serializers.ModelSerializer):

    slot_order = serializers.SerializerMethodField()
    target_list = serializers.SerializerMethodField()

    class Meta:
        model = api_models.ClassMeeting
        fields= ('id', 'teacher_id','lesson_name','slot_order', 'target_list',)

    def get_slot_order(self,obj):
        return obj.section_id.section_order
    
    def get_target_list(self,obj):
        student_id = self.context.get('student_id', None)
        if self.context['target_list'] == 'all':
            # target = [{('quiz%d (%s)' % (quiz_score.quiz.id, quiz_score.quiz.quiz_title)): quiz_score.score} for quiz_score in api_models.QuizScore.objects.filter(student=student_id, class_meeting=obj.id)]
            quiz_resp = [{quiz_score.quiz.quiz_title: quiz_score.score} for quiz_score in api_models.QuizScore.objects.filter(student=student_id, class_meeting=obj.id)]
            status_resp = list(api_models.PresenceAbsence.objects.filter(student=student_id, class_meeting=obj.id).values('status'))
            meeting_score_resp = list(api_models.PresenceAbsence.objects.filter(student=student_id, class_meeting=obj.id).values('meeting_score'))
            discip_resp = list(api_models.PresenceAbsence.objects.filter(student=student_id, class_meeting=obj.id).values('has_disciplinary','disciplinary'))
            target = {'quiz_scores': quiz_resp, 'status': status_resp, 'meeting_score': meeting_score_resp, 'discip': discip_resp}
        elif self.context['target_list'] == 'score':
            # target = api_models.QuizScore.objects.filter(student=student_id, class_meeting=obj.id).values('score')
            target = [{quiz_score.quiz.quiz_title: quiz_score.score} for quiz_score in api_models.QuizScore.objects.filter(student=student_id, class_meeting=obj.id)]
        elif self.context['target_list'] == 'presence':
            target = api_models.PresenceAbsence.objects.filter(student=student_id, class_meeting=obj.id).values('status')
        elif self.context['target_list'] == 'meeting_score':
            target = api_models.PresenceAbsence.objects.filter(student=student_id, class_meeting=obj.id).values('meeting_score')
        elif self.context['target_list'] == 'disciplinary':
            target = api_models.PresenceAbsence.objects.filter(student=student_id, class_meeting=obj.id).values('has_disciplinary','disciplinary')
        return target


class MeetingsSerializer(serializers.Serializer):

    #meeting_score_info = MeetingQuizScoreSerializer(many=True, read_only=True)
    date = serializers.SerializerMethodField()
    slots = serializers.SerializerMethodField()

    class Meta:
        fields= ('date','slots',)

    def get_date(self,obj):
        ClassMeeting = api_models.ClassMeeting.objects.get(id=obj.class_meeting.id)
        return ClassMeeting.date
    
    def get_slots(self,obj):
        queryset = api_models.ClassMeeting.objects.get(id=obj.class_meeting.id)
        self.context['student_id'] = obj.students.id
        return SlotsSerializer(queryset, context = self.context).data


class ClassSheetSerializer(serializers.ModelSerializer):

    #meeting_score_info = MeetingQuizScoreSerializer(many=True, read_only=True)
    meetings = serializers.SerializerMethodField()

    class Meta:
        model = api_models.User
        #fields= ['id','first_name','last_name','meeting_score_info']
        fields= ['id','first_name','last_name','meetings']

    def get_meetings(self,obj):
        target_list = self.context['target_list']
        class_id = self.context['class_id']
        queryset = api_models.ClassMeetingStudents.objects.filter(students=obj.id, class_meeting__class_id = class_id)
        
        #is it nesseccary to check if teacher_id is and integer?? 
        teacher_id = self.context.get('teacher_id')
        if teacher_id:
            queryset = queryset.filter(class_meeting__teacher_id = teacher_id)

        from_date = self.context.get('from_date')
        to_date = self.context.get('to_date')
        if from_date:
            queryset = queryset.filter(class_meeting__date__gte = from_date)
        if to_date:  
            queryset = queryset.filter(class_meeting__date__lte = to_date)

        return MeetingsSerializer(queryset, many=True, context=dict(target_list = target_list)).data


##################################################################################
#                           srializer for exam results                           #
##################################################################################


class ExamMeetingsScoreSerializer(serializers.Serializer):

    score = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()
    quiz_title = serializers.SerializerMethodField()
    
    class Meta:
        fields = ['score', 'quiz_title', 'date', 'time', 'lesson',]

    def get_score(self,obj):
        return obj.score
    
    def get_quiz_title(self,obj):
        return obj.quiz.quiz_title

    def get_date(self,obj):
        ExamMeeting = api_models.NewExamMeeting.objects.get(id=obj.exam_meeting.id)
        return ExamMeeting.exam.date
    
    def get_time(self,obj):
        ExamMeeting = api_models.NewExamMeeting.objects.get(id=obj.exam_meeting.id)
        return ExamMeeting.exam.time
    
    def get_lesson(self,obj):
        ExamMeeting = api_models.NewExamMeeting.objects.get(id=obj.exam_meeting.id)
        return ExamMeeting.exam.lesson_id.name

class ExamSheetSerializer(serializers.ModelSerializer):

    #meeting_score_info = MeetingQuizScoreSerializer(many=True, read_only=True)
    meetings = serializers.SerializerMethodField()

    class Meta:
        model = api_models.User
        #fields= ['id','first_name','last_name','meeting_score_info']
        fields= ['id','first_name','last_name','meetings']

    def get_meetings(self,obj):
        class_id = self.context['class_id']
        teacher_id = self.context.get('teacher_id')
        if teacher_id:
            lesson_ids = api_models.Section.objects.filter(class_id=class_id,teacher_id=teacher_id).values_list('selected_lesson',flat=True)
            exam_ids = api_models.NewExam.objects.filter(class_id=class_id,lesson_id__in=lesson_ids).values_list('id',flat=True)
        else:
            exam_ids = api_models.NewExam.objects.filter(class_id=class_id).values_list('id',flat=True)
        exam_meeting_ids = api_models.NewExamMeeting.objects.filter(exam__in=exam_ids)
        queryset = api_models.NewExamScore.objects.filter(student=obj.id, exam_meeting__exam__class_id = class_id)
        return ExamMeetingsScoreSerializer(queryset, many=True).data


##################################################################################
#                  srializer for teacher time line availability                  #
##################################################################################


class TeacherAvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.TeacherAvailability
        read_only_fields = ('verified', )
        exclude = ('created_at', 'modified_at', )


class TeacherReservedSectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Section
        fields = ['id', 'teacher_id', 'day_of_week', 'start_time', 'end_time', 'selected_lesson', 'class_id']

##################################################################################
#                         srializer for teacher lessons                          #
##################################################################################


class TeacherLessonsSerializer(serializers.ModelSerializer):

    teacher_full_name = serializers.ReadOnlyField(source='teacher_id.full_name')
    lesson_name = serializers.ReadOnlyField(source='lesson_id.name')

    class Meta:
        model = api_models.TeacherLessons
        fields = ['id', 'teacher_id', 'teacher_full_name', 'lesson_id', 'lesson_name']


##################################################################################
#                             srializer for classroom                            #
##################################################################################


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Classroom
        fields = ['id', 'degree', 'field', 'level', 'name']


##################################################################################
#                      srializer for per day meeting score                       #
##################################################################################


class MeetingScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.MeetingScorePerDay
        fields = ['id', 'teacher_id', 'student_id', 'lesson_id', 'class_id', 'date', 'score']


##################################################################################
#                    srializer for per day disciplinary notes                    #
##################################################################################


class DisciplinarySerializer(serializers.ModelSerializer):

    # teacher_full_name = serializers.ReadOnlyField(source='teacher_id.full_name')
    # student_full_name = serializers.ReadOnlyField(source='student_id.full_name')
    # lesson_name = serializers.ReadOnlyField(source='lesson_id.name')
    # class_name = serializers.ReadOnlyField(source='class_id.name')

    class Meta:
        model = api_models.DisciplinaryPerDay
        fields = ['id', 'teacher_id', 'student_id', 'lesson_id', 'class_id', 'date', 'has_disciplinary', 'disciplinary']

##################################################################################
#                          srializer for lessons from section                    #
##################################################################################

class LessonsFromSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Lesson
        fields = ['id', 'name']


##################################################################################
#                       srializer for simple presence absence                    #
##################################################################################

class PresenceAbsencePerMeetingSerializer(serializers.ModelSerializer):

    student_full_name = serializers.ReadOnlyField(source='student.full_name')

    class Meta:
        model = api_models.PresenceAbsence
        fields = ['class_meeting', 'student', 'student_full_name', 'status']


##################################################################################
#                             srializer for parent child                         #
##################################################################################

class ParentChildSerializer(serializers.ModelSerializer):

    parent_full_name = serializers.ReadOnlyField(source='parent.full_name')
    parent_national_code = serializers.ReadOnlyField(source='parent.national_code')
    child_full_name = serializers.ReadOnlyField(source='child.full_name')
    child_national_code = serializers.ReadOnlyField(source='child.national_code')
    class_info = serializers.SerializerMethodField()

    class Meta:
        model = api_models.ParentChild
        fields = ['id', 'parent', 'child', 'parent_full_name', 'parent_national_code', 'child_full_name', 'child_national_code', 'class_info']
    
    def get_class_info(self, obj):
        resp = []
        class_ids = api_models.ClassroomStudents.objects.filter(students=obj.child).values_list('classroom', flat=True)
        for class_id in class_ids:
            classroom = api_models.Classroom.objects.get(id=class_id)
            school = api_models.School.objects.get(id=classroom.school_id)
            resp.append({'class_name': classroom.name, 'school_name': school.name, 'degree': {'id': classroom.degree}, 'level': {'id': classroom.level}, 'field': {'id': classroom.field}})
        return resp


##################################################################################
#                             srializer for parent child                         #
##################################################################################


class ParentDashboardsSerializer(serializers.ModelSerializer):

    student_full_name = serializers.ReadOnlyField(source='students.full_name')
    class_info = serializers.SerializerMethodField()

    class Meta:
        model = api_models.ClassroomStudents
        fields = ['students', 'classroom', 'student_full_name', 'class_info']
    
    def get_class_info(self, obj):
        classroom = obj.classroom
        school = api_models.School.objects.get(id=classroom.school_id) 
        resp = {'class_name': classroom.name, 'school_name': school.name, 'degree': {'id': classroom.degree, 'title': settings.DEGREE_MAP.get(classroom.degree, None)}, 'level': {'id': classroom.level, 'title': settings.LEVEL_MAP.get(classroom.level, None)}, 'field': {'id': classroom.field, 'title': settings.FIELD_MAP.get(classroom.field, None)}}
        return resp


##################################################################################
#                                   srializer for Lesson                         #
##################################################################################


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Lesson
        fields = '__all__'
